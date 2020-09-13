localization = {
    'en': {
        'start': 'Hi! This *Bank of #brobots*',
        'help': u'*List of commands:*\n'
                u'/help - _see list of commands_\n'
                u'/profile - _your profile_\n'
                u'/transactions - _list of transactions_\n',

        'register': 'Would you like to register?',
        'register_success': 'Successfully registered',
        'register_failure': 'Something went wrong. Developers are notified',
        'register_cancel': 'Registration successfully cancelled',
        'register_first': 'You need to register to use this!',

        'transaction_success': 'Success',
        'transaction_failure': 'Something went wrong',
        'transaction_cancel': 'Cancelled',

        'transaction_list_title': '*Transactions*\n',
        'transaction_list_item': u'- _{} bc_ from _{}_ to _{}_\n'
                                 u'     - _{}_\n',

        'profile': u'*Profile*\n'
                    u'Name: _{name}_\n'
                    u'Money: _{money} bc_\n'
                    u'Total transactions: _{transactions}_\n',
        'profile_admin': 'Admin: _{}_\n',

        'inline_keyboard': {
            'yes': 'Yes',
            'no': 'No',
            'cancel': 'Cancel',
            'receive': 'Receive',
            'give': 'Give'
        },

        'inline_mode': {
            'message_text_trans_message': '\nMessage: _{}_',
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
