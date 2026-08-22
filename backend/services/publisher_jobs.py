"""Background orchestration for publisher readiness runs.

The readiness matrix compiles many PDFs, so it must not hold an HTTP request open.
This manager keeps one run at a time, coalesces duplicate clicks, and queues one
fresh run when a save arrives while the current run is still compiling.
"""

from __future__ import annotations

from datetime import datetime, timezone
import threading
import uuid
from typing import Any, Dict, List, Optional, Tuple


class PublisherReadinessJobManager:
    def __init__(self, service: Any):
        self.service = service
        self._lock = threading.RLock()
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._active_job_id: Optional[str] = None
        self._queued_request: Optional[Tuple[Optional[str], Optional[List[str]], str]] = None

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _snapshot_locked(self, job_id: str) -> Dict[str, Any]:
        return dict(self._jobs[job_id])

    def _start_locked(self, target_filename: Optional[str], venues: Optional[List[str]], trigger: str) -> Dict[str, Any]:
        job_id = f"publisher-{uuid.uuid4().hex[:12]}"
        self._jobs[job_id] = {
            "job_id": job_id,
            "status": "running",
            "trigger": trigger,
            "target_filename": target_filename,
            "started_at": self._now(),
            "finished_at": None,
            "error": None,
            "report": None,
            "next_job_id": None,
        }
        self._active_job_id = job_id
        thread = threading.Thread(
            target=self._execute,
            args=(job_id, target_filename, venues, trigger),
            daemon=True,
            name=f"publisher-readiness-{job_id}",
        )
        thread.start()
        return self._snapshot_locked(job_id)

    def start(
        self,
        target_filename: Optional[str] = None,
        venues: Optional[List[str]] = None,
        trigger: str = "manual",
    ) -> Dict[str, Any]:
        with self._lock:
            if self._active_job_id:
                active = self._jobs.get(self._active_job_id)
                if active and active.get("status") == "running":
                    self._queued_request = (target_filename, venues, trigger)
                    response = self._snapshot_locked(self._active_job_id)
                    response["queued_rerun"] = True
                    return response
            return self._start_locked(target_filename, venues, trigger)

    def _execute(
        self,
        job_id: str,
        target_filename: Optional[str],
        venues: Optional[List[str]],
        trigger: str,
    ) -> None:
        try:
            report = self.service.run(target_filename=target_filename, venues=venues)
            with self._lock:
                self._jobs[job_id].update({
                    "status": "completed",
                    "finished_at": self._now(),
                    "report": report,
                })
        except Exception as error:
            with self._lock:
                self._jobs[job_id].update({
                    "status": "failed",
                    "finished_at": self._now(),
                    "error": str(error),
                })
        finally:
            with self._lock:
                if self._active_job_id == job_id:
                    self._active_job_id = None
                queued = self._queued_request
                self._queued_request = None
                if queued:
                    next_job = self._start_locked(*queued)
                    self._jobs[job_id]["next_job_id"] = next_job["job_id"]

    def get(self, job_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        with self._lock:
            resolved_id = job_id or self._active_job_id
            if not resolved_id or resolved_id not in self._jobs:
                return None
            return self._snapshot_locked(resolved_id)
