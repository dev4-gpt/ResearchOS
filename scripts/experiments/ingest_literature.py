"""Ingest topically relevant literature for each manuscript.

The citation problem in this repository is a corpus problem. Auditing relevance
showed 91 citations with no topical connection to the sentence citing them, and
the best replacement the 448-paper vault could offer for a sentence about repair
convergence was a paper on generative AI in business, scoring 0.18. The vault was
assembled scattershot; it does not contain the literature these manuscripts need.

Dropping bad citations without adding good ones would leave papers that already
have too few references with even fewer. So this fetches real, topically matched
work per manuscript from arXiv and OpenAlex, writes it into ``vault/01_Papers``
in the existing note format, and lets the citation repair pass draw on it.

Every note records a resolvable URL and a real abstract. Nothing is synthesised.

    backend/.venv/bin/python scripts/experiments/ingest_literature.py
    backend/.venv/bin/python scripts/experiments/ingest_literature.py --per-query 12
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manuscript_sync import REPO_ROOT  # noqa: E402

PAPERS_DIR = os.path.join(REPO_ROOT, "vault", "01_Papers")
MAILTO = "asd5520@psu.edu"
ARXIV_API = "http://export.arxiv.org/api/query"
OPENALEX = "https://api.openalex.org/works"

#: Search terms per manuscript, written to match what each paper is actually
#: about rather than the broad field it sits in.
QUERIES: Dict[str, List[str]] = {
    "autonomous_code_synthesis_and_self_healing_multi_agent_systems": [
        "automated program repair large language model",
        "mutation testing abstract syntax tree",
        "SMT solver program verification patch",
        "self-healing software runtime repair",
    ],
    "review_symbol_graph_rag_vs_qlora_swe_bench_lite": [
        "code retrieval repository context ranking",
        "retrieval augmented generation software engineering",
        "SWE-bench issue resolution agent",
        "parameter efficient fine-tuning LoRA code",
    ],
    "review_architectural_dynamics_long_12_page": [
        "compute optimal scaling laws language model training",
        "KV cache memory attention inference",
        "mixture of experts routing load balancing",
        "low-rank adaptation intrinsic dimensionality",
    ],
    "review_enterprise_genai_roi": [
        "enterprise generative AI adoption return on investment",
        "total cost of ownership large language model deployment",
        "systematic review generative AI business value",
    ],
    "review_enterprise_adoption_of_multi_agent_ai_systems_infr": [
        "multi-agent coordination protocol message complexity",
        "distributed system fault tolerance cascade failure",
        "agent orchestration topology scalability",
    ],
    "review_trustworthy_multi_agent_systems_formal_verification": [
        "linear temporal logic model checking verification",
        "Byzantine fault tolerant consensus protocol",
        "formal verification multi-agent system safety",
    ],
    "review_continual_safety_alignment_in_vision_language_models": [
        "safety alignment fine-tuning degradation language model",
        "continual learning catastrophic forgetting alignment",
        "vision language model safety jailbreak",
        "gradient based sample selection training data",
    ],
    "review_spatio_temporal_grounding_in_video_question_answering": [
        "video question answering temporal grounding",
        "spatio-temporal reasoning video transformer",
        "cross-modal attention video language",
    ],
    "review_composable_ai_systems_for_trustworthy_agentic_pipelines": [
        "compositional AI system contract specification",
        "modular machine learning pipeline reliability",
        "agentic workflow composition verification",
    ],
}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")


def fetch_arxiv(query: str, limit: int) -> List[Dict[str, Any]]:
    params = urllib.parse.urlencode({
        "search_query": f"all:{query}", "start": 0, "max_results": limit,
        "sortBy": "relevance", "sortOrder": "descending",
    })
    try:
        with urllib.request.urlopen(f"{ARXIV_API}?{params}", timeout=60) as response:
            root = ET.fromstring(response.read().decode("utf-8"))
    except Exception as exc:
        print(f"    arXiv failed ({query[:34]}...): {exc}")
        return []

    ns = {"a": "http://www.w3.org/2005/Atom"}
    works = []
    for entry in root.findall("a:entry", ns):
        raw_id = (entry.findtext("a:id", "", ns) or "").rsplit("/", 1)[-1]
        arxiv_id = re.sub(r"v\d+$", "", raw_id)
        abstract = " ".join((entry.findtext("a:summary", "", ns) or "").split())
        title = " ".join((entry.findtext("a:title", "", ns) or "").split())
        if not arxiv_id or not abstract or not title:
            continue
        works.append({
            "key": f"arxiv_{arxiv_id}",
            "title": title,
            "authors": [a.findtext("a:name", "", ns) for a in entry.findall("a:author", ns)],
            "url": entry.findtext("a:id", "", ns),
            "published": (entry.findtext("a:published", "", ns) or "")[:10],
            "abstract": abstract,
            "source": "arXiv",
            "id": f"arxiv:{arxiv_id}",
        })
    return works


def reconstruct_abstract(work: Dict[str, Any]) -> str:
    index = work.get("abstract_inverted_index")
    if not index:
        return ""
    positions: Dict[int, str] = {}
    for word, spots in index.items():
        for spot in spots:
            positions[spot] = word
    return " ".join(positions[k] for k in sorted(positions))


def fetch_openalex(query: str, limit: int) -> List[Dict[str, Any]]:
    params = urllib.parse.urlencode({
        "search": query, "per-page": limit, "mailto": MAILTO,
        "filter": "from_publication_date:2018-01-01,has_abstract:true",
    })
    try:
        request = urllib.request.Request(
            f"{OPENALEX}?{params}", headers={"User-Agent": f"ResearchingOS ({MAILTO})"})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        print(f"    OpenAlex failed ({query[:34]}...): {exc}")
        return []

    works = []
    for row in payload.get("results", []):
        abstract = reconstruct_abstract(row)
        doi = (row.get("doi") or "").replace("https://doi.org/", "")
        if not abstract or not doi or not row.get("title"):
            continue
        key = "crossref_" + re.sub(r"[^A-Za-z0-9]+", "_", doi).strip("_")
        works.append({
            "key": key,
            "title": row["title"],
            "authors": [a["author"]["display_name"]
                        for a in (row.get("authorships") or [])[:8]
                        if a.get("author", {}).get("display_name")],
            "url": row.get("doi") or "",
            "published": str(row.get("publication_year") or ""),
            "abstract": abstract,
            "source": "Crossref",
            "id": doi,
            "citations": row.get("cited_by_count", 0),
        })
    return works


def write_note(work: Dict[str, Any], topic_slug: str) -> bool:
    """Write one vault note. Returns True when a new file was created."""
    path = os.path.join(PAPERS_DIR, f"{work['key']}.md")
    if os.path.exists(path):
        return False

    authors = work.get("authors") or ["Unknown"]
    author_lines = "\n".join(f'  - "{a}"' for a in authors)
    body = (
        "---\n"
        f'title: "{work["title"].replace(chr(34), chr(39))}"\n'
        f"authors:\n{author_lines}\n"
        f'url: "{work["url"]}"\n'
        f'published: "{work["published"]}"\n'
        f'citations: "{work.get("citations", 0)}"\n'
        f'source: "{work["source"]}"\n'
        f'id: "{work["id"]}"\n'
        'full_pdf_ingested: "False"\n'
        "tags:\n"
        '  - "research-paper"\n'
        f'  - "{topic_slug}"\n'
        "---\n"
        f"# {work['title']}\n\n"
        f"**Authors**: {', '.join(authors)}\n"
        f"**Published**: {work['published']} | **Source**: {work['source']}\n"
        f"**URL**: {work['url']}\n\n"
        "## Abstract\n"
        f"{work['abstract']}\n"
    )
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(body)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-query", type=int, default=10)
    args = parser.parse_args()

    os.makedirs(PAPERS_DIR, exist_ok=True)
    before = len(os.listdir(PAPERS_DIR))
    print(f"=== ingesting literature ({before} notes already present) ===")

    total_new = 0
    for stem, queries in QUERIES.items():
        slug = slugify(stem)[:70]
        added = 0
        for query in queries:
            works = fetch_arxiv(query, args.per_query)
            time.sleep(0.5)
            works += fetch_openalex(query, args.per_query)
            time.sleep(0.3)
            for work in works:
                if write_note(work, slug):
                    added += 1
        total_new += added
        print(f"  {stem[:52]:54} +{added} notes")

    print(f"\n{total_new} new notes; vault now holds "
          f"{len(os.listdir(PAPERS_DIR))} papers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
