# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Views for url"""


from datetime import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import get_debug_queries
from app import app, db, lm, oid
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, SQLALCHEMY_RECORD_QUERIES, DATABASE_QUERY_TIMEOUT
from .forms import LoginForm, EditForm, PostForm, SearchForm
from .models import User, Post
from .emails import follower_notification


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    title = "Home"
    name = "gagaga"
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash("You post is now live.")
        return redirect(url_for('index'))
    # posts = Post.query.filter_by(author=g.user).order_by(Post.timestamp.desc()).all()
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template("index.html", title=title, name=name, form=form, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session["remember_me"] = form.remember_me.data
        # result = oid.try_login(form.openid.data, ask_for=["nickname", "email"])
        # result = True
        return after_login(email=form.email.data, nickname=form.nickname.data)
        # return result
        # return oid.try_login(form.openid.data, ask_for=["nickname", "email"])
    return render_template('login.html', form=form, providers=app.config["OPENID_PROVIDERS"])


@lm.user_loader
def loader_user(id):
    return User.query.get(int(id))


# @oid.after_login
# def after_login(resp):
#     print('=====')
#     if resp.email is None or resp.email == "":
#         flash("Invalid login. Please try again.")
#         return redirect(url_for('login'))
#     user = User.query.filter_by(email=resp.email).first()
#     if user is None:
#         nickname = resp.nickname
#         if nickname is None or nickname == "":
#             nickname = resp.email.split('@')[0]
#         user = User(nickname=nickname, email=resp.email)
#         db.session.add(user)
#         db.session.commit()
#     remember_me = False
#     if "remember_me" in session:
#         remember_me = session["remember_me"]
#         session.pop("remember", None)
#     login_user(user, remember=remember_me)
#     return redirect(request.args.get('next') or url_for('index'))


# @oid.after_login
def after_login(email, nickname):
    print('=====')
    user = User.query.filter_by(email=email).first()
    if user is None:
        nickname = nickname
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]
        user = User(nickname=nickname, email=email)
        db.session.add(user)
        db.session.add(user.follow(user))  # self followed
        db.session.commit()
    remember_me = False
    if "remember_me" in session:
        remember_me = session["remember_me"]
        session.pop("remember", None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@app.after_request
def after_request(response):
    # warning log if slow db query more than 0.5s
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(f"User {nickname} is not found.")
        return redirect(url_for('index'))
    posts = g.user.posts.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    # posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(f"User {nickname} is not found.")
        return redirect(url_for('index'))
    if user == g.user:
        flash(f"You can't follow yourself.")
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash(f"Cannot follow {user}.")
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(f"You are now following {nickname}.")
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))


@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(f"User {nickname} is not found.")
        return redirect(url_for('index'))
    if user == g.user:
        flash(f"You can't unfollow yourself.")
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash(f"Cannot unfollow {user}.")
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(f"You have stopped following {nickname}.")
    return redirect(url_for('user', nickname=nickname))


@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html', query=query, results=results)
