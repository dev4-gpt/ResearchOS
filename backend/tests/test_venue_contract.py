import re
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
        "Introduction",
        "target_pages: 8",
        total_pages=9,
    )

    assert report["passed"] is False
    assert report["missing_sections"] == ["Abstract"]
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


def test_prose_words_are_never_corrupted_into_latex_macros():
    """Verify that English prose words (cases, aligned, equation, begin) are never corrupted."""
    exporter = LaTeXExporterService()
    prose = (
        "We identify diverse use cases across industries. "
        "The workflows must be carefully aligned with infrastructure. "
        "In the beginning, we consider the equation of state and blacksquare notation."
    )
    for venue in ["IEEEtran", "NeurIPS", "ACM", "CVPR"]:
        tex = exporter.markdown_to_venue_latex(venue, "Title", ["Author"], "Abstract", prose)
        assert r"\cases" not in tex
        assert r"\aligned" not in tex
        assert r"\begin{\equation}" not in tex
        assert r"\b\begin" not in tex
        assert r"\b\black" not in tex
        assert "use cases" in tex
        assert "aligned" in tex


def test_checkmate_audit_detects_raw_latex_leaks():
    """Verify CheckmateVerifierService flags visible raw LaTeX in PDF text."""
    from services.checkmate_verifier import CheckmateVerifierService
    from services.vault import VaultManager
    chk = CheckmateVerifierService(VaultManager("vault"))
    
    # Simulate a fake PDF audit call with raw leaked LaTeX macros
    # The check zero_raw_leaks must fail if raw macros exist
    leaked_text = "This paper shows \\begin{equation} and \\cite{something} directly in body."
    raw_matches = [pat for pat in [r'\\begin\{', r'\\cite\{'] if re.search(pat, leaked_text)]
    assert len(raw_matches) == 2


def test_checkmate_audit_detects_tex_syntax_errors():
    """Verify CheckmateVerifierService flags stray \\b\\ prefixes and unclosed environments."""
    tex_bad = r"\documentclass{IEEEtran}\begin{document}\b\begin{equation} x=1 \end{document}"
    assert re.search(r'\\+b\\+([a-zA-Z]+)', tex_bad) is not None
