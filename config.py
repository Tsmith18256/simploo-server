import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SECRET_KEY = '0tRjWH29pvoQfIh2y7De6QJX62f1FTC8' or \
        os.environ.get('SECRET_KEY')
    SOCIAL_FACEBOOK = {
        'consumer_key': os.environ.get('FACEBOOK_APP_ID'),
        'consumer_secret': os.environ.get('FACEBOOK_APP_SECRET')
    }
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://simploo:password@localhost/simploo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    # TODO: remove this line after there are some properties in this class
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
