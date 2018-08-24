# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""auth email"""


from flask import render_template, current_app
from app.emails import send_email


def send_password_reset_email(user):
    """
    send email for password reset
    :param user: sqlalchemy user obj
    """
    token = user.get_reset_password_token()
    send_email('[BSP] Reset Your Password',
               sender=current_app.config["ADMINS"][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))
