from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates')

from .resources import authentication
from .resources import login
from .resources import logout
from .resources import signup
from .resources import userExist
