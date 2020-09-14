from os import environ

from queries import telegramToUserId, transactions
from services import graphql_request


def get_transactions(user_id=None, telegram_id=None):
    api_url = environ.get('API_URL')

    if not user_id:
        res = graphql_request(api_url,
                              telegramToUserId.format(telegram_id),
                              telegram_id=telegram_id)

        if res.get('errors', None):
            return None

        user_id = res['data']['telegramToUserId']

    res = graphql_request(api_url,
                          transactions.format(user_id), u_id=user_id)['data']['user']

    if res.get('errors', None):
        return None

    return res
