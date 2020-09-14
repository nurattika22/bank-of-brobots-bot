import re
import time
from datetime import datetime
from os import environ

import requests
import telebot
from telebot import types

from common import get_user_str, load_config, user_exists, yesno_keyboard
from localization import localization
from queries import profile, telegramToUserId, transactions, transfer
from services import graphql_request

load_config()
localization = localization['en']

bot = telebot.AsyncTeleBot(environ.get(
    'TELEGRAM_API_TOKEN_DEV'), parse_mode='HTML')


@bot.message_handler(commands=['start'])
def on_start(message: types.Message):
    u_id = message.from_user.id

    bot.reply_to(message, localization['start'])
    bot.send_chat_action(u_id, 'typing')
    time.sleep(1)

    exists = user_exists(u_id, environ.get('API_URL'))

    if not exists:
        kb = yesno_keyboard(
            'register', localization['inline_keyboard']['yes'], localization['inline_keyboard']['no'])
        bot.send_message(u_id, localization['register'], reply_markup=kb)
        return

    end_date = datetime.strptime(environ.get(
        'STOP_WHAT_IS_NEW'), '%Y-%m-%d %H:%M:%S')

    if datetime.now() <= end_date:
        bot.send_message(u_id, localization['what_is_new'])

    else:
        bot.send_message(u_id, localization['help'])


@bot.message_handler(commands=['help'])
def on_help(message: types.Message):
    bot.reply_to(message, localization['help'])


@bot.message_handler(commands=['new'])
def on_new(message: types.Message):
    u_id = message.from_user.id
    bot.send_message(u_id, localization['what_is_new'])


@bot.message_handler(commands=["ping"])
def on_ping(message: types.Message):
    bot.reply_to(message, localization['ping'])


@bot.message_handler(commands=['profile'])
def on_profile(message: types.Message):
    u_id = message.from_user.id
    api_url = environ.get('API_URL')

    res = graphql_request(api_url,
                          telegramToUserId.format(u_id),
                          telegram_id=u_id)

    if res.get('errors', None):
        bot.reply_to(message, localization['register_first'])
        return

    internal_id = res['data']['telegramToUserId']

    res = graphql_request(api_url,
                          profile.format(internal_id), telegram_id=u_id)['data']['user']

    user_data = {
        'name': res['name'],
        'money': res['money'],
        'transactions': len(res['transactions']),
    }

    text_response = localization['profile'].format(**user_data)

    if res['is_admin']:
        text_response += localization['profile_admin'].format(res['is_admin'])

    bot.send_message(u_id, text_response)


@bot.message_handler(commands=['transactions'])
def on_transactions(message: types.Message):
    u_id = message.from_user.id
    api_url = environ.get('API_URL')

    res = graphql_request(api_url,
                          telegramToUserId.format(u_id),
                          telegram_id=u_id)

    if res.get('errors', None):
        bot.reply_to(message, localization['register_first'])
        return

    internal_id = res['data']['telegramToUserId']

    res = graphql_request(api_url,
                          transactions.format(internal_id), telegram_id=u_id)['data']['user']

    text_response = localization['transaction_list_title']

    for t in res['transactions']:
        user1, user2 = '', ''

        if not t['fromUser']['username']:
            user1 = t['fromUser']['name']

        else:
            user1 = '@' + t['fromUser']['username']

        if not t['toUser']['username']:
            user2 = t['toUser']['name']

        else:
            user2 = '@' + t['toUser']['username']

        text_response += localization['transaction_list_item'].format(
            t['money'], user1, user2, t['message'] if t['message'] else 'no message')

    if not len(res['transactions']):
        text_response += localization['empty_list']

    bot.reply_to(message, text_response)


