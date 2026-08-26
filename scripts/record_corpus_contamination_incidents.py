"""Record the 2026-08-26 corpus-contamination and re-sync incidents.

Idempotent: each incident is keyed by its summary, so re-running will not
duplicate entries or renumber the prevention rules.

    backend/.venv/bin/python scripts/record_corpus_contamination_incidents.py
"""
import sys

sys.path.insert(0, "backend")

from services.error_ledger import ErrorLedgerService  # noqa: E402


INCIDENTS = [
    {
        "component": "p1_symbol_graph_retrieval.build_corpus / p3_ast_repair",
        "stage": "experiment_corpus_construction",
        "error_type": "Contaminated Experimental Corpus",
        "summary": (
            "Four iCloud sync-conflict duplicates ('<stem> 2.py') were admitted to the "
            "p1 and p3 corpora as if they were source modules. They supplied 9 of the "
            "15 duplicate top-level symbol definitions in p1's symbol graph, and one "
            "docstring query took its gold answer from a stale copy that no other "
            "module references, so PPR was scored as a rank-1 miss for routing to the "
            "real module. Removing them reverses the sign of p1's headline delta: on "
            "the same working tree the contaminated corpus reports diffusion improves "
            "MRR (delta=+0.0005, p=0.987) and the cleaned corpus reports it does not "
            "(delta=-0.0040, p=0.891)."
        ),
        "root_cause": (
            "The corpus globs excluded .venv and node_modules but nothing else, and a "
            "sync-conflict copy is a syntactically valid Python file, so every filter "
            "in the pipeline treated it as real source."
        ),
        "resolution": (
            "harness.is_sync_conflict_copy() added and applied in both corpus builders; "
            "p1 and p3 re-run against the cleaned corpus. The conclusion is unchanged "
            "in substance -- neither delta is close to significant -- but the direction "
            "the manuscript reported was an artifact of duplicate files."
        ),
        "prevention_rule": (
            "An experiment that draws its corpus from a working tree must state and "
            "enforce what a corpus member is. A near-duplicate admitted as a document "
            "double-counts its symbols and can supply a gold answer the rest of the "
            "corpus contradicts; when the measured effect is small, corpus hygiene "
            "decides the sign of the result."
        ),
    },
    {
        "component": "rewrite_p1_p2_p4 / generate_appendices / ManuscriptEditor",
        "stage": "manuscript_generation",
        "error_type": "Non-Idempotent Generation",
        "summary": (
            "Every manuscript generator is one-shot. ManuscriptEditor.already_rewritten "
            "skips a draft whose sentinel is present because the rewrites consume their "
            "own anchors, so after p1 and p3 were re-run there was no supported path to "
            "bring the drafts back into agreement with measurements.jsonl: rewrite_p1_p2_p4, "
            "generate_appendices and analysis_pass all reported 'already rewritten, "
            "skipping' while the drafts still carried the superseded values."
        ),
        "root_cause": (
            "Generation was designed as a one-time migration off fabricated numbers "
            "rather than as a repeatable projection from measurements to prose, so the "
            "anchors it needs are destroyed by its own first run."
        ),
        "resolution": (
            "OPEN. The submission gate caught the divergence -- 17 claims went UNGROUNDED "
            "and p1 and p3 were demoted to arXiv -- so nothing shipped stale. The fix is "
            "an idempotent re-sync pass with anchors that survive rewriting; that is an "
            "authoring decision and was not made unilaterally."
        ),
        "prevention_rule": (
            "A generator that projects recorded data into prose must be re-runnable "
            "against changed data. If its anchors do not survive its own output, the "
            "manuscript can only ever be correct for the run that first produced it, "
            "and re-running an experiment silently desynchronises the paper."
        ),
        "status": "OPEN_NOT_FIXED",
    },
]


def main() -> int:
    ledger = ErrorLedgerService()
    seen = {e.get("summary") for e in ledger.data.get("history", [])}
    for incident in INCIDENTS:
        if incident["summary"] in seen:
            print(f"  already recorded: {incident['error_type']}")
            continue
        entry = ledger.record_error(**incident)
        print(f"  {entry['error_id']} [{entry['status']}] {entry['error_type']}")

    updated = ledger.resolve_error(
        "ERR-063",
        resolution=(
            "Conflict directories 'Projects 2' and 'Projects 4' moved to the Trash after "
            "confirming their only unique content was two .env files and one whitespace-"
            "only variant of citation_graph.py. The four API keys they held hash-match the "
            "live .env, so they are current credentials and still require rotation by the "
            "owner -- that part remains open. 'Projects 3' is empty and was left in place. "
            "Six conflict copies committed inside the repository remain tracked because "
            "p1 and p3 recorded measurements against them; see the corpus-contamination "
            "entry."
        ),
        status="PARTIALLY_RESOLVED",
    )
    print(f"  ERR-063 -> {updated['status'] if updated else 'NOT FOUND'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
