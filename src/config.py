import os

from dotenv import load_dotenv

load_dotenv()

VK_API_KEY = os.getenv('VK_API_KEY')
DEFAULT_BLOCK = 'animated guro'+' '

DB_PATH = "./db.db"
INTERNAL_BAN_WORDS: tuple = ("vto.pe", "vtope", "сова никогда не спит", "синий кит")
