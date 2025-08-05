from . import main
from flask import current_app, render_template, request, url_for, redirect, flash
from flask import make_response
from sqlalchemy import select, func, exc
from chocodist.date.db import db
from chocodist.date.modele import Producator, Produs
from chocodist.params import APPNAME

from .forms import ProducerAddForm, ProductModifyForm
from .producator_ctrl import ProducatorCtrl
from .produs_ctrl import ProdusCtrl

import logging

logger = logging.getLogger(f"{APPNAME}.{__name__}")

@main.route("/")
def index():
    logger.debug("/ - index")
    return render_template("index.html", APPNAME=APPNAME)

@main.route("/producatori", methods = ['GET', 'POST'])
def producatori():
    
    response = ""
    
    if request.method == "POST":
        logger.debug(f"POST request action: {request.form.get('action')}")
        #logger.debug(f"POST request: {request.form}")
        if request.form['action'] == "add":
            logger.debug(f"form: {request.form.to_dict()}")
            p_info = {
                'nume': request.form['name']
            }
            #print("Inainte de adaugare")
            r = ProducatorCtrl.addNewProducer(**p_info)
            if r[0]:
                flash(f"Producatorul: {request.form['name']}, a fost adaugat", category="success")
            else:
                logger.error(f"Producatorul cu numele request.form['name'] exista deja: {r[1]}")
                flash(f"Prducatorul: {request.form['name']}, nu poate fi adaugat! Exista deja!", category="danger")
            
            response = make_response(redirect(url_for('.producatori')));
            response.set_cookie('adauga', value="1", max_age = 1);

        elif request.form['action'] == 'delete':
            logger.debug(f"form: {request.form.to_dict()}")
            try:
                with db.session.begin():
                    p = db.session.get(Producator, request.form['item-id'])
                    #if p.produse = []:
                    db.session.delete(p)
                flash(f"Producatorul: {p.nume}, a fost sters!", category='success')
            except exc.IntegrityError:
                flash(f"Producatorul {p.nume} nu poate fi sters. Are produse asociate!", category="danger")

        elif request.form['action'] == "modify":
            logger.debug(f"form: {request.form.to_dict()}")
            #return(request.form['new-value'])
            logger.debug(f"form: {request.form.to_dict()}")
            p_id = request.form['item-id']
            p_new_val = request.form['new-value']
            p_attr = request.form['item-attr']

            ret = ProducatorCtrl.modifyProducerAttr(p_id, p_new_val)
            return ret[1]
        else:
            logger.debug(f"POST page /producatori ... but not add new / modify / delete ...")
            logger.debug(f"POST request. form: {request.form}")
            #return(request.form['new-value'])
        #logger.debug(f"request.form: {request.form}")
        logger.debug("POST processing - done. Doing a redirect (helps for page reload, will not resubmit the form.)")
        if response != "":
            return response
        else:
            return redirect(url_for('.producatori')) # name full: main.producatori or relative .producatori

    logger.debug("GET request. pagina: /producatori")
    form = ProducerAddForm()
    #count_products = func.count(Produs.id.distinct()).label(None)
    count_products = func.count(Produs.id).label(None) # here it works the same as with distinct
    q = select(Producator.id, Producator.nume, count_products).join(Producator.produse, isouter=True).order_by(Producator.nume).group_by(Producator) # join on objects link
    print("q = ", q)
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

    #Exemple de utilizare mesaje flash -usor de vazut
    #mesajul flash nu se apeleaza cu parametrul categorie - care poate genera mesaje formatate diferit
    #bootstrap are ferestre/div-uri de alerta / succes / danger / warning formatate diferit
    #daca se apeleaza flash cu parametrul categorie, se poate folosi categoria pentru a formata
    #diferit mesajele flash - de vazut in base.html, cum se preiau cu get_flashed_messages categoria si mesajul
    #si cum este folosita categoria pentru a formata mesajul

    #flash("Pagina produse 1")
    #flash("Pagina produse 2")
    #flash("Pagina produse 3")
    #flash("Pagina produse 4")


    response = ""

    if request.method == "POST":
        logger.debug(f"POST request action: {request.form.get('action')}")

        if request.form['action'] == "add":
            logger.debug(f"form: {request.form.to_dict()}")
            p_info = {
                'nume': request.form['new_product_name'],
                'id_producator': request.form['producator'],
                'cantitate_stoc': request.form['cantitate_stoc'],
            }

            # Am creat o clasa ProdusCtrl - unde sa adaug metode specifice de control a produsului
            # Nu tratez aceste lucruri in clasa model produs pentru ca o incarc prea mult
            # (nu stiu daca-i neaparat o practica buna)
            r = ProdusCtrl.addNewProduct(**p_info)
            if r[0] == False:
                flash(f"Produsul: {r[1]['nume']}, de la producatorul: {r[1]['producator']} exista deja!", category='danger')
            else:
                flash(f"Produsul: {r[1]['nume']} de la producatorul: {r[1]['producator']} a fost adaugat!", category='success')

            '''
            # codul initial - inlocuit de codul din ProdusCtrl (apelat in liniile de mai sus)
            #
            with db.session.begin():
                # verific daca exista o noua ciocolata cu acelasi nume
                q = select(Produs).where(Produs.nume == request.form['new_product_name'], Produs.id_producator == request.form['producator'])
                print("q =", q)
                check_p_n = db.session.scalar(q)
                print("check_p_n: ", check_p_n)
                if check_p_n == None:
                    p_info = {
                        'nume': request.form['new_product_name'],
                        'id_producator': request.form['producator'],
                        'cantitate_stoc': request.form['cantitate_stoc'],
                    }
                    p = Produs(**p_info)
                    print("p =", p)
                    db.session.add(p)
                else:
                    flash(F"Produsul: {request.form['new_product_name']}, de la producatorul: {check_p_n.producator.nume} exista deja in baza de date!")
            '''

            response = make_response(redirect(url_for('.produse')));
            response.set_cookie('adauga', value="1", max_age = 1);


        elif request.form['action'] == 'delete':
            logger.debug(f"form: {request.form.to_dict()}")
            with db.session.begin():
                p = db.session.get(Produs, request.form['item-id'])
                db.session.delete(p)
                flash(f"Produsul: {p.nume}, a fost sters!", category='success')
                #'with' will take care 
                #about: session.commit() and session.close()
                #o sesiune memoreaza operatiunile cu baza de date pana la commit
                #adica adaugam, stergem, modificam inregistrari in baza de date - prima data in memorie
                #la commit, modificarile se fac in baza de date
                #o sesiune memoreaza aceste modifiari, la commit se fac si in baza de date
                #o sesiune ar trebui facuta pentru fiecare set de operatiuni inrudite

        elif request.form['action'] == "modify":
            logger.debug(f"form: {request.form.to_dict()}")
            p_id = request.form['item-id']
            p_new_val = request.form['new-value']
            p_attr = request.form['item-attr']
            '''
            orig_info = ""
            # fac modificarea in baza de date. gasesc produsul cu ID-ul trimis din pagina si-i schimb numele
            with db.session.begin():
                p = db.session.get(Produs, p_id)
                if p_attr == "nume":
                    orig_info = p.nume
                    p.nume = p_new_val
                elif p_attr == "cantitate_stoc":
                    orig_info = p.cantitate_stoc
                    p.cantitate_stoc = p_new_val
                #'with' will do the commit - which will make the change in db

            # vreau sa afisez in pagina numele nou din baza de date - care ar trebui sa fie cel trimis
            # asa ma asigur ca valoarea trimisa din browser de catre client a ajuns in baza de date
            # si ca ajunge inapoi, din baza de date in interfata grafica
            with db.session.begin():
                m_p = db.session.get(Produs, p_id)

            if p_attr == "nume":
                logger.debug(f"Noul nume - actualizat in baza de date: {m_p.nume}")
                ret = m_p.nume
            elif p_attr == "cantitate_stoc":
                logger.debug(f"Noua cantitate din stoc - actualizata in baza de date: {m_p.cantitate_stoc}")
                ret = m_p.cantitate_stoc
            else:
                ret = orig_info
            return str(ret)
            '''
            ret = ProdusCtrl.modifyProductAttr(p_id, p_attr, p_new_val)

            #pentru ca modificarea se face prin JS, mesajul flash nu functioneaza
            #modificarea nu genereaza reincarcarea paginii, ceea ce nu duce la afisarea mesajelor flash
            '''
            print("ret =", ret)
            if ret[0] == True:
                flash("Produsul a fost modificat", category="success")
            else:
                flash("Produsul nu a fost modificat", category="danger")
            '''
            # ret[1] este valoarea - fie cea noua, fie cea veche, daca cea noua nu s-a putut configura
            # totusi as avea nevoie de flash - in cazul in care vreau sa configurez acelasi nume
            # 
            return ret[1]
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

@main.route("/modifica-produs", methods = ['GET', 'POST'])
def modifica_produs():
    form = ProductModifyForm()
    p = ProdusCtrl.get_product(request.args['id'])
    form.name.data = p.nume
    producatori = ProducatorCtrl.get_producers_id_name()
    #print("producatori =", producatori)
    form.producer_id.choices = [(p.id, p.nume) for p in producatori]
    form.producer_id.data = 3
    form.cantitate_stoc.data = p.cantitate_stoc
    print(p.cantitate_stoc)
    return render_template("modifica_produs.html",  APPNAME=APPNAME, form=form)