import time

from services.publisher_jobs import PublisherReadinessJobManager


class FakeReadinessService:
    def __init__(self):
        self.calls = []

    def run(self, target_filename=None, venues=None):
        self.calls.append((target_filename, venues))
        time.sleep(0.02)
        return {"success": True, "ready_count": 1, "total_tests": 1}


def _wait_for(manager, job_id):
    for _ in range(100):
        job = manager.get(job_id)
        if job and job["status"] in {"completed", "failed"}:
            return job
        time.sleep(0.01)
    raise AssertionError("job did not finish")


def test_job_manager_runs_in_background_and_returns_report():
    service = FakeReadinessService()
    manager = PublisherReadinessJobManager(service)

    started = manager.start(trigger="test")
    finished = _wait_for(manager, started["job_id"])

    assert finished["status"] == "completed"
    assert finished["report"]["ready_count"] == 1
    assert service.calls == [(None, None)]


def test_job_manager_coalesces_a_save_during_an_active_run():
    service = FakeReadinessService()
    manager = PublisherReadinessJobManager(service)
    started = manager.start(trigger="manual")
    queued = manager.start(target_filename="draft.md", trigger="draft_save")
    finished = _wait_for(manager, started["job_id"])

    assert queued["job_id"] == started["job_id"]
    assert queued["queued_rerun"] is True
    assert finished["next_job_id"]
    next_finished = _wait_for(manager, finished["next_job_id"])
    assert next_finished["status"] == "completed"
    assert service.calls == [(None, None), ("draft.md", None)]
