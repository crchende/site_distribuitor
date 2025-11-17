from . import auth
from .forms import LoginForm

from flask import current_app, render_template, request, url_for, redirect, flash
from flask import make_response

from flask_login import login_user, logout_user, login_required, current_user

from chocodist.date.db import db
from chocodist.date.modele import Utilizator, Rol
from sqlalchemy import select

from chocodist.params import APPNAME, basedir

import logging

logger = logging.getLogger(f"{APPNAME}.{__name__}")


@auth.route("/login", methods=['GET', 'POST'])
def login():
    logger.debug("/login")
   
    form = LoginForm()
    if form.validate_on_submit():
        print(form.user.data, form.password.data)
        user = db.session.scalar(select(Utilizator).where(Utilizator.nume_utilizator == form.user.data))
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash("Nume de utilizator sau parola invalide!", category="error")
    return render_template("auth/login.html", APPNAME=APPNAME, form=form)

@auth.route('/logout')
@login_required
def logout():
    u = current_user.nume_utilizator
    logout_user()
    flash(f"Utilizatorul: {u}, a fost deconectat!", category='info')
    return redirect(url_for('main.index'))