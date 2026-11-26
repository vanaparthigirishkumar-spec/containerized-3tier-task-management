"""Pytest configuration and fixtures."""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Use an in-memory SQLite database for local tests.
# Preserve an explicitly configured DATABASE_URL, such as test PostgreSQL.
os.environ.setdefault("DATABASE_URL", "sqlite://")

from backend.app.database import Base, get_db  # noqa: E402
from backend.app.main import app  # noqa: E402

TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://")

if TEST_DATABASE_URL.startswith("sqlite"):
    test_engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(scope="function")
def db():
    """Create a clean database for each test."""
    Base.metadata.create_all(bind=test_engine)

    db_session = TestingSessionLocal()

    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db):
    """Provide a FastAPI test client using the test database."""

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
