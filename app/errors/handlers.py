# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Errors handler"""


import logging
from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """error hanler 404"""
    logging.info(f'404 request: {error}')
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """error handler 500"""
    logging.info(f'500 request: {error}')
    db.session.rollback()
    return render_template('errors/500.html'), 500
