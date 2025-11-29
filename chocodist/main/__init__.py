from flask import Blueprint
from chocodist.date.modele import Permisiuni

main = Blueprint("main", __name__)

@main.app_context_processor
def inject_permissions():
    return dict(Permisiuni=Permisiuni)

from . import views