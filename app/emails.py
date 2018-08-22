# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""email"""


from flask import render_template
from flask_mail import Message
from app import app, mail
from config import ADMINS
from .decorators import async


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)


def follower_notification(followed, follower):
    """Send the user was followed a email when a follower coming."""
    send_email("[BSP] %s is now following you!" % follower.nickname,
               ADMINS[0],
               [followed.email],
               render_template("follower_email.txt",
                               user=followed, follower=follower),
               render_template("follower_email.html",
                               user=followed, follower=follower))


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[BSP] Reset Your Password',
               sender=app.config["ADMINS"][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))
