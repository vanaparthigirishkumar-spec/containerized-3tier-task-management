"""Configuration for the Task Management backend.

All configuration is read from environment variables. Nothing is hardcoded.
Docker Compose injects these values, and .env.example documents them for
developers running the project locally.
"""

import os

# Database connection settings (individual parts, also used to build DATABASE_URL)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "taskdb")
DB_USER = os.getenv("DB_USER", "taskuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "taskpass")

# Full SQLAlchemy database URL. Override entirely with DATABASE_URL if needed.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

# Application settings
APP_TITLE = os.getenv("APP_TITLE", "Task Management API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
