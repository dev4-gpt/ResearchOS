"""Record the 2026-08-25 export and integrity incidents in the system error ledger.

Idempotent: each incident is keyed by its summary, so re-running will not duplicate
entries or renumber the prevention rules.

Run from the repository root:

    backend/.venv/bin/python scripts/record_provenance_incidents.py
"""
import sys

sys.path.insert(0, "backend")

from services.error_ledger import ErrorLedgerService  # noqa: E402


INCIDENTS = [
    {
        "component": "LaTeXExporterService.convert_markdown_body",
        "stage": "markdown_to_venue_latex",
        "error_type": "Silent Content Loss",
        "summary": (
            "ASCII box-art filter '^[|\\+].*[|\\+]$' deleted every Markdown table row "
            "before the booktabs builder ran, so 96 of 108 venue packages shipped "
            "'Table N:' captions with no table anywhere in the document."
        ),
        "root_cause": (
            "The filter intended to strip ASCII diagrams matched any line starting and "
            "ending with a pipe, which is exactly the shape of a Markdown table row. It "
            "ran in step 2; the table builder runs in step 10 and found nothing left."
        ),
        "resolution": (
            "Narrowed the filter to '^\\+.*\\+$' plus a '|=== |' rule form. Verified 41 "
            "tables across 9 drafts now reach the PDFs."
        ),
        "prevention_rule": (
            "Content-stripping regexes must never match a construct the converter is "
            "also expected to render. Any filter using '|' or '+' anchors must be "
            "asserted against a Markdown table fixture before merge."
        ),
    },
    {
        "component": "LaTeXExporterService.convert_markdown_body",
        "stage": "markdown_to_venue_latex",
        "error_type": "Table Header Loss",
        "summary": (
            "Deleting the Markdown alignment row '|:---|:---:|' left a blank line that "
            "split the table, so the header row was dropped and the first data row was "
            "typeset as the header."
        ),
        "root_cause": (
            "The table builder flushes on any non-table line. An emptied separator line "
            "reads as a flush boundary, producing a one-row fragment (discarded for "
            "having fewer than two rows) followed by a headerless second table."
        ),
        "resolution": (
            "Alignment rows are left in place for the builder, which skips them itself "
            "via its '---' check."
        ),
        "prevention_rule": (
            "Never delete a line that a later line-oriented parser uses as an in-block "
            "delimiter; let the owning parser skip it."
        ),
    },
    {
        "component": "LaTeXExporterService.convert_markdown_body",
        "stage": "list_parsing",
        "error_type": "Emphasis Corruption",
        "summary": (
            "The '1)-bullet-artifact' stripper consumed one asterisk of '**Term**:', so "
            "every contributions and metrics list rendered as "
            "\\textit{Term\\textbf{: body}}."
        ),
        "root_cause": (
            "The character class [bullet|*] matched a single '*' that was in fact the "
            "first half of a bold delimiter. The unbalanced remainder was then 'repaired' "
            "by the step 11 balancer, which appended further asterisks."
        ),
        "resolution": (
            "Bullet match tightened to '(?:bullet|\\*(?!\\*))' so a bold run is never "
            "split. Verified 0 mangled emphasis spans across all 9 drafts."
        ),
        "prevention_rule": (
            "Any single-'*' match in Markdown processing must carry a (?!\\*) lookahead "
            "and a (?<!\\*) lookbehind so bold delimiters are never partially consumed."
        ),
    },
    {
        "component": "LaTeXExporterService._emit_booktabs_table",
        "stage": "table_rendering",
        "error_type": "Unconverted Markup",
        "summary": (
            "Bold cell values reached the PDF as literal '**47.2**' because step 11 holds "
            "every table environment aside as protected math and restores it verbatim."
        ),
        "root_cause": (
            "Emphasis conversion runs after table construction but skips table bodies by "
            "design, leaving no stage that converts markup inside cells."
        ),
        "resolution": (
            "Cell-level emphasis conversion moved into the table builder itself. Verified "
            "0 PDFs containing literal '**'."
        ),
        "prevention_rule": (
            "When a later pass protects a region from transformation, that region's own "
            "builder owns every transformation the region needs."
        ),
    },
    {
        "component": "LaTeXExporterService._emit_booktabs_table",
        "stage": "table_rendering",
        "error_type": "Layout Overflow",
        "summary": (
            "Generated tabulars used a bare 'l'*N preamble with no width control and "
            "overflowed the text column (measured 614pt in a 612pt page); captions were "
            "loose bold paragraphs rather than \\caption."
        ),
        "root_cause": (
            "The builder emitted a fixed left-aligned preamble regardless of column count "
            "or venue column width, and had no concept of a caption."
        ),
        "resolution": (
            "Shrink-only \\resizebox clamp, numeric-column centring, and promotion of the "
            "preceding '**Table N: ...**' line into a real \\caption with the manual "
            "number stripped."
        ),
        "prevention_rule": (
            "Every generated float must be clamped to \\columnwidth and carry a real "
            "\\caption; verify by asserting no text block exceeds the page text width."
        ),
    },
    {
        "component": "LaTeXExporterService.sanitize_latex",
        "stage": "sanitization",
        "error_type": "Fatal Compile Error",
        "summary": (
            "Unmapped Unicode maths glyphs (U+2082, U+00D7, U+2212) inside table cells "
            "aborted compilation once tables stopped being discarded."
        ),
        "root_cause": (
            "The character map covered typographic quotes and box drawing but not maths "
            "glyphs. These occur almost exclusively in table cells, so the gap stayed "
            "latent for as long as tables were being deleted."
        ),
        "resolution": (
            "Added a mode-aware _MATH_GLYPHS map applied inside and outside math regions, "
            "ordered after underscore escaping so subscripts are not re-escaped."
        ),
        "prevention_rule": (
            "Unicode maps must be applied mode-aware ($...$ vs text) and ordered after "
            "escaping passes that would corrupt the inserted TeX."
        ),
    },
    {
        "component": "LaTeXExporterService.sanitize_latex",
        "stage": "sanitization",
        "error_type": "Math Mode Runaway",
        "summary": (
            "A single unescaped currency '$' in a 'Cost ($)' header opened a math run "
            "that swallowed the rest of the table row, breaking all 12 p1 builds."
        ),
        "root_cause": (
            "The inline-math split pattern allowed a run to span newlines and cell "
            "boundaries, and residual unpaired '$' in text regions was never escaped."
        ),
        "resolution": (
            "Inline math may no longer span '\\n' or '|', and any '$' surviving in a "
            "non-math region is escaped before the '<'/'>' rules add math shifts."
        ),
        "prevention_rule": (
            "After splitting out genuine math regions, every remaining '$' is literal and "
            "must be escaped; inline math must not span line or cell boundaries."
        ),
    },
    {
        "component": "CheckmateVerifierService + PublisherReadinessService",
        "stage": "release_audit",
        "error_type": "False Green Audit",
        "summary": (
            "The audit reported checkmate_score 100.0 and 'Deep Audit Verification: "
            "108/108 PASSED - ZERO DEFECTS' on manuscripts where every table was missing, "
            "and again in a run where p1 compiled 0 of its 12 venues."
        ),
        "root_cause": (
            "The audit checks section numbering, abstract shape, citation-key resolution "
            "and TeX balance. It never checks that floats referenced in prose exist, and "
            "the final banner is not gated on per-paper compile success."
        ),
        "resolution": (
            "Recorded as a standing caveat; per-paper 'ready=N/12' is the trustworthy "
            "signal. Independent verification now counts \\begin{tabular} in the .tex and "
            "extracts PDF text before any release is believed."
        ),
        "prevention_rule": (
            "A release audit must fail when a manuscript references a float it does not "
            "contain, and the aggregate banner must be gated on every per-paper compile "
            "succeeding. Never report an aggregate pass that a per-item result contradicts."
        ),
    },
    {
        "component": "ClaimProvenanceService",
        "stage": "manuscript_authoring",
        "error_type": "Ungrounded Empirical Claim",
        "summary": (
            "726 of 728 quantitative claims across the 9 manuscripts have no recorded "
            "artifact: N=500, 47.2% DRR, p<0.001 and Cohen's d=1.14 on 'SWE-bench-"
            "Enterprise', which is not a public benchmark and which no run in runs/ "
            "produced."
        ),
        "root_cause": (
            "No stage bound a numeric claim to evidence. Manuscript text was generated "
            "with plausible statistics and every downstream check treated it as given."
        ),
        "resolution": (
            "Added the ClaimProvenanceService gate: claims resolve to EXPERIMENT (matching "
            "measurement with artifact + sha256 in runs/<run_id>/measurements.jsonl), "
            "CITATION (attributed to a resolvable source), or UNGROUNDED. Peer-reviewed "
            "venues are blocked while any UNGROUNDED claim remains."
        ),
        "prevention_rule": (
            "Every quantitative claim must resolve to a recorded artifact or an explicit "
            "attribution before the manuscript may be built for any peer-reviewed venue. "
            "Publishing an unmeasured number as a measurement is misconduct, not a "
            "formatting defect."
        ),
    },
    {
        "component": "LaTeXExporterService author block",
        "stage": "markdown_to_venue_latex",
        "error_type": "Placeholder Identity Shipped",
        "summary": (
            "All 108 packages carried affiliation 'Institute for Advanced AI Systems & "
            "Empirical Software Engineering' and email 'researcher@institute.org', "
            "neither of which is a real association."
        ),
        "root_cause": (
            "The placeholder was set in draft frontmatter and read as filled-in, so no "
            "check distinguished it from a real value."
        ),
        "resolution": (
            "Added is_placeholder_identity(); a placeholder now types as "
            "'[AFFILIATION NOT SET]' in the PDF instead of asserting a false institution."
        ),
        "prevention_rule": (
            "Author identity fields must be validated against a placeholder list and fail "
            "visibly in the typeset output. Never emit a plausible-looking default for an "
            "unset identity field."
        ),
    },
    {
        "component": "LaTeXExporterService.derive_keywords",
        "stage": "markdown_to_venue_latex",
        "error_type": "Non-Distinct Metadata",
        "summary": (
            "All nine manuscripts carried the identical hardcoded keyword line "
            "'Generative AI, Empirical Evaluation, AI Systems, Enterprise Operations, "
            "Systematic Review.'"
        ),
        "root_cause": "The keyword block was a literal string in the venue template branch.",
        "resolution": (
            "Keywords are derived per manuscript from title terms first, then distinctive "
            "body terms, excluding generic words and citation-key fragments."
        ),
        "prevention_rule": (
            "Per-manuscript metadata (keywords, index terms) must be derived from that "
            "manuscript's own content; identical metadata across drafts is a defect."
        ),
    },
    {
        "component": "VenueSelectorService",
        "stage": "venue_targeting",
        "error_type": "Duplicate Submission Risk",
        "summary": (
            "Draft frontmatter recorded publisher_best_venues as all 12 venues at once, "
            "presenting concurrent submission to IEEE, NeurIPS, ICML, CVPR and ACL as the "
            "intended workflow."
        ),
        "root_cause": (
            "The 12-venue build matrix is a formatting capability, but nothing in the "
            "pipeline distinguished 'can be typeset for' from 'should be submitted to'."
        ),
        "resolution": (
            "Added VenueSelectorService, which allocates exactly one venue per manuscript "
            "from provenance eligibility, scope fit, length fit and portfolio spread, and "
            "refuses index-only and unverifiable venues."
        ),
        "prevention_rule": (
            "Exactly one venue per manuscript may be marked as a submission target. "
            "Simultaneous submission is prohibited by every venue in the matrix, so a "
            "multi-venue build must be labelled formatting-only."
        ),
    },
]


