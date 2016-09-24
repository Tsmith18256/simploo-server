from flask import Blueprint

washrooms = Blueprint('washrooms', __name__)

from . import routes
