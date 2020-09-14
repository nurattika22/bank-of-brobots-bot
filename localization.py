localization = {
    'en': {
        'start': 'Hi! This *Bank of #brobots*',
        'help': u'*List of commands:*\n'
                u'/help - <i>see list of commands</i>\n'
                u'/profile - <i>your profile</i>\n'
                u'/transactions - <i>list of transactions</i>\n'
                u'\nTo transfer money type @brobank_bot in chat with your friend and follow instructions there',

        'register': 'Would you like to register?',
        'register_success': 'Successfully registered',
        'register_failure': 'Something went wrong. Developers are notified',
        'register_cancel': 'Registration successfully cancelled',
        'register_first': 'You need to register to use this!',

        'transaction_success': 'Success',
        'transaction_failure': 'Something went wrong',
        'transaction_cancel': 'Cancelled',

        'transaction_list_title': '<b>Transactions</b>\n',
        'transaction_list_item': u'- <i>{} bc</i> from {} to {}\n'
                                 u'     - <i>{}</i>\n',

        'profile': u'*Profile*\n'
                    u'Name: <i>{name}</i>\n'
                    u'Money: <i>{money} bc</i>\n'
                    u'Total transactions: <i>{transactions}</i>\n',
        'profile_admin': 'Admin: <i>{}</i>\n',

        'inline_keyboard': {
            'yes': 'Yes',
            'no': 'No',
            'cancel': 'Cancel',
            'receive': 'Receive',
            'give': 'Give'
        },

        'inline_mode': {
            'message_text_trans_message': '\nMessage: <i>{}</i>',
            'no_message': 'No message provided',
            'empty': {
                'title': '💵 Enter amount of brocoins',
                'description': 'and choose one of operations above',
                'message_text': '❌ Amount of brocoins wasn\'t entered!'
            },
            'not_registered': {
                'title': '❌ You\'re not registered!',
                'description': '',
                'message_text': '❌ User is not registered!'
            },
            'overflow': {
                'title': '❌ Message is too long!',
                'description': '',
                'message_text': '❌ Message is too long!'
            },
            'give': {
                'title': 'Send {} brocoins',
                'description': 'Message: {}',
                'message_text': 'Receive your {} brocoins!'
            },
            'request': {
                'title': 'Request {} brocoins',
                'description': 'Message: {}',
                'message_text': 'Send me {} brocoins!',
            }
        },

        'cannot': 'You can\'t do that! ❌',
        'empty_list': 'List is empty 😟',
        'ping': 'Still alive! 👍'
    }
}
