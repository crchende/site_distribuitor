from flask import Blueprint

api_v1 = Blueprint("api_v1", __name__)

from . import apiv1, errors, authentication