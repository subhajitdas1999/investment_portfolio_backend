from flask import Blueprint


# Define the main API blueprint with the base URL prefix
api_bp = Blueprint('api_bp', __name__, url_prefix='/api/v1')

from .system_routes import system_bp
api_bp.register_blueprint(system_bp) # Registers system_bp directly under /api/v1/ (no additional prefix)

# Import and register sub-blueprints
from .user_routes import user_bp
api_bp.register_blueprint(user_bp, url_prefix='/users') # Registers user_bp under /api/v1/users
