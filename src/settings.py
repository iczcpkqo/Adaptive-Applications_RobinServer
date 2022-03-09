from os import environ

DB_CONNECTION_STRING = environ.get('DB_CONNECTION_STRING')
DB_NAME = environ.get('DB_NAME')
FLASK_RUN_PORT = int(environ.get('FLASK_RUN_PORT'))