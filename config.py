# Third-party
from dotenv import load_dotenv

# Standard
import os

load_dotenv()  # Load environment variables from .env

BASE = os.path.dirname(os.path.abspath(__file__))

project = {
    'base': BASE,
    'storage': BASE + '/storage'
}

bot = {
    'token': os.getenv('BOT_TOKEN'),
}

database = {
    'host': os.getenv('DATABASE_HOST'),
    'port': os.getenv('DATABASE_PORT'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
}

server = {
    'host': os.getenv('PANEL_HOST'),
    'port': os.getenv('PANEL_PORT'),
    'secret_key': os.getenv('SECRET_KEY')
}

DEFAULT_CHANNEL_ID = -1001838215343
DEFAULT_CHANNEL_URL = 'https://t.me/taestate'

admin_ids = [1870623013]
