from services.latex_exporter import LaTeXExporterService
from services.venue_contract import audit_venue_contract


def test_package_fallback_is_preview_only_not_submission_ready():
    report = audit_venue_contract(
        "NeurIPS",
        r"\documentclass{article}\usepackage[final]{neurips_2026}",
        "Abstract\nLimitations",
        "target_pages: 9\n# Limitations",
        total_pages=6,
        package_fallback_used=True,
    )

    assert report["passed"] is False
    assert report["template_passed"] is False
    assert "preview-only" in report["detail"]


def test_doaj_is_rejected_as_a_submission_venue():
    report = audit_venue_contract(
        "DOAJ",
        r"\documentclass[10pt]{article}",
        "Abstract",
        "target_pages: 4",
        total_pages=4,
    )

    assert report["passed"] is False
    assert report["index_only"] is True
    assert "indexing service" in report["detail"]


def test_required_sections_and_page_scope_are_enforced_on_rendered_artifact():
    report = audit_venue_contract(
        "CVPR",
        r"\documentclass[10pt,twocolumn,letterpaper]{article}\usepackage{cvpr}",
        "Abstract\nIntroduction",
        "target_pages: 8\n# Limitations",
        total_pages=9,
    )

    assert report["passed"] is False
    assert report["missing_sections"] == ["Limitations"]
    assert report["page_passed"] is False


def test_acm_export_uses_acmart_contract():
    tex = LaTeXExporterService().markdown_to_venue_latex(
        "ACM", "A Paper", ["Author"], "Abstract.", "## Methods\nText."
    )

    assert r"\documentclass[manuscript,review]{acmart}" in tex
    assert r"\settopmatter{printacmref=false}" in tex
