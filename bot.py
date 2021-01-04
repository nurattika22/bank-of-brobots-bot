from localization import localization
from common import load_config
import logging
from os import environ

from aiogram import Bot, Dispatcher

load_config()
localization = localization['en']

token = environ.get('TELEGRAM_API_TOKEN_DEV') if environ.get(
    'ENVIRONMENT') == 'DEVELOPMENT' else environ.get('TELEGRAM_API_TOKEN')

bot = Bot(token, parse_mode='HTML')
dp = Dispatcher(bot)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logging.basicConfig(filename=environ.get('LOGGING_FILENAME'),
                    format=environ.get('LOGGING_FORMAT'),
                    level=logging.INFO)
