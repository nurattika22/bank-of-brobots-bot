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
