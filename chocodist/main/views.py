from . import main
from flask import current_app
from chocodist import db
from ..date import modele

@main.route("/")
def index():
    current_app.logger.debug("in INDEX")
    return "INDEX"