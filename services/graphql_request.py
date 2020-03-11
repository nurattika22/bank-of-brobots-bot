import requests
from services.login import login


def graphql_request(db, user_query, url, id, query, need_login=False):
    if need_login:
        login(db, user_query, url, id)

    token = db.search(user_query.telegram_id == id)[0]['token']
    hed = {'Authorization': 'Bearer ' + token}
    data = {'query': query}

    try:
        response = requests.post(url, json=data, headers=hed)
    except Exception as ex:
        return graphql_request(db, user_query, url, id, query, True)

    return response.json()
