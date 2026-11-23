import io
import json
from pathlib import Path
import time
import zipfile

from services.publisher_jobs import PublisherReadinessJobManager
from services.publisher_readiness import PublisherReadinessService
from services.visual_auditor import VisualLayoutAuditorService


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


def test_job_manager_runs_in_background_and_returns_report(tmp_path):
    service = FakeReadinessService()
    manager = PublisherReadinessJobManager(service, path=tmp_path / "publisher.db")

    started = manager.start(trigger="test")
    finished = _wait_for(manager, started["job_id"])

    assert finished["status"] == "completed"
    assert finished["report"]["ready_count"] == 1
    assert service.calls == [(None, None)]
    manager.worker.stop()


def test_job_manager_preserves_all_requests_during_an_active_run(tmp_path):
    service = FakeReadinessService()
    manager = PublisherReadinessJobManager(service, path=tmp_path / "publisher.db")
    started = manager.start(trigger="manual")
    queued = manager.start(target_filename="draft.md", trigger="draft_save")
    third = manager.start(target_filename="other.md", trigger="draft_save")
    finished = _wait_for(manager, started["job_id"])

    assert queued["job_id"] != started["job_id"]
    assert finished["status"] == "completed"
    assert _wait_for(manager, queued["job_id"])["status"] == "completed"
    assert _wait_for(manager, third["job_id"])["status"] == "completed"
    assert service.calls == [(None, None), ("draft.md", None), ("other.md", None)]
    manager.worker.stop()


def test_bundle_preserves_each_published_revision_and_rejects_artifact_damage(api_client, vault, tmp_path, monkeypatch):
    import main

    service = PublisherReadinessService(vault)
    # Exercise real job, vault, manifest and ZIP code with deterministic renderer outputs.
    monkeypatch.setattr(service, "audit_substantive_value", lambda *args, **kwargs: {
        "substantive_value_passed": True, "score": 100,
    })
    monkeypatch.setattr(service.checkmate, "auto_remediate_markdown", lambda content: content)
    monkeypatch.setattr(service.checkmate, "audit_pdf", lambda *args, **kwargs: {
        "checkmate_passed": True, "checks": {"venue_contract": {"passed": True}},
    })
    monkeypatch.setattr(VisualLayoutAuditorService, "audit_layout_geometry", lambda *args, **kwargs: {"passed": True})
    monkeypatch.setattr(service.exporter, "generate_bibtex", lambda papers, manuscript_content: f"BIB {manuscript_content}")
    monkeypatch.setattr(service.exporter, "markdown_to_venue_latex", lambda venue, title, authors, abstract, content, **kwargs: f"TEX {content}")
    monkeypatch.setattr(service.exporter, "compile_pdflatex", lambda tex, **kwargs: f"PDF {tex}".encode())
    manager = PublisherReadinessJobManager(service, path=tmp_path / "revision_jobs.db")
    monkeypatch.setattr(main, "publisher_readiness_jobs", manager)

    readiness_url = "/api/vault/publisher/readiness"
    bundle_url = f"{readiness_url}/bundle"
    filename = "manuscript.md"

    def publish(content):
        vault.save_markdown("drafts", filename, content)
        response = api_client.post(readiness_url, params={"filename": filename, "venues": "IEEEtran"})
        assert response.status_code == 202
        job = _wait_for(manager, response.json()["job"]["job_id"])
        assert job["status"] == "completed", job["error"]
        assert job["report"]["ready_count"] == 1, job["report"]["results"]
        return job

    try:
        original = publish("Original manuscript text.")
        revised = publish("Revised manuscript text.")
    finally:
        manager.worker.stop()

    def download(job):
        return api_client.get(bundle_url, params={"job_id": job["job_id"]})

    assert original["run_id"] != revised["run_id"]
    assert api_client.get(bundle_url).status_code == 422
    assert api_client.get(bundle_url, params={"job_id": "unknown"}).status_code == 404

    for job, content in ((original, "Original manuscript text."), (revised, "Revised manuscript text.")):
        response = download(job)
        assert response.status_code == 200, response.text
        assert response.headers["content-type"] == "application/zip"
        with zipfile.ZipFile(io.BytesIO(response.content)) as bundle:
            assert json.loads(bundle.read("publisher_readiness_manifest.json"))["run_id"] == job["run_id"]
            assert json.loads(bundle.read("run_manifest.json"))["run_id"] == job["run_id"]
            assert bundle.read("manuscript_IEEEtran.pdf") == f"PDF TEX {content}".encode()
            assert bundle.read("manuscript_IEEEtran.tex") == f"TEX {content}".encode()
            assert bundle.read("manuscript_references.bib") == f"BIB {content}".encode()
            assert bundle.read("stage_events.jsonl")

    report = original["report"]
    manifest = Path(report["artifact_manifest"])
    for artifact in (
        manifest, manifest.with_name("manifest.json"), Path(report["stage_events_path"]),
        *(Path(report["results"][0][key]) for key in ("pdf_path", "tex_path", "bib_path")),
    ):
        original_bytes = artifact.read_bytes()
        artifact.unlink()
        assert download(original).status_code == 409, artifact.name
        artifact.write_bytes(original_bytes + b" ")
        assert download(original).status_code == 409, artifact.name
        artifact.write_bytes(original_bytes)
    assert download(original).status_code == 200
    assert download(revised).status_code == 200
