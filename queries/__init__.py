profile = '''query {{
    user(id: "{0}") {{
        name
        planName
        planCost
        weekLeft
        weekLimit
        accounts {{
            id
            customName
            money
        }}
    }}
}}'''

create_account = '''mutation {{
    createAccount(customName: "{0}") {{
        id
    }}
}}
'''

remove_account = '''mutation {{
    removeAccount(accountId: "{0}")
}}
'''
