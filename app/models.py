# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Models"""


from hashlib import md5
from app import db


class User(db.Model):
    """User table"""
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def avatar(self, size):
        md5_email = md5(self.email.encode('utf-8')).hexdigest()
        return f"http://www.gravatar.com/avatar/{md5_email}?d=mm&s={size}"

    def __repr__(self):
        return f"<User {self.nickname}>"


class Post(db.Model):
    """Post table"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Post {self.body}>"
