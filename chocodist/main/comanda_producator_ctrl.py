import json
import os
import requests
from sqlalchemy import select, func
from chocodist.main.obj_ctrl import ObjCtrl
from chocodist.params import APPNAME, basedir
from chocodist.date.db import db
from chocodist.date.modele import Producator, Produs, ComandaLaProducator
from chocodist.date.modele import StareComandaLaProducator, ProdusComandaLaProducator

from chocodist import cfg

import logging
logger = logging.getLogger(f"{APPNAME}.{__name__}")

"""
adauga, sterge, modifica
"""
class ComandaProducatorCtrl(ObjCtrl):
    
    token = None

    @classmethod
    def getProducerOffer(cls, producer_name):
        #oferta = [] # lista cu produse
        oferta = cls.getProducerOfferViaAPI(producer_name)
        if oferta != []:
            return oferta

        # icarcare din fisier local - in caz ca nu s-a luat oferta prin RESTAPI
        try:
            n = "oferta_" + producer_name.lower() + ".json"
            logger.debug(f"current folder: {os.getcwd()}")
            logger.debug(f"basedir: {basedir}")
            f_path_n = os.path.join(basedir, "date", "oferte_producatori", n)
            logger.debug(f"Oferta json: file path and name: {f_path_n}")
            with open(f_path_n, "r") as f:
                txt_jsn = f.read()
                print("txt_jsn:", txt_jsn)
                oferta = json.loads(txt_jsn)
                logger.debug(f"Oferta (obiecte obtinute din json): {oferta}")
        except Exception as e:
            logger.error("Eroare incarcare oferta de la producator:\n" + str(e))
    
        return oferta
    
    @classmethod
    def addProducerOrder(cls, form_info):
        #print(form_info)
        logger.debug(f"Producator: {form_info['producator']}, ID: {form_info['id-producator']}")

        # numele produsului si pretul unitar sunt transmise in partea de "name" din formular
        cheie_produs = "produs: "
        l_cheie_produs = len(cheie_produs)
        cheie_pret = "pret: "
        l_cheie_pret = len(cheie_pret)

        logger.debug(f"Produse comandate. Continut comanda:")

        producator = db.session.get(Producator, form_info['id-producator'])

        #Pentru simplificare consideram orice comanda plasata si primita - ID StareComandaLaProducator: 2
        stare_implicita = db.session.get(StareComandaLaProducator, 2)
        #stare = stare_implicita
        print("*** stare implicita:", stare_implicita)
        
        #'''
        # creare comanda
        c = ComandaLaProducator()
        producator.comenzi_la_producator.add(c)
        stare_implicita.comenzi.add(c)
        db.session.commit()
        logger.debug(f"Comanda: {c} a fost adaugata")
        # adaugare produs in comanda
        #'''
        #c = db.session.get(ComandaLaProducator, 1)

        for produs_comanda in form_info:
            cantitate = form_info[produs_comanda]
            if cheie_produs in produs_comanda and (cantitate != "" and cantitate != '0'):
                p_cmd_lst = produs_comanda.split(",")
                p_cmd_nume = p_cmd_lst[0].strip()
                p_cmd_pret = p_cmd_lst[1].strip()
                nume_din_form = p_cmd_nume[l_cheie_produs:].strip()
                pret_din_form = p_cmd_pret[l_cheie_pret:].strip()
                logger.debug(f" - {nume_din_form}, pret unitar: {pret_din_form}, cantitate: {form_info[produs_comanda]}")
                # verific daca am produs de la producator cu numele produsului
                # - daca nu il adaug in produse cu stoc 0
                # - creez intrari corespunzatoare in tabelul articole_comanda_la_producator
                #
                # *ar trebui sa astept sa fie onorata comanda pentru a actualiza stocul
                # *in aceasta faza, pentru a nu complica exemplul prea mult
                # *ipoteza de simplificare - comanda plasata este si onorata
                # - actualizez stocul pentru produsele existente - dupa ce au fost adaugate in 
                #   articole commenzii

                #verific daca am producatorul
                q = select(Produs).\
                            where(Produs.id_producator == form_info['id-producator'] , \
                                Produs.nume == nume_din_form)
                #print("Interogare produs:", q.compile(compile_kwargs={'literal_binds': True}))
                produs_db = db.session.scalar(q)

                if produs_db == None:
                    logger.debug(f"Produsul: {nume_din_form}, de la producatorul: {form_info['producator']}, nu exista. Trebuie adaugat")
                    # adaugare produs nou - pe baza comenzii
                    #id_producator=form_info['id-producator'], 
                    p = Produs(nume=nume_din_form, cantitate_stoc=cantitate, pret_unitar=pret_din_form) # creez fara id_producator
                    # ??? initial trebuie sa creez produsul cu cantitate_stoc = 0 si pret_unitar = 1 - adica un produs nou pe care nu-l am pe stoc.
                    producator.produse.append(p) # fac legatura, ma astept sa se creeze si valoarea pentru campul id_producator
                    #print("p=", p, "; id_producator:", p.id_producator)
                    #db.session.add(p)
                    #db.session.commit()

                    produs_comanda = ProdusComandaLaProducator(produs=p, pret_unitar=pret_din_form, cantitate=cantitate)
                    c.produse_comanda_la_producator.append(produs_comanda)

                    db.session.commit()

                else:
                    logger.debug(f"Produsul EXISTA: {nume_din_form} / {form_info['producator']}: {produs_db}, de crescut stocul")
                    #producator = db.session.get(Producator, form_info['id-producator'])
                    #p = Produs(nume = nume_din_form, pret = pret_din_form, cantitate_stoc = form_info['cantitate_stoc']) # creez fara id_producator
                    #producator.produse.append(p) # fac legatura, ma astept sa se creeze si valoarea pentru campul
                    #db.session.commit()
                
                    #
                    # Creare intrari produse in comanda
                    # 

                    # doar pentru aceasta situatie
                    #c = db.session.get(ComandaLaProducator, 7) # comanda 7
                    print("comanda:", c)
                    print("produs:", produs_db)
                    #
                    try:
                        #produs_comanda = ProdusComandaLaProducator(id_produs=produs_db.id, id_comanda=c.id, pret_unitar=pret_din_form, cantitate=cantitate)
                        
                        #c.produse_comanda_la_producator.append(produs_comanda)
                        c.produse_comanda_la_producator.append(ProdusComandaLaProducator(produs=produs_db, pret_unitar=pret_din_form, cantitate=cantitate))
                        produs_db.cantitate_stoc += int(cantitate)
                        produs_db.pret_unitar = int(pret_din_form)
                        print("produs_comanda:", produs_comanda)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        raise(e)


    @classmethod
    def getAllOrders(cls):

        q  = select(ComandaLaProducator.id, Producator.nume, \
                    func.count(ProdusComandaLaProducator.id_produs), \
                    func.sum(ProdusComandaLaProducator.cantitate * ProdusComandaLaProducator.pret_unitar))\
            .join(ComandaLaProducator.producator)\
            .join(ComandaLaProducator.produse_comanda_la_producator)\
            .group_by(ProdusComandaLaProducator.id_comanda)

     
        #q = select(ComandaLaProducator)

        print("q = ", q.compile(compile_kwargs={'literal_binds': True})) # MERGE ASA, e bine.
        comenzi = db.session.execute(q).all()
        logger.debug(f"comenzi: {comenzi}")
        return comenzi

    @classmethod
    def getOrderDetails(cls, id_comanda):
        info_cmd = {}
        q = select(ComandaLaProducator.id, Producator.nume, ComandaLaProducator.datatimp, func.sum(ProdusComandaLaProducator.pret_unitar * ProdusComandaLaProducator.cantitate))\
            .join(ComandaLaProducator.producator)\
            .join(ComandaLaProducator.produse_comanda_la_producator)\
            .join(ProdusComandaLaProducator.produs)\
            .where(ComandaLaProducator.id == id_comanda)
        #cmd = db.session.get(ComandaLaProducator, id_comanda) - folosim interogarea de mai sus pentru a afla si totalul
        cmd = db.session.execute(q).first()
        info_cmd['id_comanda'] = cmd[0]
        info_cmd['nume_producator'] = cmd[1]
        info_cmd['data_comanda'] = cmd[2].strftime("%Y-%m-%d %H:%M")
        info_cmd['total_comanda'] = cmd[3]

        print(info_cmd['data_comanda'])
        print(info_cmd['total_comanda'])

        q = select(Produs.nume, ProdusComandaLaProducator.cantitate, \
                    ProdusComandaLaProducator.pret_unitar, \
                    ProdusComandaLaProducator.pret_unitar * ProdusComandaLaProducator.cantitate)\
            .join(ComandaLaProducator.producator)\
            .join(ComandaLaProducator.produse_comanda_la_producator)\
            .join(ProdusComandaLaProducator.produs)\
            .where(ComandaLaProducator.id == id_comanda)

        continut_comanda = db.session.execute(q).all()
        info_cmd['continut_comanda'] = continut_comanda
        return info_cmd
    
    @classmethod
    def getProducerOfferViaAPI(cls, producer):
        ret = []
        # incerc cu token-ul existent
        if cls.token == None:
            cls.getProducerOfferAPIToken()


        response = requests.get(
            f'http://localhost:5001/api/v1/oferta/{producer}',
            auth = (cls.token, '')
        )
        if not response.ok:
            # posibil sa fie un token vechi
            # refac token-ul
            logger.debug(f"token NOT OK: {cls.token}")
            cls.getProducerOfferAPIToken()
            logger.debug(f"token NOU:    {cls.token}")

            response = requests.get(
                f'http://localhost:5001/api/v1/oferta/{producer}',
                auth = (cls.token, '')
            )
            if response.ok:
                ret = response.json()
                logger.debug(f"OFERTA de la {producer}:\n{json.dumps(ret, indent=4)}")
            else:
                logger.debug(f"EROARE preluare oferta prin RESTAPI: {response.status_code} {response.text}")
                logger.debug("oferta care va fi returnata: []")
        else:
            ret = response.json()

        # in caz de eroare de preuare oferta, se va intoarce o lista goala
        return ret

    @classmethod
    def getAllProducersOffersViaAPI(cls):
        ret = []
        # incerc cu token-ul existent
        if cls.token == None:
            cls.getProducerOfferAPIToken()


        response = requests.get(
            f'http://localhost:5001/api/v1/oferte',
            auth = (cls.token, '')
        )
        if not response.ok:
            # posibil sa fie un token vechi
            # refac token-ul
            logger.debug(f"token NOT OK: {cls.token}")
            cls.getProducerOfferAPIToken()
            logger.debug(f"token NOU:    {cls.token}")

            response = requests.get(
                f'http://localhost:5001/api/v1/oferte',
                auth = (cls.token, '')
            )
            if response.ok:
                ret = response.json()
                logger.debug(f"OFERTA de la producatori disponibile pe RESTAPI:\n{json.dumps(ret, indent=4)}")
            else:
                logger.debug(f"EROARE preluare oferta prin RESTAPI: {response.status_code} {response.text}")
                logger.debug("oferta care va fi returnata: []")
        else:
            ret = response.json()

        # in caz de eroare de preuare oferta, se va intoarce o lista goala
        return ret


    @classmethod
    def getProducerOfferAPIToken(cls):
        ret = ()

        response = requests.get(
            'http://localhost:5001/api/v1/tokens',
            auth = (cfg['APIUSER'], cfg['APIPASS'])
            #auth = (cfg['APIUSER'], 'parola gresita')
            #auth = ('utilizator inexistant', 'parola gresita')
        )
        if response.ok:
            r_json = response.json()
            print("response.status_code     ", response.status_code)
            print("response.ok:             ", response.ok)
            print("response.json()['token']:", r_json['token'])
            print("response.json()[user]    ", r_json['user'])
            ret = (True, r_json)
            # salvare token ca variabila de clasa pentru utilizari ulterioare
            cls.token = r_json['token']
            logger.debug(f"generat token: {cls.token}")
        else:
            print("Eroare: ", response.status_code, response.text)
            ret = str(response.status_code) + " " + response.text
            ret = (False, ret)

        return ret