# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Config for server"""


# WTF_CSRF_ENABLED = False
CSRF_ENABLED = True
SECRET_KEY = "BOOKMARKS_SHARE_PLAN"

OPENID_PROVIDERS = [
    {"name": 'Google', "url": 'https://www.google.com/accounts/o8/id'},
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' },
    { 'name': 'BSP', 'url': 'http://bsp.openid.org.cn/' },
]

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# pagination
POSTS_PER_PAGE = 3

# whoosh search
WHOOSH_BASH = os.path.join(basedir, "search.db")
MAX_SEARCH_RESULTS = 50

# mail
MAIL_SERVER = "smtp.163.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "test_jiangtao@163.com"
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "h123456"
# admins
ADMINS = ["test_jiangtao@163.com"]

# sql test
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5
