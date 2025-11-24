from flask import Flask, render_template
from flask import config as flask_config

from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment

from flask_migrate import Migrate

from flask_wtf.csrf import CSRFProtect

import os
import unittest
import click
import csv, json

from sqlalchemy import select # obiect necesar pentru a construi select-uri
from sqlalchemy import insert, update, delete # necesare a construi interogari de adaugare/modificare/stergere
from sqlalchemy import text # pentru a declara interogari explicit: text("SE")
from sqlalchemy import exc # pentru exceptii sepecifice sqlalchemy

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

from .params import APPNAME, basedir

from .date.db import db
from .date import modele

from .loggingsetup import logger
logger.debug('Incarcare configuratie')

basedir = os.path.abspath(os.path.dirname(__file__))
parent = os.path.dirname(basedir)

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
csrf = CSRFProtect()

#cfg = config.Config(os.path.join(parent, 'instance')).from_pyfile('config.py')
# this is the apicfg - for this case it works, both chocodist and offers from producers api
# are in the same place - I can use a singe file
# this info should be actually duplicated in the chocodist and api cfg files 
cfg = flask_config.Config(os.path.join(parent, 'instance'))
cfg.from_pyfile('config.py')
logger.debug(f"cfg['APIUSER']  : {cfg['APIUSER']}")
logger.debug(f"\ncfg['APIOFERTE'] = {json.dumps(cfg['APIOFERTE'], indent=4)}")

# Factory method - creates the WEB app and connects to it all its components
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    mail.init_app(app)
    #moment.init_app(app)
    csrf.init_app(app)

    # create the engine - db connection - using the URL from app config
    db.init_app(app)

    login_manager.init_app(app)

    migrate = Migrate(app, db)  

    # app blueprints (app subdivisions / modules, each one specialized in a speciffic area)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

# Creare aplicatie cu functia factory: create_app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
logger.debug("Aplicatia a fost creata.")
#migrate = Migrate(app, db)

# Creare shell aplicatie
@app.shell_context_processor
def make_shell_context():
    return dict(db = db, modele = modele)


# Command line params with click library
# flask --app chocodist cmd-arg1 --help # afisare help din linia de comanda
@app.cli.command()
@click.argument("arg1")
@click.option("--repeta", default=1, help="de cate ori sa afiseze arg1")
def cmd_arg1(repeta, arg1):
    """
    CLI command:            cmd-arg1 
    Required params: arg1 - argument obligatoriu pentru comanda cli 
    Optional parameters:  - repeta - how many times to show arg
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

@app.cli.command()
def db_listare_producatori():
    q = select(modele.Producator)
    print("Interogare producatori:", q)
    rez = db.session.scalars(q).all()   # scalar in loc de execute - pentru a-mi intoarce doar elementul nu un tuplu cu acel element
    print(rez)

@app.cli.command()
def sqlite_afiseaza_tabele():
    q = text("SELECT name FROM sqlite_master WHERE type='table'")
    r = db.session.execute(q).all()
    logger.info(f"rezultat interogare - cu execute: {r}")
    r = db.session.scalars(q).all()
    logger.info(f"rezultat interogare - cu scalars: {r}")
    logger.info("Se observa in primul set de rezultate - lista tupluri cu un singur element / al doilea set de rezultate - lista")


@app.cli.command()
def db_add_towns():
    with db.session.begin():
        for oras in ["Bucuresti", "Suceava", "Zalau", "Cluj-Napoca", "Bistrita", "Drobeta Turnu Severin"]:
            o = modele.Oras(nume=oras)
            db.session.add(o)

@app.cli.command()
def db_view_producator_comenzi_relatie_write_only():
    # Utilitate - Producator are relatie WriteOnly catre ComenziLaProducator
    # motiv - pot fi foarte multe comenzi pentru un producator si nu este\
    # util sa avem o relatie lazy load, cum avem de exemplu pentru Produs.
    # Relatia WriteOnly ajuta la generarea interogarii care trebuie executata
    # apoi separat
    producator1 = db.session.get(modele.Producator, 1)
    query_from_write_only = producator1.comenzi_la_producator.select()
    print("Interogare pentru tot tabelul - generata de relatia WriteOnly:", query_from_write_only.compile().string)
    # Voi folosi aceasta interogare sa vad daca am macar o comanda de la producator
    # daca da, nu voi sterge producatorul
    # Cum pot fi foarte multe comenzi, este ineficient sa fac o interogare pentru 
    # toate elementele, este suficient sa gasesc o comanda
    query_with_limit = query_from_write_only.limit(1)
    print("Interogarea anterioara - limitata la o singura intrare:", query_with_limit)

    print(" ========== Executarea interogarilor de mai sus =========== ")
    print(" --- Toate comenzile pentru produsul selectat --- ")
    print(db.session.scalars(query_from_write_only).all())

    print(" --- Doar o singura comanda (prima?) varianta cu scalars - evidentiere ca avem un singur element in lista --- ")
    print(db.session.scalars(query_with_limit).all())

    print(" --- Doar o singura comanda (prima?) varianta cu scalar - mai buna de folosit pentru un singur element --- ")
    print(db.session.scalar(query_with_limit))

@app.cli.command()
def help_migration():
    print("""

