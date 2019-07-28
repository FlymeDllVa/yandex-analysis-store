import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ya'
    SQLALCHEMY_DATABASE_URI = f"postgres://postgres:postgres@localhost:5432/ya"
    SQLALCHEMY_TRACK_MODIFICATIONS = False