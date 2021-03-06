import requests


def graphql_request(url, query, u_id=None, telegram_id=None):
    hed = {}
    data = {'query': query}

    if u_id:
        hed = {'id': str(u_id)}
    elif telegram_id:
        hed = {'telegram_id': str(telegram_id)}

    response = requests.post(url, json=data, headers=hed).json()
    return response
