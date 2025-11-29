from .db import db
from datetime import datetime
from typing import List
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped
from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

from chocodist import login_manager

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
    produse: Mapped[list["Produs"]] = relationship(back_populates="producator")
    comenzi_la_producator: WriteOnlyMapped['ComandaLaProducator'] = relationship(back_populates="producator", passive_deletes=True)
    # vreau sa pot sterge producatorii fara comenzi, fara passive_deletes = True, nu pot

    def __repr__(self):
        return f"Producator({self.id}, {self.nume})"
        #return f"Producator(id={self.id!r}, nume={self.nume!r})" # !r = nu elimina/interpreteaza backslash-urile: \n -> \\n


ProdusOras = Table(
    'produse_orase',
    db.Model.metadata,
    Column('product_id', ForeignKey('produse.id'), primary_key=True, nullable=False),
    Column('oras_id', ForeignKey('orase.id'), primary_key=True, nullable=False),
)

class Produs(db.Model):
    __tablename__ = "produse"

    id: Mapped[int] = mapped_column(primary_key=True)
    nume: Mapped[str] = mapped_column(String(40))
    id_producator: Mapped[int] = mapped_column(ForeignKey("producatori.id"), index=True)

    cantitate_stoc: Mapped[Optional[int]] = mapped_column(default=1)
    pret_unitar: Mapped[int] = mapped_column(default=0)

    producator: Mapped['Producator'] = relationship(back_populates='produse')
    orase: Mapped[list['Oras']] = relationship(secondary=ProdusOras, back_populates='produse')

    #produs_comenzi_la_producator: WriteOnlyMapped['ProdusComandaLaProducator'] = relationship(back_populates='produs', passive_deletes=True)
    # daca n-am passive_deletes=True, nu pot sterge produsul, chiar daca nu este in nici o comanda
    # de vazut ce se intampla daca am produsul adaugat intr-o comanda
    # separarea logica - produs cumparat de la producator
    produs_comenzi_la_producator: WriteOnlyMapped['ProdusComandaLaProducator'] = relationship(back_populates='produs', passive_deletes=True)

    # separare logica - partea de vanzare, putem avea produs vandut
    produs_comenzi_client: WriteOnlyMapped['ProdusComandaClient'] = relationship(back_populates='produs', passive_deletes=True)


    # tratare problema duplicat nume pentru acelasi producator aici
    # nu pare o idee buna - ar trebui sa incerc sa creez un obiect
    # la creare - le verific pe celelalte si daca mai este unu cu acelasi nume
    # pentru acelasi producator renunt ... - pare prea complex ...
    #
    # totusi - am validat ca se apeleaza constructorul si ca-l pot suprascrie
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("apel __init__ Produs", self, kwargs)

    def __repr__(self):
        return f"Produs({self.id}, {self.nume}, {self.producator}, {self.cantitate_stoc}, {self.pret_unitar})"
    
class Oras(db.Model):
    __tablename__ = "orase"

    id: Mapped[int] = mapped_column(primary_key = True)
    nume: Mapped[str] = mapped_column(String(40), index=True, unique=True)

    produse: Mapped[list['Produs']] = relationship(secondary=ProdusOras, back_populates='orase')

    def __repr__(self):
        return f"Oras({self.id}, {self.nume})"


####################
# COMANDA PRODUCATOR
####################
class ComandaLaProducator(db.Model):
    __tablename__ = "comenzi_la_producator"
    id: Mapped[int] = mapped_column(primary_key = True)
    datatimp: Mapped[datetime] = mapped_column(default=datetime.now, index=True)
    id_producator: Mapped[int] = mapped_column(ForeignKey('producatori.id'))
    id_stare: Mapped[int] = mapped_column(ForeignKey('stari_comanda_la_producator.id'))

    producator: Mapped['Producator'] = relationship(back_populates='comenzi_la_producator')
    stare: Mapped['StareComandaLaProducator'] = relationship(back_populates="comenzi")
    produse_comanda_la_producator: Mapped[list['ProdusComandaLaProducator']] = relationship(back_populates='comanda_la_producator')
    #spre deosebire de produse - unde un produs poate sa apara foarte multe intrari din produsele din comenzi, aici pentru 
    #o comanda avem un set unic de intrari in produse_comenzi_la_producator, relatia nu este de tip: WriteOnlyMapped

    def __repr__(self):
        return f"ComandaLaProducator({self.id}, {self.datatimp}, {self.id_producator}, {self.id_stare}, {self.produse_comanda_la_producator})"

