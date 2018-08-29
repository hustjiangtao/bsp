# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""init flask app"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from elasticsearch import Elasticsearch

from app.momentjs import momentjs


# init extension instances
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()


def create_app(cfg="config"):
    """create flask app instance from here"""
    # init app
    app = Flask(__name__)
    app.config.from_object(cfg)
    app.jinja_env.globals["momentjs"] = momentjs

    # es
    app.elasticsearch = Elasticsearch([app.config["ELASTICSEARCH_URL"]]) if app.config["ELASTICSEARCH_URL"] else None

    # init the extension instances with app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    # register blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # api blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # logging handler config
    from app.logging_handler import logging_handler
    logging_handler(app)

    return app


from app import models
