import json
import os
from sqlalchemy import select, func
from chocodist.main.obj_ctrl import ObjCtrl
from chocodist.params import APPNAME, basedir
from chocodist.date.db import db
from chocodist.date.modele import Producator, Produs, ComandaLaProducator, Utilizator
from chocodist.date.modele import StareComandaClient, ProdusComandaClient
from chocodist.date.modele import Utilizator, ComandaClient, Rol

import logging
logger = logging.getLogger(f"{APPNAME}.{__name__}")

class ComandaClientCtrl(ObjCtrl):
    @classmethod
    def getOfferInfo(cls, producator="ALL"):
        q = select(Producator.nume, Produs.nume, Produs.pret_unitar, Produs.cantitate_stoc, Produs.id).join(Produs.producator).order_by(Producator.nume).order_by(Produs.nume)
        ret = db.session.execute(q).all()
        return ret
    
    @classmethod
    def addNew(cls, request_form):
        print("addNew: args:", request_form)
        try:
            with db.session.begin():
                # pana implementarea functionalitatii Login, iau primul utilizator
                client = db.session.get(Utilizator, 1)
                print("cient.rol:", client.rol.nume)
                if client.rol.nume != "client":
                    logger.error("Rolul utilizatorului nu este 'client', nu poate da comanda!")
                    return False

                
                stare_implicita = db.session.get(StareComandaClient, 2)
                print(stare_implicita)
                c = ComandaClient()

                stare_implicita.comenzi.add(c)
                client.comenzi_client.add(c)
                
                #print("request_form_param:", request_form)

                for (input_info, cantitate) in request_form.items():
                    # ignor intrarile pentru care nu s-a selectat o cantitate
                    if cantitate == "" or cantitate == "0":
                        continue
                    # sau care nu sunt referitoare la produse
                    prod_info = cls.parse_offer_row_input(input_info)
                    if prod_info == None:
                        continue
                    
                    p = db.session.get(Produs, prod_info["produs"])
                    print(p, "cantitate cumparata:", cantitate)

                    # Actualizare stoc - se cantitatea vanduta
                    p.cantitate_stoc = p.cantitate_stoc - int(cantitate)

                    p_cmd_cl = ProdusComandaClient(pret_unitar=prod_info['pret'], cantitate=cantitate)

                    p_cmd_cl.produs = p
                    p_cmd_cl.comanda_client = c
                    db.session.add(p_cmd_cl)
        except Exception as e:
            print(e)
            raise(e)

    @classmethod
    def getAllOrders(cls):
        # func.concat nu merge in sqlite3
        with db.session.begin():
            q = select(ComandaClient.id,\
                       Utilizator.prenume.op('||')(' ').op('||')(Utilizator.nume_familie).label("nume"),\
                       ComandaClient.datatimp,\
                       func.count(ProdusComandaClient.id_produs), \
                       func.sum(ProdusComandaClient.cantitate * ProdusComandaClient.pret_unitar)\
                       )\
                .join(ComandaClient.client)\
                .join(ComandaClient.produse_comanda_client)\
                .group_by(ProdusComandaClient.id_comanda)
            all_orders = db.session.execute(q).all()
            #print(all_orders)
            return all_orders
        

    @classmethod
    def getOrderDetails(cls, id_comanda):
        info_cmd = {}
        q = select(ComandaClient.id, 
                   Utilizator.prenume.op('||')(' ').op('||')(Utilizator.nume_familie).label("nume"),\
                   ComandaClient.datatimp, \
                   func.sum(ProdusComandaClient.pret_unitar * ProdusComandaClient.cantitate))\
            .join(ComandaClient.client)\
            .join(ComandaClient.produse_comanda_client)\
            .join(ProdusComandaClient.produs)\
            .where(ComandaClient.id == id_comanda)
        #cmd = db.session.get(ComandaLaProducator, id_comanda) - folosim interogarea de mai sus pentru a afla si totalul
        cmd = db.session.execute(q).first()
        info_cmd['id_comanda'] = cmd[0]
        info_cmd['nume'] = cmd[1]
        info_cmd['data_comanda'] = cmd[2].strftime("%Y-%m-%d %H:%M")
        info_cmd['total_comanda'] = cmd[3]

        print(info_cmd['data_comanda'])
        print(info_cmd['total_comanda'])

        q = select(Produs.nume, ProdusComandaClient.cantitate, \
                    ProdusComandaClient.pret_unitar, \
                    ProdusComandaClient.pret_unitar * ProdusComandaClient.cantitate)\
            .join(ComandaClient.client)\
            .join(ComandaClient.produse_comanda_client)\
            .join(ProdusComandaClient.produs)\
            .where(ComandaClient.id == id_comanda)

        continut_comanda = db.session.execute(q).all()
        info_cmd['continut_comanda'] = continut_comanda
        return info_cmd