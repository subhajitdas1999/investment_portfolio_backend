from flask import Blueprint
from app.__init__ import print_colored, Colors

# Define the Blueprint for user-related API endpoints
# This will be registered under api_bp, with a prefix like /api/v1/users
users_bp = Blueprint('users_bp', __name__)
print_colored("Blueprint: 'users_bp' created.", color=Colors.BLUE)

# Import the routes to associate them with this blueprint
from . import routes # noqa: F401