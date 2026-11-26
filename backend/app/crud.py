"""CRUD (Create, Read, Update, Delete) operations for tasks.

These functions encapsulate all direct database access. Route handlers call
these instead of writing raw SQLAlchemy queries, keeping the data layer
separate from the API layer.
"""

from sqlalchemy.orm import Session

from . import models, schemas


def get_task(db: Session, task_id: int):
    """Return a single task by id, or None if not found."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    """Return a list of tasks with pagination."""
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    """Insert a new task and return the created row (with generated id)."""
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    """Update fields on an existing task. Returns the updated task or None."""
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    # exclude_unset=True means only fields the client actually sent are updated.
    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    """Delete a task by id. Returns True if deleted, False if not found."""
    db_task = get_task(db, task_id)
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True
