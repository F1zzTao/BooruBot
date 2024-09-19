import os

from dotenv import load_dotenv

load_dotenv()

VK_API_KEY = os.getenv('VK_API_KEY')
DEFAULT_BLOCK = 'animated guro'+' '

DB_PATH = "./db.db"
