import requests


def login(db, user_query, url, id):
    r = requests.post(url + '/login', data={'telegram_id': id})

    token = r.json()['token']

    db.update({'token': token},
              user_query.telegram_id == id)

    return token
