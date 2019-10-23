import os


class Configuration():
    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{APP_DIR}/blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'development'
    DEBUG = True
