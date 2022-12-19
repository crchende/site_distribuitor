from ..date.modele import \
    ModelComenziLaProducatori, \
    ModelContinutComenziLaProducatori, \
    ModelProduse, \
    ModelProducatori
    
from .. import db

import logging
logger = logging.getLogger(__name__)

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
