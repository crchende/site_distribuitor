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

@main.route("/login")
def login():
    logger.debug("/login")
    return render_template("login.html", APPNAME=APPNAME)


@main.route("/producatori", methods = ['GET', 'POST'])
def producatori():
    response = ""
    if request.method == "POST":
        logger.debug(f"POST request action: {request.form.get('action')}")
        #logger.debug(f"POST request: {request.form}")
        if request.form['action'] == "add" and request.form.get('submit_add_producer_form'):
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
    #q =  SELECT producatori.id, producatori.nume, count(produse.id) AS count_1 
    #FROM producatori LEFT OUTER JOIN produse ON producatori.id = produse.id_producator GROUP BY producatori.id, producatori.nume ORDER BY producatori.nume

    lst_producatori_count_produse = db.session.execute(q).all()
    logger.debug(f"id si nume producator si nr produse: {lst_producatori_count_produse}")

    return render_template("producatori.html", APPNAME=APPNAME, producatori=lst_producatori_count_produse, form=form)

@main.route("/produse", methods = ['GET', 'POST'])
def produse():
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

            r = ProdusCtrl.addNewProduct(**p_info)
            if r[0] == False:
                flash(f"Produsul: {r[1]['nume']}, de la producatorul: {r[1]['producator']} exista deja!", category='danger')
            else:
                flash(f"Produsul: {r[1]['nume']} de la producatorul: {r[1]['producator']} a fost adaugat!", category='success')

            response = make_response(redirect(url_for('.produse')));
            # add a cookie - to keep add form expanded after adding a product
            response.set_cookie('adauga', value="1", max_age = 1);


        elif request.form['action'] == 'delete':
            logger.debug(f"form: {request.form.to_dict()}")
            with db.session.begin():
                p = db.session.get(Produs, request.form['item-id'])
                db.session.delete(p)
                flash(f"Produsul: {p.nume}, a fost sters!", category='success')

        elif request.form['action'] == "modify":
            logger.debug(f"form: {request.form.to_dict()}")
            p_id = request.form['item-id']
            p_new_val = request.form['new-value']
            p_attr = request.form['item-attr']
            ret = ProdusCtrl.modifyProductAttr(p_id, p_attr, p_new_val)
            # inline change - flash msg does not work. Handling duplicate name in a different way - in modifyProductAttr controller method
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
            return redirect(url_for('.produse')) # name full: main.producatori or relative .producator

    q = select(Produs).join(Producator).order_by(Producator.nume)

    logger.debug("q = " + str(q))
    lst_prod = db.session.scalars(q).all()

    lst_producatori = db.session.scalars(select(Producator)).all()
    return render_template("produse.html", APPNAME=APPNAME, produse=lst_prod, producatori=lst_producatori)

@main.route("/modifica-produs", methods = ['GET', 'POST'])
def modifica_produs():
    # the form to modify the product data - will be filled-out with current values for the selected product
    # BUG in WTF - for IntegerField, if the form remains on the screen - e.g. duplicate name, the value cantitate_stoc 
    # will remain the one in the field, not the one in DB, even below it is set: form.cantitate_stoc.data = ...
    form = ProductModifyForm()
    p = ProdusCtrl.getProductInfo(request.args['id'])
    form.name.data = p['nume']
    producatori = ProducatorCtrl.get_producers_id_name()
    form.producer_id.choices = [(prd.id, prd.nume) for prd in producatori]
    form.producer_id.data = str(p['id_producator'])
    form.cantitate_stoc.data = str(p['cantitate_stoc'])

    # process the info in the form - if SUBMIT
    if request.method == "POST":
        logger.debug(f"Date formular modificare produs: {request.form.to_dict()}")
        if request.form.get('cancel'):
            return redirect(url_for('.produse'))
        
        if form.validate_on_submit():
            if p['nume'] == request.form['name'] and \
                p['id_producator'] == int(request.form['producer_id']):
                if p['cantitate_stoc'] == int(request.form['cantitate_stoc']):
                    logger.debug("Nu sunt schimbari pentru produs, datele din formular sunt cele initiale pentru produs!")
                else:
                    ProdusCtrl.modifyProduct(id_product=request.args['id'], nume=None, id_producator=None, cantitate_stoc=request.form['cantitate_stoc'])
                    flash(f"Modificat cantitate stoc de la: {p['cantitate_stoc']} la {request.form['cantitate_stoc']} pentru produsul: {p['nume']} de la producatorul: {p['producator']}", category="success")

                return redirect(url_for('.produse'))
            else:
                m_info =  ProdusCtrl.modifyProduct(id_product=request.args['id'], \
                                            nume=request.form['name'], \
                                            id_producator=request.form['producer_id'], \
                                            cantitate_stoc=request.form['cantitate_stoc'])

                if m_info[0] == True:
                    flash(f"Produsul:   {p['nume']}, {p['producator']} va fi modificat!", category="warning")
                    flash(f"Produsul a fost modificat: {m_info[1][0]}, {m_info[1][1]}, cantitate: {m_info[1][2]}", category="success")
                    return redirect(url_for('.produse'))
                else:
                    flash(f"Nume duplicat pentru produs, mai exista un produs cu acelasi nume de la: {m_info[1][1]}!", category="danger")
                    # form data problems - keep the form on the screen
        else:
            flash("Datele introduse in formular nu sunt valide. Produsul nu poate fi modificat", category="danger")
            logger.error("Problema validare date din formular!")
        
    # show the form - for get or if no redirect above (e.g. duplicate product case)
    return render_template("modifica_produs.html",  APPNAME=APPNAME, form=form)