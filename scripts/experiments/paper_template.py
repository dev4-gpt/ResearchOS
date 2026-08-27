"""The house paper template, derived by measuring a reference paper.

Structure and length are taken from Bach et al., "Continual Safety Alignment via
Gradient-Based Sample Selection" (arXiv 2604.17215), measured rather than guessed:

    main body      5,182 words over 9 pages   (Introduction -> Conclusion)
    references     ~1,373 words
    appendices A-F 3,987 words over 7 pages
    total          10,542 words, 18 pages

Two properties of that paper drive this template.

First, the ordering. An **Analysis** section comes *before* the Method: the paper
establishes empirically which samples cause drift, and only then proposes a method
that follows from the finding. That is the same discipline the provenance gate
enforces -- measure, then claim -- so it suits this repository's manuscripts.

Second, where the weight sits. Related Work and Limitations live in the appendix,
ACL-style, leaving the main body for the argument. Our manuscripts average 3,200
words with no appendix at all, so the shortfall is mostly appendix material:
experimental setup, methodology detail, and the results that did not fit a main
table. All of that is derivable from recorded artifacts rather than written from
imagination, which is why it is safe to generate.
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manuscript_sync import DRAFTS  # noqa: E402


@dataclass(frozen=True)
class SectionSpec:
    """One expected section, with the word budget measured from the reference."""

    key: str
    heading: str
    target_words: int
    appendix: bool = False
    #: Alternative headings our manuscripts already use for the same role.
    aliases: Tuple[str, ...] = ()

    def matches(self, heading: str) -> bool:
        lowered = heading.lower()
        candidates = (self.heading.lower(),) + tuple(a.lower() for a in self.aliases)
        return any(c in lowered for c in candidates)


#: Word budgets are the reference paper's own section lengths, rounded.
MAIN_BODY: Tuple[SectionSpec, ...] = (
    SectionSpec("abstract", "Abstract", 260, aliases=("executive abstract",)),
    SectionSpec("introduction", "Introduction", 900,
                aliases=("introduction & research scope", "introduction and")),
    SectionSpec("background", "Background", 1000,
                aliases=("theoretical foundations", "theoretical formulations",
                         "formal", "preliminaries", "scaling law theory")),
    SectionSpec("analysis", "Analysis", 900,
                aliases=("empirical analysis", "what we observe", "motivating")),
    SectionSpec("method", "Method", 900,
                aliases=("architecture", "framework", "protocol", "system")),
    SectionSpec("experiments", "Experiments", 1000,
                aliases=("empirical results", "quantitative results",
                         "verification results", "experimental protocol",
                         "simulation methodology", "review methodology")),
    SectionSpec("conclusion", "Conclusion", 320),
)

APPENDICES: Tuple[SectionSpec, ...] = (
    SectionSpec("related_work", "Appendix A: Related Work", 900, appendix=True,
                aliases=("related work",)),
    SectionSpec("extended_background", "Appendix B: Extended Background", 700,
                appendix=True, aliases=("extended background",)),
    SectionSpec("extended_setup", "Appendix C: Extended Experimental Setup", 700,
                appendix=True, aliases=("extended experimental setup",)),
    SectionSpec("methodology", "Appendix D: Methodology Detail", 600,
                appendix=True, aliases=("methodology detail", "algorithmic detail")),
    SectionSpec("additional_results", "Appendix E: Additional Results", 800,
                appendix=True, aliases=("additional results",
                                        "additional experimental results")),
    SectionSpec("limitations", "Appendix F: Limitations and Future Work", 500,
                appendix=True, aliases=("limitations", "threats to validity",
                                        "future work", "future research")),
)

ALL_SECTIONS = MAIN_BODY + APPENDICES

REFERENCE = {
    "main_body_words": 5182,
    "appendix_words": 3987,
    "total_words": 10542,
    "pages": 18,
    "source": "arXiv 2604.17215 (Bach et al.)",
}


@dataclass
class Conformance:
    stem: str
    words: int
    present: List[str]
    missing: List[str]
    main_body_words: int
    appendix_words: int

    @property
    def main_gap(self) -> int:
        return max(0, REFERENCE["main_body_words"] - self.main_body_words)

    @property
    def appendix_gap(self) -> int:
        return max(0, REFERENCE["appendix_words"] - self.appendix_words)


def split_sections(markdown: str) -> List[Tuple[str, str]]:
    """Return [(heading, body)] for level-2 headings."""
    body = re.sub(r"^---[\s\S]*?\n---\n", "", markdown)
    parts = re.split(r"^##\s+(.+)$", body, flags=re.MULTILINE)
    out: List[Tuple[str, str]] = []
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i + 1]))
    return out


def is_appendix(heading: str) -> bool:
    return bool(re.match(r"^\s*(appendix\b|[A-F]\s*[:.]\s)", heading, re.IGNORECASE))


def assess(stem: str) -> Conformance:
    path = os.path.join(DRAFTS, f"{stem}.md")
    markdown = open(path, encoding="utf-8").read()
    sections = split_sections(markdown)

    present, main_words, appendix_words = [], 0, 0
    for heading, text in sections:
        count = len(re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text).split())
        if is_appendix(heading):
            appendix_words += count
        else:
            main_words += count
        for spec in ALL_SECTIONS:
            if spec.matches(heading) and spec.key not in present:
                present.append(spec.key)

    missing = [s.key for s in ALL_SECTIONS if s.key not in present]
    total = len(re.sub(r"^---[\s\S]*?\n---\n", "", markdown).split())
    return Conformance(stem, total, present, missing, main_words, appendix_words)


def main() -> int:
    stems = [f[:-3] for f in sorted(os.listdir(DRAFTS)) if f.endswith(".md")]
    print(f"Template from {REFERENCE['source']}: "
          f"{REFERENCE['main_body_words']} main + {REFERENCE['appendix_words']} appendix "
          f"= {REFERENCE['total_words']} words\n")
    print(f"{'manuscript':44}{'main':>6}{'+gap':>7}{'appx':>6}{'+gap':>7}  missing")
    for stem in stems:
        c = assess(stem)
        missing = ",".join(c.missing[:5]) or "-"
        print(f"{stem[:42]:44}{c.main_body_words:>6}{c.main_gap:>7}"
              f"{c.appendix_words:>6}{c.appendix_gap:>7}  {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
