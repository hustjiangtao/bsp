# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Forms"""


from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Login form"""
    # openid = StringField("openid", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me", default=False)
    submit = SubmitField("Sign In")


class EditForm(FlaskForm):
    """Edit form"""
    nickname = StringField("nickname", validators=[DataRequired()])
    about_me = TextAreaField("about_me", validators=[Length(min=0, max=140)])


class PostForm(FlaskForm):
    """Post form"""
    post = StringField("post", validators=[DataRequired()])


class SearchForm(FlaskForm):
    """Search form"""
    search = StringField("search", validators=[DataRequired()])
