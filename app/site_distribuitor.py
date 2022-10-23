from flask import Flask, render_template
from flask import request
from flask_bootstrap import Bootstrap

from app.date.date import date_distribuitor
from app.date.prelucrare_date import *
from app.componente.produse import Produse

app = Flask(__name__)
bootstrap = Bootstrap(app)

produse = Produse()

@app.route('/')
def index():
    return render_template('index.html', page="distribuitor ciocolata")
    

@app.route('/comenzi-producatori')
def afisare_comenzi_producatori():
    return render_template('index.html', page="comenzi la producatori")

@app.route('/produse', methods = ['GET', 'POST'])
def actiuni_produse():
    # Adaugare / stergere daca este cazul.
    # Metodele contin in ele codul care stie daca se adauga / sterge sau 
    # doar se afiseaza.
    produse.adauga_produs_nou()
    produse.sterge_produs()

    # Afisare produse
    lst_produse = produse.genereaza_date_produse()
    lst_producatori = genereaza_date_producatori()
    
    return render_template('index.html', page="produse", \
        produse = lst_produse, \
        producatori = lst_producatori)
        
@app.route('/modifica/produs', methods = ['POST'])
def modifica_produs():
    #print(dir(request))
    #print("DBG. request.form: id, valnoua, "request.form["id"], request.form["valnoua"])

    '''
    #afisare componente request - chei si valori
    for k in request.__dict__:
        try:
            print(k, eval("request.{}".format(k)))
        except Exception as e:
            print("Eroare: ", e)
    '''
    
    # functia modifica_produs intoarce valoarea citita din baza de date
    # dupa modificare
    # aceasta valoare va fi folosita in script_uri.html pentru a seta 
    # valoarea in celula tabelului
    
    ret = produse.modifica_produs(request.form["id"], request.form["valnoua"])
    #penru a vedea mesajul de debug corect trebuie sa execut functia inaintea
    #acestuia
    print("DBG: - verificare modificare in date:", date_distribuitor["produse"])
    
    return ret



@app.route('/producatori')
def actiuni_producatori():
    return render_template('index.html', page="producatori")

    
