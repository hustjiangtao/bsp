# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""email"""


from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from app import mail
from config import ADMINS


def async(func):
    """Async decorator"""
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@async
def send_async_email(app, msg):
    """send email async"""
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """send email"""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(current_app._get_current_object(), msg)


def follower_notification(followed, follower):
    """Send the user was followed a email when a follower coming."""
    send_email("[BSP] %s is now following you!" % follower.nickname,
               ADMINS[0],
               [followed.email],
               render_template("main/follower_email.txt",
                               user=followed, follower=follower),
               render_template("main/follower_email.html",
                               user=followed, follower=follower))
