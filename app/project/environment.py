from os import environ

POSTGRES_USER = environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD')
POSTGRES_PORT = environ.get('POSTGRES_PORT')
POSTGRES_DB = environ.get('POSTGRES_DB')
REDIS_HOST = environ.get("REDIS_HOST")
REDIS_PORT = environ.get("REDIS_PORT")
REDIS_PASSWORD = environ.get("REDIS_PASSWORD")