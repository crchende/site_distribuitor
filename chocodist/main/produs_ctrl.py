from chocodist.date.db import db
from sqlalchemy import select, func
from chocodist.date.modele import Produs
from chocodist.params import APPNAME
from flask import flash

import logging

logger = logging.getLogger(f"{APPNAME}.{__name__}")

'''
Am o problema cu functiile cu with, nu merg peste tot - in special acolo unde am selectat ceva

Problema cea mai mare apare la modifica_produs - unde am nevoie de datele produsului pentru a
popula formularul.
Aici nu pot folosi with - primesc eroarea: sqlalchemy.exc.InvalidRequestError: A transaction is already begun on this Session.
'''

class ProdusCtrl:
    @classmethod
    def checkNameDuplicate(cls, **kwargs):
        p = None
        with db.session.begin():
            q = select(Produs).where(Produs.nume == kwargs['nume'], Produs.id_producator == kwargs['id_producator'])
            print("q =", q)
            p = db.session.scalar(q)
            if p != None:
                logger.debug(f"Detectat produs duplicat: {p}. Produsul de la producatorul: {p.producator.nume} exista deja!")
        return p
    
    @classmethod
    def addNewProduct(cls, **kwargs):
        verific_duplicat_p =  cls.checkNameDuplicate(**kwargs)
        if verific_duplicat_p == None:
            with db.session.begin():
                p = Produs(**kwargs)
                db.session.add(p)
                #db.session.commit() # daca nu folosesc with, trebuie sa fac commit dupa adaugare
                logger.debug(f"Adding new product: {p}")
            return (True, {'nume': p.nume, 'producator': p.producator.nume})
        else:
            return (False, {'nume': kwargs['nume'], 'producator': verific_duplicat_p.producator.nume})
        
    @classmethod
    def modifyProductAttr(cls, id, attr_name, value):
        #verific daca exista un produs cu aceeasi denumire, de la acelasi utilizator
        with db.session.begin():
            p = db.session.get(Produs, id)
            if attr_name == "nume": # doar la nume este obligatoriu sa nu avem duplicat
                q = select(Produs).where(Produs.id_producator == p.id_producator, Produs.nume == value)
                r = db.session.scalars(q).one_or_none()
            else:
                r = False
        print("r =", r)
        if r:
            logger.error(f"Deja exista un produs cu acelasi nume: {value}. Numele vechi: {p.nume} nu se modifica!")
            return (False, p.nume)
        else:
            #modific si memorez valoarea initiala
            orig_attr_val = None
            
            with db.session.begin():
                exec(f"orig_attr_val = p.{attr_name}")
                if type(value) is str:
                    modify_cmd = f"p.{attr_name} = '{value}'"
                else:
                    modify_cmd = f"p.{attr_name} = {value}"
                exec(modify_cmd)
            
            # Get and return the new value from db
            with db.session.begin():
                modified_p = db.session.get(Produs, id)
            
            ret = None
            #exec(f"ret = modified_p.{attr_name}")
            ret = eval(f"modified_p.{attr_name}")
            print(ret)

            if ret != None:
                logger.debug(f"The product: {p},` was modified. the new value for {attr_name} is: {ret}")
                return (True, str(ret))
            else:
                logger.error(f"The product: {p}, was not modified. returning the original value {orig_attr_val} for {attr_name}")
                return (False, str(orig_attr_val))
            
    @classmethod
    def get_product(cls, product_id):
        with db.session.begin():
            p = db.session.get(Produs, product_id)
        return p

    @classmethod
    def modifyProduct(cls, product, nume, id_prducator, cantitate_stoc):
        pass