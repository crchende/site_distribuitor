from . import api_v1
from flask import g

from flask import jsonify
'''
# Serverul genereaza pagina de eroare.
# Nu este nevoie sa definesc raspunsul la eroare in mai multe locuri
# folosesc raspunsul din 'blog', unde am adaugat modul de tratare al erorii
# pentru cazul in care se asteapta raspuns JSON
#

Utilizare curl pentru a verifica raspunsul:

#cip@cipasus:~/programare/git/flaskinfo$ curl --header 'Accept:application/json' http://127.0.0.1:5000/api/v1/test_api_v11
#{"error":"not found"}

@api_v1.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({"error": "not found"})
    response.status_code = 404
    return response
'''

def forbidden(message):
    '''
    Functie utila in cazul in care resura nu este accesibila
    Ar merge folosita pentru user-ul anonim sau pentru user nevalidat
    '''
    response = jsonify({'user': g.get('current_user'), 'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response