class StareComandaLaProducator(db.Model):
    __tablename__ = "stari_comanda_la_producator"

    id: Mapped[int] = mapped_column(primary_key = True)
    nume: Mapped[str] = mapped_column(String(30), index=True, unique=True) # 1. trimisa (catre producator), 2. primita (de la producator)
    comenzi: WriteOnlyMapped['ComandaLaProducator'] = relationship(back_populates='stare')

    def __repr__(self):
        return f"StareComandaLaProducator({self.id},{self.nume})"

class ProdusComandaLaProducator(db.Model):
    __tablename__ = "produse_comenzi_la_producator"
    id_produs: Mapped[int] = mapped_column(ForeignKey('produse.id'), primary_key=True)
    id_comanda: Mapped[int] = mapped_column(ForeignKey('comenzi_la_producator.id'), primary_key=True)
    pret_unitar: Mapped[float]
    cantitate: Mapped[int]

    produs: Mapped['Produs'] = relationship(back_populates='produs_comenzi_la_producator')
    comanda_la_producator: Mapped['ComandaLaProducator']= relationship(back_populates='produse_comanda_la_producator')

    def __repr__(self):
        return f"ProdusComandaLaProducator({self.id_produs}, {self.id_comanda}, {self.pret_unitar}, {self.cantitate})"

################
# UTILIZATOR + ROL
################
class Utilizator(UserMixin, db.Model):
    __tablename__ = "utilizatori"
    id: Mapped[int] = mapped_column(primary_key=True)
    nume_utilizator: Mapped[str] = mapped_column(String(30), index=True, unique=True)
    prenume: Mapped[str] = mapped_column(String[30]) # name, first name, given name
    nume_familie: Mapped[str] = mapped_column(String[30]) # surname, family name, last name
    password_hash: Mapped[str] = mapped_column(String(128))
    id_rol: Mapped[int] = mapped_column(ForeignKey('roluri.id'))
    confirmat: Mapped[Optional[bool]] = mapped_column(default=False)

    rol: Mapped['Rol'] = relationship(back_populates='utilizatori')
    comenzi_client: WriteOnlyMapped['ComandaClient'] = relationship(back_populates="client", passive_deletes=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #super(Utilizator, self).__init__(**kwargs) # varianta pt PY 2.7
        #adaug un rol default cand creez un utilizator. Rol default: Client
        if self.rol is None:
            self.rol = db.session.scalar(select(Rol).where(Rol.default==True))

    @property
    def password(self):
        raise AttributeError("parola nu este un atribut care poate fi citit")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Utilizator({self.id}, {self.nume_utilizator}, {self.prenume}, {self.nume_familie}, {self.id_rol})"
    
    def poate(self, perm):
        return self.rol is not None and self.rol.are_permisiune(perm)
    
    def este_administrator(self):
        return self.poate(Permisiuni.ADMINISTRARE)

# clasa pentru a trata cazul utilizatorilor nelogati: anonim / vizitator (guest)
# aplicatia poate apela current_user.poate() si current_user.este_administrator()
# fara sa mai fie nevoie sa verifice daca userul este logat sa nu
class AnonymousUser(AnonymousUserMixin):
    def poate(self, permisiuni):
        return False
    
    def este_administrator(self):
        return False

# login manager este configurat sa utilizeze clasa definita in aplicatie AnonymousUser 
# prin atributul acestuia anonymous_user
login_manager.anonymous_user = AnonymousUser

class Rol(db.Model):
    __tablename__ = "roluri"
    id: Mapped[int] = mapped_column(primary_key=True)
    nume: Mapped[str] = mapped_column(String(30), index=True, unique=True)
    default: Mapped[Optional[bool]] = mapped_column(default=False, index=True)
    permisiuni: Mapped[Optional[int]] = mapped_column(default=0)

    utilizatori: Mapped[list['Utilizator']] = relationship(back_populates='rol')

    def __init__(self, **kwargs):
        """
        Initial valoarea pentru permisiuni este None.
        Trebuie setata la 0, de aceea avem nevoie de acest constructor.
        """

        #super(Rol, self).__init__(**kwargs) # pt compatibilitate cu Pytnon 2.7
        # se specifica tipul si obiectul. In Python3 apelul este simplificat:
        super().__init__(**kwargs)

        if self.permisiuni == None:
            self.permisiuni = 0

    def __repr__(self):
        return f"Rol({self.id}, {self.nume})"
    
    def are_permisiune(self, perm):
        return self.permisiuni&perm == perm

    def elimina_permisiune(self, perm):
        if self.are_permisiune(perm):
            self.permisiuni -= perm

    def adauga_permisiune(self, perm):
        if not self.are_permisiune(perm):
            self.permisiuni += perm

    def reset_permisiuni(self):
        self.permisiuni = 0

    @staticmethod
    def insereaza_roluri():
        """
        Functia adauga rolurile de mai jos in baza de date si configureaza 
        permisiunile pentru fiecare din ele.

        Nu se observa aici utilizatorul 'anonim' / 'vizitator' - un utilizator
        care vizualizeaza site-ul fara sa fie logat.
        Acesta nu va avea nici unul din drepturile de mai jos.
        Va putea vizualiza pagina de informare si ofeta pentru clienti
        """
        roluri = {
            'Client': [Permisiuni.COMENZICLIENT],
            'Angajat': [Permisiuni.COMENZICLIENT, Permisiuni.COMENZIPRODUCATOR, 
                        Permisiuni.VIZUALIZAREDATEADMIN],
            'Administrator': [Permisiuni.COMENZICLIENT, Permisiuni.COMENZIPRODUCATOR, 
                              Permisiuni.VIZUALIZAREDATEADMIN, Permisiuni.ADMINISTRARE]
        }
        for rol in roluri:
            db_r = db.session.scalar(select(Rol).where(Rol.nume == rol))
            if db_r == None:
                db_r = Rol(nume=rol)
                db.session.add(db_r)
            print(db_r)
            for perm in roluri[rol]:
                db_r.adauga_permisiune(perm)
            
            db.session.commit()

# functie ceruta de catre extensia Flask-Login (LoginManager) pentru a fi apelata cand extensia
# trebuie sa incarce un user din baza de date - dat fiind ID-ul user-ului
# decorator pus la dispozitie de extensia login manager
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Utilizator, int(user_id))

