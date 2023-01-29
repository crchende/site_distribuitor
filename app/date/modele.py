from .. import db

from .dateinitiale.date import date_distribuitor
import logging

logger = logging.getLogger(__name__)

################################################################################
# ORM - Object Relational Mapper
################################################################################
class ModelProducatori(db.Model):
    __tablename__ = "producatori"
    
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(30))
    
    produse = db.relation('ModelProduse', backref='producator')
    
    def __str__(self):
        return f"({self.id!r}, {self.nume!r})"
    
    def __repr__(self):
        return f"Producatori(id={self.id!r}, nume={self.nume!r})"
        
    def date(self):
        return (self.id, self.nume)


class ModelProduse(db.Model):
    __tablename__ = "produse"
    
    id = db.Column(\
        db.Integer, primary_key=True)
    id_producator = db.Column(\
        db.Integer,\
        db.ForeignKey("producatori.id"),\
        nullable=False)
        
    nume = db.Column(\
        db.String(30))
            
    def __str__(self):
        return f"({self.id!r}, {self.id_producator!r} {self.nume!r})"
    
    def __repr__(self):
        return f"Produse(id={self.id!r}, id_producator={self.id_producator!r} nume={self.nume!r})"
        
    def date(self):
        return (self.id, self.id_producator, self.nume)


class ModelComenziLaProducatori(db.Model):
    __tablename__ = 'comenzi_la_producatori'
    
    id = db.Column(db.Integer, primary_key=True)
    id_producator = db.Column(\
        db.Integer,\
        db.ForeignKey("producatori.id"),\
        nullable=False)
        
    def __str__(self):
        return f"({self.id!r}, {self.id_producator!r})"
        
    
    def date(self):
        return (self.id, self.id_producator)
        
    
class ModelContinutComenziLaProducatori(db.Model):
    __tablename__ = "continut_comenzi_la_producatori"
    
    id_comanda = db.Column(\
        db.Integer,\
        db.ForeignKey("comenzi_la_producatori.id"),\
        nullable=False,\
        primary_key=True)
        
    id_produs = db.Column(\
        db.Integer,\
        db.ForeignKey("produse.id"),\
        nullable=False,
        primary_key=True)
        
    cantitate = db.Column(\
        db.Integer)
        
    def __str__(self):
        return f"(x={self.id_comanda!r}, {self.id_produs!r}, {self.cantitate})"

    def __repr__(self):
        return f"ModelCotinutComenziLaProducator(id_comanda={self.id_comanda!r}, id_produs={self.id_produs!r}, cantitate={self.cantitate})"
        
    def date(self):
        return (self.id_comanda, self.id_produs, self.cantitate)
        
    
class BazaDateBaza:
    '''
        Clasa are metode statice pentru initializare / stergere baza de date.
            init_db
            sterge_continut_db
       
        Prima metoda - creaza si initializeaza baza de date.
        Daca baza de date nu exista, trebuie executata aceasta medoda din 
        flask shell.
        Din app executa comanda 
        'porneste_flask_shell' (linux) sau 
        'porneste_flask_shell.bat' (windows)
        Executa din shell:
        >>> modele.BazaDateBaza.init_db()
        
        pentru stergerea tuturor datelor executa:
        >>> modele.BazaDateBaza.sterge_continut_db()
        
        Pe langa acestea, clasa mai contine o metoda statica cu exemple de 
        interogari:
            exemple_interogari_db.
            
        Aici mai pot fi adaugate si alte exemple, pentru a le avea grupate toate
        intr-un loc sa fie usor de urmarit si de folosite ca exemple pentru 
        interogari folosite in aplicatie
        
    '''

    @staticmethod
    def init_db(dbdebug = True):
        global date_distribuitor
        '''
        Creaza tabelele in baza de date sqlite.
        Adauga datele din date_distribuitor in baza de date.
        '''
        if dbdebug:
            logger.debug("Creere si initializare baza de date cu datele initiale")
        #logger.debug(f"dbdebug = {dbdebug}")
        
        # creere tabele
        db.create_all()
        
        # adaugare date in tabele
        for el in date_distribuitor['producatori']:
            obiect_rand = ModelProducatori(id = el["id"], nume = el["nume"])
            db.session.add(obiect_rand)
            #db.session.commit()
            
        for el in date_distribuitor['produse']:
            obiect_rand = ModelProduse(id = el["id"],\
                id_producator = el["id_producator"],\
                nume = el["nume"])
            db.session.add(obiect_rand)
        
        for el in date_distribuitor["comenzi_la_producatori"]:
            obiect_rand = ModelComenziLaProducatori(id=el["id"],\
                id_producator=el["id_producator"])
            db.session.add(obiect_rand)
        
        for el in date_distribuitor["continut_comenzi_la_producatori"]:
            obiect_rand = ModelContinutComenziLaProducatori(\
                id_comanda=el["id_comanda"],\
                id_produs=el["id_produs"],\
                cantitate=el["cantitate"])
            db.session.add(obiect_rand)    
        
        db.session.commit()
        
        if dbdebug:
            logger.debug("Verificare DB SQLITE - citire date:")
            logger.debug("Vefificare DB Producatori:")
            for l in ModelProducatori.query.all():
                print(l)
                
            print("---\n")
            logger.debug("Verificare DB Produse:")
            for l in  ModelProduse.query.all():
                print(l)
            
            print("---\n")
            logger.debug("Verificare DB Comenzi La Producatori:")
            for l in  ModelComenziLaProducatori.query.all():
                print(l)
            
            print("---\n")
            logger.debug("Verificare DB Continut Comenzi La Producatori:")
            logger.debug(f'Tot continutul: {ModelContinutComenziLaProducatori.query.all()}')
            logger.debug("--linie cu linie--")
            for l in  ModelContinutComenziLaProducatori.query.all():
                print(l)

    @staticmethod
    def ia_date_producatori():
        #logger.debug("Verificare date in DB pentru Producatori:")
        p = ModelProducatori.query.all()
        lst_p = [(l.id, l.nume) for l in p]
        return(lst_p)
   
    @staticmethod
    def ia_date_produse():
        #logger.debug("Verificare date in DB pentru Produse:")
        p = ModelProduse.query.all()
        lst_p = [l.date() for l in p]
        return lst_p
         
                
    @staticmethod
    def sterge_continut_db():
        db.drop_all()


    @staticmethod
    def exemple_interogari_db():
        logger.debug("\nEchivalent cu: SELECT id, nume from produse")
        x = ModelProduse.query.\
            with_entities(ModelProduse.id, ModelProduse.nume).\
            all()
        for el in x:
            print(type(el), el)

        logger.debug("\nEchivalent cu SELECT * from produse")
        x = ModelProduse.query.all()
        for el in x:
            print(el)

        logger.debug("\nEchivalent cu SELECT * from produse where produse.id_producator = 1")
        x = ModelProduse.query.filter(ModelProduse.id_producator == 1).all()
        for el in x:
            print(el)

        print(x[1])
        print(x[1].id)

        '''
        Interogare compusa - JOIN intre mai multe tabele
        ------------------------------------------------
        '''
        logger.debug("\nEchivalent cu:\n\
                SELECT producatori.nume, produse.nume FROM producatori, produse\n\
                WHERE produse.id_producator = producatori")
        
        
        x = db.session.query(ModelProduse, ModelProducatori)\
                .join(ModelProducatori, \
                    ModelProduse.id_producator == \
                    ModelProducatori.id)\
                .with_entities(ModelProducatori.nume, \
                                ModelProduse.nume)\
                .all()
                
        for el in x:
            print(el)
