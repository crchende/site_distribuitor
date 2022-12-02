import os

from flask import Flask, render_template
from flask import request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap

from app.date.mysqldb import selecteaza, insereaza, sterge, modifica, deconectare

from app.date.prelucrare_date import *
from app.componente.produse import Produse, FormProduse
from app.componente.producatori import Producatori

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir:", basedir) 

app = Flask(__name__)

# Cerut de FlaskForm. Daca nu se pune apare eroarea:
# RuntimeError: A secret key is required to use CSRF.
app.config['SECRET_KEY'] = "parola pentru wtforms"

bootstrap = Bootstrap(app)

# initializare obiecte
produse = Produse()
producatori = Producatori()




################################################################################
# RUTE
################################################################################
@app.route('/')
def index():
    return render_template('index.html', page="distribuitor ciocolata")
    
##################################################
# produse
##################################################
@app.route('/produse', methods = ['GET', 'POST'])
def actiuni_produse():
    # Adaugare / stergere daca este cazul.

    if "action" in request.values and request.values["action"] == "delete":
        # la stergere am adaugat parametrul action=sterge in URL
        produse.sterge()
        flash("S-a sters produsul selectat")

    # Afisare produse
    lst_produse = produse.genereaza_date_produse()
    lst_producatori = producatori.genereaza_date_producatori()
    
    form_produse = FormProduse()
    c = [("", "")]
    c.extend([(pr[0], pr[1]) for pr in lst_producatori]) 
    form_produse.id_producator.choices = c
    
    #request.method == "POST":
    #validate_on_submit - verifica deja ca avem metoda POST
    #Atat form_produse.data cat si request.form.values contin
    #valorile de care avem nevoie. 
    # TBD - de clarificat diferenta intre acestea
    
    if form_produse.validate_on_submit():
        print("DBG: validate_on_submit = True; date form:")
        print("DBG: request.form.values:", request.form.values)
        print("DBG: form_produse.data:", form_produse.data)
        print("DBG: form_produse.id_producator.data: ", \
            form_produse.id_producator.data)
    
        p_n = produse.adauga(form_produse.id_producator.data, \
            form_produse.nume_produs_nou.data)
        flash("Adaugat produs nou: " + str(p_n), "success")
            
        return redirect(url_for('actiuni_produse'))
    else:
        print("DBG: validate_on_submit = False; date form:")
        print("DBG: request.form.values:", request.form.values)
        print("DBG: form_produse.data:", form_produse.data)
        print("DBG: form_produse.id_producator.data: ", \
            form_produse.id_producator.data)
    
    return render_template('index.html', page="produse", \
        form = form_produse, \
        produse = lst_produse, \
        producatori = lst_producatori)


@app.route('/modifica/produse', methods = ['POST'])
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
    
    ret = produse.modifica(request.form["id"], request.form["valnoua"])
    #penru a vedea mesajul de debug corect trebuie sa execut functia inaintea
    #acestuia
    print("DBG: - verificare modificare in date:", date_distribuitor["produse"])
    
    return ret

##################################################
# producatori
##################################################
@app.route('/producatori', methods = ['GET', 'POST'])
def actiuni_producatori():
    if len(request.form) != 0:
        # === Adaugare ===
        # acum este suficient sa verific ca primesc date de la un forumular
        # pentru adaugare de date noi
        producatori.adauga()
    elif "action" in request.values and request.values["action"] == "delete":
        #print(request.values)
        # === Stergere ===
        # la stergere am adaugat parametrul action=sterge in URL
        producatori.sterge()
    
    # === Afisare ===
    lst_producatori = producatori.genereaza_date_producatori(cu_cap_tabel = 1)
    return render_template('index.html', page="producatori", \
        producatori=lst_producatori)

@app.route('/modifica/producatori', methods=["POST"])
def modifica_producatori():
    #print(request.values)
    ret = producatori.modifica(request.form["id"], request.form["valnoua"])
    #penru a vedea mesajul de debug corect trebuie sa execut functia inaintea
    #acestuia
    print("DBG: - verificare modificare in date:", date_distribuitor["producatori"])
    
    return ret
    
##################################################
# comenzi producatori
##################################################
@app.route('/comenzi-producatori')
def afisare_comenzi_producatori():
    lst_continut_cmd_prod = genereaza_date_continut_comenzi_producator()
    print(lst_continut_cmd_prod)
    return render_template('index.html', page="comenzi la producatori", \
        continut_comenzi_producatori = lst_continut_cmd_prod)

