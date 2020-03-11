profile = '''query {{
    user(id: "{0}") {{
        name
        money
        planName
        planCost
        weekLeft
        weekLimit
        isAdmin
        transactions {{
            id
            money
            fromUser {{
                name
            }}
            toUser {{
                name
            }}
        }}
    }}
}}'''

transfer = '''mutation {{
    transfer(money: {}, from_user_id: "{}", to_user_id: "{}") {{
        id
    }}
}}'''
