import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, text
import redis

app = Flask(__name__)

# --- Database (PostgreSQL) Configuration ---
# Get DB connection string from environment variable.
# When running Python app on host, 'localhost' refers to the host machine,
# where Docker maps the container ports.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/portfolio_tracker_db")
engine = create_engine(DATABASE_URL)

# --- Redis Configuration ---
# Get Redis host and port from environment variables.
# When running Python app on host, 'localhost' refers to the host machine,
# where Docker maps the container ports.
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

@app.route('/')
def hello_world():
    return jsonify(message="Welcome to the Investment Portfolio Tracker Backend!")

@app.route('/db_test')
def db_test():
    """
    Endpoint to test PostgreSQL connection and perform a simple query.
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            if result == 1:
                return jsonify(message="Successfully connected to PostgreSQL!", db_status="OK")
            else:
                return jsonify(message="PostgreSQL connection failed unexpectedly.", db_status="ERROR"), 500
    except Exception as e:
        return jsonify(message=f"Error connecting to PostgreSQL: {str(e)}", db_status="ERROR"), 500

@app.route('/redis_test')
def redis_test():
    """
    Endpoint to test Redis connection and perform a simple set/get operation.
    """
    try:
        redis_client.set("test_key", "test_value")
        value = redis_client.get("test_key")
        if value == "test_value":
            return jsonify(message="Successfully connected to Redis!", redis_status="OK", retrieved_value=value)
        else:
            return jsonify(message="Redis connection failed unexpectedly.", redis_status="ERROR"), 500
    except Exception as e:
        return jsonify(message=f"Error connecting to Redis: {str(e)}", redis_status="ERROR"), 500

if __name__ == '__main__':
    # When running the Python application directly on the host,
    # it will connect to Docker containers via localhost and the exposed ports.
    app.run(host='0.0.0.0', port=8000, debug=True)