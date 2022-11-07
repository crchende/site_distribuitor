##########################
# API prelucrare date
##########################

from app.date.date import date_distribuitor

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

'''
    genereaza_date_prodcatori

    Descriere:
    
        Preia datele din tabelul / elementul 'produse' pentru a fi utilizate
        pentru controale select sau alte controale.

    Parametrii:
        -
    
    Return:
        O lista de liste care cuprinde toate datele din 'producatori'
        Fiecare sublista contine:
        id-ul din baza de date si numele producatorului.
'''
def genereaza_date_producatori():
    global date_distribuitor
    
    ret = []
        
    for el in date_distribuitor['producatori']:
        ret.append([el["id"], el["nume"]])
    
    return ret


    
def genereaza_tabel_continut_comenzi():
    global date_distribuitor
    
    print("\nAfisare comenzi - fara prelucrare, cu ID-uri")
    for el in date_distribuitor["continut_comenzi_la_producatori"]:
        print(el)
    
    print("\nAfisare comenzi cu nume producator si nume produs, nu ID-uri")
    for el in date_distribuitor["continut_comenzi_la_producatori"]:
        n_ps = gaseste_nume_produs(el["id_produs"])
        n_pr = gaseste_nume_producator_produs(el["id_produs"])
        print("comanda:", el["id_comanda"], "de la:", n_pr, "produs:", n_ps, \
            "cantitate:", el["cantitate"])

