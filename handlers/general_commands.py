import logging
import time
from datetime import datetime
from os import environ

from bot import bot, localization
from common import user_exists, yesno_keyboard
from telebot import types


@bot.message_handler(commands=['start'])
def on_start(message: types.Message):
    u_id = message.from_user.id
    logging.debug('/start from %s', u_id)

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
    logging.debug('/help from %s', message.from_user.id)


@bot.message_handler(commands=['new'])
def on_new(message: types.Message):
    u_id = message.from_user.id
    bot.send_message(u_id, localization['what_is_new'])
    logging.debug('/new from %s', u_id)


@bot.message_handler(commands=["ping"])
def on_ping(message: types.Message):
    bot.reply_to(message, localization['ping'])
    logging.debug('/ping from %s', message.from_user.id)
