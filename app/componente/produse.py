from app.date.date import date_distribuitor
from app.date.prelucrare_date import gaseste_nume_producator
from flask import request

class Produse:

    '''
    genereaza_tabel_produse
    
    Descriere:
        Preia datele referitoare la produse. 

    Parametrii:
        cu_cap_tabel:   valoare default 1; adauga o lista cu numele coloanelor
                        pentru tabelul cu produse
                        
    Return:
        O lista de liste, cu toate datele din produse, inclusiv ID-ul pentru
        a putea implementa si operatiunile de stergere si modificare.
    
    '''
    def genereaza_date_produse(self, cu_cap_tabel=1):
        global date_distribuitor

        # initializare cu cap tabel
        ret = [["ID", "Producator", "Produs"]] 
        # va fi o lista de liste - fiecare element - un rand in tabel
        
        for el in date_distribuitor["produse"]:
            nume_producator = gaseste_nume_producator(el["id_producator"])
            ret.append([el["id"], nume_producator, el["nume"]])
        
        return ret
        
    def adauga_produs_nou(self):
        global date_distribuitor
        
        #E OK acum doar aceasta verificare sa fiu sigur ca adaug 
        #de fapt, ca am un formular
        if len(request.form) == 0:
            return
        else:
            print("request.form:", request.form)
            print("DBG: Dorim sa adaugam produsul:", 
                request.form["nume_produs_nou"], \
                "de la producatorul cu ID:", \
                request.form["id_producator"],)
            
            max_id = max([el["id"] for el in date_distribuitor["produse"]])
            id_nou = max_id + 1
            
            date_distribuitor["produse"].append(\
                {\
                    "id": id_nou,\
                    "id_producator": int(request.values["id_producator"]),\
                    "nume": request.values["nume_produs_nou"]\
                })
                
            #print("DBG:", date_distribuitor["produse"])
          
    def modifica_produs(self, id_prod, nume_nou):
        global date_distribuitor
        ret = "-"
        
        print("DBG: modificare denumire produs cu ID:", id_prod, "la: ", nume_nou)
        prod = date_distribuitor["produse"]
        lst_index = [prod.index(el) for el in prod if el["id"] == int(id_prod)]
        print("lst_index", lst_index)
        index = int(lst_index[0])
        
        prod[index]["nume"] = nume_nou
        ret = prod[index]["nume"]
        
        return ret
        
         
            
    def sterge_produs(self):
        global date_distribuitor
        print("DBG: sterge - request.values", request.values)
        
        print("action" in request.values)
        
        if len(request.values) == 0 or ("action" in request.values) == False:
            return
        else:
            id_prod = int(request.values["id"])
            #print("DBG: id_prod de sters:", id_prod)
            
            #print(date_distribuitor["produse"])
            prod = date_distribuitor["produse"]
            print(prod)
            
            # ar trebui sa obtinem o lista cu un singur element
            lst_index = [prod.index(el) for el in prod if el["id"] == id_prod]
            
            #print("Index-ul de sters:", lst_index) 
               
            index = int(lst_index[0])
            
            date_distribuitor["produse"].pop(index)
        
