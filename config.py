import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False
    GA = 'UA-139433876-1'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    GA = 'UA-139433876-2'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    GA = 'UA-139433876-3'


class TestingConfig(Config):
    TESTING = True
