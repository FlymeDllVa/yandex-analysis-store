import os

class Flask_Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ya'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/ya'
    SQLALCHEMY_TRACK_MODIFICATIONS = False