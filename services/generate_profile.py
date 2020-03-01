def generate_profile(user):
    base = '''*{name}:*
==========
Plan: {planName}
Cost: {planCost}
Left: {weekLeft}/{weekLimit}

*Accounts:*
===========
'''.format(**user)

    if not len(user['accounts']):
        base += 'No accounts yet'

    for account in user['accounts']:
        if not account['customName']:
            account['customName'] = 'Untitled'

        base += '{customName} - {money} bc\n'.format(**account)

    return base
