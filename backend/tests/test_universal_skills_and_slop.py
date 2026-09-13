"""Tests for Universal Skills discovery, Academic Voice (Stop-Slop/Humanizer), Conference Slides, and Diagrams."""

import os
import tempfile
from pathlib import Path

import _langsmith_stub  # noqa: F401
from fastapi.testclient import TestClient
from main import app
from services.academic_voice_linter import AcademicVoiceLinter
from services.conference_slides_service import ConferenceSlidesService
from services.diagram_generator import DiagramGeneratorService
from services.universal_skills import UniversalSkillsService


def test_universal_skills_discovery():
    """Verify universal skills service discovers globally installed tools with zero storage duplication."""
    service = UniversalSkillsService()
    summary = service.get_summary()

    assert summary["zero_storage_duplication"] is True
    assert summary["total_skills_installed"] > 10
    assert "categories" in summary

    # Check that key curated categories exist
    curations = summary["highlighted_curations"]
    assert curations["academic_voice"] >= 1
    assert curations["presentations"] >= 1
    assert curations["diagrams"] >= 1

    # Check filtering by category
    voice_skills = service.list_universal_skills(category="academic_voice")
    assert any(s["name"] == "stop-slop" for s in voice_skills)

    # Check detail retrieval
    details = service.get_skill_details("stop-slop")
    assert details is not None
    assert details["name"] == "stop-slop"
    assert "hardikpandya" in details["author"]
    assert len(details["content"]) > 50


def test_academic_voice_linter_audit():
    """Verify AcademicVoiceLinter flags AI clichés, staging contrasts, and throat-clearing."""
    linter = AcademicVoiceLinter()

    slop_prose = (
        "It is worth noting that at its core, this groundbreaking framework seamlessly "
        "delves into a tapestry of neural networks. Make no mistake, it is not only scalable but also optimal."
    )
    result = linter.audit_prose(slop_prose)

    assert result["academic_voice_score"] < 70
    assert result["total_findings"] >= 4
    assert result["breakdown"]["blockers"] >= 2  # tapestry, groundbreaking, make no mistake
    assert result["breakdown"]["majors"] >= 2    # delves into, at its core, it is worth noting

    clean_prose = (
        "We evaluate the parameter scaling laws of state-space models against Transformer baselines. "
        "Across N = 1,420 benchmark runs, the proposed routing architecture achieves a 28.4% reduction "
        "in latency (p < 0.001) under identical compute constraints."
    )
    clean_result = linter.audit_prose(clean_prose)
    assert clean_result["academic_voice_score"] == 100
    assert clean_result["total_findings"] == 0
    assert clean_result["rating"] == "AUTHENTIC_HUMAN_SCHOLARLY"


def test_academic_voice_humanizer():
    """Verify humanize_text cleans AI cliches and improves scholarly score."""
    linter = AcademicVoiceLinter()

    slop_text = "It is worth noting that at its core, this groundbreaking system seamlessly delves into sparse attention."
    cleaned_res = linter.humanize_text(slop_text)

    assert cleaned_res["cleaned_score"] > cleaned_res["original_score"]
    assert cleaned_res["score_improvement"] > 0
    assert "It is worth noting that" not in cleaned_res["humanized_text"]
    assert "delves into" not in cleaned_res["humanized_text"]
    assert "analyzes" in cleaned_res["humanized_text"] or "examine" in cleaned_res["humanized_text"]


def test_conference_slides_generation():
    """Verify ConferenceSlidesService generates 16:9 fixed-stage presentation deck."""
    with tempfile.TemporaryDirectory() as tmpdir:
        service = ConferenceSlidesService(vault_path=tmpdir)
        manuscript = (
            "# Sparse Modular State Space Models\n\n"
            "Executive Abstract: We present an empirical benchmark of multi-agent council dynamics "
            "evaluating N = 1,420 runs and achieving 47.2% gain with p < 0.001."
        )
        deck = service.generate_deck_from_manuscript("Sparse Modular Models", manuscript)

        assert deck["total_slides"] == 5
        assert os.path.exists(deck["file_path"])

        content = Path(deck["file_path"]).read_text(encoding="utf-8")
        assert "1920" in content
        assert "1080" in content
        assert "Sparse Modular State Space Models" in content
        assert "slide-1" in content
        assert "slide-5" in content


def test_diagram_generation():
    """Verify DiagramGeneratorService outputs publication-grade SVG schematics."""
    with tempfile.TemporaryDirectory() as tmpdir:
        service = DiagramGeneratorService(vault_path=tmpdir)
        res = service.generate_pipeline_diagram(title="Test Verification Pipeline")

        assert os.path.exists(res["file_path"])
        assert "<svg" in res["svg"]
        assert "STAGE 1" in res["svg"]
        assert "STAGE 6" in res["svg"]
        assert "Test Verification Pipeline" in res["svg"]


def test_api_routes():
    """Verify FastAPI endpoints for universal skills, slop audit/humanize, slides, and diagrams."""
    client = TestClient(app)

    # 1. Universal Skills API
    res_skills = client.get("/api/skills/universal")
    assert res_skills.status_code == 200
    skills_data = res_skills.json()
    assert "summary" in skills_data
    assert "skills" in skills_data
    assert skills_data["summary"]["zero_storage_duplication"] is True

    # 2. Slop Audit API
    res_audit = client.post("/api/slop/audit", json={"text": "At its core, this groundbreaking model seamlessly operates."})
    assert res_audit.status_code == 200
    audit_data = res_audit.json()
    assert "academic_voice_score" in audit_data
    assert audit_data["total_findings"] >= 2

    # 3. Slop Humanize API
    res_humanize = client.post("/api/slop/humanize", json={"text": "At its core, this groundbreaking model seamlessly operates."})
    assert res_humanize.status_code == 200
    humanize_data = res_humanize.json()
    assert humanize_data["score_improvement"] >= 0
    assert "humanized_text" in humanize_data

    # 4. Diagram Generate API
    res_diag = client.post("/api/diagram/generate", json={"title": "FastAPI Automated Diagram"})
    assert res_diag.status_code == 200
    diag_data = res_diag.json()
    assert "<svg" in diag_data["svg"]
    assert "FastAPI Automated Diagram" in diag_data["title"]

    # 5. Slides Generate API
    res_slides = client.post(
        "/api/slides/generate",
        json={"title": "FastAPI Slide Test", "text": "# Test Paper\nExecutive Abstract: Benchmark of N = 500."},
    )
    assert res_slides.status_code == 200
    slides_data = res_slides.json()
    assert slides_data["total_slides"] == 5
