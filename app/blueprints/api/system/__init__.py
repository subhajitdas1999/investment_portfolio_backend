from flask import Blueprint
from app.__init__ import print_colored, Colors

# Define the Blueprint for general system/health API endpoints
# This will be registered under api_bp.
system_bp = Blueprint('system_bp', __name__)
print_colored("Blueprint: 'system_bp' created.", color=Colors.BLUE)

# Import the routes to associate them with this blueprint
from . import routes # noqa: F401