config = {
    'API_ADDR': 'your_url',

    'DB': {
        'PATH': './db/users.json',
    },

    'LOG': {
        'PATH': './bot.log',
        'FORMAT': '%(asctime)s %(levelname)s: %(message)s',
    },

    'BOT': {
        'TOKEN': 'your_token',

        'START': 'Welcome back!',

        'START_REGISTER': 'Welcome to Bank of Brobots!\nWould you like to register?',
        'SUCCESS_REG': 'Welcome to Bank of Brobots!\nRegistration completed successfully!',
        'CANCEL_REG': 'Welcome to Bank of Brobots!\nRegistration is cancelled!',

        'SUCCESS': 'Alright!',

        'KEYBOARDS': {
            'YES': 'Yes',
            'NO': 'No'
        }
    }
}
