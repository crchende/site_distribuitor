from functools import wraps
from flask import abort
from flask_login import current_user
from chocodist.date.modele import Permisiuni

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.poate(permission):
                abort(404)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permisiuni.ADMINISTRARE)(f)