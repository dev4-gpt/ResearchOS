"""Repoint citations whose key contradicts the name written beside it.

The manuscripts contain passages of the form ``Vision Transformers [[key]]`` where
the key resolves to an unrelated paper -- in that case a study of network topology
self-healing. Others cite "LoRA" pointing at contrastive domain adaptation, and
"MM-SafetyBench" pointing at a paper on active-particle search.

This is a false attribution rather than a weak one: the manuscript asserts that a
named system is described by a source that does not describe it, and a reviewer who
checks a single one of these finds a fabricated reference.

The fix is precise rather than statistical. Each named entity is searched on arXiv
by name, the returned title is required to actually contain the name, the paper is
ingested into the vault, and the citation key is repointed. A name that cannot be
resolved confidently is left alone and reported.

    backend/.venv/bin/python scripts/experiments/fix_miskeyed_citations.py
    backend/.venv/bin/python scripts/experiments/fix_miskeyed_citations.py --apply
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "backend"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.citation_relevance import CitationRelevanceService  # noqa: E402
from manuscript_sync import DRAFTS  # noqa: E402
from ingest_literature import (  # noqa: E402
    fetch_arxiv, fetch_openalex, write_note, slugify,
)


#: "<Named System> [[key]]" -- up to four capitalised words before the citation.
NAMED_CITATION = re.compile(
    r"([A-Z][A-Za-z0-9\-]*(?:[\s\-][A-Z][A-Za-z0-9\-]*){0,3})\s*\[\[([^\]]+)\]\]"
)

#: Names that are ordinary prose rather than a system or paper, so a title
#: mismatch says nothing.
NOT_A_SYSTEM = frozenset({
    "The", "This", "These", "Our", "We", "In", "For", "As", "By", "With", "From",
    "Recent", "Prior", "Such", "Both", "Two", "One", "Section", "Table", "Figure",
    "However", "Moreover", "Furthermore", "Here", "Thus", "Therefore", "While",
    "Although", "Given", "Using", "Based", "It", "They", "Its", "Their",
})


def named_entities(line: str) -> List[Tuple[str, str]]:
    """Extract (name, key) pairs worth checking from one line."""
    out = []
    for match in NAMED_CITATION.finditer(line):
        name = match.group(1).strip()
        key = match.group(2).split(",")[0].strip()
        head = name.split()[-1]
        if name.split()[0] in NOT_A_SYSTEM or len(head) < 4:
            continue
        out.append((name, key))
    return out


def title_matches(name: str, title: str) -> bool:
    """Does this title belong to the paper that introduced the named system?

    Short names must be *named* by the title, not merely contained in it. A
    substring test let "RETRO" resolve to a paper on retro-inverso peptides, which
    would have replaced a wrong citation with a worse one.
    """
    lowered = title.lower().strip()
    target = name.lower()

    # The title must lead with the name, as papers introducing a system almost
    # always do ("QLoRA: Efficient Finetuning of ..."). Accepting the name anywhere
    # in the title resolved "Vision Transformers" to DINO and "Dark Experience
    # Replay" to a follow-up paper: closer than the original error, but still the
    # wrong attribution, and this pass exists to stop exactly that.
    return bool(re.match(rf"^{re.escape(target)}\b", lowered))


def verified(name: str, work: Optional[dict]) -> Optional[dict]:
    """Accept a resolution only when the title genuinely names the system."""
    if work and title_matches(name, work["title"]):
        return work
    return None


def resolve(name: str, cache: Dict[str, Optional[dict]]) -> Optional[dict]:
    """Find the paper actually introducing this name, or None.

    OpenAlex is tried first: arXiv rate-limits hard enough that a bulk pass over
    every name returns 429 for most of them, which would silently look like
    "cannot resolve" rather than "was not asked".
    """
    if name in cache:
        return cache[name]

    works = fetch_openalex(f'"{name}"', 10)
    hit = next((w for w in works if title_matches(name, w["title"])), None)
    if hit is None:
        time.sleep(3.0)
        works = fetch_arxiv(name, 8)
        hit = next((w for w in works if title_matches(name, w["title"])), None)
    cache[name] = hit
    return hit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    service = CitationRelevanceService()
    notes = service.load_notes()
    cache: Dict[str, Optional[dict]] = {}

    fixed = unresolved = 0
    for filename in sorted(os.listdir(DRAFTS)):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(DRAFTS, filename)
        lines = open(path, encoding="utf-8").read().split("\n")
        stem = filename[:-3]
        changed = 0

        for index, line in enumerate(lines):
            for name, key in named_entities(line):
                entry = service._lookup(notes, key)
                if entry is None or title_matches(name, entry["title"]):
                    continue

                correct = resolve(name, cache)
                if correct is None:
                    print(f"  UNRESOLVED {stem[:30]:32} {name!r:28} "
                          f"(key points at {entry['title'][:34]!r})")
                    unresolved += 1
                    continue

                print(f"  REPOINT    {stem[:30]:32} {name!r:28}")
                print(f"             {entry['title'][:44]!r}")
                print(f"          -> {correct['title'][:44]!r}  [{correct['key']}]")
                if args.apply:
                    write_note(correct, slugify(stem)[:70])
                    lines[index] = lines[index].replace(f"[[{key}]]",
                                                        f"[[{correct['key']}]]")
                    changed += 1
                fixed += 1

        if args.apply and changed:
            open(path, "w", encoding="utf-8").write("\n".join(lines))
            print(f"    {stem[:44]}: {changed} citation(s) repointed")

    print(f"\nrepointed={fixed} unresolved={unresolved}")
    if not args.apply:
        print("Dry run. Re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
