import logging
import os
import re

import requests
import tinydb
import telebot
from telebot import types

import queries
from config import config
from services import *

if not os.path.exists(config['DB']['PATH']):
    os.makedirs(os.path.dirname(config['DB']['PATH']), exist_ok=True)

db = tinydb.TinyDB(config['DB']['PATH'])
user_query = tinydb.Query()

bot = telebot.TeleBot(config['BOT']['TOKEN'])

logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

logging.basicConfig(filename=config['LOG']['PATH'],
                    format=config['LOG']['FORMAT'],
                    level=logging.DEBUG)


@bot.message_handler(commands=['start'])
def start_menu(message: types.Message):
    u = message.chat
    user_str = generate_user_str(u)

    if not find_by_telegram_id(db, user_query, u.id):
        kb = yesno_keyboard(config, 'register')
        bot.reply_to(message, config['BOT']['START_REGISTER'], reply_markup=kb)

    else:
        bot.send_message(u.id, config['BOT']['START'])

    logging.info('/start from %s:%s', u.id, user_str)


@bot.message_handler(commands=['help'])
def help_menu(message: types.Message):
    u = message.chat
    user = find_by_telegram_id(db, user_query, u.id)
    user_str = generate_user_str(u)

    if not user:
        bot.send_message(u.id, config['BOT']['NOT_USER'])
        return

    bot.send_message(u.id, config['BOT']['HELP'])
    logging.info('/help from %s:%s', u.id, user_str)


@bot.message_handler(commands=['me'])
def profile(message: types.Message):
    u = message.chat
    user = find_by_telegram_id(db, user_query, u.id)
    user_str = generate_user_str(u)

    if not user:
        bot.send_message(u.id, config['BOT']['NOT_USER'])
        return

    r = graphql_request(
        db, user_query, config['API_ADDR'], u.id,
        queries.profile.format(user['db_id']))

    bot.send_message(u.id, generate_profile(
        r['data']['user']), parse_mode='Markdown')

    logging.info('/me from %s:%s', u.id, user_str)


@bot.message_handler(commands=['my_transactions'])
def transactions(message: types.Message):
    u = message.chat
    user = find_by_telegram_id(db, user_query, u.id)
    base = 'Transactions:\n'

    if not user:
        bot.send_message(u.id, config['BOT']['NOT_USER'])
        return

    r = graphql_request(db, user_query, config['API_ADDR'],
                        u.id, queries.profile.format(user['db_id']))
    transactions = r['data']['user']['transactions']

    if not transactions:
        base += 'Empty...'

    for t in transactions:
        if not t:
            continue

        if not t['toUser']:
            base += ' ~ {} brocoins from *{}*\n'.format(
                abs(t['money']), t['fromUser']['name'])
            base += '   _~~ {}_\n'.format(t['message']) if t['message'] else ''

        else:
            base += ' ~ *{}* sent {} brocoins to *{}*\n'.format(
                t['fromUser']['name'], t['money'], t['toUser']['name'])
            base += '   _~~ {}_\n'.format(t['message']) if t['message'] else ''

    bot.send_message(u.id, base, parse_mode='Markdown')


@bot.message_handler(commands=['change_subscription', 'change_subs'])
def change_subsription(message: types.Message):
    u = message.chat
    user = find_by_telegram_id(db, user_query, u.id)

    if not user:
        bot.send_message(u.id, config['BOT']['NOT_USER'])
        return

    r = graphql_request(
        db, user_query, config['API_ADDR'], u.id,
        queries.subscriptions)

    subs = types.InlineKeyboardMarkup(row_width=1)

    for sub in r['data']['subscriptions']:
        if not sub['limit']:
            sub['limit'] = 'Unlimited'

        subs.row(
            types.InlineKeyboardButton(
                text='{name} - {cost} - {limit}'.format(**sub),
                callback_data='change_sub:{}'.format(sub['id'])
            )
        )

    bot.send_message(
        u.id,
        'Choose one of these:\n_name_ - _cost_ - _limit_',
        reply_markup=subs,
        parse_mode='Markdown')


@bot.message_handler(commands=['ping'])
def ping(message: types.Message):
    bot.reply_to(message, 'Pong!')


