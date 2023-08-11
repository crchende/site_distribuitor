from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
#from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
APPNAME = 'site_distribuitor'

import logging
###################
# Logger setup
###################
#
# The logger is configured in the program
# The producer_consumer_srv uses a config file for logger. 
#
# this is for the root logger from which all the loggers are derived
#logging.basicConfig(level = logging.DEBUG)

logger = logging.getLogger(APPNAME +"."+__name__)
#We can configure strictly our logger
logger.setLevel(logging.DEBUG)
# creating a logging handler with level DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

#log messages formating
#datefmt: "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(\
    fmt='%(asctime)s: %(levelname)s: %(name)s: %(funcName)s: %(message)s', \
    datefmt="%y-%m-%d %H:%M:%S")
#attaching the formater to the handler:
console_handler.setFormatter(formatter)

#attaching the handler to the logger
logger.addHandler(console_handler)


logger.debug('Incarcare configuratie')
from config import config

logger.debug("Initializare aplicatie")
###########################################################
bootstrap = Bootstrap()
mail = Mail()
# moment - Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    mail.init_app(app)
    #moment.init_app(app)
    db.init_app(app)
    
    # attach routes and custom error pages here
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
