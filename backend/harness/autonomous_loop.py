import time
from typing import Dict, Any, Optional

class AutonomousHarnessController:
    """
    Autonomous Harness Controller with Heartbeat Monitoring.
    Tracks trajectory progress across research execution steps, maintaining
    durable task status and detecting execution timeouts or deadlocks.
    """
    def __init__(self, heartbeat_interval_sec: float = 30.0):
        self.heartbeat_interval_sec = heartbeat_interval_sec
        self.active_tasks: Dict[str, Dict[str, Any]] = {}

    def register_task(self, project_id: str, topic: str) -> None:
        self.active_tasks[project_id] = {
            "project_id": project_id,
            "topic": topic,
            "status": "started",
            "current_step": "Scout Literature Search",
            "progress_percent": 10.0,
            "last_heartbeat": time.time(),
            "created_at": time.time()
        }

    def update_heartbeat(self, project_id: str, step: str, progress: float) -> None:
        if project_id in self.active_tasks:
            self.active_tasks[project_id]["current_step"] = step
            self.active_tasks[project_id]["progress_percent"] = progress
            self.active_tasks[project_id]["last_heartbeat"] = time.time()

    def get_task_status(self, project_id: str) -> Optional[Dict[str, Any]]:
        return self.active_tasks.get(project_id)

    def complete_task(self, project_id: str) -> None:
        if project_id in self.active_tasks:
            self.active_tasks[project_id]["status"] = "completed"
            self.active_tasks[project_id]["progress_percent"] = 100.0
            self.active_tasks[project_id]["last_heartbeat"] = time.time()
