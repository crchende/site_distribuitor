from chocodist.date.db import db
from chocodist.main.obj_ctrl import ObjCtrl
from chocodist.params import APPNAME
from chocodist.date.modele import Producator, Produs, ComandaLaProducator
from flask import flash
from sqlalchemy import exc

import logging
logger = logging.getLogger(f"{APPNAME}.{__name__}")

class ProducatorCtrl(ObjCtrl):
    @classmethod
    def delObj(cls, id):
        err = 0
        try:
            #with db.session.begin():
            p = db.session.get(Producator, id)
            query_comenzi_write_only = p.comenzi_la_producator.select().limit(1)
            if db.session.scalar(query_comenzi_write_only) == None:
                db.session.delete(p)
                db.session.commit()
            else:
                err = 1
                flash(f"Producatorul {p.nume} nu poate fi sters. Are comenzi asociate!", category="danger")
        except exc.IntegrityError:
            err = 1
            flash(f"Producatorul {p.nume} nu poate fi sters. Are produse asociate!", category="danger")

        if err == 0:
            flash(f"Producatorul: {p.nume}, a fost sters!", category='success')

        
ProducatorCtrl.set_obj(Producator)