"""SQLAlchemy database models.

Each model maps to a table in PostgreSQL. The Task model stores the
permanent task data for this application.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from .database import Base


class Task(Base):
    """Tasks table.

    Columns:
        id: primary key
        title: short task title (required)
        description: longer optional description
        status: e.g. pending, in_progress, completed
        is_completed: convenience boolean mirroring status
        created_at: row creation timestamp
        updated_at: auto-updated on every row change
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
