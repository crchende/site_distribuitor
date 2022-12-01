from app.date.date import date_distribuitor
from flask import request


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
        global date_distribuitor
        
        if cu_cap_tabel == 1:
            ret = [["ID", "Producator"]]
        else:
            ret = []
            
        for el in date_distribuitor['producatori']:
            ret.append([el["id"], el["nume"]])
        
        return ret
        
        
    def adauga(self):
        global date_distribuitor
        
        print("request.form:", request.form)
        print("DBG: Dorim sa adaugam producatorul:", 
            request.form["nume_producator_nou"])
        
        max_id = max([el["id"] for el in date_distribuitor["producatori"]])
        id_nou = max_id + 1
        
        date_distribuitor["producatori"].append(\
            {\
                "id": id_nou,\
                "nume": request.values["nume_producator_nou"]\
            })
        
    
    def modifica(self, id_prod, nume_nou):
        global date_distribuitor
        ret = "-"
        
        print("DBG: modificare denumire producator cu ID:", id_prod, "la: ", nume_nou)
        
        prod = date_distribuitor["producatori"]
        lst_index = [prod.index(el) for el in prod if el["id"] == int(id_prod)]
        print("lst_index", lst_index)
        index = int(lst_index[0])
        
        prod[index]["nume"] = nume_nou
        ret = prod[index]["nume"]
        
        return ret
        
        
    def sterge(self):
        global date_distribuitor
        print("DBG: sterge - request.values", request.values)
            
        id_prod = int(request.values["id"])
        #print("DBG: id_prod de sters:", id_prod)
        
        #print(date_distribuitor["produse"])
        prod = date_distribuitor["producatori"]
        print(prod)
        
        # ar trebui sa obtinem o lista cu un singur element
        lst_index = [prod.index(el) for el in prod if el["id"] == id_prod]
        
        #print("Index-ul de sters:", lst_index) 
           
        index = int(lst_index[0])
        
        date_distribuitor["producatori"].pop(index)
        
