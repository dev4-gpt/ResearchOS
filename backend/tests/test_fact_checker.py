from services.fact_checker import FactCheckerService

def test_validate_citations():
    checker = FactCheckerService()
    content = "As shown in [[arxiv_2203_11171]] and [[openalex_W4221161695]], accuracy improved."
    report = checker.validate_citations(content)
    assert report["total_citations"] == 2
    assert "arxiv_2203_11171" in report["verified_links"] or "arxiv_2203_11171" in report["broken_links"]


def test_unsupported_significance_is_blocked():
    report = FactCheckerService().audit_document(
        'The result was significant with p < 0.001 [[source]].',
        source_records={'source': 'No significance test was performed.'}, strict_evidence=True)
    assert report['status'] == 'needs_review'
    assert 'p < 0.001' in report['metric_report']['unverified_claims']

def test_validate_numeric_claims():
    checker = FactCheckerService()
    draft = "Our model achieved 85.4% accuracy with N = 1000 samples and p < 0.05."
    source_texts = ["We evaluated 85.4% accuracy across N = 1000 samples."]
    report = checker.validate_numeric_claims(draft, source_texts)
    assert report["total_numeric_claims"] >= 2
    assert "85.4%" in report["grounded_claims"]

def test_numeric_claims_ignore_confidence_interval_header():
    checker = FactCheckerService()
    draft = "| Metric | Value | 95% CI |\n|---|---:|---|\n| Drift | 3.96 degrees | -- |"
    report = checker.validate_numeric_claims(draft, ["Drift was 3.96 degrees."])
    assert "95%" not in report["unverified_claims"]


def test_audit_document():
    checker = FactCheckerService()
    content = "# Review\nCitation [[arxiv_1234_5678]] shows 92.5% success rate."
    source_texts = ["Report shows 92.5% success rate."]
    audit = checker.audit_document(content, source_texts)
    assert "fact_check_score" in audit
    assert "verification_matrix" in audit


def test_citations_require_exact_evidence_even_without_vault():
    checker = FactCheckerService()
    assert checker.validate_citations('[[made_up]]')["verified_count"] == 0
    assert checker.validate_citations('[[paper_12]]', {"paper_123": "text"})["verified_count"] == 0
    report = checker.validate_citations('[[smith2026]]', {})
    assert report["citation_score"] == 0
    assert report["unresolved_count"] == 1


def test_matching_number_in_uncited_or_negated_source_is_not_support():
    checker = FactCheckerService()
    sources = {"paper": "The system did not achieve 85% accuracy."}
    claim = "The system achieved 85% accuracy [[paper]]."
    assert not checker._source_match(claim, "85%", ["paper"], sources)
    report = checker.validate_numeric_claims(claim, ["The system achieved 85% accuracy."], sources)
    assert report["grounded_count"] == 0


def test_exact_attributed_sentence_has_quotation_support():
    checker = FactCheckerService()
    sentence = "The system achieved 85% accuracy."
    assert checker._source_match("The system achieved 85% accuracy [[paper]].", "85%", ["paper"], {"paper": sentence})


def test_bare_numbers_and_unrelated_artifacts_do_not_verify_strict_claims():
    checker = FactCheckerService()
    draft = "Our system achieves 85% accuracy."
    records = checker.extract_claim_evidence_records(draft, measured_values=[85], strict=True)
    assert records[0]["status"] == "BLOCKED"
    records = checker.extract_claim_evidence_records(draft, measurement_records=[{
        "value": 85, "metric": "latency", "artifact": "missing.json", "sha256": "a" * 64,
    }], strict=True)
    assert records[0]["status"] == "BLOCKED"


def test_contribution_claim_is_not_verified_by_reference_existence():
    checker = FactCheckerService()
    records = checker.extract_claim_evidence_records("We introduce a novel framework [[paper]].", {"paper": "A different method."})
    assert records[0]["status"] == "BLOCKED"
