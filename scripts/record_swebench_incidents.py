"""Record the multi-experiment measurement hazard found while adding p1b. Idempotent."""
import sys
sys.path.insert(0, "backend")
from services.error_ledger import ErrorLedgerService

INCIDENTS = [{
    "component": "ExperimentRecorder.finalize",
    "stage": "measurement_recording",
    "error_type": "One Experiment Deletes Another's Evidence",
    "summary": (
        "measurements.jsonl is keyed by paper, and finalize() opens it with 'w'. A "
        "second experiment contributing to the same paper therefore truncates the "
        "first one's rows. Adding p1b (SWE-bench retrieval) alongside p1 would have "
        "destroyed all 26 of p1's measurements on its first run. The existing guard "
        "does not catch this: it refuses only an *empty* result set, and p1b had "
        "nine rows of its own. Then the fix itself misfired -- p1b declared it owned "
        "the 'swebench_' namespace while p1 was already recording four census "
        "metrics under that prefix, and deleted them."
    ),
    "root_cause": (
        "The file is named for the paper but written as though one experiment owns "
        "it. Nothing declared which metrics a run is responsible for, so 'replace "
        "the file' was the only available semantics."
    ),
    "resolution": (
        "A recorder may declare owns_prefix: it then replaces exactly the metrics in "
        "that namespace and carries every other row through untouched, so p1 and p1b "
        "can run in either order. Rows a run removes from its own namespace are "
        "listed by name at finalize, which is what makes a wrong prefix visible "
        "instead of silent -- the misfire above printed nothing the first time. Four "
        "tests cover it, including the prefix-collision case."
    ),
    "prevention_rule": (
        "A run that overwrites shared evidence must declare what it owns and report "
        "what it removed. A namespace must be one no other experiment writes into, "
        "and 'replace everything' is only correct when a paper has exactly one "
        "experiment behind it."
    ),
}]

ledger = ErrorLedgerService()
seen = {e.get("summary") for e in ledger.data.get("history", [])}
for inc in INCIDENTS:
    if inc["summary"] in seen:
        print(f"  already recorded: {inc['error_type']}")
    else:
        e = ledger.record_error(**inc)
        print(f"  {e['error_id']} [{e['status']}] {e['error_type']}")
