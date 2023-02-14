from flask import Blueprint

search_bp = Blueprint('search', __name__, template_folder='templates')

from .resources import downloadCSV
from .resources import downloadJSON
from .resources import searchCowData
from .resources import searchCowForm
from .resources import searches
