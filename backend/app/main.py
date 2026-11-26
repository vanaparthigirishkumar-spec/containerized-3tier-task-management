"""Task Management Backend - Application entry point.

This file creates the FastAPI application, creates database tables on startup,
and wires up the API routes under the /api prefix.
"""

from fastapi import FastAPI

from .database import engine, Base
from .api import routes

# Create all database tables defined in models.py.
# In production you would use Alembic migrations instead, but create_all is
# simple and works well for this portfolio project.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="A 3-tier task management application backend built with FastAPI and PostgreSQL.",
    version="1.0.0",
)

# Mount all API routes under /api so nginx can proxy /api/* to this service.
app.include_router(routes.router, prefix="/api")


@app.get("/", tags=["root"])
def read_root():
    """Root endpoint - useful as a quick smoke test."""
    return {"message": "Task Management API is running. See /docs for API documentation."}
