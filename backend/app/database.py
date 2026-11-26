"""Database connection setup.

Creates the SQLAlchemy engine, a session factory, and the declarative Base
class that models inherit from. Provides a get_db() dependency that FastAPI
uses to open and close a database session per request.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL

# pool_pre_ping=True helps recover from stale connections after DB restarts.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yield a database session and ensure it is closed afterwards.

    Used as a FastAPI dependency (Depends(get_db)) in route handlers.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
