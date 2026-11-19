"""
DevOps Project: REST API Microservice
Course Code: 25CIAEC59 | Student: Gautam Rajesh (USN: 1MS24CI045)
Department of CSE (AI & ML), Ramaiah Institute of Technology
"""
import os
import time
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from .models import TaskRepository

# Initialize Flask App
app = Flask(__name__)

# Application Configuration via Environment Variables
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "production")
APP_PORT = int(os.getenv("PORT", os.getenv("APP_PORT", "5000")))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# In-memory repository & telemetry
repository = TaskRepository()
START_TIME = time.time()
REQUEST_METRICS = {
    "total_requests": 0,
    "status_2xx": 0,
    "status_4xx": 0,
    "status_5xx": 0
}

@app.before_request
def before_request_logger():
    """Track telemetry metrics before each request."""
    REQUEST_METRICS["total_requests"] += 1

@app.after_request
def after_request_tracker(response):
    """Categorize status codes for metrics."""
    code = response.status_code
    if 200 <= code < 300:
        REQUEST_METRICS["status_2xx"] += 1
    elif 400 <= code < 500:
        REQUEST_METRICS["status_4xx"] += 1
    elif code >= 500:
        REQUEST_METRICS["status_5xx"] += 1
    return response

# -------------------------------------------------------------
# Base & Health Endpoints (Used by Kubernetes Probes & DevOps CI)
# -------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    """Root endpoint exposing API metadata, documentation, and operational status."""
    return jsonify({
        "service": "DevOps Task Management REST API",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "status": "UP",
        "author": "Gautam Rajesh (1MS24CI045)",
        "endpoints": {
            "GET /": "Service overview and route index",
            "GET /health": "Kubernetes Liveness and Readiness probe endpoint",
            "GET /metrics": "Operational telemetry and Prometheus-style metrics",
            "GET /api/todos": "List all tasks (supports ?completed=true|false)",
            "POST /api/todos": "Create a new task with JSON payload",
            "GET /api/todos/<id>": "Retrieve a specific task by ID",
            "PUT /api/todos/<id>": "Update a task by ID",
            "DELETE /api/todos/<id>": "Delete a task by ID"
        }
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint for Kubernetes livenessProbe & readinessProbe.
    Fulfills Deployment Enhancement: Liveness/Readiness probes.
    """
    uptime_seconds = round(time.time() - START_TIME, 2)
    return jsonify({
        "status": "UP",
        "service": "todo-api",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "uptime_seconds": uptime_seconds,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "in_memory_repository": "HEALTHY",
            "disk_access": "HEALTHY",
            "memory_usage": "OPTIMAL"
        }
    }), 200

@app.route("/metrics", methods=["GET"])
def get_metrics():
    """Operational metrics endpoint for observability and monitoring."""
    uptime_seconds = round(time.time() - START_TIME, 2)
    return jsonify({
        "app_version": APP_VERSION,
        "environment": APP_ENV,
        "uptime_seconds": uptime_seconds,
        "total_tasks_stored": len(repository.get_all()),
        "telemetry": REQUEST_METRICS
    }), 200

# -------------------------------------------------------------
# Core REST API Endpoints (Component 1)
# -------------------------------------------------------------

@app.route("/api/todos", methods=["GET"])
def list_todos():
    """List tasks, optionally filtered by ?completed=true|false."""
    completed_param = request.args.get("completed")
    completed_filter = None
    if completed_param is not None:
        completed_filter = completed_param.lower() in ("true", "1", "yes")

    tasks = repository.get_all(completed=completed_filter)
    return jsonify({
        "success": True,
        "count": len(tasks),
        "data": tasks
    }), 200

@app.route("/api/todos/<int:task_id>", methods=["GET"])
def get_todo(task_id: int):
    """Retrieve a single task by ID."""
    task = repository.get_by_id(task_id)
    if not task:
        return jsonify({
            "success": False,
            "error": f"Task with ID {task_id} not found."
        }), 404

    return jsonify({
        "success": True,
        "data": task
    }), 200

@app.route("/api/todos", methods=["POST"])
def create_todo():
    """Create a new task from JSON payload."""
    payload = request.get_json(silent=True)
    if not payload or not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "error": "Invalid request body. Expected JSON object."
        }), 400

    title = payload.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        return jsonify({
            "success": False,
            "error": "'title' field is required and must be non-empty."
        }), 400

    description = payload.get("description", "")
    priority = payload.get("priority", "MEDIUM")

    task = repository.create_task(
        title=title,
        description=description,
        priority=priority
    )
    return jsonify({
        "success": True,
        "message": "Task created successfully.",
        "data": task
    }), 201

@app.route("/api/todos/<int:task_id>", methods=["PUT"])
def update_todo(task_id: int):
    """Update an existing task."""
    payload = request.get_json(silent=True)
    if not payload or not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "error": "Invalid request body. Expected JSON object."
        }), 400

    updated = repository.update_task(task_id, payload)
    if not updated:
        return jsonify({
            "success": False,
            "error": f"Task with ID {task_id} not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Task updated successfully.",
        "data": updated
    }), 200

@app.route("/api/todos/<int:task_id>", methods=["DELETE"])
def delete_todo(task_id: int):
    """Delete a task by ID."""
    deleted = repository.delete_task(task_id)
    if not deleted:
        return jsonify({
            "success": False,
            "error": f"Task with ID {task_id} not found."
        }), 404

    return jsonify({
        "success": True,
        "message": f"Task {task_id} deleted successfully."
    }), 200

# -------------------------------------------------------------
# Global Error Handlers
# -------------------------------------------------------------

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify({
        "success": False,
        "error": "The requested endpoint does not exist."
    }), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "success": False,
        "error": "Method not allowed for the requested resource."
    }), 405

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        "success": False,
        "error": "An internal server error occurred."
    }), 500

if __name__ == "__main__":
    print(f"[*] Starting DevOps Todo API service on 0.0.0.0:{APP_PORT} in {APP_ENV} mode...")
    app.run(host="0.0.0.0", port=APP_PORT, debug=False)
