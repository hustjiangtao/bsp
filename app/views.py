# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Views for url"""


from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    title = "Home"
    name = "gagaga"
    return render_template("index.html", title=title, name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"openid={form.openid.data}, remember_me={form.remember_me.data}")
        return redirect('/index')
    return render_template('login.html', form=form, providers=app.config["OPENID_PROVIDERS"])
