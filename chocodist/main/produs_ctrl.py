from chocodist.date.db import db
from sqlalchemy import select, func
from chocodist.date.modele import Producator, Produs, Oras, ProdusComandaLaProducator
from chocodist.params import APPNAME
from flask import flash
from chocodist.main.obj_ctrl import ObjCtrl
from chocodist.main.oras_ctrl import OrasCtrl
from chocodist.main.producator_ctrl import ProducatorCtrl

import logging

logger = logging.getLogger(f"{APPNAME}.{__name__}")

'''
Am o problema cu functiile cu with, nu merg peste tot - in special acolo unde am selectat ceva

Problema cea mai mare apare la modifica_produs - unde am nevoie de datele produsului pentru a
popula formularul.
Aici nu pot folosi with - primesc eroarea: sqlalchemy.exc.InvalidRequestError: A transaction is already begun on this Session.
'''

class ProdusCtrl(ObjCtrl):
    @classmethod
    def isDuplicate(cls, **kwargs):
        p = None
        
        #with db.session.begin():
        q = select(Produs).where(Produs.nume == kwargs['nume'], Produs.id_producator == kwargs['id_producator'])
        logger.debug(f"q = {q}")
        p = db.session.scalar(q)
        if p != None:
            logger.debug(f"Detectat produs duplicat: {p}. Produsul de la producatorul: {p.producator.nume} exista deja!")
        #print(db.session.in_transaction())
        return p
    
    '''
        **kwargs = {
            'nume': <nume produs>
            'id_producator': <id producator>
            'cantitate_stoc': <valoare cantitate stoc>
            'pret_unitar': <valoare pret>
        }
    '''
    @classmethod
    def addNewProduct(cls, lst_locatii, **kwargs):
        duplicate_product = cls.isDuplicate(**kwargs)
        if duplicate_product == None:
            #with db.session.begin():
            p = Produs(**kwargs) # nume, id_producator, cantitate_stoc, pret_unitar
            # nu-i clar daca se populeaza automat prin adaugarea id_produs
            db.session.add(p)

            # relatie de la mai multi la mai multi prin tabel de legatura fara atribute extra
            # prin popularea relatiei: p.orase.append(oras), se populeaza si tabelul de legatura
            for id in lst_locatii:
                oras = db.session.get(Oras, int(id))
                #print(oras)
                p.orase.append(oras)
            db.session.commit() # daca nu folosesc with, trebuie sa fac commit dupa adaugare
            logger.debug(f"Adding new product: {p}")
            return (True, {'nume': p.nume, 'producator': p.producator.nume})
        else:
            return (False, {'nume': kwargs['nume'], 'producator': duplicate_product.producator.nume})
        
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
    def deleteProduct(cls, id):
        ret = [0, ""]
        p = db.session.get(Produs, id)
        nume_p = p.nume
        p_in_comenzi = db.session.scalars(select(ProdusComandaLaProducator).where(ProdusComandaLaProducator.id_produs == p.id)).first()
        if p_in_comenzi:
            logger.error(f"Produsul: {p_in_comenzi}, nu poate fi sters. Este adaugat in comenzi!")
            ret = [0, p.nume]
            return ret

        try:
            db.session.delete(p)
            db.session.commit()
            ret = [1, nume_p]
        except Exception as e:
            logger.error(e)
            ret = [0, nume_p]
        
        return ret

    
    # trei metode pentru a obtine produsul ...
    # - prima foloseste with - dar nu merge apelata peste tot si returneaza obiectul produs
    # - a doua face acelasi lucru dar fara with
    # - a treia nu intoarce produsul ci atributele acestuia intr-un dictionar ...
    # cred ca pana la urma ar avea sens doar a doua metoda - eventual cu un mesaj de eroare daca nu gaseste produsul
    # Acum in cod este folosita a treia varianta
    @classmethod
    def get_product(cls, product_id):
        with db.session.begin():
            p = db.session.get(Produs, product_id)
        return p
    
    @classmethod
    def getProduct(cls, product_id):
        return db.session.get(Produs, product_id)

    @classmethod
    def getProductInfo(cls, product_id):
        ret = None
        #with db.session.begin():
        p = db.session.get(Produs, product_id)
        ret = {"nume": p.nume, "id_producator": p.id_producator, "cantitate_stoc": p.cantitate_stoc, "producator": p.producator.nume, "pret_unitar": p.pret_unitar}
        return ret
    
    @classmethod
    def initModifyForm(cls, form, id_produs):
        p = ProdusCtrl.getProductInfo(id_produs) # de vazut daca renunt la varianta asta, pot folosi obiectul
        p_obj = ProdusCtrl.getProduct(id_produs)
        p_obj_locatii = [str(oras.id) for oras in p_obj.orase]
        
        form.name.data = p['nume']
        producatori = ProducatorCtrl.get_obj_id_name()
        locatii = OrasCtrl.get_obj_id_name() # lista tupluri [(id, nume, si alte atribute), ...]
        form.producer_id.choices = [(prd.id, prd.nume) for prd in producatori]
        form.locatie.choices = [(l.id, l.nume) for l in locatii]
        form.locatie.data = p_obj_locatii
        form.producer_id.data = str(p['id_producator'])
        form.cantitate_stoc.data = str(p['cantitate_stoc'])
        form.pret_unitar.data = str(p['pret_unitar'])


    @classmethod
    def modifyProduct(cls, id_product, nume, id_producator, cantitate_stoc, pret_unitar, lst_locatii):
        p = db.session.get(Produs, id_product)
        logger.debug(f"Produsul pe care vrem sa-l modificam: {p.id}, {p.nume}, {p.producator.nume}, {p.cantitate_stoc}")
        duplicate_product = cls.isDuplicate(nume=nume, id_producator=id_producator)
        if duplicate_product == None:
            #with db.session.begin():
            if nume != None:
                print("------ NUME --------")
                p.nume = nume
            if id_producator != None:
                print("----- ID Producator -----")
                p.id_producator = id_producator
            if cantitate_stoc != None:
                print("----- Cantitate STOC --------")
                p.cantitate_stoc = cantitate_stoc
            if pret_unitar != None:
                print("----- Pret Unitar --------")
                p.pret_unitar = pret_unitar

            p.orase.clear() # pentru a nu memora locatia anterioara
            for id_locatie in lst_locatii:
                l_obj = db.session.get(Oras, int(id_locatie))
                p.orase.append(l_obj)
            db.session.commit()

            logger.debug(f"Produsul modificat. noile valori: {p.nume}, {p.producator.nume}, {p.cantitate_stoc}, {p.cantitate_stoc}, {p.orase}")
            return (True, (p.nume, p.producator.nume, p.cantitate_stoc, p.pret_unitar, p.orase))
        else:
            logger.debug("Nume duplicat pentru produs, mai exista un produs cu acelasi nume: {duplicate_product.nume} de la acelasi producator: {duplicate_product.producator.nume}")
            return (False, (duplicate_product.nume, duplicate_product.producator.nume)) # or it will fail with error in with - if problems
        
    @classmethod
    def analysisAndModifyProduct(cls, form, request_form, request_args):
        p = ProdusCtrl.getProductInfo(request_args['id']) # dictionar cu atributele obiectului, nu obiectul
        # poate nu are sens ..., deocamdata merg asa
        p_obj = ProdusCtrl.getProduct(request_args['id'])
        p_obj_locatii = [str(oras.id) for oras in p_obj.orase]

        if form.validate_on_submit():
            # mesaj daca nu sunt modificari
            if p['nume'] == request_form['name'] and \
                p['id_producator'] == int(request_form['producer_id']) and \
                p['cantitate_stoc'] == int(request_form['cantitate_stoc']) and \
                p['pret_unitar'] == int(request_form['pret_unitar']) and \
                p_obj_locatii == request_form.getlist('locatie'):
                logger.debug("Nu sunt schimbari pentru produs, datele din formular sunt cele initiale pentru produs!")
                return ""
            
            # valori implicite pentru nume si id_producator
            if p['nume'] == request_form['name']:
                nume_nou = None
            else:
                nume_nou = request_form['name']
            if p['id_producator'] == int(request_form['producer_id']):
                id_producator_nou = None
            else:
                id_producator_nou = request_form['producer_id']

            m_info =  ProdusCtrl.modifyProduct(id_product=request_args['id'], \
                                        nume=nume_nou, \
                                        id_producator=id_producator_nou, \
                                        cantitate_stoc=request_form['cantitate_stoc'], \
                                        pret_unitar = request_form['pret_unitar'], \
                                        lst_locatii = request_form.getlist("locatie"))
            if m_info[0] == True:
                lst_orase = [x.nume for x in m_info[1][4]]
                flash(f"Produsul:   {p['nume']}, {p['producator']} va fi modificat!", category="warning")
                flash(f"""Produsul a fost modificat: {m_info[1][0]}, {m_info[1][1]}, 
                        - cantitate: {m_info[1][2]}, 
                        - pret unitar: {m_info[1][3]}
                        - locatii: {lst_orase}""", category="success")
                return "redirect"
            else:
                flash(f"Nume duplicat pentru produs, mai exista un produs cu acelasi nume de la producatorul {m_info[1][1]}!", category="danger")
                # form data problems - keep the form on the screen
        else:
            flash("Datele introduse in formular nu sunt valide. Produsul nu poate fi modificat", category="danger")
            logger.error("Problema validare date din formular!")

        return ""