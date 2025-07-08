import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import redis
from flask import Flask

# --- SQLAlchemy Setup ---
# Define the base for declarative models (will be used by models.py later)
Base = declarative_base()

# Global variables to hold our engine, session factory, and Redis client
db_engine = None
Session = None # Callable to create a new session
redis_client = None



def init_db_and_redis():
    """
    Initializes the global database engine, session factory, and Redis client.
    This function should be called once at application startup.
    """
    global db_engine, Session, redis_client

    # Get connection details from environment variables or use defaults
    # These defaults assume you're running the Python app on the host
    # and Docker is mapping ports to localhost.
    database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/portfolio_tracker_db")
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))

    # Initialize SQLAlchemy Engine
    db_engine = create_engine(database_url)
    print(f"Database Engine initialized for: {database_url.split('@')[-1]}")

    # Initialize SQLAlchemy Session factory
    Session = sessionmaker(bind=db_engine)
    print("SQLAlchemy Session factory created.")

    # Initialize Redis Client
    redis_client = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        db=0, # Default Redis database
        decode_responses=True # Auto-decode responses to strings
    )
    print(f"Redis Client initialized for: {redis_host}:{redis_port}")

# Helper function to get a new DB session
def get_db_session():
    if Session is None:
        raise RuntimeError("Database not initialized. Call init_db_and_redis() first.")
    return Session()

# Helper function to get the Redis client
def get_redis_client():
    if redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_db_and_redis() first.")
    return redis_client


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    # Background colors (optional)
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'

# Function to print colored messages
def print_colored(message, color=Colors.GREEN, bold=False):
    if os.name == 'nt': # Check if running on Windows
        # Windows command prompt may not support ANSI codes by default
        # Modern Windows Terminal does, but for cmd.exe, it's problematic
        # For simplicity, we'll just print plain text on Windows.
        # For full cross-platform support, consider the 'colorama' library.
        print(message)
    else:
        prefix = color
        if bold:
            prefix += Colors.BOLD
        print(f"{prefix}{message}{Colors.RESET}")

def create_app():
    """
    Creates and configures the Flask application.
    Calls init_db_and_redis to set up connections.
    """
    app = Flask(__name__)

    # --- Configuration ---
    # Load configuration from environment variables or provide defaults
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_super_secret_key_for_flask_sessions") # Important for Flask sessions/security

    # Initialize DB and Redis connections
    init_db_and_redis()

    # Import and register blueprints (routes)
    from .routes import api_bp
    app.register_blueprint(api_bp)


    return app