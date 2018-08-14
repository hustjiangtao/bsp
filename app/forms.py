# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Forms"""


from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Login form"""
    # openid = StringField("openid", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    nickname = StringField("nickname", validators=[DataRequired()])
    remember_me = BooleanField("remember_me", default=False)


class EditForm(FlaskForm):
    """Edit form"""
    nickname = StringField("nickname", validators=[DataRequired()])
    about_me = TextAreaField("about_me", validators=[Length(min=0, max=140)])


class PostForm(FlaskForm):
    """Post form"""
    post = StringField("post", validators=[DataRequired()])
