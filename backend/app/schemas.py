"""Pydantic request/response schemas.

Schemas validate incoming request bodies and shape outgoing responses.
Pydantic v2 is used (shipped with FastAPI), which is why we use model_dump()
and from_attributes instead of the v1 dict() and orm_mode.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    """Fields shared between create and update schemas."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(
        None, max_length=1000, description="Optional task description"
    )
    status: str = Field(
        default="pending", max_length=50, description="Task status (e.g. pending)"
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task (POST /api/tasks)."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (PUT /api/tasks/{id}). All fields optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None, max_length=50)
    is_completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Schema returned to the client after reading/creating/updating a task."""
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
