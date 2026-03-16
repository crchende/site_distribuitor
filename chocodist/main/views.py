from . import main
import os, json, requests
from flask import current_app, render_template, request, url_for, redirect, flash
from flask import make_response
from sqlalchemy import select, func, exc

from flask_login import login_required

from chocodist.date.db import db
from chocodist.date.modele import Producator, Produs, Oras, Permisiuni
from chocodist.params import APPNAME, basedir

from .forms import ProducerAddForm, ProductModifyForm
from .producator_ctrl import ProducatorCtrl
from .produs_ctrl import ProdusCtrl
from .oras_ctrl import OrasCtrl
from .comanda_producator_ctrl import ComandaProducatorCtrl
from .comanda_client_ctrl import ComandaClientCtrl
#from .obj_ctrl import ObjCtrl

from .decoratori import permission_required, admin_required

import logging

logger = logging.getLogger(f"{APPNAME}.{__name__}")

@main.route("/")
def index():
    logger.debug("/ - index")
    return render_template("index.html", APPNAME=APPNAME)

@main.route("/producatori", methods = ['GET', 'POST'])
@login_required
@permission_required(Permisiuni.VIZUALIZAREDATEADMIN)
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
            r = ProducatorCtrl.addNew(**p_info)
            if r[0]:
                flash(f"Producatorul: {request.form['name']}, a fost adaugat", category="success")
            else:
                logger.error(f"Producatorul cu numele request.form['name'] exista deja: {r[1]}")
                flash(f"Prducatorul: {request.form['name']}, nu poate fi adaugat! Exista deja!", category="danger")
            
            response = make_response(redirect(url_for('.producatori')));
            response.set_cookie('adauga', value="1", max_age = 1);

        elif request.form['action'] == 'delete':
            logger.debug(f"form: {request.form.to_dict()}")
            ProducatorCtrl.delObj(request.form['item-id'])

        elif request.form['action'] == "modify":
            logger.debug(f"form: {request.form.to_dict()}")
            #return(request.form['new-value'])
            logger.debug(f"form: {request.form.to_dict()}")
            p_id = request.form['item-id']
            p_new_val = request.form['new-value']
            p_attr = request.form['item-attr']

            ret = ProducatorCtrl.modifyAttr(p_id, p_new_val)
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
@login_required
@permission_required(Permisiuni.VIZUALIZAREDATEADMIN)
def produse():
    response = ""

    if request.method == "POST":
        logger.debug(f"POST request action: {request.form.get('action')}")

        if request.form['action'] == "add":
            # Afisare continut formular. Pentru multislect to_dict da doar prima valoare
            logger.debug(f"form: {request.form.to_dict()}")
            logger.debug(f'locatie: {request.form.getlist("locatie")}')
            p_info = {
                'nume': request.form['new_product_name'],
                'id_producator': request.form['producator'],
                'cantitate_stoc': request.form['cantitate_stoc'],
            }

            r = ProdusCtrl.addNewProduct(lst_locatii = request.form.getlist("locatie"), **p_info,)
            if r[0] == False:
                flash(f"Produsul: {r[1]['nume']}, de la producatorul: {r[1]['producator']} exista deja!", category='danger')
            else:
                flash(f"Produsul: {r[1]['nume']} de la producatorul: {r[1]['producator']} a fost adaugat!", category='success')

            response = make_response(redirect(url_for('.produse')));
            # add a cookie - to keep add form expanded after adding a product
            response.set_cookie('adauga', value="1", max_age = 1);


        elif request.form['action'] == 'delete':
            logger.debug(f"form: {request.form.to_dict()}")
            ret = ProdusCtrl.deleteProduct(request.form['item-id'])
            if ret[0]:
                flash(f"Produsul: {ret[1]}, a fost sters!", category='success')
            else:
                flash(f"Produsul {ret[1]} nu poate fi sters. Este adaugat in comenzi!", category="danger")

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

    # Doar produse si prroducatori
    # q = select(Produs).join(Producator).order_by(Producator.nume).order_by(Produs.nume)
    #logger.debug("q = " + str(q))
    # produse si nr orase
    q = select(Produs, Producator.nume, func.count(Oras.id))\
            .join(Produs.orase, isouter=True)\
            .join(Produs.producator)\
            .group_by(Produs.nume)\
            .order_by(Producator.nume)\
            .order_by(Produs.nume)

    lst_prod = db.session.execute(q).all()
    logger.debug(f"Produs, nume producator, nr orase: {lst_prod}")
    lst_producatori = db.session.scalars(select(Producator)).all()
    orase = db.session.execute(select(Oras.id, Oras.nume).order_by(Oras.nume)).all()
    #logger.debug(f"Orase = {orase}")

    return render_template("produse.html", APPNAME=APPNAME, produse=lst_prod, producatori=lst_producatori, orase=orase)