IMPORTANT: 
          
Migrarea este necesara cand se modifica schema bazei de date.
Se foloseste pachetul Alembic din flask, care se importa cu comanda:
    from flask_migrate import Migrate
In aplication factory, trebuie creat un obiect Migrate: 
    migrate = Migrate(app, db)
(Nota: Alte pachete se creaza in afara application factory si se inregistreaza
       cu aplicatia dar acesta se creaza in application factory cu app ca parametru)



1)  cd in 'chocodist'
2)  daca s-a rulat initializarea - ar trebui sa fie directorul 'migrations'
    Altfel: 
          flask --app . db init
3)  Generare fisier migrare
          
          flask --app . db migrate -m "mesaj - de ce fac migrarea"

          (cum suntem deja in chocodist - directorul cu __init__.py in care este factory method
          aplicatia este chiar '.')
          Ne asteptam sa se genereze un nou fisiere de migrare in directorul 'migrations/versions'
          cu un cod - codul migrarii + mesajul adaugat cu -m - doar daca sunt schimbari in 
          modele.py - adica daca se adauga/sterg tabele sau daca se modifica - se adauga/sterg coloane

          - pentru sqlalchemy, pentru a modifica cheia privata tabelul trebuie sters si creat
            din nou (ceea ce este destul de dezavantajos daca contine date ...)
          
          - pot sa apara erori. TBD - de adaugat exemple de erori si cum se adreseaza

4)   UPGRADE
          
          flask --app . db upgrade

          Se face upgrade-ul la ultima varianta generata

5)   DOWNGRADE
          
          Verificare pe care versiune suntem:

          flask --app . db history
          flask --app . db heads
          flask --app . db show

          De verificat si in directorul migrations/versions - versiunile afisate de comenzile de mai sus

          in baza de date, in tabelul alembic_version este id-ul ultimei migrari

          ATENTIE - o migrare de mai multe ori, poate duce la stergerea unor tabele
                  DE FOLOSIT CU MULTA ATENTIE !!!

        ERORI - de documentat
          Pot apare diverse erori, in special daca nu se duce la capat un upgrade sau un downgrade.

          ESTE BINE de avut un tool extra, de exemplu: DB BROWSER FOR SQLite, pentru SQLite, pentru a vedea baza de date.
""")


@app.cli.command()
def adauga_rol():
    nume_rol = "client"
    try:
        with db.session.begin():
            db.session.add(modele.Rol(nume=nume_rol))
    except exc.IntegrityError as e:
        print(f"Rolul: {nume_rol} nu poate fi adaugat. Exista deja.")
        print(f"Eroarea de tip {e.__class__.__name__} generata de baza de date:\n{e}")


@app.cli.command()
def adauga_utilizator():
    nume_utilizator = "client_intern"
    prenume = "Intern"
    nume_familie = "Intern"
    try:
        with db.session.begin():
            rol_client = db.session.get(modele.Rol, 1)
            cl_int = modele.Utilizator(nume_utilizator=nume_utilizator, prenume=prenume, nume_familie=nume_familie, rol=rol_client)
            cl_int.password = "client"
            db.session.add(cl_int)
    except exc.IntegrityError as e:
        print(f"Utilizatorul {nume_utilizator} nu poate fi adaugat. Exista deja.")
        print(f"Eroarea de tip: {e.__class__.__name__} generata de baza de date::\n{e}")

@app.cli.command()
def verifica_utilizator():
    cl_int = db.session.get(modele.Utilizator, 1)
    print("Rezultat validare:", cl_int.verify_password("client1"))
    try:
        print(cl_int.password)
    except AttributeError as e:
        print(f"Validat: {e}")

@app.cli.command()
def sterge_produse_si_comenzi_client():
    with db.session.begin():
        db.session.execute(delete(modele.ProdusComandaClient))
        db.session.execute(delete(modele.ComandaClient))

'''
@app.cli.command()
def exemplu_crud():
    pass
'''

@app.cli.command()
def execunittest():
    """Run the unit tests."""
    app.logger.debug("Rulare teste definite cu unittest")
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

'''
CLI command to initialize the database.
Tables:
 - producatori
 - produse
will be created and initialized with info from the csv file: 
 - chocodist/date/dateinitiale/produse_producatori.csv
'''
'''
# comenzi anulate - erau utile initial, acum nu mai sunt utile
@app.cli.command()
def db_init_producator_produse():
    'Initializare baza de date be baza unor date initiale - fisier produse_pro'
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
'''


#######################################
# Custom Error Handlers
#######################################
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
