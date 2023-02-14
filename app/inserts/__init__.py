from flask import Blueprint

inserts_bp = Blueprint('inserts', __name__, template_folder='templates')

from .resources import farmPOST
