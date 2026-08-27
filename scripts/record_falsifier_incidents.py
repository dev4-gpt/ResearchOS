"""Record what building the Falsifier and p1b exposed. Idempotent."""
import sys
sys.path.insert(0, "backend")
from services.error_ledger import ErrorLedgerService

INCIDENTS = [
    {
        "component": "resync_manuscripts.seed",
        "stage": "manuscript_resync",
        "error_type": "Interval Bounds Never Projected",
        "summary": (
            "Every results table prints a 95% confidence interval beside its point "
            "estimate, and the re-sync projected only value and n. p1's Table 1 "
            "therefore carried the intervals of the original 103-query run -- "
            "[73.79, 88.35] against a P@1 of 88.48 -- long after the estimates beside "
            "them had been re-synced to 165 queries. Two numbers in the same row "
            "describing different experiments, and the gate does not check an "
            "interval, so it passed throughout."
        ),
        "root_cause": (
            "Projectable fields were enumerated as value and n when the pass was "
            "written, and ci95 was simply not among them. The fourth instance of the "
            "same shape today: the manifest's duration, the manifest's seed, the "
            "sample size, and now the interval bounds."
        ),
        "resolution": (
            "ci95_low and ci95_high are projectable fields. p1's fourteen labelled "
            "results rows were regenerated from measurements, and the intervals now "
            "match the estimates they sit beside."
        ),
        "prevention_rule": (
            "A field a manuscript prints is a field that must be projected. Enumerate "
            "them from the measurement schema rather than from the fields a passage "
            "happened to use when the code was written -- four omissions in one day "
            "all had that cause."
        ),
    },
    {
        "component": "p10_adversarial_provenance / claim_mutations",
        "stage": "gate_coverage",
        "error_type": "Measured Gate Coverage",
        "summary": (
            "The provenance gate's blind spots were measured rather than waited for. "
            "256 deliberately broken manuscripts, six operators, deterministic under "
            "seed: overall detection 18.75%. mu_drift and mu_orphan are caught in "
            "full, which is what makes the rest believable. mu_rebind (0%), "
            "mu_attribute (0%) and mu_unitless (0%) confirm by measurement what was "
            "previously known only anecdotally: a claim binds to a value and a unit "
            "with no regard for what the sentence says it measures, an attribution "
            "verb beside any resolvable key is accepted without checking the source, "
            "and a quantity stated without a unit is never extracted at all."
        ),
        "root_cause": (
            "Not a defect in itself -- a description of one. Every hole in the gate "
            "so far was found by a person reading at the right moment, which is not a "
            "strategy that scales or that can be regression-tested."
        ),
        "resolution": (
            "Recorded as gate_detection_rate with a per-operator breakdown, and wired "
            "into CI with a floor that may rise and may not fall. Two instrument bugs "
            "were caught by the control operators before any finding was trusted: "
            "mu_orphan removed one of two measurements sharing a value and looked "
            "like a gate failure, and mu_transplant searched for a heading no draft "
            "contains and scored 0.00% without ever running. An operator that cannot "
            "run now reports 'not exercised' instead of zero."
        ),
        "prevention_rule": (
            "Measure a checker's coverage instead of inferring it from the defects it "
            "has caught. Keep a control group of mutations it must catch in full: "
            "when those slip, the instrument is broken and every other number in the "
            "table is meaningless."
        ),
    },
]

ledger = ErrorLedgerService()
seen = {e.get("summary") for e in ledger.data.get("history", [])}
for inc in INCIDENTS:
    if inc["summary"] in seen:
        print(f"  already recorded: {inc['error_type']}")
    else:
        e = ledger.record_error(**inc)
        print(f"  {e['error_id']} [{e['status']}] {e['error_type']}")

upd = ledger.resolve_error("ERR-084", resolution=(
    "Fixed in both directions, which the first fix was not. owns_prefix let p1b "
    "protect p1's rows, but p1 declared no namespace and so still truncated the "
    "whole file -- the next p1 re-run destroyed all nine of p1b's measurements, "
    "exactly the failure the fix was for. A recorder now states its position one of "
    "two ways: owns_prefix ('I own this namespace') or preserves_prefixes ('I own "
    "everything except these'), and a pair of experiments needs one of each. p1 "
    "preserves swebench_retrieval_; p1b owns it. Verified by running each after the "
    "other. Rows a run drops from its own namespace are listed by name, which is how "
    "the intermediate misfire -- p1b claiming 'swebench_' while p1 already recorded "
    "four census metrics under it -- would have been visible instead of silent."),
    status="VERIFIED_RESOLVED")
print(f"  ERR-084 -> {upd['status'] if upd else 'NOT FOUND'}")
