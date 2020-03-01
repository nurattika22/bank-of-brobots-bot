import logging
import os

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

    if not db.search(user_query.telegram_id == u.id):
        kb = yesno_keyboard(config, 'register')
        bot.reply_to(message, config['BOT']['START_REGISTER'], reply_markup=kb)

    else:
        bot.send_message(u.id, config['BOT']['START'])

    logging.info('/start from %s:%s', u.id, user_str)


@bot.message_handler(commands=['me'])
def profile(message: types.Message):
    u = message.chat
    user_str = generate_user_str(u)
    user = db.search(user_query.telegram_id == u.id)[0]

    if not user:
        bot.send_message(u.id, config['BOT']['NOT_USER'])

    r = graphql_request(
        queries.profile.format(user['db_id']),
        user['token'],
        config['API_ADDR'])

    bot.send_message(u.id, generate_profile(r['user']), parse_mode='Markdown')

    logging.info('/me from %s:%s', u.id, user_str)


@bot.callback_query_handler(func=lambda call: True)
def inline_button(callback: types.CallbackQuery):
    u = callback.message.chat
    user_str = generate_user_str(u)

    title, val = callback.data.split(':')

    if title == 'register' and val == '1':
        user = {
            'name': user_str,
            'telegram_id': u.id
        }

        r = requests.post(config['API_ADDR'] + '/register', data=user).json()
        db.insert({'name': user_str, 'telegram_id': u.id, 'db_id': r['_id']})
        login(db, user_query, config, u.id)

        bot.edit_message_text(
            config['BOT']['SUCCESS_REG'],
            u.id,
            callback.message.message_id)

    if title == 'register' and val == '0':
        bot.edit_message_text(
            config['BOT']['CANCEL_REG'],
            u.id,
            callback.message.message_id)


if __name__ == '__main__':
    bot.polling()
