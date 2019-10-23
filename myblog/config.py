import os


class Configuration():
    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{APP_DIR}/blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '1cf84d5d8a5c63660ab6e3461ae0047edd4c87e52ad6eef4605d831a95656189'
