from . import main
from flask import current_app, render_template, request, url_for, redirect, flash
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
        if 'submit_add_producer_form' in request.form:
            logger.debug("POST request page /producatori: submit_add_producer_form")
        elif request.form.get('post_action') == 'delete_producer':
            logger.debug(f"POST request page /producatori: delete_producer with id: {request.form['producer_id']}")
        else:
            logger.debug(f"POST page /producatori ... but not add new ...")
            logger.debug(request.form)
            return(request.form['new-value'])
        
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
    logger.debug(url_for('main.produse')) # url_for(blueprint.view_function) -> path from route
    logger.debug(f"request.method: {request.method}")

    '''
    print("request.host_url:", request.host_url)
    print("request.user_agent:", request.user_agent)
    print("request.url:", request.url)
    print("request.path: - same as action of form", request.path)
    '''
    
    if request.method == "POST":
        post_action = 'submit_add_product_form'
        if post_action in request.form:
            logger.debug(f"POST request: {post_action}")
            print("request.form:", request.form)
        else:
            logger.debug(f"POST but not add new ...")
        
        #print("dir(request.form):", dir(request.form))
        #print("dir(request):", dir(request))
        print(request.form.get('new_product_name'))
        if "submit_add_product_form" in request.form:
            print("S-a apasat butonul submit din formularul add_product_form!!!")

    q = select(Produs).join(Producator).order_by(Producator.nume)
    '''
    q = SELECT produse.id, produse.nume, produse.id_producator 
        FROM produse JOIN producatori ON producatori.id = produse.id_producator ORDER BY producatori.nume
    ''' 
    logger.debug("q = " + str(q))
    lst_prod = db.session.scalars(q).all()

    lst_producatori = db.session.scalars(select(Producator)).all()
    return render_template("produse.html", APPNAME=APPNAME, produse=lst_prod, producatori=lst_producatori)