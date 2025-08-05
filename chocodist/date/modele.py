from .db import db
from typing import List
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import logging
from chocodist.params import APPNAME

logger = logging.getLogger(APPNAME + "." + __name__)
logger.debug("Modele")

'''
Creare tabele pe baza modelelor
with app.app_context():
    db.create_all()

este nevoie de app_context - si se foloseste ca mai sus
'''

################################################################################
# ORM - Object Relational Mapper
################################################################################

class Producator(db.Model):
    __tablename__ = "producatori"
            
    id: Mapped[int] = mapped_column(primary_key=True)
    nume: Mapped[str] = mapped_column(String(30), index=True, unique=True)
    produse: Mapped[List["Produs"]] = relationship(back_populates="producator")

    def __repr__(self):
        return f"Producator({self.id}, {self.nume})"
        #return f"Producator(id={self.id!r}, nume={self.nume!r})" # !r = nu elimina/interpreteaza backslash-urile: \n -> \\n

class Produs(db.Model):
    __tablename__ = "produse"

    id: Mapped[int] = mapped_column(primary_key=True)
    nume: Mapped[str] = mapped_column(String(40))
    id_producator: Mapped[int] = mapped_column(ForeignKey("producatori.id"), index=True)
    producator: Mapped['Producator'] = relationship(back_populates="produse")
    cantitate_stoc: Mapped[Optional[int]] = mapped_column(default=0)

    # tratare problema duplicat nume pentru acelasi producator aici
    # nu pare o idee buna - ar trebui sa incerc sa creez un obiect
    # la creare - le verific pe celelalte si daca mai este unu cu acelasi nume
    # pentru acelasi producator renunt ... - pare prea complex ...
    #
    # totusi - am validat ca se apeleaza constructorul si ca-l pot suprascrie
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("apel __init__ Produs", self)

    def __repr__(self):
        return f"Produs({self.id}, {self.nume}, {self.producator})"