"""
DevOps REST API Test Suite
Automated Unit Tests verifying all application endpoints.
"""
import pytest
from app.app import app, repository

@pytest.fixture
def client():
    """Create and configure a Flask test client with isolated state."""
    app.config["TESTING"] = True
    repository.clear()
    repository._seed_sample_data()
    with app.test_client() as client:
        yield client

def test_index_endpoint(client):
    """Verify that root endpoint returns HTTP 200 and valid service metadata."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["service"] == "DevOps Task Management REST API"
    assert data["status"] == "UP"
    assert "endpoints" in data

def test_health_probe(client):
    """Verify health endpoint used by Kubernetes liveness and readiness probes."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "UP"
    assert data["service"] == "todo-api"
    assert data["checks"]["in_memory_repository"] == "HEALTHY"
    assert "uptime_seconds" in data

def test_metrics_endpoint(client):
    """Verify metrics telemetry endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.get_json()
    assert "total_tasks_stored" in data
    assert "telemetry" in data
    assert data["telemetry"]["total_requests"] > 0

def test_list_todos(client):
    """Verify listing all tasks."""
    response = client.get("/api/todos")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert data["count"] >= 3

def test_create_todo_success(client):
    """Verify task creation with valid payload."""
    payload = {
        "title": "Configure Prometheus Alertmanager",
        "description": "Send alerts on high latency and container restarts",
        "priority": "HIGH"
    }
    response = client.post("/api/todos", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["title"] == payload["title"]
    assert data["data"]["priority"] == "HIGH"
    assert data["data"]["completed"] is False
    assert "id" in data["data"]

def test_create_todo_validation_empty_title(client):
    """Verify 400 Bad Request error when creating task without title."""
    response = client.post("/api/todos", json={"title": "   "})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "required" in data["error"]

def test_create_todo_validation_no_json(client):
    """Verify 400 Bad Request error when non-JSON body is sent."""
    response = client.post("/api/todos", data="raw string")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False

def test_get_todo_by_id(client):
    """Verify retrieving a specific task by ID."""
    response = client.get("/api/todos/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["id"] == 1

def test_get_todo_not_found(client):
    """Verify 404 response for non-existent task ID."""
    response = client.get("/api/todos/9999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False

def test_update_todo(client):
    """Verify updating task status and title."""
    update_payload = {
        "title": "Setup CI/CD Pipeline with Jenkins - COMPLETED",
        "completed": True
    }
    response = client.put("/api/todos/1", json=update_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["completed"] is True
    assert data["data"]["title"] == update_payload["title"]

def test_delete_todo(client):
    """Verify deleting a task and confirming it is no longer accessible."""
    response = client.delete("/api/todos/2")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True

    # Confirm deletion
    get_res = client.get("/api/todos/2")
    assert get_res.status_code == 404
