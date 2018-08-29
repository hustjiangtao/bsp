# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Models"""


from time import time
from hashlib import md5
from datetime import datetime
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import json
from app import db, login
from app.search import SearchableMixin


# es search with sqlalchemy db event
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


followers = db.Table("followers",
                     db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
                     db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))
                     )


class PaginatedAPIMixin:
    """paginate mixin for api"""
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        """convert to a collection dict"""
        resources = query.paginate(page, per_page, False)
        data = {
            "item": [item.to_dict() for item in resources.items],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total_pages": resources.pages,
                "total_items": resources.total
            },
            "_links": {
                "self": url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                "next": url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                "prev": url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None,
            }
        }
        return data


class User(PaginatedAPIMixin, UserMixin, db.Model):
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
    message_sent = db.relationship("Message",
                                   foreign_keys="Message.sender_id",
                                   backref="author", lazy="dynamic")
    message_recivied = db.relationship("Message",
                                       foreign_keys="Message.recipient_id",
                                       backref="recipient", lazy="dynamic")
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship("Notification", backref="user", lazy="dynamic")

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

    def new_messages(self):
        """count of messages unread"""
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def to_dict(self, include_email=False):
        """convert sqlalchemy model obj to a python dict"""
        data = {
            "id": self.id,
            "username": self.username,
            "last_seen": self.last_seen.isoformat() + 'Z',
            "about_me": self.about_me,
            "post_count": self.posts.count(),
            "follower_count": self.followers.count(),
            "followed_count": self.followed.count(),
            "_links": {
                "self": url_for('api.get_user', id=self.id),
                "followers": url_for('api.get_followers', id=self.id),
                "followed": url_for('api.get_followed', id=self.id),
                "avatar": self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        """convert a python dict to sqlalchemy model obj"""
        for field in ['', '']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


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


class Message(db.Model):
    """Private message"""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message {self.body}>"


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))
