"""Record the parallel pipeline audit: Checkmate, ACM output, and test isolation. Idempotent."""
import sys
sys.path.insert(0, "backend")
from services.error_ledger import ErrorLedgerService

INCIDENTS = [
    {
        "component": "CheckmateVerifierService.audit_pdf",
        "stage": "release_audit",
        "error_type": "Audit Of Absence",
        "summary": (
            "Every one of Checkmate's twelve checks looked for a bad substring and "
            "treated its absence as a pass. Nothing asserted the artifact contained a "
            "manuscript. An 8-line PDF whose entire body was 'Things are important. We "
            "studied them. They got better.' plus one fabricated number scored 100.0, "
            "PASSED, APPROVED_FOR_HUMAN_REVIEW -- with real_bibliography reporting '100% "
            "verified real academic publications' for a document containing no references "
            "at all. evidence_grounding returned passed for a report that said 726 of 728 "
            "claims were unbacked, because absent-or-'not_run' was coded as success and "
            "'not_run' is a status fact_checker.py never emits. A separate 85% threshold "
            "certified packages whose own audit had failed: leaked '[Chairman Synthesis]' "
            "meta tags and a fabricated bibliography both scored 91.7 and were approved."
        ),
        "root_cause": (
            "The checks were written to detect known past defects by name rather than to "
            "assert the properties a finished manuscript must have. A check for the absence "
            "of a bad thing cannot see a missing good thing, which is exactly why 96 "
            "packages with zero tables scored 100.0."
        ),
        "resolution": (
            "New artifact_fidelity check: minimum extractable text plus every source "
            "markdown table must be findable in the rendered PDF. evidence_grounding fails "
            "closed on an absent or failing report. The 85% threshold is gone -- "
            "checkmate_passed is now 'no check failed'. Calibrated against all 108 shipped "
            "packages: 108 pass, 0 false positives. 12 new tests, each failing against the "
            "pre-fix code."
        ),
        "prevention_rule": (
            "An audit must assert that the good thing is present, not merely that a known "
            "bad thing is absent, and it must fail when its evidence is missing. A score "
            "threshold that lets a failed check through is not a threshold, it is a waiver."
        ),
    },
    {
        "component": "backend/templates/acmart.cls + LaTeXExporter.compile_pdflatex",
        "stage": "venue_rendering",
        "error_type": "Validated Against A Substitute",
        "summary": (
            "backend/templates/acmart.cls is a 31-line stub that does \\LoadClass{article}, "
            "and compile_pdflatex copies every file in backend/templates/ into the build "
            "directory, where LaTeX resolves it ahead of the real acmart installed at "
            "/usr/local/texlive/2024. Every ACM package this pipeline has produced was "
            "typeset as a two-column article. Measured on the shipped p3 package: 9 pages "
            "under the stub, 16 under real acmart. Page-limit and layout validation for ACM "
            "have therefore never run against ACM's class, and publisher_readiness gates "
            "venue approval on that verdict."
        ),
        "root_cause": (
            "A fallback class added so builds would not fail without acmart installed was "
            "copied unconditionally, so it shadowed the real class once that was available. "
            "Nothing compared the two."
        ),
        "resolution": (
            "OPEN. The ACM author block, abstract ordering and an amssymb/newtxmath clash "
            "are fixed and verified against real acmart. Retiring the stub is not done: it "
            "roughly doubles ACM page counts and is an authoring decision about length "
            "compliance, not a cleanup."
        ),
        "prevention_rule": (
            "A local fallback must never silently outrank the real thing. If a venue's "
            "class is installed, build against it; if a stub is used, the report must say "
            "so, because a page count measured against a substitute is not a page count."
        ),
        "status": "PARTIALLY_RESOLVED",
    },
    {
        "component": "CouncilOrchestrator.__init__",
        "stage": "test_isolation",
        "error_type": "Tests Mutate Project Data",
        "summary": (
            "CouncilOrchestrator hardcoded ContinualMemoryManager() with no path, so it "
            "always wrote to the production vault/harness_memory.json regardless of the "
            "vault_path it was given. test_council.py calls run_research 18 times, and 18 "
            "'test topic' entries were already committed to that tracked file, which had "
            "grown from test runs nobody attributed."
        ),
        "root_cause": (
            "A collaborator was constructed inside the object that uses it, with a "
            "production default, so there was no seam through which a test could redirect "
            "it."
        ),
        "resolution": (
            "An injection seam on the constructor; production default unchanged. Tests pass "
            "tmp_path. An autouse conftest guard redirects any default-path manager and "
            "fails the test if the real file is written, so a future test cannot "
            "reintroduce it. CI now fails if the suite leaves the tree dirty."
        ),
        "prevention_rule": (
            "A test run must leave the working tree byte-identical. Enforce it in CI rather "
            "than trusting it: results that depend on how many times the suite has run are "
            "not results."
        ),
    },
    {
        "component": "papers/ release packages vs vault/04_Drafts",
        "stage": "release_consistency",
        "error_type": "Gate Protects The Source, Not The Artifact",
        "summary": (
            "The submission gate audits the drafts. What a human submits is a PDF under "
            "papers/. Nothing compared them. Every package was built at 22:52 on "
            "2026-08-25 and the drafts were corrected until 00:35 the next morning, so 48 "
            "of 192 built packages contained values no recorded run supports -- p1's "
            "shipped PDFs still reported MRR 0.8701 against 0.8739 over 103 queries, the "
            "numbers from the corpus contaminated with sync-conflict duplicates, whose "
            "headline delta had the opposite sign from the corrected run."
        ),
        "root_cause": (
            "The pipeline's consistency was enforced on the measurements-to-manuscript "
            "edge and simply not modelled on the manuscript-to-artifact edge."
        ),
        "resolution": (
            "scripts/check_release_freshness.py applies the provenance check to the built "
            ".tex and exits non-zero when a package disagrees with its run. Wired into CI."
        ),
        "prevention_rule": (
            "Verify the artifact that ships, not only the source it came from. Every edge "
            "in the pipeline where one representation is derived from another needs a check "
            "that they still agree, or the derived one silently becomes the older claim."
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
    "ERR-046",
    resolution=(
        "The acmart branch now emits \\author, \\affiliation{\\institution{...}\\country{...}} "
        "and \\email for every author, sourced from draft frontmatter through "
        "publisher_readiness, and verified by compiling against the real acmart class and "
        "extracting the PDF text. Two worse defects surfaced alongside it: the abstract was "
        "being dropped from ACM topmatter entirely because acmart requires it before "
        "\\maketitle, and an amssymb/newtxmath \\Bbbk clash made the package fail to compile "
        "against real acmart at all. country: \"USA\" added to all nine drafts, which acmart "
        "requires."
    ),
    status="VERIFIED_RESOLVED",
)
print(f"  ERR-046 -> {upd['status'] if upd else 'NOT FOUND'}")


# --- appended: found while rebuilding the packages the audit had just unblocked ---
LATE = [{
    "component": "Reproducibility table / PublisherReadinessService._recorded_measurements",
    "stage": "run_metadata_consistency",
    "error_type": "Metadata Nobody Projected",
    "summary": (
        "Eight drafts carry a Reproducibility table stating the run's wall-clock "
        "duration, commit, timestamp and measurement count. Those live in "
        "experiment_manifest.json, not measurements.jsonl, so the re-sync pass could "
        "not see them and the provenance gate does not check them -- p3's table "
        "claimed 10.293 s and revision 90967292066d several runs after both stopped "
        "being true, while the gate called the manuscript fully grounded. Once "
        "corrected, FactCheckerService then blocked all 12 venues with 'Unverified "
        "numeric claims: 10.575 s', because it too reads only measurements.jsonl."
    ),
    "root_cause": (
        "Run metadata is recorded evidence but lives in a different file from the "
        "measurements, and every consumer had been written against measurements only. "
        "The second half is ERR-056 recurring: two graders judging one property "
        "against different evidence sources."
    ),
    "resolution": (
        "resync_manuscripts.sync_reproducibility_table projects the manifest into the "
        "table, anchored on each row's label rather than its current value -- which is "
        "what makes it safe to rewrite the commit hash and timestamp as well as the "
        "numbers. _recorded_measurements now also reads the manifest, so the fact "
        "checker and the gate share evidence. p1 and p3 rebuilt: 12/12 publish-ready "
        "under the stricter Checkmate, and the shipped PDFs now carry the corrected "
        "values with none of the stale ones."
    ),
    "prevention_rule": (
        "Evidence is not one file. Any value a manuscript states about its own run "
        "must be projected from the artifact that recorded it, and every grader that "
        "judges grounding must read the same set of artifacts -- otherwise correcting "
        "a value in one place turns into a block in another."
    ),
}]

ledger2 = ErrorLedgerService()
seen2 = {e.get("summary") for e in ledger2.data.get("history", [])}
for inc in LATE:
    if inc["summary"] in seen2:
        print(f"  already recorded: {inc['error_type']}")
    else:
        e = ledger2.record_error(**inc)
        print(f"  {e['error_id']} [{e['status']}] {e['error_type']}")
