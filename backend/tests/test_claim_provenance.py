"""Tests for the claim provenance gate and venue selector.

The behaviour that matters: an unbacked number must block a peer-reviewed venue,
and a measurement recorded with a real artifact must release it again.
"""
import json

import pytest

from services.claim_provenance import (
    GROUNDING_CITATION,
    GROUNDING_EXPERIMENT,
    GROUNDING_UNGROUNDED,
    ClaimProvenanceService,
    certifies_measurement,
)
from services.venue_selector import VenueSelectorService


DRAFT = """# Self-Healing Code Synthesis

We benchmark across $N = 500$ defects and reach 47.2% resolution
($p < 0.001$, Cohen's d = 1.14) with a 2.5x speedup.

Prior work reports 28.1% on the same split [[arxiv_2501_02497]].
"""


@pytest.fixture()
def service(tmp_path):
    return ClaimProvenanceService(vault_path=str(tmp_path), runs_root=str(tmp_path / "runs"))


def _write_draft(tmp_path, text=DRAFT, name="paper.md"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return str(path)


def _record_measurement(tmp_path, run_id, value, artifact="bench/out.json", sha="a" * 64,
                        unit="%"):
    run_dir = tmp_path / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    with (run_dir / "measurements.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "metric": "resolution_rate", "value": value, "unit": unit,
            "artifact": artifact, "sha256": sha,
        }) + "\n")


# --------------------------------------------------------------- extraction

def test_extracts_each_kind_of_quantitative_claim(service):
    claims = service.extract_claims(DRAFT)
    kinds = {c.kind for c in claims}
    assert {"sample_size", "percentage", "p_value", "effect_size", "factor"} <= kinds


def test_headings_and_math_blocks_are_not_claims(service):
    claims = service.extract_claims("# Section 2.1\n\n$$\nx = 42\n$$\n")
    assert claims == []


def test_overlapping_matches_are_claimed_once(service):
    # 'p < 0.001' must not also surface as a bare decimal.
    claims = service.extract_claims("We find $p < 0.001$ overall.")
    assert len(claims) == 1
    assert claims[0].kind == "p_value"


# ---------------------------------------------------------------- grounding

def test_claim_without_evidence_is_ungrounded(service, tmp_path):
    report = service.audit_draft(_write_draft(tmp_path))
    assert report.measurements_found == 0
    assert report.ungrounded == report.total_claims - report.citation_backed
    assert report.experiment_backed == 0


def test_recorded_measurement_grounds_the_matching_claim(service, tmp_path):
    path = _write_draft(tmp_path)
    _record_measurement(tmp_path, "draft-paper", 47.2)

    report = service.audit_draft(path)

    backed = [c for c in report.claims if c.grounding == GROUNDING_EXPERIMENT]
    assert [c.raw for c in backed] == ["47.2%"]
    assert backed[0].evidence.startswith("bench/out.json#")


def test_measurement_without_artifact_does_not_ground_a_claim(service, tmp_path):
    """A row in a JSON file is an assertion elsewhere, not evidence."""
    path = _write_draft(tmp_path)
    run_dir = tmp_path / "runs" / "draft-paper"
    run_dir.mkdir(parents=True)
    (run_dir / "measurements.jsonl").write_text(
        json.dumps({"metric": "rate", "value": 47.2, "unit": "%"}) + "\n", encoding="utf-8"
    )

    report = service.audit_draft(path)
    assert report.experiment_backed == 0


def test_attributed_claim_counts_as_citation_backed(service, tmp_path):
    report = service.audit_draft(_write_draft(tmp_path))
    attributed = [c for c in report.claims if c.grounding == GROUNDING_CITATION]
    assert any("28.1" in c.raw for c in attributed)


def test_citation_without_attribution_language_stays_ungrounded(service, tmp_path):
    path = _write_draft(tmp_path, "We achieve 91.5% accuracy [[arxiv_1234]].\n")
    report = service.audit_draft(path)
    assert report.claims[0].grounding == GROUNDING_UNGROUNDED


# --------------------------------------------------------------------- gate

def test_peer_reviewed_venues_certify_measurement_but_preprints_do_not():
    assert certifies_measurement("NeurIPS")
    assert certifies_measurement("MDPI")
    assert certifies_measurement("SpringerOpen")
    assert not certifies_measurement("arXiv")
    assert not certifies_measurement("DOAJ")


def test_gate_blocks_reviewed_venue_when_claims_are_unbacked(service, tmp_path):
    report = service.audit_draft(_write_draft(tmp_path))

    assert service.gate(report, "NeurIPS")["allowed"] is False
    assert service.gate(report, "MDPI")["allowed"] is False
    assert service.gate(report, "arXiv")["allowed"] is True


def test_gate_releases_reviewed_venue_once_every_claim_is_backed(service, tmp_path):
    path = _write_draft(tmp_path, "We reach 47.2% resolution.\n")
    _record_measurement(tmp_path, "draft-paper", 47.2)

    report = service.audit_draft(path)
    decision = service.gate(report, "NeurIPS")

    assert report.ungrounded == 0
    assert decision["allowed"] is True
    assert decision["blocking_claim_count"] == 0


# ----------------------------------------------------------- venue selector

def test_selector_refuses_reviewed_venues_for_an_unbacked_paper():
    selector = VenueSelectorService("balanced")
    paper = selector.extract_features("p", DRAFT, ungrounded_claims=5, total_claims=6)

    allocation = selector.allocate_portfolio([paper])
    assert allocation["p"]["venue"] == "arXiv"


def test_selector_opens_reviewed_venues_for_a_backed_paper():
    selector = VenueSelectorService("balanced")
    text = DRAFT + "\nlearning model training optimization benchmark agent theorem\n"
    paper = selector.extract_features("p", text, ungrounded_claims=0, total_claims=6)

    allocation = selector.allocate_portfolio([paper])
    assert allocation["p"]["tier"] != "preprint"


def test_selector_never_routes_to_an_unverified_or_index_only_venue():
    selector = VenueSelectorService("balanced")
    paper = selector.extract_features("p", DRAFT, ungrounded_claims=0, total_claims=1)

    ranked = {s.venue: s for s in selector.rank_venues(paper)}
    assert ranked["Femington"].eligible is False
    assert ranked["DOAJ"].eligible is False


def test_balanced_strategy_caps_competitive_submissions():
    selector = VenueSelectorService("balanced")
    papers = [
        selector.extract_features(
            f"p{i}",
            "learning neural model representation optimization agent benchmark "
            "training generalization bound theorem " * 60,
            ungrounded_claims=0,
            total_claims=1,
        )
        for i in range(5)
    ]

    allocation = selector.allocate_portfolio(papers, max_competitive=2)
    competitive = [a for a in allocation.values() if a["tier"] == "competitive"]
    assert len(competitive) == 2


def test_each_manuscript_gets_exactly_one_venue():
    selector = VenueSelectorService("balanced")
    papers = [
        selector.extract_features(f"p{i}", DRAFT, ungrounded_claims=0, total_claims=1)
        for i in range(4)
    ]

    allocation = selector.allocate_portfolio(papers)
    assert all(isinstance(a["venue"], str) for a in allocation.values())
    assert len(allocation) == 4


def test_measurement_in_an_incompatible_unit_does_not_ground_a_claim(service, tmp_path):
    """A '$1' price must not be grounded by a recorded exponent that happens to be 1.0."""
    path = _write_draft(tmp_path, "Inference cost is \\$1 per task.\n")
    _record_measurement(tmp_path, "draft-paper", 1.0, unit="exponent")

    report = service.audit_draft(path)
    assert report.experiment_backed == 0
