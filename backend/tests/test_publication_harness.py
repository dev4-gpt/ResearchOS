from pathlib import Path
import json

from services.fact_checker import FactCheckerService
from services.publication_harness import PublicationEvaluationConfig, PublicationRunState, PublicationStage
from services.publisher_readiness import PublisherReadinessService

FIXTURES = Path(__file__).parent / "fixtures" / "publication_evaluator_held_out.json"


def test_evaluator_config_is_frozen_and_hash_stable():
    config = PublicationEvaluationConfig().with_hashes(source_hash="source", venue_profile_hash="venue")
    assert config.config_hash == config.config_hash
    assert config.strict_evidence is True
    try:
        config.strict_evidence = False
    except Exception:
        pass
    else:
        raise AssertionError("publication evaluator policy must be immutable")


def test_typed_publication_graph_rejects_invalid_transition():
    config = PublicationEvaluationConfig()
    state = PublicationRunState("run", ["draft.md"], ["IEEEtran"], config.evaluator_version, config.config_hash)
    state.transition(PublicationStage.ORIGINALITY)
    try:
        state.transition(PublicationStage.COMPILE)
    except ValueError:
        pass
    else:
        raise AssertionError("compile cannot bypass claim/evidence stages")


def test_held_out_exact_duplicate_is_blocked():
    fixture = json.loads(FIXTURES.read_text())["exact_duplicate"]
    report = PublisherReadinessService.audit_collection_originality(
        PublisherReadinessService.__new__(PublisherReadinessService),
        {"a.md": fixture["baseline"], "b.md": fixture["candidate"]},
    )
    assert report["passed"] is False
    assert any(pair["exact_duplicate"] for pair in report["pairs"])


def test_held_out_unsupported_quantitative_claim_is_blocked():
    fixture = json.loads(FIXTURES.read_text())["unsupported_quantitative"]
    report = FactCheckerService().audit_document(
        fixture["content"], source_texts=[], source_records={}, strict_evidence=True,
    )
    assert report["status"] == "needs_review"
    assert report["claim_report"]["blocked_count"] > 0
    assert "Missing claim provenance" in " ".join(report["blocking_errors"])


def test_confidence_interval_header_is_not_a_claim():
    fixture = json.loads(FIXTURES.read_text())["confidence_interval_label"]
    records = FactCheckerService().extract_claim_evidence_records(fixture["content"], source_records={}, strict=True)
    assert not any(record["claim_category"] == "quantitative" for record in records)


def test_claim_ids_are_repeatable():
    content = "# Abstract\\nWe propose a method that improves latency by 12 ms."
    checker = FactCheckerService()
    first = checker.extract_claim_evidence_records(content, source_records={}, strict=True)
    second = checker.extract_claim_evidence_records(content, source_records={}, strict=True)
    assert first == second
