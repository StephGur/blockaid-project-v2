from flask import Blueprint

from bloackaid import api
from . import views


def create_api_blueprints():
    main_bp = Blueprint('main', __name__)
    api.init_app(main_bp)
    return main_bp
