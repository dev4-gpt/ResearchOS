"""p1 — Symbol-graph retrieval: measured, and a census of SWE-bench Lite signal.

MEASURED here:
  A. Retrieval quality on a real Python corpus. A symbol graph is built from
     imports and call references; BM25 seeds a Personalized PageRank diffusion
     over it; the re-ranked modules are scored against ground truth with P@1,
     P@5 and MRR, paired against the BM25 baseline it re-ranks.
     Queries are docstrings with the defining symbol's own name stripped, so a
     hit cannot come from copying the answer into the query.
  B. A census of SWE-bench Lite (300 public instances, fetched live): how many
     files each gold patch touches, and how often the problem statement already
     names the file that must be edited. That is a property of the benchmark and
     needs no model to measure.

NOT measured, and therefore not claimable:
  * resolved-issue rate for Symbol-Graph RAG or for QLoRA. Both require running a
    70B model and executing the benchmark's test suites; neither happened.
  * "38.7% vs 27.3%", the 4.2x inference cost ratio, or the 160 GB dual-H100
    training figure. No model was trained, served, or measured.

The retrieval experiment is on this repository's own Python, not on SWE-bench
repositories, because evaluating retrieval there means cloning twelve large
repositories at pinned commits. The manuscript must say which corpus was used.

Run:
    backend/.venv/bin/python scripts/experiments/p1_symbol_graph_retrieval.py
"""
from __future__ import annotations

import ast
import glob
import json
import math
import os
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple

import networkx as nx
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import REPO_ROOT, ExperimentRecorder, is_sync_conflict_copy  # noqa: E402


SEED = 20260825
# Widened deliberately: on 36 modules BM25 alone reaches 100% P@5, a ceiling at
# which no re-ranker can show an effect either way. A larger, more homogeneous
# corpus makes the task discriminative.
CORPUS_GLOBS = [
    os.path.join(REPO_ROOT, "backend", "**", "*.py"),
    os.path.join(REPO_ROOT, "scripts", "**", "*.py"),
    os.path.join(REPO_ROOT, "scripts", "*.py"),
]
SWEBENCH_URL = ("https://datasets-server.huggingface.co/rows?"
                "dataset=princeton-nlp%2FSWE-bench_Lite&config=default&split=test"
                "&offset={offset}&length={length}")

STOP = frozenset("""the a an and or of to in is are for with that this it as be on by from
at not if then than which was were will can may use used using return returns given
self none true false int str dict list none type value key item args kwargs""".split())


def tokenize(text: str) -> List[str]:
    words = re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", text.lower())
    out = []
    for w in words:
        # split snake_case and camelCase so 'compile_pdflatex' matches 'compile'
        parts = re.split(r"_+", w)
        for p in parts:
            for piece in re.findall(r"[a-z]+|[0-9]+", p):
                if piece not in STOP and len(piece) > 2:
                    out.append(piece)
    return out


# ------------------------------------------------------------------- BM25

