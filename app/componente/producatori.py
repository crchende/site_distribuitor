from app.date.date import date_distribuitor
from flask import request

from app.date.mysqldb import selecteaza, insereaza, sterge, modifica

class Producatori:
    '''
    genereaza_date_producatori

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
    def genereaza_date_producatori(self, cu_cap_tabel = 0):        
        if cu_cap_tabel == 1:
            ret = [["ID", "Producator"]]
        else:
            ret = []
        
        q = "SELECT * from producatori ORDER BY id"
        date = selecteaza(q)
        
        for (p_id, nume) in date:
            print(p_id, nume)
            ret.append((p_id, nume))
        
        return ret
        
        
    def adauga(self):
     
        print("request.form:", request.form)
        print("DBG: Dorim sa adaugam producatorul:", 
            request.form["nume_producator_nou"])
        
        nume_nou = request.values["nume_producator_nou"]
        q = "INSERT INTO `site_distribuitor`.`producatori` (`nume`) VALUES (%s);"
        
        ret = insereaza(q, nume_nou)
        
    
    def modifica(self, id_prod, nume_nou):
        ret = "-"
        
        print("DBG: modificare denumire producator cu ID:", id_prod, "la: ", nume_nou)
        
        q = "UPDATE `site_distribuitor`.`producatori` SET `nume` = '" + \
            nume_nou + \
            "' WHERE (`id` = '" + \
            id_prod + \
            "');"
        modifica(q)
        
        n_nou = selecteaza("SELECT nume from producatori WHERE `id` = "\
            + id_prod + \
            ";")[0][0]
        
        print("\nN_NOU =", n_nou)
        ret = n_nou
        
        return ret
        
        
    def sterge(self):
        print("DBG: sterge - request.values", request.values)
            
        id_prod = int(request.values["id"])
        #print("DBG: id_prod de sters:", id_prod)
        
        q = "DELETE FROM `site_distribuitor`.`producatori` WHERE (`id` = '" + \
            str(id_prod) + \
            "');"
            
        sterge(q)