@bot.message_handler(commands=['stats'])
def on_stats(message: types.Message):
    u_id = str(message.from_user.id)
    api_url = environ.get('API_URL')

    res = graphql_request(api_url,
                          telegramToUserId.format(u_id),
                          telegram_id=u_id)

    if res.get('errors', None):
        bot.reply_to(message, localization['register_first'])
        return

    internal_id = res['data']['telegramToUserId']

    res = graphql_request(api_url,
                          transactions.format(internal_id), telegram_id=u_id)['data']['user']

    stats = {
        'expenses': 0,
        'income': 0,
        'top_ex': 0,
        'top_in': 0,
        'transactions': 0
    }

    stats['transactions'] = len(res['transactions'])

    for t in res['transactions']:
        if t['fromUser']['telegram_id'] == u_id:
            stats['expenses'] += t['money']
            stats['top_ex'] = t['money'] if t['money'] > stats['top_ex'] else stats['top_ex']

        if t['toUser']['telegram_id'] == u_id:
            stats['income'] += t['money']
            stats['top_in'] = t['money'] if t['money'] > stats['top_in'] else stats['top_in']

    bot.reply_to(message, localization['stats'].format(**stats))


@bot.callback_query_handler(func=lambda call: True)
def on_callback_query(query: types.CallbackQuery):
    u_id = query.from_user.id
    user_str = get_user_str(query.from_user)

    title = query.data.split(';')[0]
    value = query.data.split(';')[1:]

    if title == 'register':
        if value[0] == '1':
            user_data = {
                'name': user_str,
                'telegram_id': u_id,
                'username': query.from_user.username
            }

            requests.post(environ.get('API_URL') +
                          '/register', data=user_data).json()

            bot.edit_message_text(
                localization['register_success'], u_id, query.message.message_id)

            end_date = datetime.strptime(environ.get(
                'STOP_WHAT_IS_NEW'), '%Y-%m-%d %H:%M:%S')
            if datetime.now() <= end_date:
                bot.send_message(u_id, localization['what_is_new'])

            time.sleep(1)
            bot.send_message(u_id, localization['try_help'])

        else:
            bot.edit_message_text(
                localization['register_cancel'], u_id, query.message.message_id)

    elif title == 'give':
        if str(u_id) == value[0]:
            bot.answer_callback_query(query.id, localization['cannot'])
            return

        from_user_id = graphql_request(environ.get('API_URL'),
                                       telegramToUserId.format(value[0]),
                                       telegram_id=value[0])['data']['telegramToUserId']

        to_user_id = graphql_request(environ.get('API_URL'),
                                     telegramToUserId.format(u_id),
                                     telegram_id=u_id)

        if to_user_id.get('errors'):
            bot.edit_message_text(
                localization['register_first'],
                inline_message_id=query.inline_message_id
            )
            return

        to_user_id = to_user_id['data']['telegramToUserId']

        res = graphql_request(environ.get('API_URL'), transfer.format(
            value[1], from_user_id, to_user_id, value[2]), telegram_id=value[0])

        if res.get('errors'):
            bot.edit_message_text(
                res['errors'][0]['message'],
                inline_message_id=query.inline_message_id
            )
            return

        bot.edit_message_text(
            localization['transaction_success'],
            inline_message_id=query.inline_message_id
        )

    elif title == 'recv':
        if str(u_id) == value[0]:
            bot.answer_callback_query(query.id, localization['cannot'])
            return

        from_user_id = graphql_request(environ.get('API_URL'),
                                       telegramToUserId.format(u_id),
                                       telegram_id=u_id)

        if from_user_id.get('errors'):
            bot.edit_message_text(
                localization['register_first'],
                inline_message_id=query.inline_message_id
            )
            return

        from_user_id = from_user_id['data']['telegramToUserId']

        to_user_id = graphql_request(environ.get('API_URL'),
                                     telegramToUserId.format(value[0]),
                                     telegram_id=value[0])['data']['telegramToUserId']

        res = graphql_request(environ.get('API_URL'), transfer.format(
            value[1], from_user_id, to_user_id, value[2]), telegram_id=u_id)

        if res.get('errors'):
            bot.edit_message_text(
                res['errors'][0]['message'],
                inline_message_id=query.inline_message_id
            )
            return

        bot.edit_message_text(
            localization['transaction_success'],
            inline_message_id=query.inline_message_id
        )

    elif title == 'cancel_request':
        bot.edit_message_text(
            localization['transaction_cancel'],
            inline_message_id=query.inline_message_id
        )


