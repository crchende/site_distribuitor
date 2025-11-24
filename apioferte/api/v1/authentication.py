from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import g, current_app

from apioferte import cfg as config

#https://stackoverflow.com/questions/71292764/which-timed-jsonwebsignature-serializer-replacement-for-itsdangerous-is-better
import jwt # from pyjwt NOT from jwt. DO not install jwt
import datetime

auth = HTTPBasicAuth()

#utilizator_validat = current_app.config['USER']
#hash_parola_utilizator_validat = generate_password_hash(current_app.config['PASS'])
utilizator_validat = config['APIUSER']
hash_parola_utilizator_validat = generate_password_hash(config['APIPASS'])

@auth.verify_password
def verify_password(user_or_token, password):
    verification_result = False
    
    print("VERIFY PASSWORD:")
    print("user_or_token:", user_or_token)
    print("password:     ", password)

    if user_or_token == '':
        print("no user or token - return false - this will trigher httpautuh in browser so you'll get a browser auth form")
        return False
    
    g.current_user = user_or_token

    if user_or_token == utilizator_validat:
        g.validat = True
        # verificare parola - in mod normal se face hash pe parola primita
        # si se compara cu hash-ul salva
        return check_password_hash(hash_parola_utilizator_validat, password)
    
    if password == "": # no password - assuming token is used
        verification = verify_jwt_token(user_or_token)
        print("token auth verification result:", verification)
        
        verification_result = verification[0]
        # in cazul in care fie parola fie tokenul este bun
        # verific daca utilizatorul este validat
        if verification_result:
            user_from_token = verification[1]['user']
            if user_from_token == utilizator_validat:
                g.validat = True
            else:
                g.validat = False
                print("Utilizatorul nevalidat:", user_from_token)
        
        return verification_result

def generate_jwt_token(user, expiration):
    print("generate_jwt_token: ", user, expiration)
    '''
        generate_jwt_token - generates a jwt token

        user:        the usder for which to generate the token
        expiration:  how many seconds to be available
    '''
    token = jwt.encode(
        {
            "confirm": user,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expiration),
        },
        config['SECRET_KEY'],  # ar trebui sa fie ceva secret, specific aplicatiei - se poate lua din env
        algorithm="HS256"
    )
    return token

def verify_jwt_token(token):
    try:
        data = jwt.decode(
            token,
            config['SECRET_KEY'],
            leeway=datetime.timedelta(seconds=1),
            algorithms=["HS256"]
        )
        print("token decodat:", data)
    except Exception as e:
        print("Decoding failed with error:", e)
        return (False, None)
    
    return (True, {"user": data.get('confirm')})