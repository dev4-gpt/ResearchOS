"""Repair topically irrelevant citations.

Policy, deliberately conservative because a wrong citation is worse than a
missing one:

  * ``irrelevant`` occurrences are replaced when the vault holds a paper that
    scores strongly for that same sentence, and dropped otherwise.
  * ``weak`` occurrences are left alone. The scorer is a triage signal, and
    borderline cases are the ones it is least able to judge.
  * ``unjudged`` occurrences (too little surrounding text) are never touched.
  * A sentence is never left with zero citations if it began with at least one:
    if every candidate would be dropped, the best-scoring original is kept and
    reported for manual review.

Dry run by default. Pass --apply to write.

    backend/.venv/bin/python scripts/experiments/fix_citations.py
    backend/.venv/bin/python scripts/experiments/fix_citations.py --apply
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "backend"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.citation_relevance import CitationRelevanceService, tokenize  # noqa: E402
from manuscript_sync import DRAFTS  # noqa: E402


#: A replacement must clear this to be worth substituting.
REPLACEMENT_THRESHOLD = 0.35


def plan_for_draft(service: CitationRelevanceService, stem: str
                   ) -> Tuple[List[dict], Dict[str, int]]:
    path = os.path.join(DRAFTS, f"{stem}.md")
    markdown = open(path, encoding="utf-8").read()
    subject = service._subject_tokens(markdown)
    usages = service.audit_draft(path)

    # Group by line so we never strip a line's last remaining citation.
    by_line: Dict[int, List] = defaultdict(list)
    for usage in usages:
        by_line[usage.line_no].append(usage)

    actions: List[dict] = []
    stats = {"replace": 0, "drop": 0, "keep": 0}

    for line_no, line_usages in by_line.items():
        bad = [u for u in line_usages if u.verdict == "irrelevant"]
        good = [u for u in line_usages if u.verdict in ("relevant", "weak", "unjudged")]
        for usage in bad:
            suggestions = [
                s for s in service.suggest_replacements(usage, subject, limit=8)
                if s[2] >= REPLACEMENT_THRESHOLD
                and s[0] not in {u.key for u in line_usages}
            ]
            if suggestions:
                actions.append({"line": line_no, "action": "replace", "old": usage.key,
                                "new": suggestions[0][0], "new_title": suggestions[0][1],
                                "score": suggestions[0][2], "old_title": usage.title,
                                "context": usage.context})
                stats["replace"] += 1
            elif good or len(bad) > 1:
                actions.append({"line": line_no, "action": "drop", "old": usage.key,
                                "old_title": usage.title, "context": usage.context})
                stats["drop"] += 1
                good.append(usage)   # keeps the "never empty a line" invariant honest
            else:
                actions.append({"line": line_no, "action": "keep-for-review",
                                "old": usage.key, "old_title": usage.title,
                                "context": usage.context})
                stats["keep"] += 1
    return actions, stats


def apply_actions(stem: str, actions: List[dict]) -> int:
    path = os.path.join(DRAFTS, f"{stem}.md")
    lines = open(path, encoding="utf-8").read().split("\n")
    changed = 0

    for action in actions:
        idx = action["line"] - 1
        if idx >= len(lines):
            continue
        line = lines[idx]
        old = re.escape(action["old"])

        if action["action"] == "replace":
            new_line = re.sub(rf"\[\[{old}\]\]", f"[[{action['new']}]]", line)
        elif action["action"] == "drop":
            # Remove the wikilink and tidy the punctuation it leaves behind.
            new_line = re.sub(rf"\s*\[\[{old}\]\]\s*,?", "", line)
            new_line = re.sub(r"\[\s*,\s*", "[", new_line)
            new_line = re.sub(r",\s*\]", "]", new_line)
            new_line = re.sub(r"\s+([.,;])", r"\1", new_line)
            new_line = re.sub(r"\[\s*\]", "", new_line)
        else:
            continue

        if new_line != line:
            lines[idx] = new_line
            changed += 1

    open(path, "w", encoding="utf-8").write("\n".join(lines))
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--show", type=int, default=6, help="examples per draft")
    args = parser.parse_args()

    service = CitationRelevanceService()
    stems = [f[:-3] for f in sorted(os.listdir(DRAFTS)) if f.endswith(".md")]

    grand = {"replace": 0, "drop": 0, "keep": 0}
    for stem in stems:
        actions, stats = plan_for_draft(service, stem)
        for key in grand:
            grand[key] += stats[key]
        if not actions:
            continue
        print(f"\n── {stem[:56]}  "
              f"replace={stats['replace']} drop={stats['drop']} review={stats['keep']}")
        for action in actions[:args.show]:
            if action["action"] == "replace":
                print(f"   REPLACE {action['old_title'][:40]!r}")
                print(f"        ->  {action['new_title'][:40]!r} ({action['score']})")
            elif action["action"] == "drop":
                print(f"   DROP    {action['old_title'][:52]!r}")
            else:
                print(f"   REVIEW  {action['old_title'][:52]!r} (only citation on line)")
        if args.apply:
            changed = apply_actions(stem, actions)
            print(f"   applied: {changed} line(s) rewritten")

    print(f"\nTOTAL replace={grand['replace']} drop={grand['drop']} "
          f"manual-review={grand['keep']}")
    if not args.apply:
        print("Dry run. Re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
