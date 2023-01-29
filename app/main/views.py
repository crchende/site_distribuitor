from flask import render_template, request, redirect, url_for, session, flash
import logging

from flask_mail import Message
import time

from . import main
from .. import db
from .. import mail

import app.date.modele as modele

#from ..date.dateinitiale.date import date_distribuitor
from ..date.dateinitiale.prelucrare_date import *
from ..componente.produse import Produse, FormProduse
from ..componente.producatori import Producatori
from ..componente.comenzi_la_producatori import ContinutComenziLaProducatori

# initializare obiecte
produse = Produse()
producatori = Producatori()
ccmdlaprod = ContinutComenziLaProducatori()

logger = logging.getLogger(__name__)

################################################################################
# RUTE
################################################################################
@main.route('/')
def index():
    return render_template('index.html', page="distribuitor ciocolata")
    
##################################################
# produse
##################################################
@main.route('/produse', methods = ['GET', 'POST'])
def actiuni_produse():
    '''
    Actiuni tratate: afisare / adaugare / stergere
    '''

    if "action" in request.values and request.values["action"] == "delete":
        # la stergere am adaugat parametrul action=sterge in URL
        msg = produse.sterge(request.values['id'])
        flash(msg)

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
        logger.debug("validate_on_submit = True; date form:")
        logger.debug(f"request.form.values: {request.form.values}")
        logger.debug(f"form_produse.data: {form_produse.data}")
        logger.debug(f"form_produse.id_producator.data: {form_produse.id_producator.data}")
    
        p_n = produse.adauga(form_produse.id_producator.data, \
            form_produse.nume_produs_nou.data)
            
        flash("Adaugat produs nou: " + str(p_n) + ". Success")
            
        return redirect(url_for('.actiuni_produse'))
    else:
        logger.debug(f"validate_on_submit = False;")
        logger.debug(f"request.form.values: {request.form.values}")
        logger.debug(f"form_produse.data: {form_produse.data}")
        logger.debug(f"form_produse.id_producator.data: {form_produse.id_producator.data}")
    
    return render_template('index.html', page="produse", \
        form = form_produse, \
        produse = lst_produse, \
        producatori = lst_producatori)


@main.route('/modifica/produse', methods = ['POST'])
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
@main.route('/producatori', methods = ['GET', 'POST'])
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
        msg = producatori.sterge()
        flash(msg)

    
    # === Afisare ===
    lst_producatori = producatori.genereaza_date_producatori(cu_cap_tabel = 1)
    return render_template('index.html', page="producatori", \
        producatori=lst_producatori)

@main.route('/modifica/producatori', methods=["POST"])
def modifica_producatori():
    #print(request.values)
    ret = producatori.modifica(request.form["id"], request.form["valnoua"])
    #penru a vedea mesajul de debug corect trebuie sa execut functia inaintea
    #acestuia
    p = modele.ModelProducatori.query.filter_by(nume=request.form["valnoua"]).\
        first()
    print("DBG: - verificare modificare in baza de date:", p)
    
    return ret
    
##################################################
# comenzi producatori
##################################################
@main.route('/comenzi-producatori')
def afisare_comenzi_producatori():
    lst_continut_cmd_prod = ccmdlaprod.genereaza_date_continut_comenzi_producator()
    return render_template('index.html', page="comenzi la producatori", \
        continut_comenzi_producatori = lst_continut_cmd_prod)
        
##################################################
# Testare email   
##################################################
@main.route('/test_mail')
def test_mail():
    msg = Message(f"Salutare din site_distribuitor {time.ctime()}",
        sender="cip.chende.dev@gmail.com",
        recipients=["cip_chende@yahoo.com"])
    msg.body = "mesaj text"
    msg.html = "<b>mesaj html</b>"
    
    mail.send(msg)
    
    return "SALUT"

