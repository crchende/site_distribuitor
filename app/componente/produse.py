from flask import request

from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.date.mysqldb import selecteaza, insereaza, sterge, modifica


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

    '''
    genereaza_tabel_produse
    
    Descriere:
        Preia datele referitoare la produse. 

    Parametrii:
        cu_cap_tabel:   valoare default 1; adauga o lista cu numele coloanelor
                        pentru tabelul cu produse
                        
    Return:
        O lista de liste, cu toate datele din produse, inclusiv ID-ul pentru
        a putea implementa si operatiunile de stergere si modificare.
    
    '''
    def genereaza_date_produse(self, cu_cap_tabel=1):
        # initializare cu cap tabel
        ret = [["ID", "Producator", "Produs"]] 
        # va fi o lista de liste - fiecare element - un rand in tabel
        
        q = "SELECT produse.id, producatori.nume, produse.nume \
            FROM producatori, produse \
            WHERE produse.id_producator = producatori.id ORDER BY producatori.nume;"
        date = selecteaza(q)
        
        for (id_prds, nume_prodr, nume_prods) in date:
            print("DBG: ", id_prds, nume_prodr, nume_prods)
            ret.append((id_prds, nume_prodr, nume_prods))
            
        return ret
        
    def adauga(self, id_producator, nume_produs_nou):       
        q = "INSERT INTO `site_distribuitor`.`produse` (`id_producator`, `nume`) VALUES (%s, %s);"
        
        rez_insert = insereaza(q, id_producator, nume_produs_nou) 
        if rez_insert == []:
            ret = f"id producator: {id_producator}, nume produs: {nume_produs_nou}"
        else:
            ret = rez_insert
        
        return ret
          
    def modifica(self, id_prod, nume_nou):
        ret = "-"
        
        print("DBG: modificare denumire produs cu ID:", id_prod, "la: ", nume_nou)
        
        q = "UPDATE `site_distribuitor`.`produse` SET `nume` = '" + \
            nume_nou + \
            "' WHERE (`id` = '" + \
            id_prod + \
            "');"
        modifica(q)
        
        n_nou = selecteaza("SELECT nume from produse WHERE `id` = "\
            + id_prod + \
            ";")[0][0]
        
        print("\nN_NOU =", n_nou)
        ret = n_nou
        
        return ret        
         
    def sterge(self):
        print("DBG: sterge - request.values", request.values)
        
        id_prod = int(request.values["id"])
        print("DBG: id_prod de sters:", id_prod)
        
        q = "DELETE FROM `site_distribuitor`.`produse` WHERE (`id` = %s);"
            
        sterge(q, id_prod)
    
    
