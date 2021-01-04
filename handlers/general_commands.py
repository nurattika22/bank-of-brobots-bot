import logging
import time
from datetime import datetime
from os import environ

from bot import bot, dp, localization
from common import user_exists, yesno_keyboard
from aiogram import types


@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    u_id = message.from_user.id
    logging.debug('/start from %s', u_id)

    await message.reply(localization['start'])
    await bot.send_chat_action(u_id, 'typing')
    time.sleep(1)

    exists = user_exists(u_id, environ.get('API_URL'))

    if not exists:
        kb = yesno_keyboard(
            'register', localization['inline_keyboard']['yes'], localization['inline_keyboard']['no'])
        await bot.send_message(u_id, localization['register'], reply_markup=kb)
        return

    end_date = datetime.strptime(environ.get(
        'STOP_WHAT_IS_NEW'), '%Y-%m-%d %H:%M:%S')

    if datetime.now() <= end_date:
        await bot.send_message(u_id, localization['what_is_new'])

    else:
        await bot.send_message(u_id, localization['help'])


@dp.message_handler(commands=['help'])
async def on_help(message: types.Message):
    await message.reply(localization['help'])
    logging.debug('/help from %s', message.from_user.id)


@dp.message_handler(commands=['new'])
async def on_new(message: types.Message):
    u_id = message.from_user.id
    await bot.send_message(u_id, localization['what_is_new'])
    logging.debug('/new from %s', u_id)


@dp.message_handler(commands=["ping"])
async def on_ping(message: types.Message):
    await message.reply(localization['ping'])
    logging.debug('/ping from %s', message.from_user.id)
