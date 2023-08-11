from ..date.modele import \
    ModelComenziLaProducatori, \
    ModelContinutComenziLaProducatori, \
    ModelProduse, \
    ModelProducatori
    
from .. import db
from app import APPNAME

import logging
logger = logging.getLogger(APPNAME + "." +__name__)
logger.debug(f"Incarcare modul")

class ComenziLaProducatori:
    pass
    
    
class ContinutComenziLaProducatori:
    def genereaza_date_continut_comenzi_producator(self, cu_cap_tabel = 1):
        ret = [("ID", "ID Comanda", "Producator", "Produs", "Cantitate")]
        
        # a list of tuples
        lt = db.session.query(ModelContinutComenziLaProducatori, \
                ModelProduse, \
                ModelProducatori)\
            .join(ModelProduse, \
                ModelContinutComenziLaProducatori.id_produs == ModelProduse.id)\
            .join(ModelProducatori, ModelProduse.id_producator == \
                ModelProducatori.id) \
            .with_entities(\
                ModelContinutComenziLaProducatori.id_comanda, \
                ModelProducatori.nume, \
                ModelProduse.nume, \
                ModelContinutComenziLaProducatori.cantitate)\
            .all()

        for t in lt:
            ret.append(t)
        
        logger.debug(str(lt))
        
        return ret
