"""Record the defect classes found during the grounding and citation work.

The point of the ledger is that a defect found once is never rediscovered. These
entries cover three kinds of failure this repository actually produced:

  * manuscript defects (fabricated data, false attributions, missing figures)
  * verification defects (checks that passed things they should have caught, and
    checks that flagged things they should not have)
  * harness defects (tooling that destroyed evidence or measured nothing)

The third kind matters most. A checker that reports green on a broken manuscript
is worse than no checker, because it converts an open question into a false
assurance -- and several entries below are exactly that.

Idempotent; safe to re-run.

    backend/.venv/bin/python scripts/record_session_incidents.py
"""
import sys

sys.path.insert(0, "backend")

from services.error_ledger import ErrorLedgerService  # noqa: E402


RESOLVED = [
    {
        "component": "Manuscript corpus / CitationRelevanceService",
        "stage": "citation_authoring",
        "error_type": "False Attribution",
        "summary": (
            "27 citations named a specific system in prose while the key resolved to "
            "an unrelated paper: 'Vision Transformers' pointed at network topology "
            "self-healing, 'LoRA' at contrastive domain adaptation, 'MM-SafetyBench' "
            "at 'Target search by active particles', 'MetaGPT' at a Hanabi study."
        ),
        "root_cause": (
            "Citation checks verified that a key resolves to a real vault note and "
            "stopped there. Nothing compared the cited work against the sentence "
            "citing it, so a resolvable key pointing at the wrong paper passed."
        ),
        "resolution": (
            "Added CitationRelevanceService and a named-entity resolver. 22 keys "
            "repointed to the paper the prose names; 5 unresolved and reported."
        ),
        "prevention_rule": (
            "A citation adjacent to a named system must resolve to a work whose title "
            "leads with that name. Key resolution alone is not citation verification."
        ),
    },
    {
        "component": "Vault paper corpus",
        "stage": "literature_ingestion",
        "error_type": "Corpus Coverage Gap",
        "summary": (
            "The 448-paper vault did not contain the literature the manuscripts "
            "needed. The best available replacement for a sentence on repair "
            "convergence was a paper on generative AI in business, scoring 0.18."
        ),
        "root_cause": (
            "Ingestion was topic-agnostic, accumulating whatever search returned "
            "rather than what the drafts actually cite."
        ),
        "resolution": (
            "Added scripts/experiments/ingest_literature.py with per-manuscript "
            "queries; 562 papers ingested from arXiv and OpenAlex, vault now 1010."
        ),
        "prevention_rule": (
            "Ingestion must be driven by what the manuscripts cite. A manuscript "
            "whose topic has no matching corpus cannot be honestly cited, and "
            "citation repair must fetch sources rather than reuse unrelated ones."
        ),
    },
    {
        "component": "CitationRelevanceService scoring",
        "stage": "citation_audit",
        "error_type": "Scorer Miscalibration",
        "summary": (
            "Unweighted lexical overlap rated a paper on the card game Hanabi as "
            "relevant to program repair (0.46) because both concern 'agents', while "
            "rating an apt software-engineering citation irrelevant."
        ),
        "root_cause": (
            "Overlap counted every shared token equally, so field-generic vocabulary "
            "('agent', 'multi', 'systems') carried the match. Scoring used title and "
            "tags only, and the tag list contains the ingesting topic slug, which "
            "matches any manuscript on that topic regardless of content."
        ),
        "resolution": (
            "Weighted by inverse document frequency over the corpus, scored against "
            "the cited work's abstract, and normalised by the citing sentence."
        ),
        "prevention_rule": (
            "Lexical relevance must be specificity-weighted. Shared field vocabulary "
            "is not evidence of a topical relationship, and a metric that cannot "
            "separate them will rank generic matches highest."
        ),
    },
    {
        "component": "LaTeXExporterService.convert_markdown_body",
        "stage": "markdown_to_venue_latex",
        "error_type": "Silent Content Loss",
        "summary": (
            "Markdown images were dropped without warning, so all 108 venue packages "
            "contained zero figures despite the drafts referencing them."
        ),
        "root_cause": "The converter had no rule for image syntax; unmatched markup was discarded.",
        "resolution": (
            "Images convert to figure floats with captions and labels, and the build "
            "directory receives the figure files. Nine figures generated from "
            "measurement artifacts by scripts/experiments/figures.py."
        ),
        "prevention_rule": (
            "Every Markdown construct the drafts use must have an explicit converter "
            "rule; anything unhandled must fail loudly rather than be dropped."
        ),
    },
    {
        "component": "ExperimentRecorder.finalize",
        "stage": "measurement_recording",
        "error_type": "Evidence Destroyed By Failed Run",
        "summary": (
            "A network-failed rerun of the p4 census overwrote 10 recorded "
            "measurements with a single row, silently removing the manuscript's "
            "grounding; the provenance gate then reported p4 as 0/6 grounded."
        ),
        "root_cause": (
            "finalize() wrote measurements.jsonl unconditionally, so a run that "
            "collected nothing truncated the file a previous successful run produced."
        ),
        "resolution": (
            "finalize() now refuses to overwrite an existing measurements file with "
            "an empty result set and raises instead."
        ),
        "prevention_rule": (
            "A failed or empty run must never overwrite recorded evidence. Writes to "
            "an evidence store must be refused when the new result set is empty."
        ),
    },
    {
        "component": "Experiment corpora (p1, p3)",
        "stage": "experiment_design",
        "error_type": "Corpus Drift",
        "summary": (
            "p3's mutant count moved from 940 to 943 between identical runs, and p1's "
            "retrieval corpus grew as tooling was added, because both draw their "
            "corpus from this repository's own working tree."
        ),
        "root_cause": (
            "The corpus is the live source tree, which changes as the project is "
            "edited, so a seeded run is only reproducible against a fixed revision."
        ),
        "resolution": (
            "Corpus pinned to a named commit in the manuscript, and reported numbers "
            "regenerated from measurements.jsonl rather than typed by hand."
        ),
        "prevention_rule": (
            "An experiment whose input is the repository must record the revision it "
            "ran against, and the manuscript must state it. Reported values must be "
            "generated from the recorded run, never transcribed."
        ),
    },
    {
        "component": "p9 experiment: deadlock check",
        "stage": "experiment_design",
        "error_type": "Vacuous Verification",
        "summary": (
            "The livelock cycle detector could not fail: its state carried "
            "monotonically increasing counters, making the reachable graph acyclic by "
            "construction, so it would report 'no livelock' for a protocol that livelocks."
        ),
        "root_cause": (
            "Bounding the state space to keep the search finite removed the very "
            "property the search was meant to detect."
        ),
        "resolution": "Remodelled on the turn alone, where the cycle genuinely exists.",
        "prevention_rule": (
            "A verification must be shown capable of failing. Any checker that passes "
            "must be run against a known-bad input that it is required to reject."
        ),
    },
    {
        "component": "p9 experiment: Byzantine simulation",
        "stage": "experiment_design",
        "error_type": "Deterministic Result Reported As Sampled",
        "summary": (
            "Byzantine agreement was computed by a deterministic function of (n, f) "
            "yet reported as 20,000 Monte Carlo trials, implying a sampling "
            "distribution that did not exist."
        ),
        "root_cause": "The round had no stochastic component; repeated trials returned the same value.",
        "resolution": (
            "Modelled per-message delivery probability, which is what makes repeated "
            "trials informative. The measured threshold still lands at floor((n-1)/3)."
        ),
        "prevention_rule": (
            "A trial count may only be reported for a procedure with a genuine random "
            "component. Repeating a deterministic computation is not sampling."
        ),
    },
    {
        "component": "p1 experiment: retrieval evaluation",
        "stage": "experiment_design",
        "error_type": "Ceiling Effect And Tuning On Test",
        "summary": (
            "The first retrieval corpus was small enough that BM25 alone reached 100% "
            "P@5, a ceiling at which no re-ranker can show an effect, and the "
            "diffusion's hyperparameters were selected on the same queries used to "
            "report results."
        ),
        "root_cause": (
            "Corpus size was not checked against baseline saturation, and no held-out "
            "split separated selection from reporting."
        ),
        "resolution": (
            "Corpus widened to 109 modules; hyperparameters selected on a held-out dev "
            "half and reported on 103 unseen queries."
        ),
        "prevention_rule": (
            "Report the baseline's headroom before drawing a comparative conclusion, "
            "and never select a configuration on the split used to report it."
        ),
    },
    {
        "component": "FactCheckerService / ClaimProvenanceService",
        "stage": "release_audit",
        "error_type": "Contradictory Verification",
        "summary": (
            "FactCheckerService flagged p9's measured 0.05 ms as unverified because it "
            "is absent from the literature corpus, blocking all 12 p9 venues, while "
            "the provenance gate reported the same manuscript fully grounded."
        ),
        "root_cause": (
            "Two independent graders judged the same claims against different evidence "
            "sources, and neither knew about the other."
        ),
        "resolution": (
            "FactCheckerService accepts values recorded by the draft's own experiment, "
            "supplied by PublisherReadinessService."
        ),
        "prevention_rule": (
            "Two checks that judge the same property must share their evidence sources. "
            "A disagreement between graders is a defect in the graders, not a verdict."
        ),
    },
    {
        "component": "ClaimProvenanceService extraction",
        "stage": "provenance_audit",
        "error_type": "Extractor False Positives",
        "summary": (
            "The claim extractor read inline maths as currency ('$1 - p_k$' became a "
            "price), 'Mixtral 8x7B' as an eight-fold factor, interval levels ('95% CI') "
            "as findings, and rejected correctly rounded values ('d = 2.13' against a "
            "measured 2.1339). Decimal precision was parsed from '4.39 ms' as five places."
        ),
        "root_cause": (
            "Patterns were written against prose and matched notation, and value "
            "comparison demanded exact equality where manuscripts legitimately round."
        ),
        "resolution": (
            "Currency requires an escaped dollar; factors reject a following digit; "
            "interval levels and inline code spans are skipped; comparison accepts the "
            "claim's own precision; units must agree, not only values."
        ),
        "prevention_rule": (
            "A claim extractor must be validated against notation as well as prose, and "
            "must accept a value stated to fewer significant figures than measured. "
            "Every false positive it produces trains authors to ignore it."
        ),
    },
    {
        "component": "Manuscript structure",
        "stage": "manuscript_authoring",
        "error_type": "Structural Shortfall",
        "summary": (
            "Manuscripts averaged 3,200 words with no appendix, against a measured "
            "reference of 5,182 main-body plus 3,987 appendix words, and lacked the "
            "Analysis-before-Method ordering the reference uses."
        ),
        "root_cause": (
            "No template encoded what a complete paper of this kind contains, so "
            "structure varied per draft and appendices were absent entirely."
        ),
        "resolution": (
            "scripts/experiments/paper_template.py encodes the structure and per-section "
            "budgets measured from arXiv 2604.17215; generate_appendices.py builds "
            "Appendices C, D and E from recorded artifacts."
        ),
        "prevention_rule": (
            "Manuscript completeness must be checked against an explicit section "
            "template with word budgets. Appendix material derived from recorded runs "
            "is the safe way to add length; prose invented to reach a target is not."
        ),
    },
    {
        "component": "LaTeXExporterService author block",
        "stage": "markdown_to_venue_latex",
        "error_type": "Marker Breaks Compilation",
        "summary": (
            "The '[AFFILIATION NOT SET]' placeholder marker followed a '\\\\' line "
            "break, so LaTeX parsed it as an optional length argument and failed with "
            "'Missing number, treated as zero'."
        ),
        "root_cause": (
            "A square-bracketed marker was emitted directly after a line break, where "
            "TeX reads brackets as an optional argument."
        ),
        "resolution": "Marker emitted brace-protected so it cannot be read as an argument.",
        "prevention_rule": (
            "Generated LaTeX must never place a bracketed literal immediately after a "
            "command that accepts an optional argument."
        ),
    },
    {
        "component": "Manuscript rewrite tooling",
        "stage": "manuscript_sync",
        "error_type": "Unsafe Rewrite Operations",
        "summary": (
            "A DOTALL span pattern intended to replace one paragraph matched as far as "
            "the Conclusion's own repeated phrase and would have deleted the Related "
            "Work and Conclusion sections; rewrite scripts were also non-idempotent and "
            "crashed on a second run after consuming their own anchors."
        ),
        "root_cause": (
            "Span replacement was anchored on text that recurs later in the document, "
            "with no bound and no completion sentinel."
        ),
        "resolution": (
            "Patterns bounded to a single line, assert_absent verifies retired claims "
            "are gone before saving, and each rewrite checks a sentinel first."
        ),
        "prevention_rule": (
            "Span replacement must be bounded and verified: assert the retired content "
            "is absent before writing, and make every rewrite idempotent."
        ),
    },
]

