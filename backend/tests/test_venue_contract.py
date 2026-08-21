from services.latex_exporter import LaTeXExporterService, VENUE_SPECS
from services.publisher_readiness import DEFAULT_PUBLISHER_VENUES
from services.venue_contract import VENUE_CONTRACTS, audit_venue_contract, venue_registry_gaps
from services.venue_profiles import SUPPORTED_VENUES, VENUE_PROFILES


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


def test_every_exposed_venue_has_profile_exporter_and_contract():
    assert set(VENUE_PROFILES) == set(VENUE_SPECS)
    assert set(VENUE_PROFILES) == set(VENUE_CONTRACTS)
    assert venue_registry_gaps() == {"missing_contracts": [], "orphan_contracts": []}


def test_all_venue_readiness_is_registry_driven():
    assert tuple(DEFAULT_PUBLISHER_VENUES) == SUPPORTED_VENUES
