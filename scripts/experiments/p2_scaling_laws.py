"""p2 — Parameter efficiency and compute scaling: analytic and simulated.

MEASURED here, by computing it:
  * Chinchilla-optimal parameter/token allocation across compute budgets, solved
    numerically from the compute constraint rather than quoted
  * exact KV-cache memory as a closed-form function of architecture and context,
    which is arithmetic and needs no hardware to be correct
  * low-rank adaptation subspace capacity: real SVD on real weight-shaped matrices,
    measuring reconstruction error against rank
  * MoE router load balance: simulated routing, with entropy and expert collapse
    measured over token streams

NOT measured, and therefore not claimable:
  * the manuscript's "N = 892 multi-node GPU cluster configurations" — no GPU was
    used and no cluster was benchmarked
  * observed throughput, wall-clock latency, or realised VRAM on any accelerator
  * "68.2% memory footprint reduction while preserving 98.4% of benchmark
    performance" — the second half needs benchmark runs on trained models

Memory *formulas* are exact and reported as such. Anything requiring a model to be
run on a device is absent by construction.

Run:
    backend/.venv/bin/python scripts/experiments/p2_scaling_laws.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ExperimentRecorder  # noqa: E402


SEED = 20260825

# Hoffmann et al. parametric loss form. Coefficients are the published fit; they
# are inputs to this computation, not something measured here.
CHINCHILLA = {"E": 1.69, "A": 406.4, "B": 410.7, "alpha": 0.34, "beta": 0.28}


def chinchilla_loss(n_params: float, n_tokens: float) -> float:
    c = CHINCHILLA
    return c["E"] + c["A"] / (n_params ** c["alpha"]) + c["B"] / (n_tokens ** c["beta"])


def optimal_allocation(flops: float) -> dict:
    """Minimise the parametric loss subject to C = 6ND, by scanning the constraint.

    Solved numerically: for each candidate parameter count the token budget is
    fixed by the compute constraint, so the search is one-dimensional.
    """
    candidates = np.logspace(7, 12, 4000)
    tokens = flops / (6.0 * candidates)
    losses = np.array([chinchilla_loss(n, d) for n, d in zip(candidates, tokens)])
    best = int(np.argmin(losses))
    return {
        "flops": flops,
        "optimal_params": float(candidates[best]),
        "optimal_tokens": float(tokens[best]),
        "loss": float(losses[best]),
        "tokens_per_param": float(tokens[best] / candidates[best]),
    }


def kv_cache_bytes(layers: int, heads_kv: int, head_dim: int, context: int,
                   batch: int, dtype_bytes: int = 2) -> int:
    """Exact KV cache size. Two tensors (K and V) per layer per token."""
    return 2 * layers * heads_kv * head_dim * context * batch * dtype_bytes


def main() -> int:
    rng = np.random.default_rng(SEED)
    rec = ExperimentRecorder(
        run_id="draft-review_architectural_dynamics_long_12_page",
        paper="p2",
        description=("Analytic and simulated study of compute-optimal allocation, "
                     "KV-cache memory scaling, low-rank adaptation capacity, and MoE "
                     "router load balance. No accelerator was used."),
        seed=SEED,
    )

    print("=== p2: scaling laws (analytic + simulated) ===\n")

    # 1. Compute-optimal allocation ------------------------------------------
    budgets = [1e19, 1e20, 1e21, 1e22, 1e23, 1e24]
    allocations = [optimal_allocation(c) for c in budgets]
    ratios = [a["tokens_per_param"] for a in allocations]

    art1, sha1 = rec.save_artifact("chinchilla_allocation.json", {
        "coefficients": CHINCHILLA, "allocations": allocations,
    })
    print("  compute-optimal allocation (numerically minimised under C = 6ND):")
    for a in allocations:
        print(f"    C={a['flops']:.0e}  N={a['optimal_params']:.3e} params  "
              f"D={a['optimal_tokens']:.3e} tokens  D/N={a['tokens_per_param']:.1f}")
    mean_ratio = float(np.mean(ratios))
    rec.record("chinchilla_tokens_per_param_mean", round(mean_ratio, 3), "x",
               art1, sha1, "mean D/N over six compute budgets", n=len(budgets),
               notes="derived from published Hoffmann coefficients, not refitted here")
    print(f"\n    mean tokens/param across budgets: {mean_ratio:.2f}")

    # 2. KV cache scaling ----------------------------------------------------
    configs = {
        "MHA-7B":  dict(layers=32, heads_kv=32, head_dim=128),
        "GQA-7B":  dict(layers=32, heads_kv=8,  head_dim=128),
        "MQA-7B":  dict(layers=32, heads_kv=1,  head_dim=128),
        "MHA-70B": dict(layers=80, heads_kv=64, head_dim=128),
        "GQA-70B": dict(layers=80, heads_kv=8,  head_dim=128),
    }
    contexts = [2048, 8192, 32768, 131072]
    kv_table = {
        name: {str(ctx): kv_cache_bytes(context=ctx, batch=1, **cfg) / 2**30
               for ctx in contexts}
        for name, cfg in configs.items()
    }
    art2, sha2 = rec.save_artifact("kv_cache_scaling.json",
                                   {"configs": configs, "contexts": contexts,
                                    "gib": kv_table})
    print("\n  KV cache (GiB, batch=1, fp16) — exact arithmetic:")
    print(f"    {'config':10}" + "".join(f"{c:>12}" for c in contexts))
    for name, row in kv_table.items():
        print(f"    {name:10}" + "".join(f"{row[str(c)]:>12.3f}" for c in contexts))

    gqa_saving = 100.0 * (1 - kv_table["GQA-7B"]["32768"] / kv_table["MHA-7B"]["32768"])
    mqa_saving = 100.0 * (1 - kv_table["MQA-7B"]["32768"] / kv_table["MHA-7B"]["32768"])
    rec.record("kv_reduction_gqa_vs_mha", round(gqa_saving, 2), "%", art2, sha2,
               "exact KV cache ratio at 32k context, 7B shape")
    rec.record("kv_reduction_mqa_vs_mha", round(mqa_saving, 2), "%", art2, sha2,
               "exact KV cache ratio at 32k context, 7B shape")
    rec.record("kv_cache_gib_mha7b_128k",
               round(kv_table["MHA-7B"]["131072"], 4), "bytes", art2, sha2,
               "exact KV cache at 128k context")
    print(f"\n    GQA vs MHA at 32k: {gqa_saving:.1f}% smaller cache; "
          f"MQA vs MHA: {mqa_saving:.1f}%")

    # 2b. KV budget for the 70B-shaped configuration the manuscript tabulates --
    # The manuscript's own table captions batch size 32 while its values correspond
    # to a single sequence. Recomputing settles which is right.
    layers_70b, d_model_70b, dtype_bytes = 80, 8192, 2
    budget_contexts = [4096, 16384, 32768, 65536, 131072]
    h100_gib = 80.0
    budget = {}
    for ctx in budget_contexts:
        per_seq = 2 * layers_70b * d_model_70b * ctx * dtype_bytes
        budget[str(ctx)] = {
            "batch1_gib": per_seq / 2**30,
            "batch32_gib": per_seq * 32 / 2**30,
            "pct_of_h100_batch1": 100.0 * (per_seq / 2**30) / h100_gib,
        }
    art2b, sha2b = rec.save_artifact("kv_budget_70b.json", {
        "layers": layers_70b, "d_model": d_model_70b, "dtype_bytes": dtype_bytes,
        "h100_gib": h100_gib, "by_context": budget,
    })
    print("\n  KV budget, 80 layers / d_model 8192 / bf16 (manuscript Table 1 shape):")
    for ctx in budget_contexts:
        e = budget[str(ctx)]
        print(f"    ctx {ctx:>7}: {e['batch1_gib']:8.2f} GiB (batch 1), "
              f"{e['pct_of_h100_batch1']:6.1f}% of an 80 GiB H100")
        rec.record(f"kv_budget_gib_ctx{ctx}", round(e["batch1_gib"], 2), "bytes",
                   art2b, sha2b, "exact KV arithmetic, batch 1, bf16")
        rec.record(f"kv_budget_pct_h100_ctx{ctx}", round(e["pct_of_h100_batch1"], 1),
                   "%", art2b, sha2b, "share of an 80 GiB H100, batch 1")

    # 3. Low-rank adaptation capacity ---------------------------------------
    d_model = 1024
    base = rng.standard_normal((d_model, d_model)) / np.sqrt(d_model)
    # A realistic update is low-rank-ish plus noise, not white noise.
    true_rank = 64
    U = rng.standard_normal((d_model, true_rank)) / np.sqrt(d_model)
    V = rng.standard_normal((true_rank, d_model)) / np.sqrt(d_model)
    delta = U @ V + 0.02 * rng.standard_normal((d_model, d_model)) / np.sqrt(d_model)

    singular = np.linalg.svd(delta, compute_uv=False)
    total_energy = float((singular ** 2).sum())
    ranks = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    captured = {r: float((singular[:r] ** 2).sum() / total_energy) for r in ranks}

    art3, sha3 = rec.save_artifact("lora_subspace.json", {
        "d_model": d_model, "true_rank": true_rank,
        "singular_values": singular.tolist(),
        "energy_captured_by_rank": {str(k): v for k, v in captured.items()},
    })
    print(f"\n  low-rank capacity (d_model={d_model}, planted rank={true_rank}), "
          "measured by SVD:")
    for r in ranks:
        params_pct = 100.0 * (2 * d_model * r) / (d_model * d_model)
        print(f"    rank {r:>3}: {captured[r]*100:6.2f}% of update energy, "
              f"{params_pct:5.2f}% of dense parameters")
        rec.record(f"lora_energy_rank{r}", round(captured[r] * 100, 3), "%", art3, sha3,
                   "SVD energy captured by rank-r truncation", n=d_model)
    # The manuscript also instantiates the capacity fraction at d = k = 8192, r = 16.
    for d_big, r_big in ((8192, 16),):
        frac = 100.0 * (2 * d_big * r_big) / (d_big * d_big)
        rec.record(f"lora_param_fraction_d{d_big}_r{r_big}", round(frac, 2), "%",
                   art3, sha3, f"2*d*r / d^2 at d=k={d_big}, r={r_big}")
        print(f"    capacity fraction at d=k={d_big}, r={r_big}: {frac:.2f}%")

    rank64_params = 100.0 * (2 * d_model * 64) / (d_model * d_model)
    rec.record("lora_param_fraction_rank64", round(rank64_params, 3), "%", art3, sha3,
               "2*d*r / d^2 at r=64")

    # 4. MoE routing entropy -------------------------------------------------
    n_experts, n_tokens = 64, 200_000
    results = {}
    for label, temperature in {"uncorrected": 0.0, "noisy_topk": 0.6,
                               "load_balanced": 1.4}.items():
        logits = rng.standard_normal((n_tokens, n_experts))
        # A stronger prior on early experts models the collapse the paper describes.
        logits[:, :8] += 2.0
        if temperature > 0:
            logits = logits + temperature * rng.standard_normal(logits.shape)
        assign = np.argmax(logits, axis=1)
        counts = np.bincount(assign, minlength=n_experts).astype(float)
        p = counts / counts.sum()
        nz = p[p > 0]
        entropy = float(-(nz * np.log(nz)).sum())
        results[label] = {
            "entropy_nats": entropy,
            "max_entropy_nats": float(np.log(n_experts)),
            "normalised_entropy": entropy / float(np.log(n_experts)),
            "max_expert_share": float(p.max()),
            "dead_experts": int((counts == 0).sum()),
        }

    art4, sha4 = rec.save_artifact("moe_routing.json",
                                   {"n_experts": n_experts, "n_tokens": n_tokens,
                                    "results": results})
    print(f"\n  MoE routing over {n_tokens:,} tokens, {n_experts} experts:")
    for label, entry in results.items():
        print(f"    {label:14} H={entry['entropy_nats']:.4f} nats "
              f"({entry['normalised_entropy']*100:.1f}% of max), "
              f"max share {entry['max_expert_share']*100:.2f}%, "
              f"dead {entry['dead_experts']}")
        rec.record(f"routing_entropy_{label}", round(entry["entropy_nats"], 4),
                   "", art4, sha4, "Shannon entropy of expert assignment counts",
                   n=n_tokens)
        rec.record(f"dead_experts_{label}", entry["dead_experts"], "n", art4, sha4,
                   "experts receiving zero tokens", n=n_experts)

    rec.finalize()
    print("\n  NOTE: allocation and cache figures are exact arithmetic; SVD and routing")
    print("  are simulations. No GPU was used and no model was trained or benchmarked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
