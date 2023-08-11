from ..date.modele import ModelProducatori
from .. import db
from flask import request
from app import APPNAME

import logging
logger = logging.getLogger(APPNAME + "." +__name__)
logger.debug(f"Incarcare modul")


class Producatori:
    def genereaza_date_producatori(self, cu_cap_tabel = 0):
        '''
        Preia datele din tabelul / elementul 'produse' pentru a fi utilizate
        pentru controale select sau alte controale.

        :param: -
        
        :return: lista cu toate elementele din tabelul producatori
                 Fiecare element este un obiect producator, cu id si nume        
        '''

        #global date_distribuitor
        
        if cu_cap_tabel == 1:
            ret = [["ID", "Producator"]]
        else:
            ret = []
            
        #for el in date_distribuitor['producatori']:
        #    ret.append([el["id"], el["nume"]])
        
        q = ModelProducatori.query.with_entities(ModelProducatori.id, \
            ModelProducatori.nume)
        logger.debug(f'interogare selectare toti producatorii: {q}')
        
        for l in q:
            logger.debug(f'{type(l)}, {l}')
            ret.append((l.id, l.nume))
        logger.debug(f'ret = {ret}')
        return ret
        
            
    def adauga(self):
        '''
        Adauga un nou producator in baza de date.
        Numele producatorului este luat din request, de aceea acesta nu este
        dat ca parametru.
        Codul care apeleaza adauga, nu trebuie sa proceseze request.form si
        sa gaseasca valoarea numelui producatorului.
           
        Modul in care aceasta metoda acceseaza direct 'request' poate fi 
        privit in comparatie cu modul in care metoda 'modifica' a aceleiasi
        clasei - 'Producatori' - primeste id-ul producatorului si noul nume
        ca parametrii. 
        Spre deosebire de 'adauga' codul care apeleaza 'modifica' proceseaza
        'request', determina id-ul si noul nume si le transmite catre metoda.
        
        Cred ca ar fi de preferat varianta 'modifica' pentru a urma 
        'principul singurei responsabilitati'. 

        Aceste functii ar trebui sa poata adauga / modifica / sterge ce li
        s-a transmis prin parametrii.
        De determinarea acestor parametrii din 'request' urmand se se ocupe
        alta secventa de cod.

        :param: None
        
        :return: None

        '''
        
        logger.debug(f'request.form: {request.form}')
        logger.debug('DBG: Dorim sa adaugam producatorul: {}'.\
            format(request.form['nume_producator_nou']))
        
        # numele poate fi regasit si in request.values["nume_producator_nou"]
        # request.values["nume_producator_nou"]
        
        producator_nou = ModelProducatori(nume = request.form['nume_producator_nou'])
        # Tabalul avand id-ul de tip autoincrement, nu este nevoie sa configuram
        # si id-ul. Acesta va fi stabilit in mod automat la adaugare in baza de 
        # date.
        x = db.session.add(producator_nou)
        logger.debug(f'x = {x}')
        db.session.commit()
        
    
    def modifica(self, id_prod, nume_nou):
        '''
        Modifica numele unui producator.
        
        De vazut in comparatie cu functia 'adauga', care nu are parametrii si 
        proceseaza variabila 'request' pentru a gasi ce nume a fost transmis
        din formularul de adaugare.
        
        De preferat varianta 'modifica', cu parametrii, nu ca si in cazul 
        'adauga'. Motiv - alinierea la principiul singurei responsabilitati.
        
        :param:  id_prod:  id-ul produsului selectat sa se modifice
        :param:  nume_nou: noul nume al producatorului
        
        :return: numele nou, citit din baza de date
        '''
    
        #global date_distribuitor
        ret = "-"
        
        logger.debug("modificare denumire producator cu ID: {} la: {}"\
            .format(id_prod, nume_nou))

        #modific numele in baza de date
        producator = ModelProducatori.query.filter_by(id=id_prod).first()
        #print(dir(db.session))
        #print(dir(db.session.dirty))
        logger.debug(f'rezultat interogare SQL: {repr(producator)}')
        
        producator.nume = nume_nou
        db.session.add(producator)
        db.session.commit()
        
        #citesc data modificata din baza de date
        producator = ModelProducatori.query.filter_by(id=int(id_prod)).first()
                
        ret = producator.nume
        
        return ret
        
        
    def sterge(self):
        '''
        Sterge o inregistrare din tabelul 'producatori'
        Inregistrarea este identificata pe baza id-ului obtinut la apasarea pe
        imaginea de stergere asociata cu producatorul.
        
        :param:  None
        
        :retrun: mesaj de succes sau eroare       
        '''
    
        logger.debug(f'sterge - request.values: {request.values}')
            
        id_prod = int(request.values["id"])

        del_obj = ModelProducatori.query.filter_by(id=id_prod).first()
        if del_obj:  
            n_p = del_obj.nume
        else:
            n_p = "None"

        try:
            db.session.delete(del_obj)
            db.session.commit()
            ret = "Sters producator: " + n_p
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            err_info = str(e.__class__.__name__) + ": " + str(e.__cause__)
            ret = "Nu pot sterge producatorul: " + str(n_p) + ". " + err_info
            logger.info(ret)
            
        return ret 
        
