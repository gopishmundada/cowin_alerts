from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class BaseConfig(object):
    FLASK_APP = 'wsgi.py'
    FLASK_DEBUG = False
    TESTING = False

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    WTF_CSRF_ENABLED = True

    SERVER_NAME = environ.get('SERVER_NAME')
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_ENV = environ.get('FLASK_ENV')

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')


class DevelopmentConfig(BaseConfig):
    FLASK_DEBUG = True
    TESTING = False


class TestConfig(BaseConfig):
    FLASK_DEBUG = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URL')


config_by_name = dict(
    production=BaseConfig,
    development=DevelopmentConfig,
    testing=TestConfig,
)
