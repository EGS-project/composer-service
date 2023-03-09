'''global config'''

from typing import List
from dotenv import find_dotenv, load_dotenv
from os import environ as env

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# AUTH0
AUTH0_CLIENT_ID=env.get('AUTH0_CLIENT_ID', 'default')
AUTH0_CLIENT_SECRET=env.get('AUTH0_CLIENT_SECRET', 'default')
AUTH0_DOMAIN=env.get('AUTH0_DOMAIN', 'default')

AUTH0_ALGORITHMS=env.get('AUTH0_ALGORITHMS', 'default')
AUTH0_API_AUDIENCE=env.get('AUTH0_API_AUDIENCE', 'default')

# APP
APP_HOST=env.get('APP_HOST', '0.0.0.0')
APP_PORT=env.get('APP_PORT', 8888)
APP_SECRET_KEY=env.get('APP_SECRET_KEY', '@#$14TAKE_ON_ME!@#!5take_me_up412312')

# CORS
BACKEND_CORS_ORIGINS = [
    f"http://localhost:{APP_PORT}",
    f"http://127.0.0.1:{APP_PORT}",
    f"http://127.0.0.0:{APP_PORT}",
]
