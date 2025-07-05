from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

import logging
from chocodist.params import APPNAME

logger = logging.getLogger(APPNAME + "." + __name__)
logger.debug("Creare obiect baza de date SQLAlchemy")

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })

'''
Spre deosebire de sqlalchemy simplu, cu flask_sqlalchemy se creaza obiectul
db, prin care se poate acesa fie:
 db.session - pentru interogari
 db.Model   - pentru a crea modele
'''
db = SQLAlchemy(model_class=Base)