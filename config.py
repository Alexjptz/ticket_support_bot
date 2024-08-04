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

admin_panel = {
    'admin_name': os.getenv('ADMIN_PANEL_NAME'),
    'password': os.getenv('ADMIN_PANEL_PASSWORD')
}

DEFAULT_CHANNEL_ID = os.getenv('DEFAULT_CHANNEL_ID')
DEFAULT_CHANNEL_URL = os.getenv('DEFAULT_CHANNEL_URL')

admin_ids = [os.getenv('ADMINS_IDS')]
