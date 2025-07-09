import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv("SECRET_KEY", "a_default_secret_key_that_should_be_changed")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/portfolio_tracker_db")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

class DevelopmentConfig(Config):
    """Development specific configurations."""
    DEBUG = True

class ProductionConfig(Config):
    """Production specific configurations."""
    DEBUG = False
    # Add more production-specific settings here (e.g., logging, error handling)

# Mapping for environment to config class
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig # Default to development if env var not set
}