OPEN = [
    {
        "component": "Manuscript corpus (p6, p7, p8)",
        "stage": "manuscript_authoring",
        "error_type": "Ungrounded Empirical Claims",
        "summary": (
            "p6 (39 claims), p7 (116) and p8 (85) remain entirely ungrounded. Their "
            "results require VLM fine-tuning and video-model evaluation on hardware "
            "this project does not have."
        ),
        "root_cause": "The claims describe experiments that were never run and cannot be run here.",
        "resolution": (
            "OPEN. p7's formal core is groundable on CPU as p9's was. p6 and p8 need "
            "GPU access or must be reframed with their empirical claims removed."
        ),
        "prevention_rule": (
            "A manuscript must not be drafted with empirical claims the project has no "
            "means of producing. Feasibility of measurement is a drafting precondition."
        ),
        "status": "OPEN_NOT_FIXED",
    },
    {
        "component": "Citation relevance backlog",
        "stage": "citation_audit",
        "error_type": "Unreviewed Weak Citations",
        "summary": (
            "84 citation occurrences remain flagged as having little topical overlap "
            "with the sentence citing them, listed in vault/00_System/CITATION_REVIEW.md."
        ),
        "root_cause": (
            "Lexical scoring cannot decide whether a source supports a claim, and "
            "automatic substitution proposed replacing InstructGPT with a paper on "
            "fracture image captioning."
        ),
        "resolution": (
            "OPEN by design. These need an author decision; automated replacement was "
            "rejected as more dangerous than the defect."
        ),
        "prevention_rule": (
            "Citation relevance scoring triages, it does not decide. Automated citation "
            "replacement is prohibited: a wrong citation is worse than a weak one."
        ),
        "status": "OPEN_NOT_FIXED",
    },
    {
        "component": "Environment / iCloud",
        "stage": "repository_hygiene",
        "error_type": "Credentials In Sync Conflict Copies",
        "summary": (
            "iCloud conflict directories 'Projects 2', 'Projects 3' and 'Projects 4' "
            "each hold a partial ResearchingOS copy; two contain .env files with live "
            "Gemini, Groq, OpenRouter and NVIDIA keys. The venv's pip shebang still "
            "points into 'Projects 2', which is why pip fails and python -m pip is used."
        ),
        "root_cause": "iCloud created conflict copies of a synced project directory containing secrets.",
        "resolution": (
            "OPEN. Reported, not deleted: removing files and rotating keys is the "
            "owner's decision."
        ),
        "prevention_rule": (
            "Secrets must not live inside a cloud-synced working tree. Conflict copies "
            "duplicate them silently, and a stale copy keeps working long enough to "
            "hide the split."
        ),
        "status": "OPEN_NOT_FIXED",
    },
]


def main() -> int:
    ledger = ErrorLedgerService()
    existing = {e.get("summary", "") for e in ledger.data.get("history", [])}

    recorded = 0
    for incident in RESOLVED + OPEN:
        if incident["summary"] in existing:
            continue
        entry = ledger.record_error(**incident)
        marker = "OPEN" if incident.get("status") else "fixed"
        print(f"  {entry['error_id']}  {marker:5}  {incident['error_type']}")
        recorded += 1

    stats = ledger.data["stats"]
    print(f"\nRecorded {recorded} new incident(s).")
    print(f"Ledger: {stats['total_errors_recorded']} incidents, "
          f"{stats['resolved_count']} resolved, {stats.get('open_count', 0)} open, "
          f"{stats['active_prevention_rules']} prevention rules.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
