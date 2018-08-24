# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Models"""


from time import time
from hashlib import md5
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from app.search import SearchableMixin


# es search with sqlalchemy db event
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


followers = db.Table("followers",
                     db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
                     db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))
                     )


class User(UserMixin, db.Model):
    """User table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship("User",
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref("followers", lazy="dynamic"),
                               lazy="dynamic")

    def set_password(self, password):
        """set password with hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """check if password right"""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """get avatar of gravatar with md5 email"""
        default_avatar = "robohash"
        md5_email = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{md5_email}?d={default_avatar}&s={size}"

    def __repr__(self):
        return f"<User {self.username}>"

    def follow(self, user):
        """to follow a user"""
        if not self.is_following(user):
            self.followed.append(user)
            return self
        return None

    def unfollow(self, user):
        """unfollow a user"""
        if self.is_following(user):
            self.followed.remove(user)
            return self
        return None

    def is_following(self, user):
        """check if following the user"""
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        """get all posts created by the followed users"""
        followed = Post.query.join(followers, followers.c.followed_id == Post.user_id).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        """get a token with jwt for resetting password"""
        data = {
            "reset_password": self.id,
            "exp": time() + expires_in,
        }
        return jwt.encode(data, current_app.config["SECRET_KEY"], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        """check if the token right with jwt"""
        try:
            id = jwt.decode(token, current_app.config["SECRET_KEY"],
                            algorithms='HS256')["reset_password"]
        except:
            return None
        return User.query.get(id)


@login.user_loader
def load_user(id):
    """load user obj to session by id when user login"""
    return User.query.get(int(id))


class Post(SearchableMixin, db.Model):
    """Post table"""
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Post {self.body}>"