@bot.callback_query_handler(func=lambda call: True)
def inline_button(callback: types.CallbackQuery):
    u = callback.from_user
    user = find_by_telegram_id(db, user_query, u.id)
    user_str = generate_user_str(u)

    title = callback.data.split(':')[0]
    val = callback.data.split(':')[1:]

    if title == 'register' and val[0] == '1':
        user = {
            'name': user_str,
            'telegram_id': u.id
        }

        r = requests.post(config['API_ADDR'] + '/register', data=user).json()
        db.insert({'name': user_str, 'telegram_id': u.id, 'db_id': r['_id']})
        login(db, user_query, config['API_ADDR'], u.id)

        bot.edit_message_text(
            config['BOT']['SUCCESS_REG'],
            u.id,
            callback.message.message_id)

    if title == 'register' and val[0] == '0':
        bot.edit_message_text(
            config['BOT']['CANCEL_REG'],
            u.id,
            callback.message.message_id)

    if not user:
        bot.answer_callback_query(callback.id, 'You\'re not registered!')
        return

    if title == 'receive_money' and val:
        if val[1] == user['db_id']:
            bot.answer_callback_query(callback.id, 'You can\'t do that!')
            return

        r = db.search(user_query.db_id == val[1])[0]

        r = graphql_request(
            db, user_query, config['API_ADDR'], r['telegram_id'],
            queries.transfer.format(val[0], val[1], user['db_id'], val[2]))

        if r.get('errors', None):
            bot.edit_message_text(
                r['errors'][0]['message'],
                inline_message_id=callback.inline_message_id
            )

        else:
            bot.edit_message_text(
                config['BOT']['SUCCESS'],
                inline_message_id=callback.inline_message_id
            )

    if title == 'give_money' and val:
        if val[1] == user['db_id']:
            bot.answer_callback_query(
                callback.id, 'You can\'t do that!')
            return

        r = db.search(user_query.db_id == val[1])[0]

        r = graphql_request(
            db, user_query, config['API_ADDR'], user['telegram_id'],
            queries.transfer.format(val[0], user['db_id'], val[1], val[2]))

        if r.get('errors', None):
            bot.edit_message_text(
                r['errors'][0]['message'],
                inline_message_id=callback.inline_message_id
            )

        else:
            bot.edit_message_text(
                config['BOT']['SUCCESS'],
                inline_message_id=callback.inline_message_id
            )

    if title == 'cancel_request':
        bot.edit_message_text(
            config['BOT']['CANCEL_TRANSFER'],
            inline_message_id=callback.inline_message_id
        )

    if title == 'change_sub':
        r = graphql_request(
            db, user_query, config['API_ADDR'], user['telegram_id'],
            queries.change_subscription.format(val[0], user['db_id']))

        if r.get('errors', None):
            bot.edit_message_text(
                r['errors'][0]['message'],
                u.id,
                callback.message.message_id)

        else:
            bot.edit_message_text(
                config['BOT']['SUCCESS'],
                u.id,
                callback.message.message_id)


@bot.inline_handler(func=lambda query: len(query.query) is 0)
def empty_query(query: types.InlineQuery):
    r = types.InlineQueryResultArticle(
        id='1',
        title='Enter amount of brocoins',
        description='and choose one of operations above',
        input_message_content=types.InputTextMessageContent(
            message_text='Amount of brocoins wasn\'t entered!'),
        thumb_url='https://i.imgur.com/saDPT92.png'
    )
    bot.answer_inline_query(query.id, [r])


@bot.inline_handler(func=lambda query: len(query.query))
def answer_query(query: types.InlineQuery):
    u = query.from_user
    user = find_by_telegram_id(db, user_query, u.id)

    if not user:
        return

    try:
        matches = re.match(r'(\d+)? ?(.*)', query.query)
        num = matches.groups()[0]
        message = matches.groups()[1]
    except AttributeError:
        return

    give_kb = types.InlineKeyboardMarkup()
    give_kb.row(
        types.InlineKeyboardButton(
            'Receive', callback_data='receive_money:{}:{}:{}'.format(num, user['db_id'], message)),
        types.InlineKeyboardButton('Cancel', callback_data='cancel_request')
    )

    give = types.InlineQueryResultArticle(
        id='1',

        title='Send {} brocoins'.format(num),

        description=('Message: {}'.format(message)
                     if message else 'No message provided'),

        input_message_content=types.InputTextMessageContent(
            message_text='Get your {} brocoins!'.format(num) +
            ('\nMessage: _{}_'.format(message) if message else ''),
            parse_mode='Markdown'),

        reply_markup=give_kb,

        thumb_url='https://i.imgur.com/f2f4fJu.png'
    )

    ask_kb = types.InlineKeyboardMarkup()
    ask_kb.row(
        types.InlineKeyboardButton(
            'Give', callback_data='give_money:{}:{}:{}'.format(num, user['db_id'], message)),
        types.InlineKeyboardButton('Cancel', callback_data='cancel_request')
    )

    ask = types.InlineQueryResultArticle(
        id='2',

        title='Request {} brocoins'.format(num),

        description=('Message: {}'.format(message)
                     if message else 'No message provided'),

        input_message_content=types.InputTextMessageContent(
            message_text='Send me {} brocoins!'.format(num) +
            ('\nMessage: _{}_'.format(message) if message else ''),
            parse_mode='Markdown'),

        reply_markup=ask_kb,

        thumb_url='https://i.imgur.com/XYDwkVZ.png'
    )
    bot.answer_inline_query(query.id, [give, ask])


if __name__ == '__main__':
    bot.polling()
