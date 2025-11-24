from . import api_v1
from .authentication import auth, generate_jwt_token, verify_jwt_token
from .errors import forbidden
from flask import url_for, g, jsonify, request
from apioferte import cfg as config

import time


@api_v1.route("/")
def index_api_v1():
    raspuns_json = {
        "link1": url_for("api_v1.info"),
        "link2": url_for("api_v1.get_token"),
        "link3": url_for("api_v1.oferte")
    }
    return raspuns_json

@api_v1.route("/info")
def info():
    '''
    Raspuns public cu API v1.
    Continutul este public, nu este nevoie de autentificare pentru a-l acccesa.
    '''
    raspuns_json = {
        "version": "v1",
        "descriere": "OFERTE REST api, versiunea 1",
        "obiectiv": "test simplu REST API minimal - fara autentificare",
        "rezutat": "Se va obtine acest json",
        "dict1": {
            "d1_k1": "Exemplu json cu elemente dictionare, liste intregi",
            "d1_k2": 2,
            "d1_k3": [1, 2, 3],
            "d1_k4": {
                "d1_k4_k1": "dict in dict in dict",
                "d1_k4_k2": [],
                "d1_k4_k3": 123,
            },
        },
        #"g.current_user": g.current_user
    }
    return raspuns_json

# NOTA:
# @auth.login_required - va apela metoda decorata cu @auth.verify_password
#                        din authentication.py - numita chiar verify_password
#                        daca metoda intoarce False - nu se mai continua cu 
#                        functia view, decorata cu @auth.login_required.

@api_v1.route("/oferte") 
@auth.login_required # Fara login, se intoarce raspunsul "Unauthorized Access" - interesant de vazut cum se poate modifica
def oferte():
    'Raspuns API v1 accesibil numai cu login'
    print("Oferte disponibile")
    if g.get('current_user'):
        print("current_user:", g.get('current_user'))
        if g.get('validat') == False:
            return forbidden("Utilizator logat dar nevalidat - accesul nu este permis")
    
    raspuns_json = {
        "g.current_user": g.get('current_user'),
        "oferte": config["APIOFERTE"]
    }
    return raspuns_json

@api_v1.route("/oferta/<producator>")
@auth.login_required()
def oferta(producator):
    ret = []
    if producator in config['APIOFERTE']:
        print(f"RESTAPI OK: gasit oferta de la {producator}")
        ret = config['APIOFERTE'][producator]
    else:
        print(f"RESTAPI NOK: NU s-a gasit oferta de la {producator}")
    return ret

@api_v1.route("/tokens/")
@auth.login_required
def get_token():
    user = g.current_user
    expiration_sec = 20
    print("user:", user)
    token = generate_jwt_token(user, expiration_sec)
    return jsonify({'token': token, 'expiration[sec]': expiration_sec, "user": user})