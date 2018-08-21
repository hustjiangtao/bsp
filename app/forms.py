# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Forms"""


from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me", default=False)
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    """Register form"""
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def vaildate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    """Edit profile form"""
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About Me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    """Post form"""
    post = StringField("post", validators=[DataRequired()])


class SearchForm(FlaskForm):
    """Search form"""
    search = StringField("search", validators=[DataRequired()])
