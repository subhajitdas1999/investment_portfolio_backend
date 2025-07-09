import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import redis
from app.utils.logging import print_colored, Colors# Import print_colored for logging

# Define the base for declarative models
Base = declarative_base()

# Global variables for extensions
db_engine = None
Session = None # Callable to create a new session
redis_client = None

def init_db_and_redis(app_config):
    """
    Initializes the global database engine, session factory, and Redis client.
    Takes app_config (from Flask app.config) to get connection details.
    """
    global db_engine, Session, redis_client

    # Initialize SQLAlchemy Engine
    db_engine = create_engine(app_config['DATABASE_URL'])
    print_colored(f"Extensions: Database Engine initialized for: {app_config['DATABASE_URL'].split('@')[-1]}", color=Colors.GREEN)

    # Initialize SQLAlchemy Session factory
    Session = sessionmaker(bind=db_engine)
    print_colored("Extensions: SQLAlchemy Session factory created.", color=Colors.GREEN)

    # Initialize Redis Client
    redis_client = redis.StrictRedis(
        host=app_config['REDIS_HOST'],
        port=app_config['REDIS_PORT'],
        db=0,
        decode_responses=True # Auto-decode responses to strings
    )
    print_colored(f"Extensions: Redis Client initialized for: {app_config['REDIS_HOST']}:{app_config['REDIS_PORT']}", color=Colors.GREEN)

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