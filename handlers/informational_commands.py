import logging
from os import environ

from bot import bot, localization
from queries import profile, telegramToUserId
from services import get_transactions, graphql_request
from telebot import types


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
    logging.debug('/profile from %s', u_id)


@bot.message_handler(commands=['transactions'])
def on_transactions(message: types.Message):
    u_id = message.from_user.id
    res = get_transactions(telegram_id=u_id)

    if not res:
        bot.reply_to(message, localization['register_first'])
        return

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
    logging.debug('/transactions from %s', u_id)


@bot.message_handler(commands=['stats'])
def on_stats(message: types.Message):
    u_id = str(message.from_user.id)
    res = get_transactions(telegram_id=u_id)

    if not res:
        bot.reply_to(message, localization['register_first'])
        return

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
    logging.debug('/stats from %s', u_id)
