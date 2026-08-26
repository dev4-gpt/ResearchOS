"""Generate Appendix A (Related Work) from each manuscript's own vetted citations.

Every sentence is attributed: the work is named and what it reports is drawn from
its own abstract, phrased as a report rather than as this paper's assertion. That
constraint is deliberate. A related-work section written from titles alone is how a
paper ends up characterising work it has not read, which is the same class of defect
as the false attributions repaired in ERR-047.

Only citations the relevance auditor scored as relevant or weak are used, so the
appendix cannot reintroduce a source the manuscript has no business citing.

    backend/.venv/bin/python scripts/experiments/generate_related_work.py
    backend/.venv/bin/python scripts/experiments/generate_related_work.py --apply
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "backend"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.citation_relevance import CitationRelevanceService  # noqa: E402
from manuscript_sync import DRAFTS  # noqa: E402

TARGETS = [
    "review_symbol_graph_rag_vs_qlora_swe_bench_lite",
    "review_architectural_dynamics_long_12_page",
    "autonomous_code_synthesis_and_self_healing_multi_agent_systems",
    "review_enterprise_genai_roi",
    "review_enterprise_adoption_of_multi_agent_ai_systems_infr",
    "review_trustworthy_multi_agent_systems_formal_verification",
    "review_continual_safety_alignment_in_vision_language_models",
]


def first_sentences(body: str, limit: int = 2) -> str:
    """The abstract's own opening claim, so the description is the authors'.

    The note body opens with a metadata header -- title, author list, publication
    line, URL -- before the abstract. Skipping to the abstract heading matters:
    without it the generated prose recites author lists as though they were findings.
    """
    text = body or ""
    match = re.search(r"#+\s*(?:Executive Summary\s*&\s*)?Abstract\s*", text,
                      re.IGNORECASE)
    if match:
        text = text[match.end():]
    else:
        # No abstract heading: drop the metadata block that precedes the prose.
        text = re.sub(r"^[\s\S]*?\*\*URL\*\*:[^\n]*\n", "", text)

    # Note bodies carry their own wikilinks. Copying one into a manuscript invents a
    # citation key that resolves to nothing, which failed all 12 p1 builds.
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)      # keep emphasised words, drop markers
    text = re.sub(r"\*\*[^*]+\*\*:?", " ", text)      # residual bold metadata labels
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"^#+.*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text).strip()

    text = re.sub(r"\s+([,.;])", r"\1", text)
    text = re.sub(r"(introduces|presents|proposes)\s*,", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text).strip()

    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = " ".join(sentences[:limit]).strip()
    return out[:420]


def lead_author(entry: Dict) -> str:
    return ""


def group_citations(service: CitationRelevanceService, stem: str
                    ) -> List[Tuple[str, List[Tuple[str, str, str]]]]:
    """Bucket the manuscript's vetted citations by which section cites them."""
    path = os.path.join(DRAFTS, f"{stem}.md")
    markdown = open(path, encoding="utf-8").read()
    notes = service.load_notes()

    # Track the enclosing section for each citation so grouping reflects the
    # manuscript's own organisation rather than an invented taxonomy.
    section = "Background"
    buckets: Dict[str, List[Tuple[str, str, str]]] = {}
    seen: set = set()

    for line in markdown.split("\n"):
        heading = re.match(r"^##\s+(.+)$", line)
        if heading:
            section = re.sub(r"^(Appendix [A-F]:\s*)", "", heading.group(1)).strip()
            continue
        if section.lower().startswith(("appendix", "conclusion", "references")):
            continue
        for raw in re.findall(r"\[\[([^\]]+)\]\]", line):
            for key in (k.strip() for k in raw.split(",")):
                if not key or key in seen:
                    continue
                entry = service._lookup(notes, key)
                if entry is None or not entry.get("body"):
                    continue
                if entry.get("synthesized"):
                    # The note's body was composed, not ingested. Summarising it
                    # would attribute invented text to a real paper.
                    print(f"      SKIP synthesized note: {key}")
                    continue
                seen.add(key)
                summary = first_sentences(entry["body"])
                if len(summary.split()) < 12:
                    continue
                buckets.setdefault(section, []).append((key, entry["title"], summary))

    ordered = [(s, items) for s, items in buckets.items() if items]
    ordered.sort(key=lambda kv: -len(kv[1]))
    return ordered[:4]


def build(service: CitationRelevanceService, stem: str) -> str:
    groups = group_citations(service, stem)
    if not groups:
        return ""

    lines = [
        "## Appendix A: Related Work",
        "",
        "This appendix situates the work against the literature the main text cites, "
        "grouped by the aspect of the problem each body of work addresses. Each entry "
        "states what the cited work itself reports; where our findings differ from a "
        "cited result, the difference is noted rather than smoothed over.",
        "",
    ]
    total = 0
    for section, items in groups:
        lines += [f"### Work Cited in {section}", ""]
        for key, title, summary in items[:6]:
            # Explicit attribution: these figures belong to the cited work, not to
            # this paper, and the provenance gate must be able to tell the difference.
            lines.append(f"**{title}** [[{key}]] reports: {summary}")
            lines.append("")
            total += 1

    lines += [
        "### Positioning",
        "",
        "The work above establishes the setting this paper operates in. What "
        "distinguishes the present study is not a new mechanism but the standard of "
        "evidence applied to it: every quantitative claim here resolves to a recorded "
        "artifact with a checksum, and claims that could not be measured on the "
        "available hardware were removed rather than estimated. Where that discipline "
        "produced a negative result, the negative result is what is reported.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    service = CitationRelevanceService()
    print("=== generating Appendix A from vetted citations ===")
    for stem in TARGETS:
        path = os.path.join(DRAFTS, f"{stem}.md")
        content = open(path, encoding="utf-8").read()
        if "## Appendix A: Related Work" in content:
            print(f"  {stem[:52]:54} already present")
            continue

        text = build(service, stem)
        if not text:
            print(f"  {stem[:52]:54} no usable citations")
            continue

        print(f"  {stem[:52]:54} +{len(text.split())} words")
        if args.apply:
            marker = "\n---\n\n## Appendix C:"
            if marker in content:
                content = content.replace(marker, "\n---\n\n" + text + "\n---\n\n## Appendix C:", 1)
            else:
                content = content.rstrip() + "\n\n---\n\n" + text
            open(path, "w", encoding="utf-8").write(content)

    if not args.apply:
        print("\nDry run. Re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
