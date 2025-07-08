from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.__init__ import get_db_session, get_redis_client, db_engine, Base, print_colored, Colors

# Define a Blueprint for general system routes
# This blueprint will be registered directly under /api/v1/
system_bp = Blueprint('system_bp', __name__)

@system_bp.route('/')
def hello_world():
    """
    A simple root endpoint to confirm the Flask app is running.
    """
    return jsonify(message="Welcome to the Investment Portfolio Tracker Backend! Flask app is running.")

@system_bp.route('/db_test')
def db_test():
    """
    Endpoint to test PostgreSQL connection.
    """
    session = get_db_session()
    try:
        result = session.execute(text("SELECT 1")).scalar()
        if result == 1:
            print_colored("Route: PostgreSQL connection OK.", color=Colors.GREEN)
            return jsonify(message="Successfully connected to PostgreSQL!", db_status="OK")
        else:
            print_colored("Route: PostgreSQL connection failed unexpectedly.", color=Colors.RED)
            return jsonify(message="PostgreSQL connection failed unexpectedly.", db_status="ERROR"), 500
    except Exception as e:
        print_colored(f"Route: Error connecting to PostgreSQL: {e}", color=Colors.RED, bold=True)
        return jsonify(message=f"Error connecting to PostgreSQL: {str(e)}", db_status="ERROR"), 500
    finally:
        session.close()

@system_bp.route('/redis_test')
def redis_test():
    """
    Endpoint to test Redis connection.
    """
    redis_client = get_redis_client()
    try:
        redis_client.set("test_key_web", "test_value_web")
        value = redis_client.get("test_key_web")
        if value == "test_value_web":
            print_colored("Route: Redis connection OK.", color=Colors.GREEN)
            return jsonify(message="Successfully connected to Redis!", redis_status="OK", retrieved_value=value)
        else:
            print_colored("Route: Redis connection failed unexpectedly.", color=Colors.RED)
            return jsonify(message="Redis connection failed unexpectedly.", redis_status="ERROR"), 500
    except Exception as e:
        print_colored(f"Route: Error connecting to Redis: {e}", color=Colors.RED, bold=True)
        return jsonify(message=f"Error connecting to Redis: {str(e)}", status="ERROR"), 500

@system_bp.route('/create_tables')
def create_tables():
    """
    Endpoint to create all defined database tables.
    USE WITH CAUTION: This will create tables if they don't exist.
    For production, use proper migration tools (Alembic).
    """
    try:
        # Import models here to ensure Base.metadata knows about them
        from app.models import User # noqa: F401
        Base.metadata.create_all(db_engine)
        print_colored("Route: Database tables created successfully!", color=Colors.GREEN)
        return jsonify(message="Database tables created successfully!"), 200
    except Exception as e:
        print_colored(f"Route: Error creating tables: {e}", color=Colors.RED, bold=True)
        return jsonify(message=f"Error creating tables: {str(e)}", status="ERROR"), 500