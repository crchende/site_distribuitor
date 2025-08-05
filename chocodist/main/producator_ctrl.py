from chocodist.date.db import db
from sqlalchemy import select, func, exc
from chocodist.date.modele import Producator
from chocodist.params import APPNAME
from flask import flash

import logging

logger = logging.getLogger(f"{APPNAME}.{__name__}")

class ProducatorCtrl:
    # constrangere de unicitate pe numele producatorului - se va primi o eroare de la baza de date
    '''
    @classmethod
    def checkNameDuplicate(cls, **kwargs):
        p = None
        with db.session.begin():
            q = select(Producator).where(Producator.nume == kwargs['nume'])
            print("q =", q)
            p = db.session.scalar(q)
            if p != None:
                logger.debug(f"Detectat produs duplicat: {p}. Produsul de la producatorul: {p.producator.nume} exista deja!")
        return p
    '''
        
    @classmethod
    def addNewProducer(cls, **kwargs):
        try:
            with db.session.begin():
                p = Producator(**kwargs)
                db.session.add(p)
                #db.session.commit() # daca nu folosesc with, trebuie sa fac commit dupa adaugare
                logger.debug(f"Adding new product: {p}")
                ret = (True, {'nume': p.nume})
        except Exception as e:
            ret = (False, {e})
        
        return ret

    @classmethod
    def modifyProducerAttr(cls, id, value):
        orig_attr_val = None
        with db.session.begin():
            p = db.session.get(Producator, id)
        
        try:
            with db.session.begin():
                orig_attr_val = p.nume
                p.nume = value
        except exc.IntegrityError as e:
            logger.warning(f"Numele producatorului nu poate fi modificat. Mai avaem un producator cu acelasi nume!")
    
        # Get and return the new value from db
        with db.session.begin():
            modified_p = db.session.get(Producator, id)
        
        ret = None
        #exec(f"ret = modified_p.{attr_name}")
        ret = modified_p.nume
        print(ret)

        if ret != None:
            logger.debug(f"The product: {p}, was modified. the new value for 'nume' is: {ret}")
            return (True, str(ret))
        else:
            logger.error(f"The product: {p}, was not modified. returning the original value {orig_attr_val} for 'nume'")
            return (False, str(orig_attr_val))

    @classmethod
    def get_producers_id_name(cls):
        return db.session.scalars(select(Producator).order_by(Producator.nume)).all()