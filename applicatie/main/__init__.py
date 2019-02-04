from flask import Blueprint

bp = Blueprint('main', __name__)

from applicatie.main import routes
