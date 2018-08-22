# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""main forms"""


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User


class EditProfileForm(FlaskForm):
    """Edit profile form"""
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About Me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    """Post form"""
    post = TextAreaField("Say something", validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    """Search form"""
    search = StringField("search", validators=[DataRequired()])