@main.route("/modifica-produs", methods = ['GET', 'POST'])
@login_required
@admin_required
def modifica_produs():
    # the form to modify the product data - will be filled-out with current values for the selected product
    # BUG in WTF - for IntegerField, if the form remains on the screen - e.g. duplicate name, the value cantitate_stoc 
    # will remain the one in the field, not the one in DB, even below it is set: form.cantitate_stoc.data = ...
    form = ProductModifyForm()

    ProdusCtrl.initModifyForm(form, request.args['id'])

    # process the info in the form - if SUBMIT
    if request.method == "POST":
        logger.debug(f"Date formular modificare produs: {request.form.to_dict()}") # afiseaza doar o locatie
        logger.debug(f"locatiile trimise prin formular: {request.form.getlist('locatie')}")
        #logger.debug(f"locatiile din obiectul produs:   {p_obj_locatii}")

        if request.form.get('cancel'):
            return redirect(url_for('.produse'))
        
        ret = ProdusCtrl.analysisAndModifyProduct(form, request.form, request.args)
        if ret == "redirect":
            return redirect(url_for('.produse'))
        
    # show the form - for get or if no redirect above (e.g. duplicate product case)
    return render_template("modifica_produs.html",  APPNAME=APPNAME, form=form)


@main.route("/locatie", methods = ['GET', 'POST'])
@login_required
@permission_required(Permisiuni.VIZUALIZAREDATEADMIN)
def locatie():
    #ObjCtrl.set_obj(Oras)
    response = ""
    if request.method == "POST":
        logger.debug(f"POST request action: {request.form.get('action')}")
        logger.debug(f"POST request: {request.form}")
        if request.form['action'] == "add" and request.form.get('submit_add_form'):
            logger.debug(f"form: {request.form.to_dict()}")
            p_info = {
                'nume': request.form['name']
            }
            #print("Inainte de adaugare")
            r = OrasCtrl.addNew(**p_info)
            #r = OrasCtrl.addNew(**p_info)
            print(r)
            if r[0]:
                flash(f"Orasul: {request.form['name']}, a fost adaugat", category="success")
            else:
                logger.error(f"Orasul request.form['name'] exista deja: {r[1]}")
                flash(f"Orasul: {request.form['name']}, nu poate fi adaugat! Exista deja!", category="danger")
            
            response = make_response(redirect(url_for('.locatie')));
            response.set_cookie('adauga', value="1", max_age = 1);
        
        elif request.form['action'] == 'delete':
            logger.debug(f"form: {request.form.to_dict()}")
            try:
                with db.session.begin():
                    x = db.session.get(Oras, request.form['item-id'])
                    #if p.produse = []:
                    db.session.delete(x)
                flash(f"Orasul: {x.nume}, a fost sters!", category='success')
            except exc.IntegrityError:
                flash(f"Producatorul {x.nume} nu poate fi sters. Are produse asociate!", category="danger")
        
        elif request.form['action'] == "modify":
            logger.debug(f"form: {request.form.to_dict()}")
            #return(request.form['new-value'])
            logger.debug(f"form: {request.form.to_dict()}")
            x_id = request.form['item-id']
            x_new_val = request.form['new-value']
            #x_attr = request.form['item-attr']

            ret = OrasCtrl.modifyAttr(x_id, x_new_val)
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
            return redirect(url_for('.locatie')) # name full: main.locatie or relative .locatie

    logger.debug(f"GET request. pagina: {url_for('.locatie')}")
    #count_products = func.count(Produs.id.distinct()).label(None)
    count_products = func.count(Produs.id).label(None) # here it works the same as with distinct

    # doar orasele care au produse - nume oras si cate produse sunt fabrircate
    # select orase.nume, count(produse.nume) from orase 
    # join produse_orase on orase.id=produse_orase.oras_id 
    # join produse where produse_orase.product_id=produse.id 
    # group by oras_id

    #select orase.nume, count(produse.id) from orase 
    #left join produse_orase on orase.id=produse_orase.oras_id 
    #left join produse on produse_orase.product_id = produse.id 
    #group by orase.id

    # Aceleasi interogari dar folosind sqlalchemy ORM
    #q = select(modele.Oras.nume, func.count(modele.Produs.nume)).join(modele.Produs.orase, isouter=True).group_by(modele.Oras.nume)
    #
    #>>> orase = db.session.execute(q).all()
    #>>> orase
    #[(None, 5), ('Bucuresti', 3), ('Cluj-Napoca', 1), ('Suceava', 2), ('Zalau', 4)]
    #>>> 
    #>>> q = select(modele.Oras.nume, func.count(modele.Produs.nume)).join(modele.Oras.produse, isouter=True).group_by(modele.Oras.nume)
    #
    #>>> orase = db.session.execute(q).all()
    #>>> orase
    #[('Bistrita', 0), ('Bucuresti', 3), ('Cluj-Napoca', 1), ('Drobeta Turnu Severin', 0), ('Suceava', 2), ('Timisoara', 0), ('Zalau', 4)]


    q = select(Oras.id, Oras.nume, count_products).join(Oras.produse, isouter=True).group_by(Oras.id)
    print(q)
    
    lst_orase_count_tip_produse = db.session.execute(q).all()
    #print(lst_orase_count_tip_produse)
    # DEBUG: ChocoDist.chocodist.main.views: locatie: id, oras si nr produse:
    # [(1, 'Bucuresti', 3), (2, 'Suceava', 2), (3, 'Zalau', 4), (4, 'Cluj-Napoca', 1), (5, 'Bistrita', 0), (6, 'Drobeta Turnu Severin', 0), (7, 'Timisoara', 0)]
    #
    # print(lst_orase_count_tip_produse[0][1]) - e OK -> Bucuresti
    #
    #print(lst_orase_count_tip_produse[0]['nume']) - merge in Template dar nu si aici ...
    #adica, in template, pot accesa elementele pentru un oras si din 
    logger.debug(f"id, oras si nr produse: {lst_orase_count_tip_produse}")
    return render_template("locatie.html", APPNAME=APPNAME, orase=lst_orase_count_tip_produse)

