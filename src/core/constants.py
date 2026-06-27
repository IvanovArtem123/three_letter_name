import os
from dotenv import load_dotenv

load_dotenv()

MIN_PATH_SCHEME = 5
MAX_PATH_SCHEME = 150

MIN_DOMAIN_SCHEME = 5
MAX_DOMAIN_SCHEME = 150

MAX_COUNTRY_SCHEME = 150

EMAIL_MAX = 254
PHONE_MAX = 32
TG_ID_MAX = 64
USERNAME_MAX = 150
PASS_HASH_MAX = 255

CHECK_MAIL_FORMAT = (r"email IS NULL OR email ~ '^[a-zA-Z0-9]"
                     r"[a-zA-Z0-9._%+-]{0,63}@gmail\.com$'")

TOKEN_PANEL = os.getenv('TOKEN_PANEL')

EXAMPLE_PATH_PANEL = os.getenv('EXAMPLE_PATH_PANEL')
EXAMPLE_DOMAIN_PANEL = os.getenv('EXAMPLE_DOMAIN_PANEL')
EXAMPLE_PORT_PANEL = os.getenv('EXAMPLE_PORT_PANEL')
SERVER_METADATA_URL = ('https://accounts.google.com/'
                       '.well-known/openid-configuration')

FAKE_KEY = ('dmxlc3M6Ly8wMDAwLTAwMDAtMDAwMC0wMD'
            'AwLTAwMDBAemFiemF6YWJ6YS5jb206Nzc3Nzc3Nw==')


ANNOUNCE_HAPP = 'Если VPN не работает, скорее всего поможет кнопка - обновить подписку 🔄'
