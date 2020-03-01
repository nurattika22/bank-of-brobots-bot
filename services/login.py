import requests


def login(db, user_query, config, id):
    r = requests.post(config['API_ADDR'] + '/login', data={'telegram_id': id})

    token = r.json()['token']

    db.update({'token': token},
              user_query.telegram_id == id)

    return token