###########################################
# REST API DBG - oferte de la producatori
###########################################
@main.route("/dbgtoken", methods = ['GET', 'POST'])
@login_required
@permission_required(Permisiuni.VIZUALIZAREDATEADMIN)
def dbgtoken():
    token_or_error = json.dumps(ComandaProducatorCtrl.getProducerOfferAPIToken(), indent=4)
    logger.debug(f"token_or_error: {token_or_error}")
    return render_template("dbgrestapitoken.html", APPNAME=APPNAME, token_or_error=token_or_error)

@main.route("/dbgoferte", methods = ['GET', 'POST'])
@login_required
@permission_required(Permisiuni.VIZUALIZAREDATEADMIN)
def dbgoferte():
    api_offers = json.dumps(ComandaProducatorCtrl.getAllProducersOffersViaAPI(), indent=4)
    logger.debug(f"api_offers: {api_offers}")
    return render_template("dbgproducersrestapioffers.html", APPNAME=APPNAME, api_offers=api_offers)

###########################################
# Comenzi la producatori
###########################################
@main.route("/generare_comanda_producator", methods = ['GET', 'POST'])
@login_required
@permission_required(Permisiuni.VIZUALIZAREDATEADMIN)
@permission_required(Permisiuni.COMENZIPRODUCATOR)
def generare_comanda_producator():
    q = select(Producator).order_by(Producator.nume)
    #producatori = db.session.execute(q).all() - lista tupluri, cu un singur element in acest caz
    #print("producatori - cu execute", producatori)
    producatori = db.session.scalars(q).all() # lista obiecte
    #print("p_s:", p_s)
    selectat = "---"
    oferta = []
    id_selectat = None

    if request.method == "POST":
        if request.form.get('selecteaza-producator'):
            obj = db.session.get(Producator, request.form['producator']) # trimit din formular ID-ul producatorului
            if obj != None:
                selectat = obj.nume
                id_selectat = obj.id
                oferta = ComandaProducatorCtrl.getProducerOffer(selectat)
                #return redirect(url_for('.cumparare_produse', id_selectat=id_selectat, selectat=selectat)) # name full: main.cumparare_produse
        if request.form.get('comanda-produse'):
            print(request.form) 
            flash(f"Comanda la producatorul {request.form['producator']} a fost trimisa!", category="success")
            ComandaProducatorCtrl.addProducerOrder(request.form)
        
    return render_template("generare_comanda_producator.html", APPNAME=APPNAME, producatori=producatori, id_selectat=id_selectat, selectat=selectat, oferta=oferta)

