from . import main
from flask import current_app, render_template, request, url_for, redirect, flash
from flask import make_response
from sqlalchemy import select, func
from chocodist.date.db import db
from chocodist.date.modele import Producator, Produs
from chocodist.params import APPNAME

from .forms import PostForm

import logging

logger = logging.getLogger(f"{APPNAME}.{__name__}")

@main.route("/")
def index():
    logger.debug("/ - index")
    return render_template("index.html", APPNAME=APPNAME)

@main.route("/producatori", methods = ['GET', 'POST'])
def producatori():
    if request.method == "POST":
        logger.debug(f"POST request action: {request.form.get('action')}")
        #logger.debug(f"POST request: {request.form}")
        if request.form['action'] == "add":
            logger.debug(f"form: {request.form.to_dict()}")
        elif request.form['action'] == 'delete':
            logger.debug(f"form: {request.form.to_dict()}")
        elif request.form['action'] == "modify":
            logger.debug(f"form: {request.form.to_dict()}")
            return(request.form['new-value'])
        else:
            logger.debug(f"POST page /producatori ... but not add new / modify / delete ...")
            logger.debug(f"POST request. form: {request.form}")
            #return(request.form['new-value'])
        #logger.debug(f"request.form: {request.form}")
        logger.debug("POST processing - done. Doing a redirect (helps for page reload, will not resubmit the form.)")

        return redirect(url_for('.producatori')) # name full: main.producatori or relative .producatori

    logger.debug("GET request. pagina: /producatori")
    form = PostForm()
    #count_products = func.count(Produs.id.distinct()).label(None)
    count_products = func.count(Produs.id).label(None) # here it works the same as with distinct
    q = select(Producator.id, Producator.nume, count_products).join(Producator.produse).group_by(Producator) # join on objects link
    #print("query with join on objects link:\n", q)
    #q = select(Producator.id, Producator.nume, count_products).join(Produs).group_by(Producator) # SQLAlchemy creates the join behinc the scene / automaticaly based on objects link
    #print("same query but with join between tables - done internaly by SQLAlchemy based on object relation\n", q)

    #SELECT producatori.id, producatori.nume, count(produse.id) AS count_1 
    #FROM producatori JOIN produse ON producatori.id = produse.id_producator GROUP BY producatori.id, producatori.nume

    lst_producatori_count_produse = db.session.execute(q).all()
    logger.debug(f"id si nume producator si nr produse: {lst_producatori_count_produse}")

    return render_template("producatori.html", APPNAME=APPNAME, producatori=lst_producatori_count_produse, form=form)

@main.route("/produse", methods = ['GET', 'POST'])
def produse():
    '''
    print("request.host_url:", request.host_url)
    print("request.user_agent:", request.user_agent)
    print("request.url:", request.url)
    print("request.path: - same as action of form", request.path)
    '''
    
    response = ""

    if request.method == "POST":
        logger.debug(f"POST request action: {request.form.get('action')}")

        if request.form['action'] == "add":
            logger.debug(f"form: {request.form.to_dict()}")
            with db.session.begin():
                # verific daca exista o noua ciocolata cu acelasi nume
                check_p_n = db.session.scalar(select(Produs).where(Produs.nume == request.form['new_product_name'] and Produs.id_producator == request.form['producator']))
                if check_p_n == None:
                    p_info = {
                        'nume': request.form['new_product_name'],
                        'id_producator': request.form['producator'],
                        'cantitate_stoc': request.form['cantitate_stoc'],
                    }
                    p = Produs(**p_info)
                    print("p =", p)
                    db.session.add(p)
            response = make_response(redirect(url_for('.produse')));
            response.set_cookie('adauga', value="1", max_age = 1);


        elif request.form['action'] == 'delete':
            logger.debug(f"form: {request.form.to_dict()}")
            with db.session.begin():
                p = db.session.get(Produs, request.form['item-id'])
                db.session.delete(p)
                #with will take care about: session.commit() and session.close()
                #o sesiune memoreaza operatiunile cu baza de date pana la commit
                #adica adaugam, stergem, modificam inregistrari in baza de date - prima data in memorie
                #la commit, modificarile se fac in baza de date
                #o sesiune memoreaza aceste modifiari, la commit se fac si in baza de date
                #o sesiune ar trebui facuta pentru fiecare set de operatiuni inrudite

        elif request.form['action'] == "modify":
            logger.debug(f"form: {request.form.to_dict()}")
            p_id = request.form['item-id']
            p_new_val = request.form['new-value']
            # fac modificarea in baza de date. gasesc produsul cu ID-ul trimis din pagina si-i schimb numele
            with db.session.begin():
                p = db.session.get(Produs, p_id)
                p.nume = p_new_val
                #'with' will do the commit - which will make the change in db

            # vreau sa afisez in pagina numele nou din baza de date - care ar trebui sa fie cel trimis
            # asa ma asigur ca valoarea trimisa din browser de catre client a ajuns in baza de date
            # si ca ajunge inapoi, din baza de date in interfata grafica
            with db.session.begin():
                m_p = db.session.get(Produs, p_id)

            logger.debug(f"Noul nume - actualizat in baza de date: {m_p.nume}")
            return(m_p.nume)
        else:
            logger.debug(f"POST page /producatori ... but not add new / modify / delete ...")
            logger.debug(f"POST request. form: {request.form}")
            #return(request.form['new-value'])
        
        #logger.debug(f"request.form: {request.form}")
        logger.debug("POST processing - done. Doing a redirect (helps for page reload, will not resubmit the form.)")
        if response != "":
            return response
        else:
            return redirect(url_for('.produse')) # name full: main.producatori or relative .producatori


    #print(url_for('.produse', a=1, b=2)) #/produse?a=1&b=2
    #daca 'a' ar fi parte variabila din url atunci am avea: /produse/1?b=2
    #
    #Vreau sa transmit in browser cand adaug ceva, sa-mi ramana formularul de adaugare expandat,
    #in caz ca mai vreau sa adaug ceva.
    #pot transmite informatia in URL sau pot sa o transmit cu un cookie.

    q = select(Produs).join(Producator).order_by(Producator.nume)
    '''
    q = SELECT produse.id, produse.nume, produse.id_producator 
        FROM produse JOIN producatori ON producatori.id = produse.id_producator ORDER BY producatori.nume
    ''' 
    logger.debug("q = " + str(q))
    lst_prod = db.session.scalars(q).all()

    lst_producatori = db.session.scalars(select(Producator)).all()

    #adaugare cookie-uri functionale - debug
    #r = make_response(render_template("produse.html", APPNAME=APPNAME, produse=lst_prod, producatori=lst_producatori))
    #r.set_cookie("adauga", "0")
    #r.set_cookie("modifica", "0")
    #r.set_cookie("sterge", "0")
    #return r

    return render_template("produse.html", APPNAME=APPNAME, produse=lst_prod, producatori=lst_producatori)