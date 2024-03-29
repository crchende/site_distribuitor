import os
from app import create_app, db, logger
import app.date.modele as modele
from flask_migrate import Migrate

import unittest

# default = optiunea 'development' din config
# baza de date este: app/date/site_distribuitor_dev.sqlite

# Variabila de mediu 'FLASK_CONFIG' poate fi configurata in fisierul
# 'app/rulare_flask' sau in fisierul 'app/porneste_flask_shell'

# Daca se doreste schimbarea valorii implicite, trebuie modificata configuratia
# in config.py - asociat altceva cheia 'default'. 
logger.debug('FLASK_CONFIG: ' + str(os.getenv('FLASK_CONFIG')))

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
logger.debug("Aplicatia a fost creata.")
#migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db = db, modele = modele)
    
@app.cli.command()
def execunittest():
    """Run the unit tests."""
    logger.debug("Rulare teste definite cu unittest")
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)    
    
@app.cli.command()
def initbd():
    logger.info(app.config['SQLALCHEMY_DATABASE_URI'])
    modele.BazaDateBaza.sterge_continut_db()
    modele.BazaDateBaza.init_db()
