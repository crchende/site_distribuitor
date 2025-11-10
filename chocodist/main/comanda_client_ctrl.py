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
                #db.session.commit()
                
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

                    p_cmd_cl = ProdusComandaClient(pret_unitar=prod_info['pret'], cantitate=cantitate)

                    p_cmd_cl.produs = p
                    p_cmd_cl.comanda_client = c
                    db.session.add(p_cmd_cl)
                        

        except Exception as e:
            print(e)
            raise(e)

