import re
from os import environ

import requests
import telebot
from telebot import types

from common import get_user_str, load_config, user_exists, yesno_keyboard
from localization import localization
from queries import profile, telegramToUserId, transfer
from services import graphql_request

load_config()
localization = localization['en']

bot = telebot.TeleBot(environ.get(
    'TELEGRAM_API_TOKEN_DEV'), parse_mode='MARKDOWN')


@bot.message_handler(commands=['start'])
def on_start(message: types.Message):
    u_id = message.from_user.id

    bot.reply_to(message, localization['start'])

    exists = user_exists(u_id, environ.get('API_URL'))

    if not exists:
        kb = yesno_keyboard(
            'register', localization['inline_keyboard']['yes'], localization['inline_keyboard']['no'])
        bot.send_message(u_id, localization['register'], reply_markup=kb)
        return

    bot.send_message(u_id, localization['help'])


@bot.message_handler(commands=['help'])
def on_help(message: types.Message):
    bot.reply_to(message, localization['help'])


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


@bot.callback_query_handler(func=lambda call: True)
def on_callback_query(query: types.CallbackQuery):
    u_id = query.from_user.id
    user_str = get_user_str(query.from_user)

    title = query.data.split(';')[0]
    value = query.data.split(';')[1:]

    if title == 'register':
        if value == '1':
            user_data = {
                'name': user_str,
                'telegram_id': u_id
            }

            requests.post(environ.get('API_URL') +
                          '/register', data=user_data).json()

            bot.edit_message_text(
                localization['register'], u_id, query.message.message_id)

            bot.send_message(u_id, localization['register_success'])

        else:
            bot.edit_message_text(
                localization['register_cancel'], u_id, query.message.message_id)

    elif title == 'give_money':
        if str(u_id) == value[0]:
            bot.answer_callback_query(query.id, localization['cannot'])
            return

    elif title == 'receive_money':
        if str(u_id) == value[0]:
            bot.answer_callback_query(query.id, localization['cannot'])
            return

    elif title == 'cancel_request':
        bot.edit_message_text(
            localization['cancel'],
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

    give_kb = types.InlineKeyboardMarkup()
    give_kb.row(
        types.InlineKeyboardButton(
            localization['inline_keyboard']['receive'], callback_data='give_money;{};{}'.format(u_id, num)),
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
            parse_mode='Markdown'),

        reply_markup=give_kb,
        thumb_url='https://i.imgur.com/f2f4fJu.png'
    )

    ask_kb = types.InlineKeyboardMarkup()
    ask_kb.row(
        types.InlineKeyboardButton(
            localization['inline_keyboard']['give'], callback_data='receive_money;{};{}'.format(u_id, num)),
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
            parse_mode='Markdown'),

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
            message_text=localization['inline_mode']['not_registered']['message_text']),
        thumb_url='https://i.imgur.com/saDPT92.png'
    )

    bot.answer_inline_query(
        query.id, [r], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


if __name__ == '__main__':
    bot.polling(none_stop=True)
