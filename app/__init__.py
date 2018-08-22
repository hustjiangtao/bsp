# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""init flask app"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from app.momentjs import momentjs


# init extension instances
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()


def create_app(cfg="config"):
    # init app
    app = Flask(__name__)
    app.config.from_object(cfg)
    app.jinja_env.globals["momentjs"] = momentjs

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

    # logging email
    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        app_config = app.config
        if app_config["MAIL_SERVER"]:
            auth = None
            if app_config["MAIL_USERNAME"] and app_config["MAIL_PASSWORD"]:
                auth = (app_config["MAIL_USERNAME"], app_config["MAIL_PASSWORD"])
            secure = None
            if app_config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app_config["MAIL_SERVER"], app_config["MAIL_PORT"]),
                fromaddr='no-reply@' + app_config["MAIL_SERVER"],
                toaddrs=app_config["ADMINS"], subject='BSP Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    # logging to file
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('tmp/bsp.log', 'a+', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('bsp startup')

    return app


from app import models
