"""API route definitions for tasks and health.

Routes are registered on a router and mounted under /api in main.py.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas, database

router = APIRouter()


@router.get("/health", tags=["health"])
def health():
    """Health endpoint. Returns 200 when the API is up."""
    return {"status": "healthy"}


@router.get(
    "/tasks",
    response_model=list[schemas.TaskResponse],
    tags=["tasks"],
    summary="List all tasks",
)
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Retrieve all tasks with optional pagination."""
    return crud.get_tasks(db, skip=skip, limit=limit)


@router.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
    summary="Create a new task",
)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    """Create and store a new task permanently in PostgreSQL."""
    return crud.create_task(db, task)


@router.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
    tags=["tasks"],
    summary="Get a single task by id",
)
def get_task(task_id: int, db: Session = Depends(database.get_db)):
    """Return a task by id, or 404 if it does not exist."""
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
    tags=["tasks"],
    summary="Update a task",
)
def update_task(
    task_id: int, task: schemas.TaskUpdate, db: Session = Depends(database.get_db)
):
    """Update one or more fields of an existing task."""
    db_task = crud.update_task(db, task_id, task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
    summary="Delete a task",
)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    """Delete a task by id. Returns 204 on success, 404 if not found."""
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
