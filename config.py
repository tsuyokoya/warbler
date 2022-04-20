from base64 import b64encode
import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", b64encode(os.urandom(64)).decode('utf-8'))


class ProductionConfig(Config):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",'postgresql:///warbler')
    

class DevelopmentConfig(Config):
    ENV = 'development'
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",'postgresql:///warbler')


class TestingConfig(Config):
    TESTING = True