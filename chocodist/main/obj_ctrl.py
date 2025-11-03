from chocodist.date.db import db
from sqlalchemy import select, func, exc
from chocodist.date.modele import Oras
from chocodist.params import APPNAME
from flask import flash

import logging

logger = logging.getLogger(f"{APPNAME}.{__name__}")

class ObjCtrl:
    @classmethod 
    def set_obj(cls, obj):
        cls.obj = obj

    @classmethod
    def addNew(cls, **kwargs):
        try:
            with db.session.begin():
                print(kwargs)
                p = cls.obj(**kwargs)
                db.session.add(p)
                #db.session.commit() # daca nu folosesc with, trebuie sa fac commit dupa adaugare
                logger.debug(f"Adding new {cls.obj.__name__}: {p}")
                ret = (True, {'nume': p.nume})
        except Exception as e:
            ret = (False, {e})
        
        return ret

    @classmethod
    def modifyAttr(cls, id, value):
        orig_attr_val = None
        with db.session.begin():
            x = db.session.get(cls.obj, id)
        
        try:
            with db.session.begin():
                orig_attr_val = x.nume
                x.nume = value
        except exc.IntegrityError as e:
            logger.warning(f"Numele {cls.obj.__name__}lui nu poate fi modificat. Mai avem im cu {cls.obj.__name__} acelasi nume!")
    
        # Get and return the new value from db
        with db.session.begin():
            modified_p = db.session.get(cls.obj, id)
        
        ret = None
        #exec(f"ret = modified_p.{attr_name}")
        ret = modified_p.nume
        print(ret)

        if ret != None:
            logger.debug(f"{cls.obj.__name__}: {x}, a fost modificat. 'nume': {ret}")
            return (True, str(ret))
        else:
            logger.error(f"{cls.obj.__name__}: {x}, nu a fost modificat. Numele s-a pastrat: {orig_attr_val}")
            return (False, str(orig_attr_val))

    @classmethod
    def delObj():
        pass

    @classmethod
    def get_obj_id_name(cls, obj_attr="nume"): # practic returneaza o lista de tupluri cu toate atributele, ordonate dupa obj_attr
        order_field = None
        cmd = f"order_field = cls.obj.{obj_attr}"
        exec(cmd)
        #print("order_field = ", order_field)
        return db.session.scalars(select(cls.obj).order_by(order_field)).all()