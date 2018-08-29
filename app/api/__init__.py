# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""api blueprint"""


from flask import Blueprint


bp = Blueprint('api', __name__)


from app.api import users, errors, tokens
