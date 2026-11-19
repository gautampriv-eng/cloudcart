"""
Task & Todo Data Store Module
Provides an in-memory repository for tasks with thread-safe unique ID generation.
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

class TaskRepository:
    def __init__(self):
        self._todos: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1
        self._seed_sample_data()

    def _seed_sample_data(self):
        """Seed initial tasks to simulate existing data in the system."""
        self.create_task(
            title="Setup CI/CD Pipeline",
            description="Configure Jenkins declarative pipeline with Git integration.",
            priority="HIGH"
        )
        self.create_task(
            title="Write Ansible Playbooks",
            description="Automate environment provisioning and service configuration.",
            priority="MEDIUM"
        )
        self.create_task(
            title="Deploy to Kubernetes Cluster",
            description="Containerize app and deploy with replicas and health probes.",
            priority="HIGH"
        )

    def get_all(self, completed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Return all tasks, optionally filtered by completion status."""
        tasks = list(self._todos.values())
        if completed is not None:
            tasks = [t for t in tasks if t["completed"] == completed]
        return tasks

    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a single task by ID."""
        return self._todos.get(task_id)

    def create_task(self, title: str, description: str = "", priority: str = "MEDIUM") -> Dict[str, Any]:
        """Create and store a new task."""
        task_id = self._next_id
        self._next_id += 1
        task = {
            "id": task_id,
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority.upper(),
            "completed": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        self._todos[task_id] = task
        return task

    def update_task(self, task_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing task's fields."""
        task = self._todos.get(task_id)
        if not task:
            return None
        
        if "title" in updates and updates["title"]:
            task["title"] = updates["title"].strip()
        if "description" in updates:
            task["description"] = updates["description"].strip()
        if "priority" in updates:
            task["priority"] = updates["priority"].upper()
        if "completed" in updates:
            task["completed"] = bool(updates["completed"])
            
        task["updated_at"] = datetime.now(timezone.utc).isoformat()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Remove a task by ID."""
        if task_id in self._todos:
            del self._todos[task_id]
            return True
        return False

    def clear(self):
        """Clear all tasks (useful for test isolation)."""
        self._todos.clear()
        self._next_id = 1
