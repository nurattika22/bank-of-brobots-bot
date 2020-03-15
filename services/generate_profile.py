def generate_profile(user):
    if not user['weekLeft']:
        user['weekLeft'] = 'Unlimited'
    if not user['weekLimit']:
        user['weekLimit'] = 'Unlimited'

    base = '''*{name}:*
============
Money: {money} brocoins
Plan: {planName}
Cost: {planCost}
Left: {weekLeft}/{weekLimit}
'''.format(**user)

    return base
