"""Retire the acmart stub, delete the drifted audit script, share sample sizes. Idempotent."""
import sys
sys.path.insert(0, "backend")
from services.error_ledger import ErrorLedgerService

INCIDENTS = [{
    "component": "PublisherReadinessService._recorded_measurements",
    "stage": "grader_evidence",
    "error_type": "Shared Evidence, Third Instance",
    "summary": (
        "The fact checker blocked all 12 of p5's venues on 'Unverified numeric "
        "claims: N = 64'. That number is the n field of nine measurements whose "
        "metric names spell it out -- messages_at_n64_mesh and siblings -- but "
        "_recorded_measurements collected only value and the ci95 bounds, so the "
        "sample size was invisible to it. This is the third time today one grader "
        "refused a value another grader had evidence for: first the manifest's "
        "wall-clock duration, then the manifest's seed and measurement count, now "
        "the sample size."
    ),
    "root_cause": (
        "Evidence was enumerated field by field as each consumer happened to need "
        "it, rather than defined once as everything a run records. Each omission "
        "surfaces only when a manuscript states the missing field."
    ),
    "resolution": (
        "n is collected alongside value and ci95. p5 returned to 12/12 publish-ready. "
        "The recurring shape is worth naming: R56 says two graders judging one "
        "property must share evidence sources, and three violations in one day were "
        "all the same omission wearing different field names."
    ),
    "prevention_rule": (
        "Define what counts as recorded evidence once, in one place, and have every "
        "grader read that definition. Enumerating fields per consumer guarantees the "
        "list is incomplete somewhere, and the symptom is always a true statement "
        "being refused."
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

upd = ledger.resolve_error(
    "ERR-079",
    resolution=(
        "Retired. backend/templates/acmart.cls is deleted, and compile_pdflatex now "
        "asks kpsewhich whether TeX can already resolve each template before copying "
        "a local copy into the build directory -- a fallback may no longer outrank "
        "the real class. template_provenance() reports which file each build used. "
        "Only acmart shadowed an installed class; the four remaining local styles "
        "(acl, cvpr, icml2026, neurips_2026) have no installed counterpart and are "
        "still copied. All nine manuscripts rebuilt against the real class: the three "
        "actually allocated to ACM are publish-ready, and the three whose ACM package "
        "now fails go to ICML, SpringerOpen and arXiv, so nothing on the submission "
        "path regressed. p4's ACM layout failure is the honest page count that the "
        "stub had been hiding. scripts/comprehensive_zero_error_audit.py deleted with "
        "it: a drifted copy of Checkmate's regexes, hardcoded to p1-p5, red on 36 "
        "false positives, never in CI, whose only function was printing the '60/60 "
        "PAPERS VERIFIED' banner over a fabricated corpus."
    ),
    status="VERIFIED_RESOLVED",
)
print(f"  ERR-079 -> {upd['status'] if upd else 'NOT FOUND'}")
