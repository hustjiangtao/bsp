# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""main routes"""


from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from flask_sqlalchemy import get_debug_queries
from config import POSTS_PER_PAGE, DATABASE_QUERY_TIMEOUT
from app import db
from app.models import User, Post
from app.emails import follower_notification
from app.main import bp
from app.main.forms import EditProfileForm, PostForm, SearchForm


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """index handler"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live.")
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.filter_by(author=current_user).order_by(Post.timestamp.desc()).all()
    posts = current_user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template("main/index.html", title="Home",
                           form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.before_app_request
def before_request():
    """deal before request"""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@bp.after_request
def after_request(response):
    """deal after request"""
    # warning log if slow db query more than 0.5s
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            current_app.logger.warning(
                "SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (
                    query.statement, query.parameters, query.duration, query.context))
    return response


@bp.route('/user/<username>')
@login_required
def user(username):
    """user profile page handler"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User {username} is not found.")
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    # posts = current_user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('main/user.html', title="User",
                           user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """user profile edit handler"""
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', title="Edit Profile",
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    """follow handler"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User {username} is not found.")
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(f"You can't follow yourself.")
        return redirect(url_for('main.user', username=username))
    u = current_user.follow(user)
    if u is None:
        flash(f"Cannot follow {username}.")
        return redirect(url_for('main.user', username=username))
    db.session.add(u)
    db.session.commit()
    flash(f"You are now following {username}.")
    follower_notification(user, current_user)
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    """unfollow handler"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User {username} is not found.")
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(f"You can't unfollow yourself.")
        return redirect(url_for('main.user', username=username))
    u = current_user.unfollow(user)
    if u is None:
        flash(f"Cannot unfollow {username}.")
        return redirect(url_for('main.user', username=username))
    db.session.add(u)
    db.session.commit()
    flash(f"You have stopped following {username}.")
    return redirect(url_for('main.user', username=username))


@bp.route('/explore')
@login_required
def explore():
    """explore handler"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('main/index.html', title="Explore",
                           posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/search')
@login_required
def search():
    """search handler"""
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) if page > 1 else None
    return render_template("main/search.html", title="Search",
                           posts=posts, next_url=next_url, prev_url=prev_url)
