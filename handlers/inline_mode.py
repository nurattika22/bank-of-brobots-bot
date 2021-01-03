import logging
import re
from os import environ

from bot import bot, localization
from queries import profile, telegramToUserId
from services import graphql_request
from telebot import types


@bot.inline_handler(func=lambda query: len(query.query) == 0)
def empty_query(query: types.InlineQuery):
    u_id = query.from_user.id
    api_url = environ.get('API_URL')

    res = graphql_request(api_url,
                          telegramToUserId.format(u_id),
                          telegram_id=u_id)

    if res.get('errors', None):
        on_inline_not_registered(query)
        return

    logging.debug('empty query from %s', u_id)

    internal_id = res['data']['telegramToUserId']
    res = graphql_request(api_url,
                          profile.format(internal_id), telegram_id=u_id)['data']['user']
    money = res['money']

    balance = types.InlineQueryResultArticle(
        id='1',
        title=localization['inline_mode']['balance']['title'].format(money),
        description=localization['inline_mode']['balance']['description'],
        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['balance']['message_text'].format(money)),
        thumb_url=localization['inline_mode']['balance']['thumb_url']
    )

    instructions = types.InlineQueryResultArticle(
        id='2',
        title=localization['inline_mode']['empty']['title'],
        description=localization['inline_mode']['empty']['description'],
        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['empty']['message_text']),
        thumb_url=localization['inline_mode']['empty']['thumb_url']
    )

    bot.answer_inline_query(
        query.id, [balance, instructions], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


@bot.inline_handler(func=lambda query: len(query.query))
def answer_query(query: types.InlineQuery):
    u_id = query.from_user.id
    api_url = environ.get('API_URL')

    res = graphql_request(api_url,
                          telegramToUserId.format(u_id),
                          telegram_id=u_id)

    if res.get('errors', None):
        on_inline_not_registered(query)
        return

    internal_id = res['data']['telegramToUserId']
    res = graphql_request(api_url,
                          profile.format(internal_id), telegram_id=u_id)['data']['user']
    money = res['money']

    try:
        matches = re.match(r'(\d+)? ?(.*)', query.query)
        num = matches.groups()[0]
        message = matches.groups()[1]
    except AttributeError:
        logging.warning('wrong query \'%s\' from %s', query.query, u_id)
        return

    if not num or int(num) <= 0:
        empty_query(query)
        return

    num = int(num)
    test = len('xxxx;{};{};{}'.format(u_id, num, message).encode('utf-8'))

    if test > 64:
        on_callback_data_overflow(query)
        return

    if num >= (2**32 - 1):
        on_integer_overflow(query)
        return

    logging.info('successful query from %s', u_id)

    if num > money:
        logging.debug('not enough money on account from %s', u_id)
        give = types.InlineQueryResultArticle(
            id='2',
            title=localization['inline_mode']['not_enough']['title'],
            description=localization['inline_mode']['not_enough']['description'],
            input_message_content=types.InputTextMessageContent(
                message_text=localization['inline_mode']['not_enough']['message_text']),
            thumb_url=localization['inline_mode']['not_enough']['thumb_url']
        )

    else:
        give_kb = types.InlineKeyboardMarkup()
        give_kb.row(
            types.InlineKeyboardButton(
                localization['inline_keyboard']['receive'], callback_data='give;{};{};{}'.format(u_id, num, message)),
            types.InlineKeyboardButton(
                localization['inline_keyboard']['cancel'], callback_data='cancel_request;{}'.format(u_id))
        )

        give = types.InlineQueryResultArticle(
            id='2',
            title=localization['inline_mode']['give']['title'].format(num),
            description=(localization['inline_mode']['give']['description'].format(message)
                         if message else localization['inline_mode']['no_message']),

            input_message_content=types.InputTextMessageContent(
                message_text=localization['inline_mode']['give']['message_text'].format(num) +
                (localization['inline_mode']['message_text_trans_message'].format(
                    message) if message else ''),
                parse_mode='HTML'),

            reply_markup=give_kb,
            thumb_url=localization['inline_mode']['give']['thumb_url']
        )

    ask_kb = types.InlineKeyboardMarkup()
    ask_kb.row(
        types.InlineKeyboardButton(
            localization['inline_keyboard']['give'], callback_data='recv;{};{};{}'.format(u_id, num, message)),
        types.InlineKeyboardButton(
            localization['inline_keyboard']['cancel'], callback_data='cancel_request;{}'.format(u_id))
    )

    ask = types.InlineQueryResultArticle(
        id='3',
        title=localization['inline_mode']['request']['title'].format(num),
        description=(localization['inline_mode']['request']['description'].format(message)
                     if message else localization['inline_mode']['no_message']),

        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['request']['message_text'].format(num) +
            (localization['inline_mode']['message_text_trans_message'].format(
                message) if message else ''),
            parse_mode='HTML'),

        reply_markup=ask_kb,
        thumb_url=localization['inline_mode']['request']['thumb_url']
    )

    balance = types.InlineQueryResultArticle(
        id='1',
        title=localization['inline_mode']['balance']['title'].format(money),
        description=localization['inline_mode']['balance']['description'],
        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['balance']['message_text'].format(money)),
        thumb_url=localization['inline_mode']['balance']['thumb_url']
    )

    bot.answer_inline_query(
        query.id, [balance, give, ask], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


def on_inline_not_registered(query: types.InlineQuery):
    logging.debug('not registered query from %s', query.from_user.id)

    r = types.InlineQueryResultArticle(
        id='1',
        title=localization['inline_mode']['not_registered']['title'],
        description=localization['inline_mode']['not_registered']['description'],
        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['not_registered']['message_text']),
        thumb_url=localization['inline_mode']['not_registered']['thumb_url']
    )

    bot.answer_inline_query(
        query.id, [r], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


def on_callback_data_overflow(query: types.InlineQuery):
    logging.debug('data overflow query from %s', query.from_user.id)

    r = types.InlineQueryResultArticle(
        id='1',
        title=localization['inline_mode']['message_overflow']['title'],
        description=localization['inline_mode']['message_overflow']['description'],
        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['message_overflow']['message_text']),
        thumb_url=localization['inline_mode']['message_overflow']['thumb_url']
    )

    bot.answer_inline_query(
        query.id, [r], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


def on_integer_overflow(query: types.InlineQuery):
    logging.debug('integer overflow query from %s', query.from_user.id)

    r = types.InlineQueryResultArticle(
        id='1',
        title=localization['inline_mode']['integer_overflow']['title'],
        description=localization['inline_mode']['integer_overflow']['description'],
        input_message_content=types.InputTextMessageContent(
            message_text=localization['inline_mode']['integer_overflow']['message_text']),
        thumb_url=localization['inline_mode']['integer_overflow']['thumb_url']
    )

    bot.answer_inline_query(
        query.id, [r], cache_time=environ.get('INLINE_QUERY_CACHE_TIME'))


if __name__ == '__main__':
    bot.polling(none_stop=True)
