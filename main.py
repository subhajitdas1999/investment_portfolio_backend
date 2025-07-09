import sys
import os
# NEW: Import create_app from app.__init__ directly
from app import create_app
# NEW: Import db_engine and Base from app.extensions
from app.extensions import db_engine, Base
import app.extensions as app_extensions # Import extensions to ensure they are initialized
from app.utils.logging import print_colored, Colors# Keep Colors for logging

# Determine the configuration to use
flask_config_name = os.getenv('FLASK_CONFIG', 'development') # Default to 'development'
app = create_app(flask_config_name) # Pass the config name to create_app

if __name__ == '__main__':
    print_colored("Attempting to create database tables if they don't exist...", color=Colors.YELLOW)
    try:
        # Import models here to ensure they are registered with Base.metadata
        # The __init__.py in app/models/ will ensure all models are loaded.
        from app import models # noqa: F401
        Base.metadata.create_all(app_extensions.db_engine) # db_engine is now imported from app.extensions
        print_colored("Database tables ensured (created if not existing).", color=Colors.GREEN)
    except Exception as e:
        print_colored(f"Error during initial table creation: {e}", color=Colors.RED, bold=True)
        print_colored("Please ensure your PostgreSQL container is running and accessible.", color=Colors.RED)

    app.run(host='0.0.0.0', port=8000, debug=True)