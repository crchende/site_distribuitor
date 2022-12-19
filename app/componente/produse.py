from .. import db
from ..date.modele import ModelProduse, ModelProducatori

#from flask import request

from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError

import logging
logger = logging.getLogger(__name__)


# TBD - adaugarea mesajelor personalizate la verificare nu functioneaza ca mai 
# jos. 
# 
# Validarea extra 'validate'_'in_production' se va aplica pentru
# campul 'in_production' dupa celelalte validari date la creerea componentei.
# 
class FormProduse(FlaskForm):
    nume_produs_nou = StringField("Produs nou:", \
        [DataRequired(message="Dati numele produsului")])
    id_producator = SelectField("Producator", \
        [DataRequired(message="Selectati numele producatorului")])
    submit = SubmitField("Adauga")
    
    #def validate_id_producator(form, nume_produs_nou):
    #    raise ValidationError("AICI")
    '''
    def hidden_tag(self):
        super()    
    '''
    
class Produse:
    def genereaza_date_produse(self, cu_cap_tabel=1):
        '''
        Preia datele referitoare la produse. 

        :param:  cu_cap_tabel:   valoare default 1; adauga o lista numele 
                                coloanelor pentru tabelul cu produse
                            
        :return: o lista de obiecte, cu toate datele din produse, inclusiv ID-ul pentru
            a putea implementa si operatiunile de stergere si modificare.
        
        '''

        # initializare cu cap tabel
        ret = [["ID", "Producator", "Produs"]] 
        # va fi o lista de liste - fiecare element - un rand in tabel
        
        q = ModelProduse.query.all()
        
        for el in q:
            nume_producator = ModelProducatori.query\
            .filter_by(id=el.id_producator).first().nume
            ret.append([el.id, nume_producator, el.nume])
        
        return ret
        
    def adauga(self, id_producator, nume_produs_nou):
        '''
        Adauga un nou produs.
        
        :param: id_producator: 
        :param: nume_produs_nou:
        
        :return: obiectul adaugat, selectat din baza de date 
                 (pot verifica ca am adaugat obiectul)
        '''
        produs_nou = ModelProduse(id_producator=id_producator, \
            nume=nume_produs_nou)
            
        db.session.add(produs_nou)
        db.session.commit()              

        p_n = ModelProduse.query.filter_by(nume=nume_produs_nou).first()
        logger.debug(str(p_n))
        
        return p_n
          
    def modifica(self, id_prod, nume_nou):
        '''
        Modifica numele unui produs.
        
        :param:  id_prod:  id-ul produsului
        :param:  nume_nou: noul nume pentru produs
        
        :return: obiectul modificat selectat din baza de date
        '''
        global date_distribuitor
        ret = "-"
        
        logger.debug(f'modificare denumire produs cu ID: {id_prod} la: {nume_nou}')
        prod = date_distribuitor["produse"]
        lst_index = [prod.index(el) for el in prod if el["id"] == int(id_prod)]
        print("lst_index", lst_index)
        index = int(lst_index[0])
        
        prod[index]["nume"] = nume_nou
        ret = prod[index]["nume"]
        
        return ret
        
         
    def sterge(self, id_prod):
        '''
        Sterg produsul selectat.
        
        :param: id_prod: id-ul produsului de sters, selectat din pagina WEB
        '''
        logger.debug(f'sterge prods cu id-ul: {id_prod}')
        
        del_obj = ModelProduse.query.filter_by(id=id_prod).first()
        db.session.delete(del_obj)
        db.session.commit()
