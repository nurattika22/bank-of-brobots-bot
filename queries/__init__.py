profile = '''query {{
    user(id: "{}") {{
        name
        money
        is_admin
        transactions {{
            id
        }}
    }}
}}'''

transactions = '''query {{
    user(id: "{}") {{
        transactions {{
            money
            fromUser {{
                telegram_id
                name
                username
            }}
            toUser {{
                telegram_id
                name
                username
            }}
            message
        }}
    }}
}}'''

telegramToUserId = '''query {{
    telegramToUserId(telegram_id: "{}")
}}
'''

transfer = '''mutation {{
    transfer(money: {}, from_user_id: "{}", to_user_id: "{}", message: "{}") {{
        id
    }}
}}'''