class BM25:
    """Standard Okapi BM25. Implemented here to keep the result inspectable."""

    def __init__(self, docs: Dict[str, List[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.doc_ids = list(docs)
        self.tf = {d: Counter(t) for d, t in docs.items()}
        self.len = {d: len(t) for d, t in docs.items()}
        self.avg_len = (sum(self.len.values()) / len(self.len)) if self.len else 0.0
        df: Counter = Counter()
        for tokens in docs.values():
            df.update(set(tokens))
        n = len(docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def score(self, query: List[str]) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        for doc_id in self.doc_ids:
            tf, dl = self.tf[doc_id], self.len[doc_id]
            total = 0.0
            for term in query:
                freq = tf.get(term, 0)
                if not freq:
                    continue
                denom = freq + self.k1 * (1 - self.b + self.b * dl / (self.avg_len or 1))
                total += self.idf.get(term, 0.0) * freq * (self.k1 + 1) / denom
            scores[doc_id] = total
        return scores


# ----------------------------------------------------------- symbol graph

def build_corpus() -> Tuple[Dict[str, str], List[Tuple[str, str, str]]]:
    """Return {module: source} and [(module, symbol, docstring)] query candidates."""
    modules: Dict[str, str] = {}
    queries: List[Tuple[str, str, str]] = []
    for pattern in CORPUS_GLOBS:
        for path in sorted(glob.glob(pattern, recursive=True)):
            if os.sep + ".venv" + os.sep in path or os.sep + "node_modules" + os.sep in path:
                continue
            if is_sync_conflict_copy(path):
                continue
            rel = os.path.relpath(path, REPO_ROOT)
            try:
                text = open(path, encoding="utf-8").read()
                tree = ast.parse(text)
            except (SyntaxError, UnicodeDecodeError):
                continue
            modules[rel] = text
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    doc = ast.get_docstring(node)
                    if doc and len(doc.split()) >= 6:
                        queries.append((rel, node.name, doc))
    return modules, queries


def build_symbol_graph(modules: Dict[str, str]) -> nx.DiGraph:
    """Nodes are modules and top-level symbols; edges are definition and reference."""
    graph = nx.DiGraph()
    symbol_owner: Dict[str, str] = {}

    for rel, text in modules.items():
        graph.add_node(rel, kind="module")
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                sym = f"{rel}::{node.name}"
                graph.add_node(sym, kind="symbol")
                graph.add_edge(rel, sym, kind="defines")
                graph.add_edge(sym, rel, kind="defined_in")
                symbol_owner[node.name] = sym

    # Reference edges: a module that names a symbol defined elsewhere depends on it.
    for rel, text in modules.items():
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            name = None
            if isinstance(node, ast.Name):
                name = node.id
            elif isinstance(node, ast.Attribute):
                name = node.attr
            if name and name in symbol_owner:
                target = symbol_owner[name]
                if not target.startswith(rel + "::"):
                    graph.add_edge(rel, target, kind="references")
    return graph


def ppr_rerank(graph: nx.DiGraph, seeds: Dict[str, float], modules: List[str],
               alpha: float = 0.6) -> Dict[str, float]:
    """Personalized PageRank seeded by BM25, projected back onto modules."""
    personalization = {n: 0.0 for n in graph.nodes}
    total = sum(v for v in seeds.values() if v > 0)
    if total <= 0:
        return {m: 0.0 for m in modules}
    for node, weight in seeds.items():
        if weight > 0 and node in personalization:
            personalization[node] = weight / total
    try:
        pr = nx.pagerank(graph, alpha=alpha, personalization=personalization,
                         max_iter=100, tol=1e-08)
    except nx.PowerIterationFailedConvergence:
        return {m: seeds.get(m, 0.0) for m in modules}

    scores: Dict[str, float] = defaultdict(float)
    for node, value in pr.items():
        owner = node.split("::")[0]
        scores[owner] += value
    return {m: scores.get(m, 0.0) for m in modules}


def rank_metrics(ranking: List[str], gold: str) -> Tuple[float, float, float]:
    """Return (P@1, P@5, reciprocal rank)."""
    if gold not in ranking:
        return 0.0, 0.0, 0.0
    idx = ranking.index(gold)
    return (1.0 if idx == 0 else 0.0,
            1.0 if idx < 5 else 0.0,
            1.0 / (idx + 1))


# -------------------------------------------------------------- swe-bench

def fetch_swebench_lite(limit: int = 300) -> List[dict]:
    rows: List[dict] = []
    offset = 0
    while len(rows) < limit:
        length = min(100, limit - len(rows))
        url = SWEBENCH_URL.format(offset=offset, length=length)
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # network is not guaranteed
            print(f"    fetch failed at offset {offset}: {exc}")
            break
        batch = payload.get("rows", [])
        if not batch:
            break
        rows.extend(r["row"] for r in batch)
        offset += len(batch)
    return rows


def patched_files(patch: str) -> List[str]:
    return sorted(set(re.findall(r"^\+\+\+ b/(.+)$", patch or "", re.MULTILINE)))


def main() -> int:
    rec = ExperimentRecorder(
        run_id="draft-review_symbol_graph_rag_vs_qlora_swe_bench_lite",
        paper="p1",
        description=("Symbol-graph PPR re-ranking vs BM25 on a Python corpus with "
                     "docstring-derived queries, plus a census of retrieval signal in "
                     "SWE-bench Lite. No language model was run."),
        seed=SEED,
    )
    rng = np.random.default_rng(SEED)

    print("=== p1: symbol-graph retrieval ===\n")

    # ---------------------------------------------------- A. retrieval study
    modules, queries = build_corpus()
    print(f"  corpus: {len(modules)} modules, {len(queries)} docstring queries")

    tokenized = {m: tokenize(t) for m, t in modules.items()}
    bm25 = BM25(tokenized)
    graph = build_symbol_graph(modules)
    print(f"  symbol graph: {graph.number_of_nodes()} nodes, "
          f"{graph.number_of_edges()} edges")

    module_list = list(modules)

    prepared = []
    for gold, symbol, doc in queries:
        # Strip the defining symbol's own words so the query cannot leak the answer.
        banned = set(tokenize(symbol)) | set(tokenize(os.path.basename(gold)))
        q = [t for t in tokenize(doc) if t not in banned]
        if len(q) >= 4:
            prepared.append((gold, symbol, q, bm25.score(q)))

    # Sweep the diffusion's own hyperparameters, but select on a held-out half.
    # Reporting a single untuned setting would measure the tuning rather than the
    # method; selecting on the same queries we then report would be tuning on test.
    order = np.random.default_rng(SEED).permutation(len(prepared))
    dev_idx = set(order[: len(prepared) // 2].tolist())
    dev = [prepared[i] for i in range(len(prepared)) if i in dev_idx]
    test = [prepared[i] for i in range(len(prepared)) if i not in dev_idx]

    sweep = {}
    for alpha in (0.15, 0.3, 0.5, 0.7, 0.85):
        for seed_topk in (5, 10, 25, 0):          # 0 = seed with every module
            mrrs = []
            for gold, _sym, _q, base_scores in dev:
                ordered = sorted(base_scores.items(), key=lambda kv: -kv[1])
                chosen = ordered if seed_topk == 0 else ordered[:seed_topk]
                seeds = {m: max(0.0, s) for m, s in chosen}
                scores = ppr_rerank(graph, seeds, module_list, alpha=alpha)
                ranked = sorted(module_list, key=lambda m: -scores.get(m, 0.0))
                mrrs.append(rank_metrics(ranked, gold)[2])
            sweep[f"alpha{alpha}_topk{seed_topk}"] = float(np.mean(mrrs))

    best_key = max(sweep, key=lambda k: sweep[k])
    best_alpha = float(best_key.split("_")[0][5:])
    best_topk = int(best_key.split("topk")[1])
    print(f"  best PPR config over {len(sweep)} settings, chosen on {len(dev)} held-out "
          f"dev queries: alpha={best_alpha}, seed_topk={best_topk or 'all'} "
          f"(dev MRR {sweep[best_key]:.4f})")
    print(f"  reporting on {len(test)} unseen test queries")

    per_query = []
    for gold, symbol, _q, base_scores in test:
        base_rank = sorted(module_list, key=lambda m: -base_scores.get(m, 0.0))

        ordered = sorted(base_scores.items(), key=lambda kv: -kv[1])
        chosen = ordered if best_topk == 0 else ordered[:best_topk]
        ppr_scores = ppr_rerank(graph, {m: max(0.0, s) for m, s in chosen},
                                module_list, alpha=best_alpha)
        ppr_rank = sorted(module_list, key=lambda m: -ppr_scores.get(m, 0.0))

        b1, b5, bmrr = rank_metrics(base_rank, gold)
        p1_, p5_, pmrr = rank_metrics(ppr_rank, gold)
        per_query.append({"gold": gold, "symbol": symbol,
                          "bm25": [b1, b5, bmrr], "ppr": [p1_, p5_, pmrr]})

    n = len(per_query)
    def col(system, i):
        return [q[system][i] for q in per_query]

    art1, sha1 = rec.save_artifact("retrieval_results.json", {
        "modules": len(modules), "queries_evaluated": n,
        "graph_nodes": graph.number_of_nodes(), "graph_edges": graph.number_of_edges(),
        "ppr_sweep_mrr_dev": sweep,
        "best_config": {"alpha": best_alpha, "seed_topk": best_topk},
        "dev_queries": len(dev), "test_queries": len(test),
        "per_query": per_query,
    })

    # The corpus statistics the manuscript quotes in its first paragraph. They
    # were previously only printed and stored inside the artifact, so nothing
    # checked them and nothing could update them: the draft still described a
    # 109-module corpus several re-runs after it stopped being one. A number a
    # paper states is a claim, whether or not it is the headline (ERR-072).
    for metric, value, method in (
        ("corpus_modules", len(modules), "Python modules admitted to the corpus"),
        ("corpus_docstring_queries", len(queries), "docstrings of >=6 words"),
        ("corpus_queries_after_filter", len(prepared), "queries of >=4 non-leaking terms"),
        ("symbol_graph_nodes", graph.number_of_nodes(), "modules plus top-level symbols"),
        ("symbol_graph_edges", graph.number_of_edges(), "definition and reference edges"),
        ("dev_queries", len(dev), "held-out split used to select PPR hyperparameters"),
        ("test_queries", len(test), "unseen split the reported metrics are computed on"),
    ):
        rec.record(metric, value, "n", art1, sha1, method)

    print(f"\n  {'system':8}{'P@1':>9}{'P@5':>9}{'MRR':>9}   (n={n} queries)")
    for system, label in (("bm25", "BM25"), ("ppr", "Symbol+PPR")):
        p1v, p5v, mrr = (float(np.mean(col(system, i))) for i in range(3))
        print(f"  {label:10}{p1v*100:8.2f}%{p5v*100:8.2f}%{mrr:9.4f}")
        for metric, value, idx in (("p_at_1", p1v, 0), ("p_at_5", p5v, 1), ("mrr", mrr, 2)):
            ci = rec.bootstrap_ci(col(system, idx), iterations=2000)
            rec.record(f"{metric}_{system}",
                       round(value * (100 if metric != "mrr" else 1), 4),
                       "%" if metric != "mrr" else "", art1, sha1,
                       f"{label} over docstring queries, gold = defining module", n=n,
                       ci95=[round(c * (100 if metric != "mrr" else 1), 4) for c in ci])

    delta_mrr = float(np.mean(col("ppr", 2)) - np.mean(col("bm25", 2)))
    stats = rec.welch_t(col("ppr", 2), col("bm25", 2))
    art2, sha2 = rec.save_artifact("retrieval_significance.json",
                                   {"delta_mrr": delta_mrr, **stats})
    rec.record("mrr_delta_ppr_minus_bm25", round(delta_mrr, 5), "", art2, sha2,
               "paired difference in MRR", n=n)
    rec.record("retrieval_cohens_d", stats["cohens_d"], "", art2, sha2,
               "Welch t-test, PPR vs BM25 MRR", n=n)
    verdict = "improves" if delta_mrr > 0 else "does not improve"
    print(f"\n  symbol-graph diffusion {verdict} MRR: delta={delta_mrr:+.4f}, "
          f"p={stats['p']:.3e}, d={stats['cohens_d']}")

    # -------------------------------------------------- B. swe-bench census
    print("\n  fetching SWE-bench Lite (public, 300 instances)...")
    instances = fetch_swebench_lite(300)
    if instances:
        files_per = [len(patched_files(i.get("patch", ""))) for i in instances]
        mentions = []
        for inst in instances:
            gold = patched_files(inst.get("patch", ""))
            statement = (inst.get("problem_statement") or "").lower()
            stems = [os.path.splitext(os.path.basename(f))[0].lower() for f in gold]
            mentions.append(1.0 if any(s and s in statement for s in stems) else 0.0)

        repos = Counter(i.get("repo", "?") for i in instances)
        art3, sha3 = rec.save_artifact("swebench_census.json", {
            "instances": len(instances),
            "files_per_patch": files_per,
            "gold_file_named_in_statement": mentions,
            "repos": dict(repos),
        })
        mean_files = float(np.mean(files_per))
        single = 100.0 * float(np.mean([1.0 if f == 1 else 0.0 for f in files_per]))
        mention_rate = 100.0 * float(np.mean(mentions))

        print(f"    instances fetched: {len(instances)} across {len(repos)} repositories")
        print(f"    mean files per gold patch: {mean_files:.3f}")
        print(f"    single-file patches: {single:.2f}%")
        print(f"    problem statement names the gold file: {mention_rate:.2f}%")

        rec.record("swebench_instances", len(instances), "n", art3, sha3,
                   "rows fetched from the public dataset", n=len(instances))
        rec.record("swebench_mean_files_per_patch", round(mean_files, 4), "n",
                   art3, sha3, "parsed from gold patch headers", n=len(instances))
        rec.record("swebench_single_file_patch_rate", round(single, 2), "%",
                   art3, sha3, "share of gold patches touching exactly one file",
                   n=len(instances))
        rec.record("swebench_gold_file_named_rate", round(mention_rate, 2), "%",
                   art3, sha3, "gold filename stem appears in problem statement",
                   n=len(instances),
                   ci95=[round(c * 100, 3) for c in rec.bootstrap_ci(mentions, 2000)])
    else:
        print("    SKIPPED: dataset not reachable; no census recorded.")

    rec.finalize()
    print("\n  NOTE: retrieval measured on this repository's Python corpus. No language")
    print("  model was run, so no resolved-issue rate is reported.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
