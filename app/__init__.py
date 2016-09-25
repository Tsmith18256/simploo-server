from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
auth = HTTPBasicAuth()

BASE_PREFIX = '/api'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .main import main as main_blueprint
    from .login import login as login_blueprint
    from .users import users as users_blueprint
    from .washrooms import washrooms as washrooms_blueprint
    from .reviews import reviews as reviews_blueprint

    app.register_blueprint(main_blueprint, url_prefix=BASE_PREFIX)
    app.register_blueprint(
        login_blueprint,
        url_prefix='{}/login'.format(BASE_PREFIX)
    )
    app.register_blueprint(
        users_blueprint,
        url_prefix='{}/users'.format(BASE_PREFIX)
    )
    app.register_blueprint(
        washrooms_blueprint,
        url_prefix='{}/washrooms'.format(BASE_PREFIX)
    )
    app.register_blueprint(
        reviews_blueprint,
        url_prefix='{}/reviews'.format(BASE_PREFIX)
    )

    return app