class Permisiuni:
    """
    User-ul cu rol 'anonim' va putea vizualiza oferta 'chocodist' si pagina de introducere
    Nu poate da comenzi, nu poate vizualiza altceva

    User-ul de cu rol 'Client' - poate da comenzi client si-si poate vizualiza comenzile

    User-ul de cu rol 'Angajat' - poate da comenzi la client si producator 
                                - poate vizualiza toate comenzile
                                - poate vedea datele administrative
                                - NU le poate modifica
    
    User-ul cu rol 'Administrator' - poate face toate actiunile de mai sus si in plus poate
                                     sa si modifice datele administrative
    """
    COMENZICLIENT = 1                #2^0
    COMENZIPRODUCATOR = 2            #2^1
    VIZUALIZAREDATEADMIN = 4         #2^2
    ADMINISTRARE = 8                 #2^3

################
# COMANDA CLIENT - foarte similar cu comanda la producator, le mentin separate. Motiv - flexibilitate. Parte negativa - ~duplicat~ de cod deocamdata
################
class ComandaClient(db.Model):
    __tablename__ = "comenzi_client"
    id: Mapped[int] = mapped_column(primary_key = True)
    datatimp: Mapped[datetime] = mapped_column(default=datetime.now, index=True)
    id_utilizator: Mapped[int] = mapped_column(ForeignKey('utilizatori.id'))
    id_stare: Mapped[int] = mapped_column(ForeignKey('stari_comanda_client.id'))

    client: Mapped['Utilizator'] = relationship(back_populates='comenzi_client')
    stare: Mapped['StareComandaClient'] = relationship(back_populates="comenzi")
    produse_comanda_client: Mapped[list['ProdusComandaClient']] = relationship(back_populates='comanda_client')
    #spre deosebire de produse - unde un produs poate sa apara foarte multe intrari din produsele din comenzi, aici pentru 
    #o comanda avem un set unic de intrari in produse_comenzi_la_producator, relatia nu este de tip: WriteOnlyMapped

    def __repr__(self):
        return f"ComandaClient({self.id}, {self.datatimp}, {self.id_producator}, {self.id_stare}, {self.produse_comanda_client})"

class StareComandaClient(db.Model):
    __tablename__ = "stari_comanda_client"

    id: Mapped[int] = mapped_column(primary_key = True)
    nume: Mapped[str] = mapped_column(String(30), index=True, unique=True) # 1. primita (de la client), 2. trimisa (catre client)
    comenzi: WriteOnlyMapped['ComandaClient'] = relationship(back_populates='stare')

    def __repr__(self):
        return f"StareComandaClient({self.id},{self.nume})"

class ProdusComandaClient(db.Model):
    __tablename__ = "produse_comenzi_client"
    id_produs: Mapped[int] = mapped_column(ForeignKey('produse.id'), primary_key=True)
    id_comanda: Mapped[int] = mapped_column(ForeignKey('comenzi_client.id'), primary_key=True)
    pret_unitar: Mapped[float]
    cantitate: Mapped[int]

    produs: Mapped['Produs'] = relationship(back_populates='produs_comenzi_client')
    comanda_client: Mapped['ComandaClient']= relationship(back_populates='produse_comanda_client')

    def __repr__(self):
        return f"ProdusComandaClient({self.id_produs}, {self.id_comanda}, {self.pret_unitar}, {self.cantitate})"
    

