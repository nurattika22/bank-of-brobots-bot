import requests


def graphql_request(query, token, url):
    auth_token = 'kbkcmbkcmbkcbc9ic9vixc9vixc9v'
    hed = {'Authorization': 'Bearer ' + token}
    data = {'query': query}

    response = requests.post(url, json=data, headers=hed)
    return response.json()['data']
