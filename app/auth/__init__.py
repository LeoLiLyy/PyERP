from flask import Blueprints
auth_bp = Blueprint('auth', __name__, template_folder='templates')
from . import routes
