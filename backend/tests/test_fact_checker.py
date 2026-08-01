import pytest
from services.fact_checker import FactCheckerService

def test_validate_citations():
    checker = FactCheckerService()
    content = "As shown in [[arxiv_2203_11171]] and [[openalex_W4221161695]], accuracy improved."
    report = checker.validate_citations(content)
    assert report["total_citations"] == 2
    assert "arxiv_2203_11171" in report["verified_links"] or "arxiv_2203_11171" in report["broken_links"]

def test_validate_numeric_claims():
    checker = FactCheckerService()
    draft = "Our model achieved 85.4% accuracy with N = 1000 samples and p < 0.05."
    source_texts = ["We evaluated 85.4% accuracy across N = 1000 samples."]
    report = checker.validate_numeric_claims(draft, source_texts)
    assert report["total_numeric_claims"] >= 2
    assert "85.4%" in report["grounded_claims"]

def test_audit_document():
    checker = FactCheckerService()
    content = "# Review\nCitation [[arxiv_1234_5678]] shows 92.5% success rate."
    source_texts = ["Report shows 92.5% success rate."]
    audit = checker.audit_document(content, source_texts)
    assert "fact_check_score" in audit
    assert "verification_matrix" in audit
