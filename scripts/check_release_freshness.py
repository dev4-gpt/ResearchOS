"""Hold the built packages to the same standard as the manuscripts they came from.

The submission gate audits `vault/04_Drafts/*.md`. The thing a human actually
submits is a PDF under `papers/p*/`. Nothing checked that those two agreed, and
they did not: every package under `papers/` was built at 22:52 on 2026-08-25,
while the drafts were corrected until 00:35 the next morning. Reading a shipped
PDF back shows it -- p1's MDPI package reports MRR 0.8701 against 0.8739 and
"unchanged on 93" of 103 queries, which are the numbers produced by a corpus
contaminated with iCloud sync-conflict duplicates (ERR-071). The corrected run
says 0.9119 against 0.9201 on 138 queries, and the contaminated corpus reported
the *opposite sign* for the paper's headline result.

So the gate was protecting the source and not the artifact. Submitting from
`papers/` -- which is what that directory is for -- would have submitted numbers
the gate now rejects, and the gate would have gone on saying PASSED.

This applies the existing provenance check to the built `.tex` instead of the
draft. It is the same question asked of the thing that actually ships: does every
number in this artifact resolve to a recorded measurement? A package that fails
is stale, and the answer is to rebuild it, not to edit it.

    backend/.venv/bin/python scripts/check_release_freshness.py
    backend/.venv/bin/python scripts/check_release_freshness.py --check   # CI
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "backend"))

from services.claim_provenance import ClaimProvenanceService  # noqa: E402

PAPERS = os.path.join(REPO_ROOT, "papers")
DRAFTS = os.path.join(REPO_ROOT, "vault", "04_Drafts")


def draft_stems() -> set:
    return {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(DRAFTS, "*.md"))}


def stem_for(tex_path: str, stems: set) -> str:
    """Which manuscript a package was built from, by longest-prefix filename match.

    Package files are named '<stem>_<VENUE>.tex'. Matching on the longest stem
    that prefixes the filename avoids mis-attributing a package whose stem is
    itself a prefix of another.
    """
    name = os.path.basename(tex_path)[:-4]
    candidates = [s for s in stems if name.startswith(s)]
    return max(candidates, key=len) if candidates else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="exit non-zero if any built package is stale. For CI.")
    parser.add_argument("--limit-per-paper", type=int, default=0,
                        help="only inspect N packages per manuscript (faster spot check)")
    args = parser.parse_args()

    service = ClaimProvenanceService(
        vault_path=os.path.join(REPO_ROOT, "vault"),
        runs_root=os.path.join(REPO_ROOT, "runs"),
    )
    stems = draft_stems()

    tex_files = sorted(glob.glob(os.path.join(PAPERS, "*", "*.tex")))
    if not tex_files:
        print("No built packages under papers/. Nothing to check.")
        return 0

    by_stem: dict = {}
    for path in tex_files:
        stem = stem_for(path, stems)
        if stem:
            by_stem.setdefault(stem, []).append(path)

    print("=== built packages vs recorded measurements ===")
    total = stale = 0
    stale_stems = set()

    for stem in sorted(by_stem):
        paths = by_stem[stem]
        if args.limit_per_paper:
            paths = paths[: args.limit_per_paper]
        measurements = service.load_measurements(f"draft-{stem}")
        if not measurements:
            print(f"  {stem[:50]:50} no recorded run; skipped")
            continue

        worst = 0
        for path in paths:
            total += 1
            text = open(path, encoding="utf-8", errors="replace").read()
            claims = service.extract_claims(text)
            service.classify(claims, measurements)
            bad = [c for c in claims if c.grounding == "UNGROUNDED"]
            if bad:
                stale += 1
                worst = max(worst, len(bad))
                stale_stems.add(stem)

        flag = f"{worst} ungrounded in the worst package" if worst else "clean"
        print(f"  {stem[:50]:50} {len(paths):>3} package(s)   {flag}")

    print(f"\n{stale} of {total} built package(s) contain values no recorded run supports.")

    if stale:
        print("\nThese packages predate the corrections in their manuscripts. The fix is to\n"
              "rebuild them from the current drafts -- never to edit a built .tex, which\n"
              "would put a number into an artifact without changing what produced it.")
        print("Affected manuscripts: " + ", ".join(sorted(stale_stems)))
        if args.check:
            print("\nCHECK FAILED. The submission gate passes on the drafts, but the packages\n"
                  "a human would actually submit disagree with them.")
            return 1
    else:
        print("\nCHECK PASSED. Every built package agrees with its recorded run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
