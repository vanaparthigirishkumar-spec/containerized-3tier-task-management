"""Tests for the Task Management API.

Covers the health endpoint, full CRUD, invalid input, and error handling.
The database integration is exercised through the sqlite test fixture in
conftest.py so these tests run without an external PostgreSQL instance.
"""

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    """The /api/health endpoint should return healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_task(client: TestClient):
    """Creating a task should return 201 and the created task with an id."""
    response = client.post(
        "/api/tasks",
        json={"title": "Learn Docker", "description": "Study containers", "status": "pending"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Learn Docker"
    assert data["description"] == "Study containers"
    assert data["status"] == "pending"
    assert data["is_completed"] is False
    assert data["id"] == 1


def test_list_tasks(client: TestClient):
    """Listing tasks should return all created tasks."""
    client.post("/api/tasks", json={"title": "Task A"})
    client.post("/api/tasks", json={"title": "Task B"})

    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = {item["title"] for item in data}
    assert titles == {"Task A", "Task B"}


def test_get_single_task(client: TestClient):
    """Fetching one task by id should return that task."""
    client.post("/api/tasks", json={"title": "Solo task"})
    response = client.get("/api/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Solo task"


def test_update_task(client: TestClient):
    """Updating a task should modify only the fields sent."""
    client.post("/api/tasks", json={"title": "Original", "status": "pending"})

    response = client.put(
        "/api/tasks/1",
        json={"title": "Updated", "status": "completed", "is_completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["status"] == "completed"
    assert data["is_completed"] is True


def test_delete_task(client: TestClient):
    """Deleting a task should return 204 and the task should no longer exist."""
    client.post("/api/tasks", json={"title": "To delete"})

    response = client.delete("/api/tasks/1")
    assert response.status_code == 204

    response = client.get("/api/tasks/1")
    assert response.status_code == 404


def test_create_task_invalid_input(client: TestClient):
    """Creating a task with an empty title should be rejected (422)."""
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 422


def test_create_task_missing_title(client: TestClient):
    """Creating a task without a title should be rejected (422)."""
    response = client.post("/api/tasks", json={"description": "no title"})
    assert response.status_code == 422


def test_update_nonexistent_task(client: TestClient):
    """Updating a task that does not exist should return 404."""
    response = client.put("/api/tasks/999", json={"title": "Nope"})
    assert response.status_code == 404


def test_delete_nonexistent_task(client: TestClient):
    """Deleting a task that does not exist should return 404."""
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404
