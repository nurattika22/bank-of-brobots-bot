import logging
import time
from datetime import datetime
from os import environ

import requests
from bot import bot, dp, localization
from common import get_user_str
from queries import telegramToUserId, transfer
from services import get_transactions, graphql_request
from aiogram import types


@dp.callback_query_handler()
async def on_callback_query(query: types.CallbackQuery):
    u_id = query.from_user.id
    user_str = get_user_str(query.from_user)

    title = query.data.split(';')[0]
    value = query.data.split(';')[1:]

    logging.debug('%s callback from %s', title, u_id)

    if title == 'register':
        if value[0] == '1':
            user_data = {
                'name': user_str,
                'telegram_id': u_id,
                'username': query.from_user.username
            }

            requests.post(environ.get('API_URL') +
                          '/register', data=user_data).json()

            await bot.edit_message_text(
                localization['register_success'], u_id, query.message.message_id)

            end_date = datetime.strptime(environ.get(
                'STOP_WHAT_IS_NEW'), '%Y-%m-%d %H:%M:%S')
            if datetime.now() <= end_date:
                await bot.send_message(u_id, localization['what_is_new'])

            time.sleep(1)
            await bot.send_message(u_id, localization['try_help'])

        else:
            await bot.edit_message_text(
                localization['register_cancel'], u_id, query.message.message_id)

    elif title == 'give':
        if str(u_id) == value[0]:
            await bot.answer_callback_query(query.id, localization['cannot'])
            return

        from_user_id = graphql_request(environ.get('API_URL'),
                                       telegramToUserId.format(value[0]),
                                       telegram_id=value[0])['data']['telegramToUserId']

        res = get_transactions(user_id=from_user_id)

        for t in res['transactions']:
            if t['queryId'] == query.inline_message_id:
                return

        to_user_id = graphql_request(environ.get('API_URL'),
                                     telegramToUserId.format(u_id),
                                     telegram_id=u_id)

        if to_user_id.get('errors', None):
            await bot.edit_message_text(
                localization['register_first'],
                inline_message_id=query.inline_message_id
            )
            return

        to_user_id = to_user_id['data']['telegramToUserId']

        res = graphql_request(environ.get('API_URL'), transfer.format(
            value[1], from_user_id, to_user_id, value[2], query.inline_message_id), telegram_id=value[0])

        if res.get('errors', None):
            logging.warning(
                'transaction for %s bc failed from %s', value[1], u_id)
            await bot.answer_callback_query(query.id, res['errors'][0]['message'])
            return

        logging.info(
            'successful transaction for %s bc from %s to %s', value[1], value[0], u_id)

        await bot.edit_message_text(
            localization['transaction_success'].format(value[1]),
            inline_message_id=query.inline_message_id
        )

        name = '@' + \
            query.from_user.username if query.from_user.username else get_user_str(
                query.from_user)

        await bot.send_message(
            value[0], localization['notification_give'].format(value[1], name))

    elif title == 'recv':
        if str(u_id) == value[0]:
            await bot.answer_callback_query(query.id, localization['cannot'])
            return

        from_user_id = graphql_request(environ.get('API_URL'),
                                       telegramToUserId.format(u_id),
                                       telegram_id=u_id)

        if from_user_id.get('errors', None):
            await bot.edit_message_text(
                localization['register_first'],
                inline_message_id=query.inline_message_id
            )
            return

        from_user_id = from_user_id['data']['telegramToUserId']
        res = get_transactions(user_id=from_user_id)

        for t in res['transactions']:
            if t['queryId'] == query.inline_message_id:
                return

        to_user_id = graphql_request(environ.get('API_URL'),
                                     telegramToUserId.format(value[0]),
                                     telegram_id=value[0])['data']['telegramToUserId']

        res = graphql_request(environ.get('API_URL'), transfer.format(
            value[1], from_user_id, to_user_id, value[2], query.inline_message_id), telegram_id=u_id)

        if res.get('errors', None):
            logging.warning(
                'transaction for %s bc failed from %s', value[1], u_id)
            await bot.answer_callback_query(query.id, res['errors'][0]['message'])
            return

        logging.info(
            'successful transaction for %s bc from %s to %s', value[1], value[0], u_id)

        await bot.edit_message_text(
            localization['transaction_success'].format(value[1]),
            inline_message_id=query.inline_message_id
        )

        name = '@' + \
            query.from_user.username if query.from_user.username else get_user_str(
                query.from_user)

        await bot.send_message(
            value[0], localization['notification_request'].format(name, value[1]))

    elif title == 'cancel_request':
        if str(query.from_user.id) != value[0]:
            await bot.answer_callback_query(query.id, localization['cannot'])
            return

        await bot.edit_message_text(
            localization['transaction_cancel'],
            inline_message_id=query.inline_message_id
        )