@bot.inline_handler(func=lambda query: len(query.query) == 0)
def empty_query(query: types.InlineQuery):
    u_id = query.from_user.id

    exists = user_exists(u_id, environ.get('API_URL'))

    if not exists:
        on_inline_not_registered(query)
        return

    r = types.InlineQueryResultArticle(
        id='1',
        title=localization['inline_mode']['empty']['title'],
        description=localization['inline_mode']['empty']['description'],
        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['empty']['message_text']),
        thumb_url='https://i.imgur.com/saDPT92.png'
    )

    bot.answer_inline_query(
        query.id, [r], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


@bot.inline_handler(func=lambda query: len(query.query))
def answer_query(query: types.InlineQuery):
    u_id = query.from_user.id

    exists = user_exists(u_id, environ.get('API_URL'))

    if not exists:
        on_inline_not_registered(query)
        return

    try:
        matches = re.match(r'(\d+)? ?(.*)', query.query)
        num = matches.groups()[0]
        message = matches.groups()[1]
    except AttributeError:
        return

    if not num:
        empty_query(query)
        return

    test = len('xxxx;{};{};{}'.format(u_id, num, message).encode('utf-8'))

    if test > 64:
        on_callback_data_overflow(query)
        return

    if int(num) >= (2**32 - 1):
        on_integer_overflow(query)
        return

    give_kb = types.InlineKeyboardMarkup()
    give_kb.row(
        types.InlineKeyboardButton(
            localization['inline_keyboard']['receive'], callback_data='give;{};{};{}'.format(u_id, num, message)),
        types.InlineKeyboardButton(
            localization['inline_keyboard']['cancel'], callback_data='cancel_request')
    )

    give = types.InlineQueryResultArticle(
        id='1',
        title=localization['inline_mode']['give']['title'].format(num),
        description=(localization['inline_mode']['give']['description'].format(message)
                     if message else localization['inline_mode']['no_message']),

        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['give']['message_text'].format(num) +
            (localization['inline_mode']['message_text_trans_message'].format(
                message) if message else ''),
            parse_mode='HTML'),

        reply_markup=give_kb,
        thumb_url='https://i.imgur.com/f2f4fJu.png'
    )

    ask_kb = types.InlineKeyboardMarkup()
    ask_kb.row(
        types.InlineKeyboardButton(
            localization['inline_keyboard']['give'], callback_data='recv;{};{};{}'.format(u_id, num, message)),
        types.InlineKeyboardButton(
            localization['inline_keyboard']['cancel'], callback_data='cancel_request')
    )

    ask = types.InlineQueryResultArticle(
        id='2',
        title=localization['inline_mode']['request']['title'].format(num),
        description=(localization['inline_mode']['request']['description'].format(message)
                     if message else localization['inline_mode']['no_message']),

        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['request']['message_text'].format(num) +
            (localization['inline_mode']['message_text_trans_message'].format(
                message) if message else ''),
            parse_mode='HTML'),

        reply_markup=ask_kb,
        thumb_url='https://i.imgur.com/XYDwkVZ.png'
    )
    bot.answer_inline_query(
        query.id, [give, ask], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


def on_inline_not_registered(query: types.InlineQuery):
    r = types.InlineQueryResultArticle(
        id='1',
        title=localization['inline_mode']['not_registered']['title'],
        description=localization['inline_mode']['not_registered']['description'],
        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['not_registered']['message_text'])
    )

    bot.answer_inline_query(
        query.id, [r], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


def on_callback_data_overflow(query: types.InlineQuery):
    r = types.InlineQueryResultArticle(
        id='1',
        title=localization['inline_mode']['message_overflow']['title'],
        description=localization['inline_mode']['message_overflow']['description'],
        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['message_overflow']['message_text'])
    )

    bot.answer_inline_query(
        query.id, [r], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


def on_integer_overflow(query: types.InlineQuery):
    r = types.InlineQueryResultArticle(
        id='1',
        title=localization['inline_mode']['integer_overflow']['title'],
        description=localization['inline_mode']['integer_overflow']['description'],
        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['integer_overflow']['message_text'])
    )

    bot.answer_inline_query(
        query.id, [r], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


if __name__ == '__main__':
    bot.polling(none_stop=True)
