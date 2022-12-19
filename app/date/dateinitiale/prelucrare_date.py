##########################
# API prelucrare date
##########################

from .date import date_distribuitor

# Definire functii ajutatoare
def gaseste_nume_producator(id_producator):
    global date_distribuitor
    ret = "-"
    for el in date_distribuitor["producatori"]:
        if el["id"] == id_producator:
            ret = el["nume"]
            break
    return ret

    
def gaseste_nume_produs(id_produs):
    global date_distribuitori
    ret = "-"
    for el in date_distribuitor["produse"]:
        if el["id"] == id_produs:
            ret = el["nume"]            
    return ret


def gaseste_nume_producator_produs(id_produs):
    global date_distribuitor
    ret = "-"
    for el in date_distribuitor["produse"]:
        if el["id"] == id_produs:
            ret = gaseste_nume_producator(el["id_producator"])
    return ret

  
###############################################################################    
# definire functii care pregatesc structurile de date pentru afisare in pagina
# WEB
###############################################################################

def genereaza_date_continut_comenzi_producator(cu_cap_tabel = 1):
    global date_distribuitor
    
    ret = [["ID", "Producator", "Produs", "Cantitate"]]
        
    for el in date_distribuitor["continut_comenzi_la_producatori"]:
        n_ps = gaseste_nume_produs(el["id_produs"])
        n_pr = gaseste_nume_producator_produs(el["id_produs"])
        ret.append([el["id_comanda"], n_pr, n_ps, el["cantitate"]])

    return ret
