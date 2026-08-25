"""p4 — Enterprise GenAI literature: a real bibliometric census via OpenAlex.

MEASURED here, by querying a public API live:
  * PRISMA-style identification counts per search string
  * the deduplicated corpus size after screening
  * publication-year distribution, open-access share, venue concentration
  * citation distribution, including the share of the corpus with zero citations
  * how much of the literature is itself empirical, by keyword screening of
    abstracts for reported sample sizes

NOT measured, and therefore not claimable:
  * "N = 18,400 enterprise deployments". No survey was conducted and no such
    dataset was obtained. A literature census counts papers, not deployments.
  * ROI percentages, payback periods or total-cost-of-ownership figures for real
    organisations. Where the literature reports such numbers they belong to the
    cited study and must be attributed to it, never restated as this paper's own
    measurement.

A systematic review's own contribution is the census and the synthesis. That is
what this run supports.

Run:
    backend/.venv/bin/python scripts/experiments/p4_literature_census.py
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from typing import Any, Dict, List

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ExperimentRecorder  # noqa: E402


SEED = 20260825
OPENALEX = "https://api.openalex.org/works"
# A polite mailto puts the request in OpenAlex's faster pool and identifies the caller.
MAILTO = "asd5520@psu.edu"

SEARCH_STRINGS = [
    "generative AI enterprise adoption",
    "large language model business value",
    "AI return on investment organization",
    "multi-agent system enterprise workflow",
    "LLM deployment total cost of ownership",
]

# Screening: an abstract that reports a sample size is plausibly empirical.
EMPIRICAL_MARKERS = ("n =", "n=", "sample", "survey", "respondents", "participants",
                     "we evaluate", "experiment", "case study", "interviews")

#: OpenAlex returns relevance-ranked results, so the retrieved set is the top of
#: each query's ranking, not a random sample of the literature. Rates computed over
#: it (open-access share, median citations) describe this sample and are biased
#: upward relative to the full corpus. The manuscript must report it this way.
SAMPLING_CAVEAT = ("relevance-ranked top-N sample per query, not a random sample; "
                   "rates are biased upward relative to the full corpus")


def fetch(query: str, per_page: int = 200, pages: int = 2) -> List[Dict[str, Any]]:
    """Fetch works for one search string. Returns [] rather than raising on failure."""
    works: List[Dict[str, Any]] = []
    cursor = "*"
    for _ in range(pages):
        params = urllib.parse.urlencode({
            "search": query,
            "per-page": per_page,
            "cursor": cursor,
            "mailto": MAILTO,
            "filter": "from_publication_date:2019-01-01",
        })
        try:
            request = urllib.request.Request(
                f"{OPENALEX}?{params}", headers={"User-Agent": f"ResearchingOS ({MAILTO})"}
            )
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            print(f"    query failed ({query[:40]}...): {exc}")
            break
        batch = payload.get("results", [])
        works.extend(batch)
        cursor = (payload.get("meta") or {}).get("next_cursor")
        if not cursor or not batch:
            break
        time.sleep(0.3)
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


def main() -> int:
    rec = ExperimentRecorder(
        run_id="draft-review_enterprise_genai_roi",
        paper="p4",
        description=("Bibliometric census of enterprise generative-AI literature via the "
                     "OpenAlex API: identification counts, year and venue distribution, "
                     "open access share, citation distribution, empirical share."),
        seed=SEED,
    )

    print("=== p4: literature census (OpenAlex, live) ===\n")

    identified: Dict[str, int] = {}
    by_id: Dict[str, Dict[str, Any]] = {}
    for query in SEARCH_STRINGS:
        works = fetch(query)
        identified[query] = len(works)
        print(f"  {len(works):>5} results  <- {query}")
        for work in works:
            if work.get("id"):
                by_id[work["id"]] = work

    if not by_id:
        print("\n  No results retrieved; nothing recorded. Re-run with network access.")
        rec.finalize()
        return 1

    total_identified = sum(identified.values())
    corpus = list(by_id.values())
    print(f"\n  identified: {total_identified}, unique after deduplication: {len(corpus)}")

    # Screening: keep works with a usable abstract and a title.
    screened = [w for w in corpus if reconstruct_abstract(w) and w.get("title")]
    years = [w.get("publication_year") for w in screened if w.get("publication_year")]
    citations = [int(w.get("cited_by_count") or 0) for w in screened]
    open_access = [1.0 if (w.get("open_access") or {}).get("is_oa") else 0.0
                   for w in screened]
    venues = Counter(
        ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
        or "unknown"
        for w in screened
    )
    empirical = [
        1.0 if any(m in reconstruct_abstract(w).lower() for m in EMPIRICAL_MARKERS) else 0.0
        for w in screened
    ]

    art, sha = rec.save_artifact("literature_census.json", {
        "search_strings": SEARCH_STRINGS,
        "identified_per_query": identified,
        "unique_after_dedup": len(corpus),
        "screened": len(screened),
        "year_distribution": dict(Counter(years)),
        "citation_counts": citations,
        "open_access_flags": open_access,
        "top_venues": venues.most_common(25),
        "empirical_flags": empirical,
        "work_ids": sorted(by_id)[:2000],
    })

    zero_cited = 100.0 * float(np.mean([1.0 if c == 0 else 0.0 for c in citations]))
    oa_share = 100.0 * float(np.mean(open_access))
    empirical_share = 100.0 * float(np.mean(empirical))
    median_citations = float(np.median(citations))
    recent = 100.0 * float(np.mean([1.0 if y and y >= 2023 else 0.0 for y in years]))

    print(f"  screened (abstract present): {len(screened)}")
    print(f"  published 2023 or later:     {recent:.2f}%")
    print(f"  open access:                 {oa_share:.2f}%")
    print(f"  median citations:            {median_citations:.1f}")
    print(f"  zero-citation share:         {zero_cited:.2f}%")
    print(f"  abstracts reporting data:    {empirical_share:.2f}%")
    print(f"  distinct venues:             {len(venues)}")
    print(f"\n  SAMPLING: {SAMPLING_CAVEAT}")

    for metric, value, unit, method in (
        ("literature_identified_total", total_identified, "n",
         "sum of per-query result counts"),
        ("literature_unique_after_dedup", len(corpus), "n", "deduplicated by OpenAlex id"),
        ("literature_screened", len(screened), "n", "abstract and title present"),
        ("literature_recent_share", round(recent, 2), "%", "publication year >= 2023"),
        ("literature_open_access_share", round(oa_share, 2), "%", "OpenAlex is_oa flag"),
        ("literature_median_citations", median_citations, "n",
         "median of cited_by_count"),
        ("literature_zero_citation_share", round(zero_cited, 2), "%",
         "share with cited_by_count == 0"),
        ("literature_empirical_share", round(empirical_share, 2), "%",
         "abstract contains a sample-size or study marker"),
        ("literature_distinct_venues", len(venues), "n", "distinct primary sources"),
    ):
        rec.record(metric, value, unit, art, sha, method, n=len(screened),
                   notes=SAMPLING_CAVEAT)

    rec.record("literature_empirical_share_ci_low",
               round(rec.bootstrap_ci(empirical, 2000)[0] * 100, 3), "%", art, sha,
               "bootstrap lower bound on empirical share", n=len(screened))

    rec.finalize()
    print("\n  NOTE: this counts papers, not enterprise deployments. Any ROI or payback")
    print("  figure in the review belongs to the study that reported it and must be")
    print("  attributed to that citation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
