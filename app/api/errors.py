# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""error api handler"""


from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    """get error response"""
    payload = {"error": HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    """bad request handler for 400"""
    return error_response(400, message)
