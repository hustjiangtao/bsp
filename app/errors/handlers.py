# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Errors handler"""


import logging
from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response


def wants_json_response():
    """if json wanted"""
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    """error hanler 404"""
    logging.info(f'404 request: {error}')
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """error handler 500"""
    logging.info(f'500 request: {error}')
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500
