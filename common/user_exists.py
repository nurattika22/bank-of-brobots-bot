from services import graphql_request
from queries import telegramToUserId


def user_exists(telegram_id, api_url):
    res = graphql_request(api_url,
                          telegramToUserId.format(telegram_id),
                          telegram_id=telegram_id)

    return False if res.get('errors') else True
