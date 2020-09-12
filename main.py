from os import environ

import requests
import telebot
from telebot import types

from common import get_user_str, load_config, yesno_keyboard
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

    res = graphql_request(environ.get('API_URL'),
                          telegramToUserId.format(u_id), telegram_id=str(u_id))

    if res.get('errors', None):
        kb = yesno_keyboard(
            'register', localization['yn_keyboard']['yes'], localization['yn_keyboard']['no'])
        bot.send_message(u_id, localization['register'], reply_markup=kb)
        return

    bot.send_message(u_id, localization['help'])


@bot.message_handler(commands=['help'])
def on_help(message: types.Message):
    bot.reply_to(message, localization['help'])


@bot.message_handler(commands=["ping"])
def on_ping(message: types.Message):
    bot.reply_to(message, localization['ping'])


@bot.callback_query_handler(func=lambda call: True)
def on_callback_query(query: types.CallbackQuery):
    u_id = query.from_user.id
    user_str = get_user_str(query.from_user)

    title, value = query.data.split(';')
    value = int(value)

    if title == 'register':
        if value:
            user_data = {
                'name': user_str,
                'telegram_id': u_id
            }

            requests.post(environ.get('API_URL') +
                          '/register', data=user_data).json()

            bot.send_message(u_id, localization['register_success'])

        else:
            bot.edit_message_text(
                localization['register_cancel'], u_id, query.message.message_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
