# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
from flask_login import LoginManager
from flask_openid import OpenID
from flask_mail import Mail
from config import basedir
from .momentjs import momentjs


app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
oid = OpenID(app, os.path.join(basedir, "tmp"), safe_roots=[])

mail = Mail(app)

app.jinja_env.globals["momentjs"] = momentjs


from app import views, models


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/bsp.log', 'a+', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('bsp startup')
