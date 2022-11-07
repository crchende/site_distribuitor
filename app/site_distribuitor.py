from flask import Flask, render_template
from flask import request
from flask_bootstrap import Bootstrap

from app.date.date import date_distribuitor
from app.date.prelucrare_date import *

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html', page="distribuitor ciocolata")
    

@app.route('/comenzi-producatori')
def comenzi_producatori():
    return render_template('index.html', page="comenzi producatori")
    

@app.route('/produse')
def produse():

    lst_produse = afiseaza_produse()
    return render_template('index.html', page="produse", produse = lst_produse)


@app.route('/producatori')
def producatori():
    return render_template('index.html', page="producatori")

    
