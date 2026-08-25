"""Submission gate: provenance audit + venue allocation for every draft.

Run before any release build. It answers two questions the 12-venue matrix cannot:

1. Which quantitative claims in each manuscript are actually backed by evidence?
2. Given that, which single venue should each manuscript be submitted to?

Writes two reports into ``vault/00_System/`` so the answers are versioned alongside
the manuscripts rather than living in a terminal scrollback, and exits non-zero when
any manuscript still carries ungrounded claims — so a CI step or a release script
cannot proceed past a paper that asserts numbers it cannot support.

    backend/.venv/bin/python scripts/run_submission_gate.py [--strategy balanced]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, "backend")

from services.claim_provenance import ClaimProvenanceService  # noqa: E402
from services.latex_exporter import LaTeXExporterService  # noqa: E402
from services.venue_selector import VenueSelectorService  # noqa: E402


DRAFTS_DIR = os.path.join("vault", "04_Drafts")
REPORT_DIR = os.path.join("vault", "00_System")


def _frontmatter_field(markdown: str, field: str) -> str:
    import re
    match = re.search(rf'^{field}:\s*"?(.*?)"?\s*$', markdown, re.MULTILINE)
    return match.group(1).strip() if match else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", default="balanced",
                        choices=["balanced", "max_acceptance", "prestige"])
    parser.add_argument("--max-competitive", type=int, default=2)
    args = parser.parse_args()

    provenance = ClaimProvenanceService()
    selector = VenueSelectorService(args.strategy)
    exporter = LaTeXExporterService()

    print("=== CLAIM PROVENANCE ===")
    reports = provenance.audit_all_drafts(DRAFTS_DIR)

    papers = []
    identity_gaps = []
    for stem, report in sorted(reports.items()):
        markdown = open(os.path.join(DRAFTS_DIR, f"{stem}.md"), encoding="utf-8").read()
        papers.append(
            selector.extract_features(stem, markdown, report.ungrounded, report.total_claims)
        )
        print(f"  {stem[:46]:48} claims={report.total_claims:>4} "
              f"experiment={report.experiment_backed:>3} "
              f"cited={report.citation_backed:>3} ungrounded={report.ungrounded:>4}")

        for field, label in (("affiliation", "affiliation"), ("email", "email")):
            value = _frontmatter_field(markdown, field)
            if exporter.is_placeholder_identity(value):
                identity_gaps.append(f"{stem}: {label} is a placeholder ({value or 'empty'})")

    print("\n=== VENUE ALLOCATION ===")
    allocation = selector.allocate_portfolio(papers, max_competitive=args.max_competitive)
    for stem, entry in sorted(allocation.items()):
        print(f"  {stem[:46]:48} -> {str(entry['venue']):<14} ({entry['tier'] or 'blocked'})")

    os.makedirs(REPORT_DIR, exist_ok=True)
    provenance_md = os.path.join(REPORT_DIR, "CLAIM_PROVENANCE_REPORT.md")
    venue_md = os.path.join(REPORT_DIR, "VENUE_ALLOCATION.md")

    with open(provenance_md, "w", encoding="utf-8") as handle:
        handle.write(provenance.render_markdown(reports))
    with open(venue_md, "w", encoding="utf-8") as handle:
        handle.write(selector.render_markdown(allocation, papers))
    with open(os.path.join(REPORT_DIR, "submission_gate.json"), "w", encoding="utf-8") as handle:
        json.dump(
            {
                "strategy": args.strategy,
                "provenance": {k: v.to_dict() for k, v in reports.items()},
                "allocation": allocation,
                "identity_gaps": identity_gaps,
            },
            handle,
            indent=2,
        )

    total_claims = sum(r.total_claims for r in reports.values())
    ungrounded = sum(r.ungrounded for r in reports.values())
    blocked = [s for s, e in allocation.items() if e["venue"] is None]

    print(f"\nReports written to {REPORT_DIR}/")
    print(f"Claims: {total_claims} total, {ungrounded} ungrounded "
          f"({(total_claims - ungrounded) / total_claims * 100:.1f}% grounded)"
          if total_claims else "Claims: none found")

    if identity_gaps:
        print(f"\nIdentity gaps ({len(identity_gaps)}):")
        for gap in identity_gaps[:12]:
            print(f"  - {gap}")

    if ungrounded or blocked:
        print(
            f"\nGATE: BLOCKED. {ungrounded} claim(s) have no recorded artifact; "
            f"{len(blocked)} manuscript(s) have no eligible venue.\n"
            "Ground them (record measurements with artifacts in "
            "runs/<run_id>/measurements.jsonl), attribute them to a cited source, "
            "or remove them."
        )
        return 1

    print("\nGATE: PASSED. Every quantitative claim traces to evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
