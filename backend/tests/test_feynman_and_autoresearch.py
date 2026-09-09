"""Comprehensive tests for Feynman Research Assistant, Autoresearch Loop, and Semantic Provenance."""

import ast
import json
import tempfile
from pathlib import Path

import _langsmith_stub
from services.autoresearch_loop import AutonomousResearchHarness, FitnessScore
from services.fact_checker import FactCheckerService
from services.feynman_service import FeynmanService
from services.publication_harness import (
    PublicationEvaluationConfig,
    PublicationRunState,
    PublicationStage,
)
from services.vault import VaultManager


def test_semantic_source_match_paraphrased_metric():
    """Verify that a paraphrased claim is verified when cited source has metric and number."""
    checker = FactCheckerService()
    draft = "Prior work reports 28.1% on the benchmark split [[arxiv_2501_02497]]."
    sources = {
        "arxiv_2501_02497": "In our comprehensive evaluation, the baseline achieves 28.1% accuracy on the benchmark split."
    }
    records = checker.extract_claim_evidence_records(draft, source_records=sources, strict=True)
    assert len(records) >= 1
    assert records[0]["status"] == "VERIFIED"
    assert records[0]["verification_method"] == "cited_source_text_match"


def test_semantic_source_match_blocks_hallucinated_metric():
    """Verify that an unsupported number is blocked."""
    checker = FactCheckerService()
    draft = "Prior work reports 99.9% on the benchmark split [[arxiv_2501_02497]]."
    sources = {
        "arxiv_2501_02497": "In our evaluation, the baseline achieves 28.1% accuracy on the benchmark split."
    }
    records = checker.extract_claim_evidence_records(draft, source_records=sources, strict=True)
    assert len(records) >= 1
    assert records[0]["status"] == "BLOCKED"
    assert records[0]["verification_method"] == "no_matching_evidence"


def test_variable_level_experiment_grounding():
    """Verify that only the matching artifact hash is attached to the claim."""
    checker = FactCheckerService()
    draft = "Our architecture achieves 47.2% resolution rate."
    measurements = [
        {
            "metric": "resolution_rate",
            "value": 47.2,
            "unit": "%",
            "artifact": "artifacts/bench.json",
            "sha256": "aaaa" * 16,
        },
        {
            "metric": "other_metric",
            "value": 12.3,
            "unit": "%",
            "artifact": "artifacts/other.json",
            "sha256": "bbbb" * 16,
        },
    ]
    records = checker.extract_claim_evidence_records(
        draft, measurement_records=measurements, strict=True
    )
    assert len(records) >= 1
    assert records[0]["status"] == "VERIFIED"
    assert records[0]["verification_method"] == "recorded_experiment_measurement"
    assert records[0]["artifact_sha256"] == ["aaaa" * 16]


def test_dynamic_state_graph_remediation_transitions():
    """Verify that dynamic remediation branches in the execution graph are valid."""
    config = PublicationEvaluationConfig()
    state = PublicationRunState("run-1", ["draft.md"], ["IEEEtran"], config.evaluator_version, config.config_hash)

    # Walk to evidence grading
    state.transition(PublicationStage.ORIGINALITY)
    state.transition(PublicationStage.CLAIM_EXTRACTION)
    state.transition(PublicationStage.EVIDENCE_RETRIEVAL)
    state.transition(PublicationStage.EVIDENCE_GRADING)

    # Remediation branch
    state.transition(PublicationStage.EVIDENCE_REMEDIATION)
    assert state.can_retry("evidence_grading", max_retries=3)
    state.record_retry("evidence_grading")
    assert state.retries["evidence_grading"] == 1

    # Retry transition back to grading and then rendering
    state.transition(PublicationStage.EVIDENCE_GRADING)
    state.transition(PublicationStage.VENUE_RENDERING)
    state.transition(PublicationStage.COMPILE)

    # LaTeX remediation branch
    state.transition(PublicationStage.LATEX_REMEDIATION)
    state.transition(PublicationStage.COMPILE)
    state.transition(PublicationStage.PDF_AUDIT)
    state.transition(PublicationStage.LAYOUT_AUDIT)

    # Layout remediation branch
    state.transition(PublicationStage.LAYOUT_REMEDIATION)
    state.transition(PublicationStage.COMPILE)


def test_autoresearch_fitness_and_ledger():
    """Verify autoresearch composite fitness scoring and ledger persistence."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir) / "vault"
        (vault_dir / "04_Drafts").mkdir(parents=True)
        (vault_dir / "00_System").mkdir(parents=True)
        draft_path = vault_dir / "04_Drafts" / "paper.md"
        draft_path.write_text("# Abstract\nWe evaluate $$ x = 42\n", encoding="utf-8")

        vm = VaultManager(str(vault_dir))
        ledger_path = str(vault_dir / "00_System" / "autoresearch_ledger.jsonl")
        harness = AutonomousResearchHarness(vault_manager=vm, ledger_path=ledger_path)

        res = harness.optimize("paper.md", max_iterations=2)
        assert res["iterations_run"] >= 1
        assert res["kept_count"] >= 1

        ledger_file = Path(ledger_path)
        assert ledger_file.exists()
        entries = [json.loads(line) for line in ledger_file.read_text().splitlines() if line]
        assert len(entries) >= 1
        assert entries[0]["decision"] in ("KEEP", "DISCARD")


def test_feynman_service_code_audit_and_review():
    """Verify Feynman paper-to-code auditing and severity-triaged peer review."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir) / "vault"
        (vault_dir / "01_Papers").mkdir(parents=True)
        (vault_dir / "04_Drafts").mkdir(parents=True)

        exp_py = Path(tmpdir) / "exp.py"
        exp_py.write_text("LR = 0.0001\nEPOCHS = 100\n", encoding="utf-8")

        vm = VaultManager(str(vault_dir))
        feynman = FeynmanService(vault_manager=vm)

        draft = "# Setup\nWe train with LR = 0.0001 for 100 epochs."
        audit = feynman.audit_paper_against_code(draft, code_dir_or_file=str(exp_py))
        assert audit["matched_in_code"] >= 1
        assert audit["code_provenance_score"] > 0

        review = feynman.simulated_peer_review(draft, venue="IEEEtran")
        assert review["recommendation"] in ("ACCEPT", "WEAK_ACCEPT", "REVISE", "REJECT")
        assert any(item["severity"] in ("BLOCKER", "MAJOR", "MINOR") for item in review["review_items"])


if __name__ == "__main__":
    print("Running test_semantic_source_match_paraphrased_metric...")
    test_semantic_source_match_paraphrased_metric()
    print("Running test_semantic_source_match_blocks_hallucinated_metric...")
    test_semantic_source_match_blocks_hallucinated_metric()
    print("Running test_variable_level_experiment_grounding...")
    test_variable_level_experiment_grounding()
    print("Running test_dynamic_state_graph_remediation_transitions...")
    test_dynamic_state_graph_remediation_transitions()
    print("Running test_autoresearch_fitness_and_ledger...")
    test_autoresearch_fitness_and_ledger()
    print("Running test_feynman_service_code_audit_and_review...")
    test_feynman_service_code_audit_and_review()
    print("\nALL 6 FEYNMAN & AUTORESEARCH & PROVENANCE TESTS PASSED SUCCESSFULLY!")
