'''global config'''


from dotenv import find_dotenv, load_dotenv
from os import environ as env

if ENV_FILE := find_dotenv():
    load_dotenv(ENV_FILE)

# APP
APP_HOST=env.get('APP_HOST', 'localhost')
APP_PORT=env.get('APP_PORT', 8888)
APP_SECRET_KEY=env.get('APP_SECRET_KEY', '@#$14TAKE_ON_ME!@#!5take_me_up412312')
APP_COOKIE_NAME=env.get('APP_COOKIE_NAME', "MY_AWESOME_COOKIE")

# AUTH0
AUTH0_CLIENT_ID=env.get('AUTH0_CLIENT_ID', 'default')
AUTH0_CLIENT_SECRET=env.get('AUTH0_CLIENT_SECRET', 'SDJASNON_ME!@#!5take_me_up41$14TAKE_ON_M%')
AUTH0_DOMAIN=env.get('AUTH0_DOMAIN', 'default')

# CORS
BACKEND_CORS_ORIGINS = [
    f"http://{APP_HOST}:{APP_PORT}",
    f"http://127.0.0.1:{APP_PORT}",
    f"http://localhost:{APP_PORT}",
]

# SSL
SSL_KEYFILE_PASSPHRASE=env.get('SSL_KEYFILE_PASSPHRASE', 'nope:)')

# MONGO
DB_USER=env.get('DB_USER', 'admin')
DB_PASSWORD=env.get('DB_PASSWORD', 'admin')
DB_HOST=env.get('DB_HOST', 'localhost')
DB_PORT=env.get('DB_PORT', 3306)
DB_NAME=env.get('DB_NAME', 'super_db')
DB_CONNECTION_URL=f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'

# ACTIVEMQ CONNECTION
ACTIVEMQ_HOST = env.get('ACTIVEMQ_HOST', '')
ACTIVEMQ_PORT = env.get('ACTIVEMQ_PORT', '')
ACTIVEMQ_USERNAME = env.get('ACTIVEMQ_USERNAME', '')
ACTIVEMQ_PASSWORD = env.get('ACTIVEMQ_PASSWORD', '')

# ACTIVEMQ QUEUES - SUB
ACTIVEMQ_CONVERT_IMAGE_REPLY_QUEUE = env.get('ACTIVEMQ_CONVERT_IMAGE_REPLY_QUEUE', '')
ACTIVEMQ_STORE_IMAGE_REPLY_QUEUE = env.get('ACTIVEMQ_STORE_IMAGE_REPLY_QUEUE', '')
ACTIVEMQ_GET_IMAGE_REPLY_QUEUE = env.get('ACTIVEMQ_GET_IMAGE_REPLY_QUEUE', '')

# ACTIVEMQ QUEUES - PUB
ACTIVEMQ_CONVERT_IMAGE_QUEUE = env.get('ACTIVEMQ_CONVERT_IMAGE_QUEUE', '')
ACTIVEMQ_STORE_IMAGE_QUEUE = env.get('ACTIVEMQ_STORE_IMAGE_QUEUE', '')
ACTIVEMQ_GET_IMAGE_QUEUE = env.get('ACTIVEMQ_GET_IMAGE_QUEUE', '')
ACTIVEMQ_DELETE_IMAGE_QUEUE = env.get('ACTIVEMQ_DELETE_IMAGE_QUEUE', '')
ACTIVEMQ_SEND_NOTIFICATION_QUEUE = env.get('ACTIVEMQ_SEND_NOTIFICATION_QUEUE', '')