@main.route("/comenzi_la_producator", methods = ['GET', 'POST'])
def comenzi_la_producator():
    comenzi = ComandaProducatorCtrl.getAllOrders()
    return render_template("comenzi_la_producator.html", APPNAME=APPNAME, comenzi=comenzi)

@main.route("/detalii_comanda_producator", methods=['GET'])
def detalii_comanda_producator():
    info_cmd = ComandaProducatorCtrl.getOrderDetails(request.args['id'])
    logger.debug(f"Informatii detaliate despre comanda: {info_cmd}")
    return render_template("detalii_comanda_producator.html", APPNAME=APPNAME, info_comanda=info_cmd)


###########################################
# Comenzi de la clienti
###########################################
@main.route("/generare_comanda_client", methods = ['GET', 'POST'])
@login_required
@permission_required(Permisiuni.COMENZICLIENT)
def generare_comanda_client():
    producatori = None
    id_selectat = None
    selectat = None
    if request.method == "POST":
        print("request.form:", request.form)
        ComandaClientCtrl.addNew(request.form)

    oferta = ComandaClientCtrl.getOfferInfo()
    print("Oferta pentru clienti", oferta)
    return render_template("catalog_produse_cu_vanzare.html", APPNAME=APPNAME, producatori=producatori, id_selectat=id_selectat, selectat="CLIENT", oferta=oferta)

@main.route("/comenzi_clienti", methods=['GET'])
@login_required
@permission_required(Permisiuni.COMENZICLIENT)
def comenzi_clienti():
    info_comenzi = ComandaClientCtrl.getAllOrders()
    return render_template("comenzi_clienti.html", APPNAME=APPNAME, comenzi=info_comenzi)

@main.route("/detalii_comanda_client", methods=['GET'])
@login_required
@permission_required(Permisiuni.COMENZICLIENT)
def detalii_comanda_client():
    info_cmd = ComandaClientCtrl.getOrderDetails(request.args['id'])
    return render_template("detalii_comanda_client.html", APPNAME=APPNAME, info_comanda=info_cmd)
