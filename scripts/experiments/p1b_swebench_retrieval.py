"""p1b: the same retrieval question, asked of real repositories and real issues.

p1 measures symbol-graph re-ranking on *this* repository, with queries built from
docstrings. That is a real measurement and it is also the paper's weakest point:
the corpus is the code we wrote, the queries are synthesised from it, and a
reviewer's first question is whether the null result survives contact with
software someone else wrote about problems someone else reported.

This asks the same question of SWE-bench Lite. Every part of the task is real:

    corpus   the repository's Python files at the instance's base commit
    query    the issue text a human wrote, verbatim
    gold     the files the accepted patch actually changed

Nothing is generated and no language model is involved. Retrieval is BM25 and
Personalized PageRank over a symbol graph -- the same two systems p1 compares,
imported from it rather than reimplemented, so a difference in result cannot be
a difference in implementation.

Repository contents are read with `git cat-file --batch` against a bare clone,
so no working tree is ever checked out and the clones cannot be mistaken for
part of this project's own corpus (ERR-071: iCloud duplicates of our source got
into p1's corpus once already and flipped its headline sign). The cache lives
outside the repository by default.

    backend/.venv/bin/python scripts/experiments/p1b_swebench_retrieval.py
    SWEBENCH_CACHE=/path/to/cache backend/.venv/bin/python scripts/experiments/p1b_swebench_retrieval.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from typing import Dict, List, Optional, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ExperimentRecorder  # noqa: E402
from p1_symbol_graph_retrieval import (  # noqa: E402
    BM25, build_symbol_graph, fetch_swebench_lite, patched_files, ppr_rerank,
    rank_metrics, tokenize,
)

SEED = 20260825

# The six smallest SWE-bench Lite repositories by clone size, giving 41 of the
# 300 instances. django (114) and sympy (77) are excluded on clone cost, not on
# any property of the task -- which is a limitation of this run and is reported
# as one rather than described as a sample.
TARGET_REPOS = (
    "psf/requests",
    "pallets/flask",
    "mwaskom/seaborn",
    "pytest-dev/pytest",
    "pylint-dev/pylint",
    "pydata/xarray",
)

MAX_FILE_BYTES = 400_000   # a vendored megabyte of generated code is not a document


def cache_root() -> str:
    configured = os.environ.get("SWEBENCH_CACHE")
    if configured:
        os.makedirs(configured, exist_ok=True)
        return configured
    path = os.path.join(tempfile.gettempdir(), "researchos-swebench-clones")
    os.makedirs(path, exist_ok=True)
    return path


def git(args: List[str], cwd: str, timeout: int = 900) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                          text=False, timeout=timeout)


def ensure_clone(repo: str) -> Optional[str]:
    """A bare clone of *repo*, fetched once and reused. None if it cannot be had."""
    target = os.path.join(cache_root(), repo.replace("/", "__") + ".git")
    if os.path.isdir(os.path.join(target, "objects")):
        return target
    print(f"    cloning {repo} (once) ...", flush=True)
    proc = subprocess.run(
        ["git", "clone", "--bare", "--quiet", f"https://github.com/{repo}.git", target],
        capture_output=True, text=True, timeout=1800,
    )
    if proc.returncode != 0:
        print(f"    ! clone failed: {proc.stderr.strip()[:120]}")
        return None
    return target


def python_files_at(clone: str, commit: str) -> Dict[str, str]:
    """Every .py file at *commit*, read straight out of the object store.

    `git ls-tree` then one `git cat-file --batch` for the whole set: no checkout,
    no working tree, and one process instead of one per file.
    """
    listing = git(["ls-tree", "-r", "--name-only", commit], clone)
    if listing.returncode != 0:
        return {}
    paths = [p for p in listing.stdout.decode("utf-8", "replace").splitlines()
             if p.endswith(".py")]
    if not paths:
        return {}

    request = "".join(f"{commit}:{p}\n" for p in paths).encode()
    batch = subprocess.run(["git", "cat-file", "--batch"], cwd=clone,
                           input=request, capture_output=True, timeout=900)
    if batch.returncode != 0:
        return {}

    out: Dict[str, str] = {}
    buf, pos = batch.stdout, 0
    for path in paths:
        newline = buf.find(b"\n", pos)
        if newline < 0:
            break
        header = buf[pos:newline].decode("utf-8", "replace").split()
        pos = newline + 1
        if len(header) < 3:            # "<oid> missing" -- path absent at this commit
            continue
        size = int(header[2])
        blob, pos = buf[pos:pos + size], pos + size + 1
        if size <= MAX_FILE_BYTES:
            out[path] = blob.decode("utf-8", "replace")
    return out


def evaluate(modules: Dict[str, str], query_text: str, gold: List[str],
             alpha: float, seed_topk: int) -> Optional[Tuple[Tuple, Tuple]]:
    """(BM25 metrics, PPR metrics) for one issue, or None if it cannot be scored."""
    present = [g for g in gold if g in modules]
    if not present or len(modules) < 5:
        return None

    query = tokenize(query_text)
    if len(query) < 4:
        return None

    bm25 = BM25({m: tokenize(t) for m, t in modules.items()})
    base = bm25.score(query)
    module_list = list(modules)

    base_rank = sorted(module_list, key=lambda m: -base.get(m, 0.0))
    ordered = sorted(base.items(), key=lambda kv: -kv[1])[:seed_topk]
    seeds = {m: max(0.0, s) for m, s in ordered}
    scores = ppr_rerank(build_symbol_graph(modules), seeds, module_list, alpha=alpha)
    ppr_rank = sorted(module_list, key=lambda m: -scores.get(m, 0.0))

    # An issue may touch several files; credit the best-ranked one, which is the
    # standard localisation convention and the one that favours neither system.
    best_base = max(rank_metrics(base_rank, g) for g in present)
    best_ppr = max(rank_metrics(ppr_rank, g) for g in present)
    return best_base, best_ppr


def main() -> int:
    print("=== p1b: symbol-graph retrieval on SWE-bench Lite ===\n")
    rec = ExperimentRecorder(
        run_id="draft-review_symbol_graph_rag_vs_qlora_swe_bench_lite",
        paper="review_symbol_graph_rag_vs_qlora_swe_bench_lite",
        description=("Symbol-graph PPR vs BM25 over real repositories at SWE-bench "
                     "Lite base commits, queried with the issue text, scored against "
                     "the files the accepted patch changed."),
        seed=SEED,
        # p1 records into this same file, including four census metrics already
        # named swebench_* (swebench_instances, swebench_gold_file_named_rate,
        # and two more). Claiming "swebench_" therefore deleted them on the first
        # run of this script. The namespace has to be one nothing else writes.
        owns_prefix="swebench_retrieval_",
    )

    instances = [i for i in fetch_swebench_lite(300) if i.get("repo") in TARGET_REPOS]
    print(f"  {len(instances)} instance(s) across {len(TARGET_REPOS)} repositories\n")
    if not instances:
        print("  no instances fetched; is the network available?")
        return 1

    # p1 selected alpha=0.15 / seed_topk=25 on its own held-out split. Reusing that
    # choice here means this run tunes nothing: it reports how a configuration
    # chosen elsewhere behaves on data it has never seen.
    alpha, seed_topk = 0.15, 25
    print(f"  configuration carried over from p1, untuned here: "
          f"alpha={alpha}, seed_topk={seed_topk}\n")

    per_instance: List[dict] = []
    skipped: List[dict] = []

    for repo in TARGET_REPOS:
        clone = ensure_clone(repo)
        if clone is None:
            continue
        for inst in [i for i in instances if i["repo"] == repo]:
            gold = patched_files(inst.get("patch", ""))
            modules = python_files_at(clone, inst["base_commit"])
            if not modules:
                skipped.append({"instance_id": inst["instance_id"],
                                "reason": "commit or files unavailable"})
                continue
            scored = evaluate(modules, inst.get("problem_statement", ""),
                              gold, alpha, seed_topk)
            if scored is None:
                skipped.append({"instance_id": inst["instance_id"],
                                "reason": "gold file absent from corpus, or query too short"})
                continue
            base_m, ppr_m = scored
            per_instance.append({
                "instance_id": inst["instance_id"], "repo": repo,
                "corpus_files": len(modules), "gold_files": len(gold),
                "bm25": list(base_m), "ppr": list(ppr_m),
            })
            print(f"    {inst['instance_id'][:44]:44} {len(modules):>5} files  "
                  f"bm25 rr={base_m[2]:.3f}  ppr rr={ppr_m[2]:.3f}", flush=True)

    if not per_instance:
        print("\n  nothing scored; not recording a measurement.")
        return 1

    n = len(per_instance)
    art, sha = rec.save_artifact("swebench_retrieval.json", {
        "instances_scored": n,
        "instances_skipped": len(skipped),
        "skipped": skipped,
        "repos": sorted({p["repo"] for p in per_instance}),
        "config": {"alpha": alpha, "seed_topk": seed_topk, "tuned_here": False},
        "per_instance": per_instance,
    })

    print(f"\n  scored {n} instance(s); skipped {len(skipped)}")
    print(f"\n  {'system':12}{'P@1':>9}{'P@5':>9}{'MRR':>9}   (n={n})")
    summary: Dict[str, float] = {}
    for system, label in (("bm25", "BM25"), ("ppr", "Symbol+PPR")):
        p1v, p5v, mrr = (float(np.mean([p[system][i] for p in per_instance]))
                         for i in range(3))
        summary[system] = mrr
        print(f"  {label:12}{p1v*100:8.2f}%{p5v*100:8.2f}%{mrr:9.4f}")
        for metric, value in (("p_at_1", p1v), ("p_at_5", p5v), ("mrr", mrr)):
            ci = rec.bootstrap_ci([p[system][("p_at_1", "p_at_5", "mrr").index(metric)]
                                   for p in per_instance], iterations=2000)
            scale = 100 if metric != "mrr" else 1
            rec.record(f"swebench_retrieval_{metric}_{system}", round(value * scale, 4),
                       "%" if metric != "mrr" else "", art, sha,
                       f"{label} over SWE-bench Lite issue text, gold = patched file",
                       n=n, ci95=[round(c * scale, 4) for c in ci])

    delta = summary["ppr"] - summary["bm25"]
    rec.record("swebench_retrieval_mrr_delta", round(delta, 5), "", art, sha,
               "paired difference in MRR on real issues", n=n)
    rec.record("swebench_retrieval_instances", n, "n", art, sha,
               "SWE-bench Lite instances with a gold file present in the corpus")
    rec.record("swebench_retrieval_median_corpus_files",
               float(np.median([p["corpus_files"] for p in per_instance])), "n", art, sha,
               "median Python files in a repository at its base commit", n=n)

    verdict = "does not improve" if delta <= 0 else "improves"
    print(f"\n  symbol-graph diffusion {verdict} MRR on real issues: delta={delta:+.4f}")

    rec.finalize()
    print("\n  NOTE: six repositories, chosen by clone size; django and sympy carry")
    print("  more than half of SWE-bench Lite and are absent. This measures file")
    print("  localisation from issue text, not issue resolution -- no patch was")
    print("  generated and no test was run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
