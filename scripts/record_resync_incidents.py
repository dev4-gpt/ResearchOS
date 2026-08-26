import sys
sys.path.insert(0, "backend")
from services.error_ledger import ErrorLedgerService

INCIDENTS = [
    {
        "component": "p3 draft, Experimental Setup",
        "stage": "manuscript_method_claims",
        "error_type": "Unenforced Method Claim",
        "summary": (
            "p3's setup section stated 'The corpus is pinned at commit `90967292066d`' "
            "while p3_ast_repair.py globbed the working tree. The pin was never "
            "enforced by anything: the named commit was five re-runs old, the same "
            "sentence carried an AST-node count (35,872) that disagreed with the "
            "abstract's (36,032) and with the run's (38,413), and no check compared "
            "any of them."
        ),
        "root_cause": (
            "A claim about method was written as prose rather than generated from the "
            "run manifest, so it could only ever be true at the moment it was typed. "
            "The provenance gate checks quantities, not statements about procedure."
        ),
        "resolution": (
            "The sentence now says what is true -- the corpus is the working tree and "
            "the run manifest records which commit -- rather than naming a pin nothing "
            "implements. Both AST-node counts re-synced from measurements.jsonl."
        ),
        "prevention_rule": (
            "A manuscript may not claim a property of the method that no code enforces. "
            "Either implement the pin and generate the commit from the manifest, or "
            "describe the looser thing that actually happens; a reproducibility claim "
            "is the last place to write something aspirational."
        ),
    },
    {
        "component": "resync_manuscripts.protected_spans",
        "stage": "manuscript_resync",
        "error_type": "Near Miss: Substitution Into Quoted Source",
        "summary": (
            "The first working version of the re-sync pass would have rewritten "
            "'GPT-3, a 175-billion parameter autoregressive language model' to "
            "'172-billion' inside a quoted abstract, because p3 records 175 mutants "
            "for the substitution operator and both are spelled '175'. It would also "
            "have edited the YAML frontmatter's checkmate_score of 100.0 to match an "
            "unrelated syntactic-validity percentage. Caught before any draft was "
            "written, by reading the dry run."
        ),
        "root_cause": (
            "A value-substitution pass treats a manuscript as a bag of numbers. Quoted "
            "source text, citation keys, fenced blocks and frontmatter are all numbers "
            "that belong to someone else."
        ),
        "resolution": (
            "protected_spans() excludes quoted abstracts, wikilink citation keys, "
            "fenced blocks, blockquotes and YAML frontmatter; four tests pin the "
            "behaviour, including the GPT-3 case verbatim. Coarse roundings were also "
            "restricted: 9.86 may no longer match a bare '10'."
        ),
        "prevention_rule": (
            "An automatic rewrite must define where it is forbidden to write before it "
            "defines what it writes. Quoted material is the hard boundary: a wrong "
            "number in our own sentence is an error, and the same number inside a "
            "quotation is fabricated evidence attributed to someone else."
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

upd = ledger.resolve_error(
    "ERR-072",
    resolution=(
        "scripts/experiments/resync_manuscripts.py projects measurements back into the "
        "drafts repeatably. The anchor is a sidecar under vault/04_Drafts/.sync/ holding "
        "the exact literal last written, so it survives its own output: a second run is a "
        "no-op, which is what the one-shot generators could never be. It refuses rather "
        "than guesses -- shared spellings whose claimants have diverged are held for an "
        "author, and metrics it cannot anchor at all (single-digit values) are reported. "
        "All nine drafts now carry sidecars; p1 and p3 are back in agreement with their "
        "runs and the gate passes at 116 claims, 0 ungrounded. 21 tests cover it."
    ),
    status="VERIFIED_RESOLVED",
)
print(f"  ERR-072 -> {upd['status'] if upd else 'NOT FOUND'}")
