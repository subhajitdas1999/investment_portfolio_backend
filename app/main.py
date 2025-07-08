import sys
import os
from sqlalchemy import text
import app.__init__ as app_init
from app.__init__ import init_db_and_redis, get_db_session, get_redis_client, db_engine, Base,Colors, print_colored,create_app



def test_db_connection():
    """Tests the PostgreSQL database connection."""
    session = None
    try:
        session = get_db_session()
        # Execute a simple query to check the connection
        result = session.execute(text("SELECT 1")).scalar()
        if result == 1:
            print_colored("[DB TEST] Successfully connected to PostgreSQL!", Colors.GREEN)
            return True
        else:
            print_colored("[DB TEST] PostgreSQL connection failed unexpectedly.", Colors.RED)
            return False
    except Exception as e:
        print_colored(f"[DB TEST] Error connecting to PostgreSQL: {e}", Colors.RED)
        return False
    finally:
        if session:
            session.close()

def test_redis_connection():
    """Tests the Redis connection."""
    redis_client = None
    try:
        redis_client = get_redis_client()
        # Perform a simple PING command
        response = redis_client.ping()
        if response:
            print_colored("[REDIS TEST] Successfully connected to Redis!", Colors.GREEN)
            redis_client.set("test_key_ping", "hello_redis")
            value = redis_client.get("test_key_ping")
            print_colored(f"[REDIS TEST] Set 'test_key_ping' and got value: {value}", Colors.YELLOW)
            return True
        else:
            print_colored("[REDIS TEST] Redis connection failed unexpectedly (PING failed).", Colors.RED)
            return False
    except Exception as e:
        print_colored(f"[REDIS TEST] Error connecting to Redis: {e}", Colors.RED)
        return False



    
# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    # This block is primarily for local development.
    # In a production environment, you would typically use a WSGI server like Gunicorn.

    # Optional: Create tables on startup for development convenience.
    # In a real application, use migration tools like Alembic.
    print_colored("Attempting to create database tables if they don't exist...")
    try:
        # Import models here to ensure they are registered with Base.metadata
        # This is crucial for Base.metadata.create_all to know about your tables.
        # print_colored(app_init.db_engine, Colors.YELLOW)
        from app.models import User
        Base.metadata.create_all(app_init.db_engine)
        print_colored("Database tables ensured (created if not existing).")
    except Exception as e:
        print_colored(f"Error during initial table creation: {e}", Colors.RED)
        print_colored("Please ensure your PostgreSQL container is running and accessible.", Colors.RED)

    app.run(host='0.0.0.0', port=8000, debug=True)
