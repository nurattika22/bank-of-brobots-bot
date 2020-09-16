localization = {
    'en': {
        'start': 'Hi! This is <b>new Bank of #brobots</b>',
        'try_help': 'Try /help to see all commands!',

        'help': u'<b>List of commands:</b>\n'
                u'/help - <i>list of commands</i>\n'
                u'/profile - <i>your profile</i>\n'
                u'/stats - <i>see your stats</i>\n'
                u'/transactions - <i>list of transactions</i>\n'
                u'\nTo transfer money type @brobank_bot in chat with your friend and follow instructions there',

        'what_is_new': u'<b>What\'s <i>new</i>?</b>\n'
                       u'- Weekly limit is cancelled! 🎉\n'
                       u'- Performance increased! 🚀\n'
                       u'- Track your expenses and income! 💹\n'
                       u'    = use /stats\n'
                       u'- Bugfixes! 🐛\n',

        'stats': u'<b>Your stats</b>\n'
                 u'Expenses: <i>{expenses} bc</i> 💸\n'
                 u'Income: <i>{income} bc</i> 💰\n\n'
                 u'Top expense: <i>{top_ex} bc</i>\n'
                 u'Top income: <i>{top_in} bc</i>\n\n'
                 u'Transactions: <i>{transactions}</i>\n',

        'register': 'Would you like to register?',
        'register_success': 'Successfully registered ✅',
        'register_failure': 'Something went wrong 🙁',
        'register_cancel': 'Registration successfully cancelled',
        'register_first': 'You need to register to use this! ❌',

        'transaction_success': u'Transaction finished successfully! 😃\n'
                               u'Money sent: <i>{} bc</i>\n',
        'transaction_failure': 'Something went wrong 🙁',
        'transaction_cancel': 'Cancelled ❌',

        'transaction_list_title': '<b>Transactions</b>\n',
        'transaction_list_item': u'- <i>{} bc</i> from {} to {}\n'
                                 u'     - <i>{}</i>\n',

        'notification_give': 'You sent <i>{} bc</i> to {}',
        'notification_request': '{} sent you <i>{} bc</i>',

        'profile': u'<b>Profile</b>\n'
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
            'message_overflow': {
                'title': '❌ Message is too long!',
                'description': '',
                'message_text': '❌ Message is too long!'
            },
            'integer_overflow': {
                'title': '❌ Integer is too big!',
                'description': '',
                'message_text': '❌ Integer is too big!'
            },
            'not_enough': {
                'title': '❌ Not enough money!',
                'description': '',
                'message_text': '❌ Not enough money!'
            },
            'balance': {
                'title': '{} brocoins on account',
                'description': 'Touch to share your balance',
                'message_text': 'I have {} bc'
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
