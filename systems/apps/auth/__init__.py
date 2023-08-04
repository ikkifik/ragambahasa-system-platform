from flask import Blueprint

# Defining a blueprint
bp = Blueprint('auth', __name__, template_folder='templates', 
                          static_folder='static', static_url_path='assets')

from apps.auth import routes
from apps.auth.routes import token_required