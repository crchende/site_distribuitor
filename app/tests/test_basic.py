import unittest

from flask import current_app
from app import create_app, db, logger
from app.date.modele import BazaDateBaza
from app.date.dateinitiale.date import date_distribuitor
from app.date.dateinitiale.prelucrare_date import transforma_lista_tupluri

#import logging
#logger = logging.getLogger(__name__)

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        #logger.debug("Configurare context si baza de date")
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.bdb = BazaDateBaza
        self.bdb.init_db(current_app.config['DBDEBUG'])
        
    def tearDown(self):
        #logger.debug("Stergere baza de date!")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_app_exists(self):
        self.assertFalse(current_app is None)
        
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
        
    def test_app_config_mail_server(self):
        #logger.debug(current_app.config['MAIL_SERVER'])
        self.assertTrue(current_app.config['MAIL_SERVER'])

    def test_app_db_producatori(self):
        p = self.bdb.ia_date_producatori() 
        #logger.debug(f"Produse gasite in baza de date: {p}")
        lst_tpl = transforma_lista_tupluri(date_distribuitor["producatori"])
        #lst_tpl = []
        nr_el = len(lst_tpl)
        ok = 0
        for el in p:
            if el in lst_tpl:
                ok += 1
            else:
                print(f"EROARE: {el} citit din DB, nu se regaseste in datele initiale: {lst_tpl}")
        
        if self.assertTrue(nr_el):
            self.assertEqual(ok, nr_el)
            
            
    def test_app_db_produse(self):
        p = self.bdb.ia_date_produse() 
        #logger.debug(f"Produse gasite in baza de date: {p}")
        lst_tpl = transforma_lista_tupluri(date_distribuitor["produse"])
        #lst_tpl = []
        nr_el = len(lst_tpl)
        ok = 0
        for el in p:
            if el in lst_tpl:
                ok += 1
            else:
                print(f"EROARE: {el} citit din DB, nu se regaseste in datele initiale: {lst_tpl}")
        
        if self.assertTrue(nr_el):
            self.assertEqual(ok, nr_el)
        
        
