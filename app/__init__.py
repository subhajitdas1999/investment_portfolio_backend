import os
from flask import Flask
from app.config import config_by_name
from app.utils.logging import print_colored, Colors
from app.extensions import init_db_and_redis, get_db_session, get_redis_client, Base, db_engine


def create_app(config_name=None):
    """
    Creates and configures the Flask application.
    Initializes database and Redis connections via extensions.
    """
    app = Flask(__name__)

    # --- Configuration ---
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default') # Default to 'default' if FLASK_CONFIG not set
    app.config.from_object(config_by_name[config_name])
    print_colored(f"App: Loaded configuration: {config_name}", color=Colors.MAGENTA)

    # Initialize DB and Redis connections using the extensions module
    init_db_and_redis(app.config)

    # UPDATED: Import and register the main API blueprint from its new location
    from .blueprints.api import api_bp
    app.register_blueprint(api_bp)

    return app