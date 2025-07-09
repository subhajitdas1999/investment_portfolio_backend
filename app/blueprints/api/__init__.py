from flask import Blueprint
from app.__init__ import print_colored, Colors

# Define the main API blueprint with the base URL prefix
# All other API blueprints will be registered under this one.
api_bp = Blueprint('api_bp', __name__, url_prefix='/api/v1')
print_colored("Blueprint: 'api_bp' (API v1) created.", color=Colors.BLUE)

# Import and register sub-blueprints onto api_bp
from .users import users_bp # 'users' is the package, 'users_bp' is the blueprint object
api_bp.register_blueprint(users_bp, url_prefix='/users')
print_colored("Blueprint: 'users_bp' registered under '/users'.", color=Colors.BLUE)

from .system import system_bp # 'system' is the package, 'system_bp' is the blueprint object
api_bp.register_blueprint(system_bp) # Registered directly under /api/v1/ (no additional prefix)
print_colored("Blueprint: 'system_bp' registered.", color=Colors.BLUE)