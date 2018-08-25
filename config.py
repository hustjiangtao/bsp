# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Config for server"""


import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


# WTF_CSRF_ENABLED = False
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# pagination
POSTS_PER_PAGE = 20

# mail
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
MAIL_USE_TLS = bool(int(os.environ.get('MAIL_USE_TLS') or 0))  # default False
MAIL_USE_SSL = bool(int(os.environ.get('MAIL_USE_SSL') or 1))  # default True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# admins
ADMINS = ["test_jiangtao@163.com"]

# sql test
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5

# es
ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
