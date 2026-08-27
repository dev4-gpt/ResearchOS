"""Record the CI-enforcement and citation-triage findings. Idempotent."""
import sys
sys.path.insert(0, "backend")
from services.error_ledger import ErrorLedgerService

INCIDENTS = [
    {
        "component": "FactCheckerService.validate_numeric_claims",
        "stage": "legacy_audit_chain",
        "error_type": "Grader Accepts Claims On Vocabulary",
        "summary": (
            "A claim was marked grounded if the paragraph containing it mentioned "
            "'table', 'benchmark', 'result', 'finding', 'experiment' -- or contained "
            "a pipe character. '500 enterprise codebases' passed while its only cited "
            "source said 'a conceptual framework only'. Separately, is_non_metric_number "
            "contradicted NUMERIC_PATTERN: the pattern has alternations whose only "
            "purpose is to find 'N = 1000' and '18 months', and the filter discarded "
            "every string containing '=' and every string containing a scale noun, so "
            "the detector went looking for exactly the claims it then threw away."
        ),
        "root_cause": (
            "Two passes written at different times against opposite intentions, and an "
            "escape hatch that approximated 'this looks like a results paragraph' with "
            "a keyword list. Both made the grader lenient in the direction that produces "
            "a green report."
        ),
        "resolution": (
            "Keyword escape hatch removed -- _absolve_measured_claims already does that "
            "job against recorded values instead of vocabulary. The filter no longer "
            "discards sample sizes or scale nouns. Suite is 188 passed, 0 failed; the "
            "two ERR-044 tests pass without being modified."
        ),
        "prevention_rule": (
            "A grader may not accept a claim because of the words near it. If a claim is "
            "ours it is absolved by a recorded measurement; if it is someone else's it is "
            "absolved by the cited source containing it. There is no third category, and "
            "any heuristic that invents one exists to make the report green."
        ),
    },
    {
        "component": "vault/04_Drafts, citation keys",
        "stage": "citation_attribution",
        "error_type": "False Attribution",
        "summary": (
            "22 citations named one work in prose while the key resolved to another. "
            "'Adapter layers' cited GPT-3; 'Paged attention' cited a paper on sparse "
            "autoencoders; 'Byzantine fault tolerance' and 'Personalized PageRank "
            "diffusion' both cited papers on fine-tuning CLIP and on breast cancer "
            "classification; 'Aghajanyan et al.' cited CLUDA. 103 flagged occurrences "
            "were carried by just 30 keys, four of which accounted for 40 -- a small "
            "pool of notes used as generic filler across nine unrelated manuscripts."
        ),
        "root_cause": (
            "The relevance scorer measures vocabulary overlap and reports a weak score, "
            "which reads as 'tenuous citation'. It cannot distinguish tenuous from wrong, "
            "so a false attribution and a foundational citation looked alike, and neither "
            "was ever actioned because no decision was ever recorded."
        ),
        "resolution": (
            "scripts/review_citations.py detects the case that is not a judgement call -- "
            "prose names something the resolved title does not contain -- and removes the "
            "citation, leaving the sentence unattributed. Decisions persist in "
            "citation_decisions.json so the backlog can reach zero. No replacement is "
            "ever proposed (R62). 83 occurrences remain for an author."
        ),
        "prevention_rule": (
            "Naming a work in prose is a claim about that work, and it must match the key "
            "beside it. This is checkable without judgement and belongs in CI. Removing a "
            "false attribution needs no literature search; choosing the right source does, "
            "and stays with the author."
        ),
    },
    {
        "component": ".github/workflows/integrity.yml",
        "stage": "release_enforcement",
        "error_type": "Unenforced Check",
        "summary": (
            "Every integrity check this project built -- the submission gate, the "
            "draft/run agreement check, the test suite -- was run by hand, which is the "
            "same as not being run. The gate had exited non-zero on real defects twice "
            "in one session and nothing would have stopped a commit."
        ),
        "root_cause": "The checks were written as tools, not as gates.",
        "resolution": (
            "A workflow runs the submission gate, resync_manuscripts.py --check, the test "
            "suite and a tracked-sync-conflict-copy check on every push. --check was added "
            "for this: the re-sync pass previously always exited 0. requirements-ci.txt "
            "pins the versions the recorded measurements were produced under and omits the "
            "model-calling dependencies, so no check needs an API key."
        ),
        "prevention_rule": (
            "A check that only runs when someone remembers is not a check. Pin the "
            "dependency versions the recorded results were produced under, and keep the "
            "credentials out: an integrity check that needs a key is one that gets skipped."
        ),
    },
]

ledger = ErrorLedgerService()
seen = {e.get("summary") for e in ledger.data.get("history", [])}
for inc in INCIDENTS:
    if inc["summary"] in seen:
        print(f"  already recorded: {inc['error_type']}")
        continue
    e = ledger.record_error(**inc)
    print(f"  {e['error_id']} [{e['status']}] {e['error_type']}")

for err_id, resolution, status in [
    ("ERR-044",
     "Fixed. Two contradictions: is_non_metric_number discarded the sample sizes and "
     "scale nouns NUMERIC_PATTERN exists to find, and validate_numeric_claims accepted "
     "any claim whose paragraph mentioned 'benchmark' or 'result'. Both removed; the two "
     "failing tests pass unmodified and the suite is 188/188.",
     "VERIFIED_RESOLVED"),
    ("ERR-062",
     "22 of the flagged occurrences were false attributions, not weak citations, and were "
     "removed with the sentence left standing. Decisions now persist in "
     "citation_decisions.json so the list can shrink. 83 remain for an author; automated "
     "replacement is still prohibited and the suggestion block has been deleted from the "
     "report, since it was the thing that had to be refused.",
     "PARTIALLY_RESOLVED"),
]:
    upd = ledger.resolve_error(err_id, resolution=resolution, status=status)
    print(f"  {err_id} -> {upd['status'] if upd else 'NOT FOUND'}")