# Defects found but NOT fixed. They are recorded as OPEN so the manual stops
# claiming a clean bill of health it has not earned.
OPEN_DEFECTS = [
    {
        "component": "FactCheckerService.validate_numeric_claims",
        "stage": "fact_check",
        "error_type": "Broken Claim Detection",
        "summary": (
            "Numeric claim detection under-counts and returns no unverified claims: "
            "tests/test_fact_checker.py::test_validate_numeric_claims finds 1 claim "
            "where 2 are asserted, and test_fact_checker_catches_unsupported_scale_"
            "claims gets an empty unverified_claims list for '500 enterprise codebases'."
        ),
        "root_cause": (
            "Not yet diagnosed. Both tests fail identically on an unmodified tree, so "
            "the regression predates the 2026-08-25 export work."
        ),
        "resolution": (
            "OPEN. ClaimProvenanceService covers the same ground for the release gate, "
            "so this is not release-blocking, but the two failing tests must be fixed "
            "or the service retired rather than left silently returning empty results."
        ),
        "prevention_rule": (
            "A verification service that returns an empty finding list must be "
            "distinguishable from one that found nothing wrong. Fact-check and audit "
            "services require tests asserting they detect known-bad input."
        ),
        "status": "OPEN_NOT_FIXED",
    },
    {
        "component": "Manuscript corpus (vault/04_Drafts)",
        "stage": "manuscript_authoring",
        "error_type": "Content Gaps",
        "summary": (
            "All 9 manuscripts are 3,100-5,300 words against an 8,000-14,000 word "
            "specification, carry 11-21 citations against a 15-30+ requirement with "
            "several topically irrelevant, and contain zero figures."
        ),
        "root_cause": (
            "Drafting produced structurally complete but thin manuscripts, and no gate "
            "checked length, citation relevance or figure presence."
        ),
        "resolution": (
            "OPEN. Requires manuscript rewriting, not a pipeline fix. VenueSelectorService "
            "now scores length fit and flags under-built drafts, but does not remediate."
        ),
        "prevention_rule": (
            "Manuscript readiness must assert word count against the venue target, "
            "citation count and topical relevance of each citation, and at least one "
            "figure, before a draft is marked publisher-ready."
        ),
        "status": "OPEN_NOT_FIXED",
    },
    {
        "component": "LaTeXExporterService ACM template branch",
        "stage": "markdown_to_venue_latex",
        "error_type": "Missing Author Metadata",
        "summary": (
            "The ACM (acmart) branch emits only the first author's name, with no "
            "\\affiliation and no email, so ACM builds silently drop author metadata "
            "that acmart requires."
        ),
        "root_cause": (
            "The ACM branch was written with a minimal top matter block and never "
            "extended when affiliation handling was added to the other venues."
        ),
        "resolution": "OPEN. Needs a proper acmart \\author/\\affiliation block.",
        "prevention_rule": (
            "Every venue branch must emit the full author block that venue's document "
            "class requires; a branch that omits metadata must fail its venue contract "
            "test rather than compile quietly."
        ),
        "status": "OPEN_NOT_FIXED",
    },
]


def main() -> int:
    ledger = ErrorLedgerService()
    existing = {entry.get("summary", "") for entry in ledger.data.get("history", [])}

    recorded = 0
    for incident in INCIDENTS + OPEN_DEFECTS:
        if incident["summary"] in existing:
            continue
        entry = ledger.record_error(**incident)
        print(f"  {entry['error_id']}  {entry['prevention_rule'].split(':')[0]}  "
              f"{incident['error_type']}")
        recorded += 1

    summary = ledger.get_ledger_summary()
    print(f"\nRecorded {recorded} new incident(s).")
    print(f"Ledger now holds {len(ledger.data['history'])} incidents "
          f"and {len(summary['prevention_rules'])} prevention rules.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
