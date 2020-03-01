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

        'START': 'Welcome back!\n\nTry /me to see your profile',

        'START_REGISTER': 'Welcome to Bank of Brobots!\nWould you like to register?',
        'SUCCESS_REG': 'Welcome to Bank of Brobots!\nRegistration completed successfully!',
        'CANCEL_REG': 'Welcome to Bank of Brobots!\nRegistration is cancelled!',

        'NOT_USER': 'You\'re not registered. Use /start first',

        'KEYBOARDS': {
            'YES': 'Yes',
            'NO': 'No'
        }
    }
}
