from flask import Blueprint
print("__name__ (from auth __init__.py):", __name__)
auth = Blueprint('auth', __name__)

from . import views