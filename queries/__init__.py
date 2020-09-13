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
                name
            }}
            toUser {{
                name
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
