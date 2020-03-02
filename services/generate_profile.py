def generate_profile(user):
    base = '''*{name}:*
============
Money: {money} brocoins
Plan: {planName}
Cost: {planCost}
Left: {weekLeft}/{weekLimit}
'''.format(**user)

    return base
