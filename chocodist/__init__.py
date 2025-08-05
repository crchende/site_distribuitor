from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
import os
import unittest
import click
import csv

from sqlalchemy import select # obiect necesar pentru a construi select-uri
from sqlalchemy import insert, update, delete # necesare a construi interogari de adaugare/modificare/stergere
from sqlalchemy import text # pentru a declara interogari explicit: text("SE")

from .params import APPNAME, basedir

from .date.db import db
from .date import modele

from .loggingsetup import logger


logger.debug('Incarcare configuratie')

basedir = os.path.abspath(os.path.dirname(__file__))
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()

# Functie factory  - fabrica care va crea aplicatia, o va configura si va 
# intializa subdiviziunile aplicatiei
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    mail.init_app(app)
    #moment.init_app(app)

    # Acest apel creaza engine-ul / conexiunea la baza de date
    # Informatiile de conectare sunt preluate din configuratia importata din 
    # fisierul config
    db.init_app(app)
    
    # de adaugat mai jos blueprint-uri (subdiviziuni ale aplicatiei)
    # rute
    # pagini de eroare specifice
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    '''
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    '''

    return app

# Creare aplicatie cu functia factory: create_app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
logger.debug("Aplicatia a fost creata.")
#migrate = Migrate(app, db)

# Creare shell aplicatie
@app.shell_context_processor
def make_shell_context():
    return dict(db = db, modele = modele)


# Adaugare parametrii la comenzile cli cu click
# flask --app chocodist cmd-arg1 --help # afisare help din linia de comanda
@app.cli.command()
@click.argument("arg1")
@click.option("--repeta", default=1, help="de cate ori sa afiseze arg1")
def cmd_arg1(repeta, arg1):
    """
    Comanda cli:            cmd-arg1 
    Parametrii obligatorii: arg1 - argument obligatoriu pentru comanda cli 
    Parametrii optionali:   repeta - de cate ori se afiseaza arg1 
    """
    print(f"afisare {arg1} de {repeta} ori")
    for i in range(repeta):
        print("arg1:", arg1, "(de", i+1,"ori)")

@app.cli.command()
def db_afiseaza_engine():
    """Afisare engine / driver pentru baza de date"""
    print("db.engine:        ", db.engine) # db.get_engine() - o alta metoda de a gasi engine-ul
    print("db.engine.url:    ", db.engine.url)
    print("db,engine.name:   ", db.engine.name)
    print("db,engine.driver: ", db.engine.driver)


@app.cli.command()
def db_engine_afiseaza_tabele():
    connection = db.engine.connect()
    print("Tabele din baza de date:", db.engine.dialect.get_table_names(connection))
    print("\ncoloane tabel produse:")
    print("[")
    for el in db.engine.dialect.get_columns(connection, "produse"):
        print(el)
    print("]")

    print("\ncoloane tabel producatori:")
    print("[")
    for el in db.engine.dialect.get_columns(connection, "producatori"):
        print(el)
    print("]")




'''
# Rezultat executie comanda (cu baza de date doar cu datele initiale)
[2025-07-05 23:58:27,188]: DEBUG: ChocoDist: <module>: Incarcare configuratie
[2025-07-05 23:58:27,195]: DEBUG: ChocoDist: <module>: Aplicatia a fost creata.
Interogare producatori: SELECT producatori.id, producatori.nume 
FROM producatori
[Producator(1, Poiana), Producator(2, Kandia), Producator(3, Kandia"), Producator(4, Milka)]
'''
@app.cli.command()
def db_listare_producatori():
    q = select(modele.Producator)
    print("Interogare producatori:", q)
    rez = db.session.scalars(q).all()   # scalar in loc de execute - pentru a-mi intoarce doar elementul nu un tuplu cu acel element
    print(rez)


"""
# Rezultat executie comanda (cu baa de date doar cu datele initiale)
flask --app chocodist db-afiseaza-tabele
25-05-29 23:42:42: DEBUG: ChocoDist: <module>: Incarcare configuratie
[2025-05-29 23:42:42,163] DEBUG in __init__: Aplicatia a fost creata.
25-05-29 23:42:42: INFO: ChocoDist: db_afiseaza_tabele: q_lst: [('model_producatori',), ('model_produse',)]
"""
@app.cli.command()
def sqlite_afiseaza_tabele():
    q = text("SELECT name FROM sqlite_master WHERE type='table'")
    r = db.session.execute(q).all()
    logger.info(f"rezultat interogare - cu execute: {r}")
    r = db.session.scalars(q).all()
    logger.info(f"rezultat interogare - cu scalars: {r}")
    logger.info("Se observa in primul set de rezultate - lista tupluri cu un singur element / al doilea set de rezultate - lista")


@app.cli.command()
def exemplu_crud():
    pass


@app.cli.command()
def execunittest():
    """Run the unit tests."""
    app.logger.debug("Rulare teste definite cu unittest")
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

'''
Initializare baza de date cu tabelele
 - producatori
 - produse
si datele din fisierul csv: chocodist/date/dateinitiale/produse_producatori.csv
'''    
@app.cli.command()
def db_init_producator_produse():
    '''
    Initializare baza de date be baza unor date initiale - fisier produse_pro
    '''
    logger.info("Sterg toate tabelele inclusiv datele si le creez de la zero.")
    db.drop_all()
    db.create_all()

    # folosire with, pentru a da commit automat la sesiune si pentru a inchide fisierul
    with db.session.begin():           # la sfarsit se da commit automat
        with open(os.path.join(basedir, "date", "dateinitiale", "produse_producatori.csv"), "r") as f:   # la sfarsit se inchide automat fisierul
            reader = csv.DictReader(f)
            
            toti_producatorii = {}

            for row in reader:
                producator = row.pop('producator') # Numele producatorului din CSV
                print(f"-{row['nume']}-")
                print(row)
                produs_ob = modele.Produs(**row) # obiect Produs
            
                if producator not in toti_producatorii:
                    p_ob = modele.Producator(nume = producator) # obiect producator
                    db.session.add(p_ob)
                    toti_producatorii[producator] = p_ob
                
                toti_producatorii[producator].produse.append(produs_ob) # stabilirea relatiei intre obiecte
                # Ca urmare a acestui apel, se adauga in sesiune si obiectul produs - care nu a fost adaugat
                # explicit mai sus
                # Este suficient sa se adauge obiectul produs (parte 1 din relatia 1 - mai multi)
                # Cand se face legatura intre obiecte, se adauga si obiectele din parte 'mai multi' a relatiei

@app.cli.command()
def db_sterge_tabele():
    """
    Sterge toate tabelele din baza de date.
    """
    db.drop_all()

@app.cli.command()
def db_creaza_tabele_din_modele():
    """
    Creaza toate tabelele pe baza claselor model.
    (2025/05) ModelProducatori (nume clasa) -> model_producatori (nume tabel)
    """
    db.create_all()


#from flask import render_template
#from . import main
#from app import APPNAME

#import logging
#logger = logging.getLogger(APPNAME + "." +__name__)
#logger.debug(f"Incarcare modul")


@app.errorhandler(404)
def page_not_found(e):
    print(dir(e))
    return render_template('404.html', APPNAME=APPNAME, e=e), 404

@app.errorhandler(400)
def page_not_found(e):
    print(dir(e))
    return render_template('400.html', APPNAME=APPNAME, e=e), 400
    
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', APPNAME=APPNAME, e=e), 500
