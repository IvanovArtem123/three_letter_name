import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL', '')
LOGIN_URL = BASE_URL + "/login"
BASE_URL_INBOUNDS = os.getenv('BASE_URL_INBOUNDS', '')
