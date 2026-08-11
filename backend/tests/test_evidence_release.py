from domain.models import ClaimRecord, EvidenceSpan, RunManifest, SourceRecord, citation_key
from services.fact_checker import FactCheckerService
from services.pdf_qa import PDFQualityAssurance
from services.release_controller import ReleaseController


def test_citation_key_is_stable_across_source_formats():
    assert citation_key("arxiv:2203.11171.md") == "arxiv_2203_11171"
    assert citation_key("arxiv_2203_11171") == "arxiv_2203_11171"


def test_fact_checker_requires_cited_source_for_numeric_claims():
    checker = FactCheckerService()
    content = "The method achieved 91.2% accuracy [[arxiv_2203_11171]]."
    report = checker.audit_document(
        content,
        source_records={"arxiv:2203.11171": "The method achieved 91.2% accuracy."},
    )
    assert report["status"] == "passed"
    assert report["blocking_errors"] == []


def test_fact_checker_rejects_metric_from_wrong_source():
    checker = FactCheckerService()
    content = "The method achieved 91.2% accuracy [[arxiv_2203_11171]]."
    report = checker.audit_document(
        content,
        source_records={"arxiv:2203.11171": "The method achieved 80.0% accuracy."},
    )
    assert report["status"] == "needs_review"
    assert report["metric_report"]["unverified_claims"] == ["91.2%"]


def test_bibliography_audit_blocks_empty_duplicate_and_missing_keys():
    checker = FactCheckerService()
    report = checker.validate_bibliography(
        "Claim [[arxiv_2203_11171]] and [[missing_key]].",
        "@article{, title={Broken}}\n@article{arxiv_2203_11171, title={A}}\n@article{arxiv_2203_11171, title={Duplicate}}",
    )
    assert report["status"] == "failed"
    assert any("empty" in error.lower() for error in report["errors"])
    assert any("duplicate" in error.lower() for error in report["errors"])
    assert any("missing" in error.lower() for error in report["errors"])


def test_release_controller_blocks_missing_or_synthetic_evidence():
    decision = ReleaseController().evaluate(
        manifest=RunManifest(run_id="run-1", topic="test", synthetic=True),
        fact_audit={"status": "passed"},
        qa_report={"status": "passed", "errors": []},
        peer_review={"schema_valid": True, "overall_decision": "ACCEPT"},
        synthetic=True,
    )
    assert decision.status == "blocked"
    assert any("Synthetic" in error for error in decision.errors)


def test_pdf_qa_catches_known_artifacts():
    report = PDFQualityAssurance().inspect_text("Text with ¡ and [?] and a /Users/private path")
    assert report["status"] == "failed"
    assert len(report["errors"]) >= 3
