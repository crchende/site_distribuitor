from . import main
from flask import current_app, render_template
from sqlalchemy import select
from chocodist.date.db import db
from chocodist.date.modele import Producator, Produs
from chocodist.params import APPNAME

import logging

logger = logging.getLogger(f"{APPNAME}.{__name__}")

@main.route("/")
def index():
    logger.debug("/ - index")
    return render_template("index.html", APPNAME=APPNAME)

@main.route("/producatori")
def producatori():
    logger.debug("pagina: /producatori")
    lst_prod = db.session.scalars(select(Producator)).all()
    return render_template("producatori.html", APPNAME=APPNAME, producatori=lst_prod)

@main.route("/produse")
def produse():
    logger.debug("/produse")
    q = select(Produs).join(Producator).order_by(Producator.nume)
    '''
    q = SELECT produse.id, produse.nume, produse.id_producator 
        FROM produse JOIN producatori ON producatori.id = produse.id_producator ORDER BY producatori.nume
    '''

    logger.debug("q = " + str(q))
    lst_prod = db.session.scalars(q).all()
    return render_template("produse.html", APPNAME=APPNAME, produse=lst_prod)