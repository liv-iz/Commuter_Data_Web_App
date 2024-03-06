import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///project.db'


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'


class ProdConfig(Config):
    Production = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'  # TODO: Update to prod URI for coursework 2?


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True
