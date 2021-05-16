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

    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://")

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    ALERT_INTERVAL = environ.get('ALERT_INTERVAL') or 30


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
