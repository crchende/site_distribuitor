from . import auth
from .forms import LoginForm, RegisterForm

from flask import current_app, render_template, request, url_for, redirect, flash
from flask import make_response

from flask_login import login_user, logout_user, login_required, current_user

from chocodist.date.db import db
from chocodist.date.modele import Utilizator, Rol
from sqlalchemy import select, func

from chocodist.params import APPNAME, basedir

import logging

logger = logging.getLogger(f"{APPNAME}.{__name__}")


@auth.route("/login", methods=['GET', 'POST'])
def login():
    logger.debug("/login")
   
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(Utilizator).where(Utilizator.nume_utilizator == form.user.data))

        # Utilizatorii neconfirmati sunt tratati ca utilizatori anonimi / guest
        if user is not None and user.verify_password(form.password.data):
            if user.confirmat != True:
                flash("Utilizatorul nu este confirmat. Contactati administratorul site-ului pentru confirmare!", category='danger')
            else:
                login_user(user, form.remember_me.data)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
        else:
            flash("Nume de utilizator sau parola invalide!", category="danger")

    return render_template("auth/login.html", APPNAME=APPNAME, form=form)

@auth.route('/logout')
@login_required
def logout():
    u = current_user.nume_utilizator
    logout_user()
    flash(f"Utilizatorul: {u}, a fost deconectat!", category='info')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # validarea ca nu sunt mai multi utilizatori nevalidati se face in validatorul formularului pentru 'user'

        # aici nu merge db.session.begin() - trebuie varianta clasica cu commit la sfarsit
        u = Utilizator(nume_utilizator = form.user.data, prenume=form.prenume.data, nume_familie=form.nume.data, id_rol=1)
        u.password = form.password.data
        logger.debug(f"S-a creat utilizatorul {u}")
        db.session.add(u)
        db.session.commit()

        flash(f"Utilizatorul: {form.user.data} a fost creat. Trebuie validat cu administratorul site-ului inainte de a-l putea folosi!")
        return(redirect(url_for('auth.login')))
    return render_template("auth/inregistrare.html", APPNAME=APPNAME, form=form)