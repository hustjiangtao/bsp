# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""api blueprint"""


from flask import Blueprint
from flask_cors import CORS


bp = Blueprint('api', __name__)
CORS(bp, supports_credentials=True)  # enable CORS on the API blue print with cookies


from app.api import users, errors, tokens
