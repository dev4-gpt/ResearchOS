"""The mutation operators must produce genuinely false manuscripts.

A "detection failure" is only meaningful if the mutant was actually wrong. An
operator that perturbs a value inside the gate's rounding tolerance, or that
silently produces nothing, manufactures a finding about coverage that is really
a bug in the instrument -- which happened twice while building this: mu_orphan
removed one of two measurements sharing a value and looked like a gate failure,
and mu_transplant searched for a heading no draft contains and scored 0.00%
without ever running.
"""
import random
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.claim_mutations import MUST_CATCH, OPERATORS, generate, mu_drift, mu_orphan
from services.claim_provenance import ClaimProvenanceService


DRAFT = """# Paper

## Results

The pre-filter rejection rate is 43.96\\% across all operators.
Byzantine agreement holds at 100.00\\% for the honest majority.

## Conclusion

Nothing further.
"""

MEASUREMENTS = [
    {"metric": "prefilter_rejection_rate_overall", "value": 43.96, "unit": "%",
     "artifact": "artifacts/a.json", "sha256": "a" * 64, "method": "m"},
    {"metric": "byzantine_agreement_f0", "value": 100.0, "unit": "%",
     "artifact": "artifacts/b.json", "sha256": "b" * 64, "method": "m"},
]


def _classified(text=DRAFT, measurements=None):
    service = ClaimProvenanceService()
    claims = service.extract_claims(text)
    service.classify(claims, measurements if measurements is not None else MEASUREMENTS)
    return service, claims


def test_the_fixture_starts_fully_grounded():
    """If the baseline is not clean, every 'detection' below is meaningless."""
    _, claims = _classified()
    assert claims, "no claims extracted; the fixture cannot test anything"
    assert all(c.grounding == "EXPERIMENT" for c in claims)


def test_drift_moves_past_the_rounding_tolerance():
    """43.96 -> 43.99 must not still resolve; the gate accepts correct rounding."""
    service, claims = _classified()
    mutant = mu_drift(DRAFT, claims, MEASUREMENTS, random.Random(1))
    assert mutant is not None

    mutated = service.extract_claims(mutant.text)
    service.classify(mutated, mutant.measurements)
    assert any(c.grounding == "UNGROUNDED" for c in mutated), (
        f"drift produced a mutant the gate still accepts: {mutant.description}")


def test_orphan_removes_every_measurement_that_could_satisfy_the_claim():
    """Two metrics recording the same value must both go, or the claim survives."""
    duplicated = MEASUREMENTS + [
        {"metric": "livelock_cycle_with_priority", "value": 100.0, "unit": "%",
         "artifact": "artifacts/c.json", "sha256": "c" * 64, "method": "m"},
    ]
    service, claims = _classified(measurements=duplicated)
    target = [c for c in claims if c.value == 100.0]
    assert target, "fixture must contain a claim of 100.00%"

    for _ in range(20):
        mutant = mu_orphan(DRAFT, claims, duplicated, random.Random(7))
        if mutant and mutant.target == target[0].raw:
            remaining = [m for m in mutant.measurements if m["value"] == 100.0]
            assert not remaining, "a colliding measurement was left behind"
            return


def test_every_operator_either_produces_a_mutant_or_none_at_all():
    """An operator must not return something indistinguishable from the original."""
    _, claims = _classified()
    for name in OPERATORS:
        mutants = generate(name, DRAFT, claims, MEASUREMENTS, seed=3, attempts=5,
                           metric_vocab=["Byzantine agreement rate"],
                           foreign_claims=[], citation_keys={"somekey"})
        for mutant in mutants:
            changed = mutant.text != DRAFT or mutant.measurements != MEASUREMENTS
            assert changed, f"{name} returned an unchanged manuscript"


def test_must_catch_operators_are_the_control_group():
    """These two define whether the instrument works, so the list must not drift."""
    assert set(MUST_CATCH) == {"mu_drift", "mu_orphan"}
    assert all(op in OPERATORS for op in MUST_CATCH)
