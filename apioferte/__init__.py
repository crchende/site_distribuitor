from flask import Flask, request, config
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
parent = os.path.dirname(basedir)
reldir = os.path.relpath(os.path.dirname(__file__))
basename = os.path.basename(os.path.dirname(__file__))

import logging
import logging.handlers
logger = logging.getLogger("apioferte")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

rotating_file_handler = logging.handlers.RotatingFileHandler(os.path.join(basedir, "logs", "apioferte.log"), maxBytes=10000, backupCount=10)
rotating_file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(\
    fmt='[%(asctime)s]: %(levelname)s: %(name)s: %(funcName)s: %(message)s')
    #, \
    #datefmt="%y-%m-%d %H:%M:%S %f") # milisecundele se afiseaza default iar formatarea este ca in datefmt
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(rotating_file_handler)

logger.info("=========================================")
logger.info(f"       {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]}")
logger.info("=========================================")

logger.debug(f"basedir (abspath):            {basedir}")
logger.debug(f"parent dir (abspath):         {parent}")
logger.debug(f"reldir  (rel to start dir):   {reldir}")
logger.debug(f"basename (same as above):     {basename}")

#cfg = config.Config(os.path.join(parent, 'instance')).from_pyfile('config.py')
cfg = config.Config(os.path.join(parent, 'instance'))
cfg.from_pyfile('config.py')
logger.debug(f"cfg['APIUSER']: {cfg['APIUSER']}")

def create_app():
    app = Flask(__name__,  instance_relative_config=True)
    # incarca fisierul de configurare din directorul 'instance', nu din root
    # fara acest parametru, se va incerca incarcarea config.py din 'flaskr'
    # cu acesta - din directorul 'instance' care este in afara 'flaskr'

    logger.debug(f"__name__: { __name__}")
    app.config.from_pyfile('config.py')
    logger.debug(f"app.config['APIUSER']: {app.config['APIUSER']}")

    from .api.v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix="/api/v1")
    #app.config['FLASK_RUN_PORT'] = 5001 # nu merge asa, ar trebui sa configurez o variabila de mediu

    return app
