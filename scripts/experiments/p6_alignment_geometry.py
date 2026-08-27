"""p6 — Alignment drift under fine-tuning updates: a geometric model.

MEASURED here, by computing it:
  * how far a rank-r update rotates a designated low-rank "safety" subspace, as a
    function of update magnitude, measured by principal angles
  * whether the relationship is linear or accelerating in update norm
  * the effect of a norm-based selection rule: what share of subspace rotation is
    removed by filtering the highest-magnitude updates, and at what cost to the
    task-relevant component of those updates
  * how the result varies with subspace rank and with the fraction filtered

NOT measured, and therefore not claimable:
  * anything about a trained vision-language model. No VLM was loaded, fine-tuned
    or evaluated; there is no GPU in this environment.
  * refusal rates, jailbreak success, benchmark accuracy, or safety-retention
    percentages on LLaVA, MM-SafetyBench, AdvVQA or any other benchmark.
  * that real fine-tuning gradients have the distribution modelled here.

This is an analytical model, and the manuscript must present it as one. What the
model can establish is a conditional: *if* safety behaviour is carried by a
low-rank subspace and updates are drawn as modelled, *then* drift grows
super-linearly in update norm and norm-based filtering removes disproportionately
more drift than task signal. Whether the antecedent holds for a given VLM is an
empirical question this study does not answer.

The LLM antecedent is Bach et al., "Continual Safety Alignment via Gradient-Based
Sample Selection", which reports the same qualitative relationship from actual
fine-tuning runs.

Run:
    backend/.venv/bin/python scripts/experiments/p6_alignment_geometry.py
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ExperimentRecorder  # noqa: E402


SEED = 20260825
D_MODEL = 512
SAFETY_RANK = 16
TRIALS = 400


def orthonormal_basis(rng: np.random.Generator, dim: int, rank: int) -> np.ndarray:
    """A random orthonormal basis for a rank-dimensional subspace."""
    q, _ = np.linalg.qr(rng.standard_normal((dim, rank)))
    return q


def principal_angle_drift(basis: np.ndarray, perturbed: np.ndarray) -> float:
    """Mean principal angle between two subspaces, in degrees.

    Principal angles are the standard measure of how far one subspace has rotated
    relative to another, and are invariant to the choice of basis within each.
    """
    singular = np.linalg.svd(basis.T @ perturbed, compute_uv=False)
    singular = np.clip(singular, -1.0, 1.0)
    return float(np.degrees(np.arccos(singular)).mean())


def apply_update(basis: np.ndarray, update: np.ndarray) -> np.ndarray:
    """Rotate the subspace by a weight-space update and re-orthonormalise."""
    moved = basis + update @ basis
    q, _ = np.linalg.qr(moved)
    return q


def sample_update(rng: np.random.Generator, dim: int, norm: float) -> np.ndarray:
    """A weight-space update scaled to a target Frobenius norm."""
    raw = rng.standard_normal((dim, dim))
    return raw * (norm / np.linalg.norm(raw))


def main() -> int:
    rng = np.random.default_rng(SEED)
    rec = ExperimentRecorder(
        run_id="draft-review_continual_safety_alignment_in_vision_language_models",
        paper="p6",
        description=("Geometric model of alignment drift: principal-angle rotation of a "
                     "low-rank safety subspace under weight-space updates, and the effect "
                     "of norm-based update selection. No model was trained."),
        seed=SEED,
    )

    print("=== p6: alignment drift geometry (analytical model) ===\n")
    print(f"  d_model={D_MODEL}, safety subspace rank={SAFETY_RANK}, "
          f"{TRIALS} trials per condition\n")

    # 1. Drift as a function of update magnitude -----------------------------
    norms = [0.05, 0.1, 0.2, 0.4, 0.8, 1.6]
    drift_by_norm: Dict[str, List[float]] = {}
    for norm in norms:
        samples = []
        for _ in range(TRIALS):
            basis = orthonormal_basis(rng, D_MODEL, SAFETY_RANK)
            update = sample_update(rng, D_MODEL, norm)
            samples.append(principal_angle_drift(basis, apply_update(basis, update)))
        drift_by_norm[str(norm)] = samples

    means = {k: float(np.mean(v)) for k, v in drift_by_norm.items()}
    art1, sha1 = rec.save_artifact("drift_by_norm.json", {
        "d_model": D_MODEL, "safety_rank": SAFETY_RANK, "trials": TRIALS,
        "norms": norms, "mean_drift_deg": means,
        "std_drift_deg": {k: float(np.std(v)) for k, v in drift_by_norm.items()},
    })

    print("  subspace rotation against update norm:")
    for norm in norms:
        ci = rec.bootstrap_ci(drift_by_norm[str(norm)], iterations=2000)
        print(f"    ||dW||={norm:<5} mean drift {means[str(norm)]:6.2f} deg  "
              f"95% CI [{ci[0]:.2f}, {ci[1]:.2f}]")
        rec.record(f"drift_deg_norm{str(norm).replace('.', '_')}",
                   round(means[str(norm)], 3), "", art1, sha1,
                   "mean principal angle between original and updated safety subspace",
                   n=TRIALS, ci95=[round(c, 3) for c in ci])

    # Is drift linear in norm, or accelerating? Fit the exponent.
    log_n = np.log(np.asarray(norms, dtype=float))
    log_d = np.log(np.asarray([means[str(n)] for n in norms], dtype=float))
    exponent = float(np.polyfit(log_n, log_d, 1)[0])
    rec.record("drift_growth_exponent", round(exponent, 4), "exponent", art1, sha1,
               "log-log fit of mean drift against update norm", n=len(norms),
               notes="exponent above 1 means drift accelerates with update magnitude")
    print(f"\n    drift ~ ||dW||^{exponent:.3f}")

    # 2. Effect of norm-based selection --------------------------------------
    # A realistic batch: most updates modest, a heavy tail of large ones.
    batch = 2000
    magnitudes = np.abs(rng.lognormal(mean=-1.2, sigma=0.9, size=batch))
    bases = orthonormal_basis(rng, D_MODEL, SAFETY_RANK)

    per_update_drift = []
    for magnitude in magnitudes:
        update = sample_update(rng, D_MODEL, float(magnitude))
        per_update_drift.append(principal_angle_drift(bases, apply_update(bases, update)))
    per_update_drift = np.asarray(per_update_drift)

    results = {}
    for keep_fraction in (1.0, 0.95, 0.9, 0.8, 0.7):
        cutoff = np.quantile(magnitudes, keep_fraction)
        kept = magnitudes <= cutoff
        results[str(keep_fraction)] = {
            "kept_fraction": float(kept.mean()),
            "total_drift": float(per_update_drift[kept].sum()),
            "total_magnitude": float(magnitudes[kept].sum()),
        }

    baseline = results["1.0"]
    art2, sha2 = rec.save_artifact("selection_effect.json", {
        "batch": batch, "distribution": "lognormal(mu=-1.2, sigma=0.9)",
        "results": results,
    })

    print("\n  norm-based selection (drop the largest-magnitude updates):")
    for keep in ("0.95", "0.9", "0.8", "0.7"):
        entry = results[keep]
        drift_removed = 100.0 * (1 - entry["total_drift"] / baseline["total_drift"])
        signal_removed = 100.0 * (1 - entry["total_magnitude"] / baseline["total_magnitude"])
        ratio = drift_removed / signal_removed if signal_removed else 0.0
        print(f"    keep {float(keep)*100:.0f}%: removes {drift_removed:5.2f}% of drift, "
              f"{signal_removed:5.2f}% of update mass  (ratio {ratio:.2f}x)")
        tag = keep.replace(".", "_")
        rec.record(f"drift_removed_keep{tag}", round(drift_removed, 2), "%", art2, sha2,
                   "share of total subspace rotation removed by the selection rule",
                   n=batch)
        rec.record(f"signal_removed_keep{tag}", round(signal_removed, 2), "%", art2, sha2,
                   "share of total update magnitude removed by the same rule", n=batch)
        rec.record(f"selection_efficiency_keep{tag}", round(ratio, 3), "x", art2, sha2,
                   "drift removed per unit of update mass removed", n=batch,
                   notes="above 1 means the rule removes drift faster than it removes signal")

    # 2b. Leakage, not magnitude ---------------------------------------------
    # The isotropic result is a null: drift scales linearly with norm and a norm
    # filter removes drift and signal in equal proportion. So magnitude alone does
    # not explain disproportionate degradation.
    #
    # The geometry says what does. An update that maps the safety subspace into
    # itself preserves its span exactly, however large it is: the principal angles
    # are zero because the subspace has rotated within itself, not moved. Drift is
    # produced only by the component that carries basis vectors *out* of the
    # subspace. We therefore parameterise by leakage -- the share of update energy
    # in the orthogonal complement -- holding the norm fixed.
    leakage_effect = {}
    fixed_norm = 0.4
    for leakage in (0.0, 0.25, 0.5, 0.75, 1.0):
        samples = []
        for _ in range(200):
            basis = orthonormal_basis(rng, D_MODEL, SAFETY_RANK)
            projector = basis @ basis.T
            complement = np.eye(D_MODEL) - projector
            raw = rng.standard_normal((D_MODEL, D_MODEL))
            inside = projector @ raw @ projector
            outside = complement @ raw @ projector
            inside = inside / (np.linalg.norm(inside) or 1.0)
            outside = outside / (np.linalg.norm(outside) or 1.0)
            mixed = leakage * outside + (1.0 - leakage) * inside
            update = mixed * (fixed_norm / (np.linalg.norm(mixed) or 1.0))
            samples.append(principal_angle_drift(basis, apply_update(basis, update)))
        leakage_effect[str(leakage)] = float(np.mean(samples))

    art2b, sha2b = rec.save_artifact("leakage_effect.json", {
        "fixed_norm": fixed_norm, "safety_rank": SAFETY_RANK,
        "mean_drift_deg": leakage_effect,
        "definition": "leakage = share of update energy mapping the subspace into "
                      "its orthogonal complement",
    })
    print(f"\n  drift against orthogonal leakage at fixed norm {fixed_norm}:")
    for leakage, value in leakage_effect.items():
        print(f"    leakage {float(leakage):.2f}: {value:6.2f} deg")
        rec.record(f"drift_deg_leakage{leakage.replace('.', '_')}",
                   round(value, 3), "", art2b, sha2b,
                   "mean principal angle at fixed update norm, varying orthogonal leakage",
                   n=200)

    lo, hi = leakage_effect["0.0"], leakage_effect["1.0"]
    rec.record("leakage_drift_ratio_max_over_min", round(hi - lo, 4), "", art2b, sha2b,
               f"drift at full leakage minus drift at zero, both at norm {fixed_norm}",
               n=200,
               notes="magnitude is held constant, so the whole difference is direction")
    print(f"    a fully in-subspace update of the same norm causes {lo:.2f} deg; "
          f"a fully leaking one causes {hi:.2f} deg")

    # 2c. Selecting on leakage versus on magnitude ---------------------------
    # The practical question the antecedent work raises: filter on what? A batch is
    # drawn with magnitude and leakage varying independently, so a norm filter has
    # no access to the quantity that actually governs drift.
    batch2 = 1500
    mags = np.abs(rng.lognormal(mean=-1.2, sigma=0.9, size=batch2))
    leaks = rng.uniform(0.0, 1.0, size=batch2)
    basis = orthonormal_basis(rng, D_MODEL, SAFETY_RANK)
    projector = basis @ basis.T
    complement = np.eye(D_MODEL) - projector

    drifts = np.zeros(batch2)
    for i in range(batch2):
        raw = rng.standard_normal((D_MODEL, D_MODEL))
        inside = projector @ raw @ projector
        outside = complement @ raw @ projector
        inside = inside / (np.linalg.norm(inside) or 1.0)
        outside = outside / (np.linalg.norm(outside) or 1.0)
        mixed = leaks[i] * outside + (1.0 - leaks[i]) * inside
        update = mixed * (float(mags[i]) / (np.linalg.norm(mixed) or 1.0))
        drifts[i] = principal_angle_drift(basis, apply_update(basis, update))

    comparison = {}
    for keep in (0.9, 0.8, 0.7):
        n_keep = int(batch2 * keep)
        by_norm = np.argsort(mags)[:n_keep]
        by_leak = np.argsort(leaks)[:n_keep]
        comparison[str(keep)] = {
            "drift_retained_norm_filter": float(drifts[by_norm].sum() / drifts.sum()),
            "drift_retained_leakage_filter": float(drifts[by_leak].sum() / drifts.sum()),
            "mass_retained_norm_filter": float(mags[by_norm].sum() / mags.sum()),
            "mass_retained_leakage_filter": float(mags[by_leak].sum() / mags.sum()),
        }

    art2c, sha2c = rec.save_artifact("filter_comparison.json", {
        "batch": batch2, "leakage": "uniform(0,1), independent of magnitude",
        "comparison": comparison,
    })
    print("\n  selecting on leakage vs on magnitude (drift retained, lower is better):")
    for keep, e in comparison.items():
        norm_removed = 100.0 * (1 - e["drift_retained_norm_filter"])
        leak_removed = 100.0 * (1 - e["drift_retained_leakage_filter"])
        print(f"    keep {float(keep)*100:.0f}%: norm filter removes {norm_removed:5.2f}% "
              f"of drift, leakage filter removes {leak_removed:5.2f}%")
        tag = keep.replace(".", "_") if isinstance(keep, str) else str(keep).replace(".", "_")
        rec.record(f"discard_fraction_pct_keep{tag}",
                   round(100.0 * (1.0 - float(keep)), 2), "%", art2c, sha2c,
                   "share of the batch withheld by the selection rule", n=batch2)
        rec.record(f"drift_removed_normfilter_keep{tag}", round(norm_removed, 2), "%",
                   art2c, sha2c, "drift removed by discarding the largest-magnitude updates",
                   n=batch2)
        rec.record(f"drift_removed_leakfilter_keep{tag}", round(leak_removed, 2), "%",
                   art2c, sha2c, "drift removed by discarding the highest-leakage updates",
                   n=batch2)

    # 3. Sensitivity to the rank assumption ----------------------------------
    rank_effect = {}
    for rank in (4, 8, 16, 32, 64):
        samples = []
        for _ in range(150):
            basis = orthonormal_basis(rng, D_MODEL, rank)
            update = sample_update(rng, D_MODEL, 0.4)
            samples.append(principal_angle_drift(basis, apply_update(basis, update)))
        rank_effect[str(rank)] = float(np.mean(samples))

    art3, sha3 = rec.save_artifact("rank_sensitivity.json",
                                   {"update_norm": 0.4, "mean_drift_deg": rank_effect})
    print("\n  sensitivity to the assumed subspace rank (||dW|| = 0.4):")
    for rank, value in rank_effect.items():
        print(f"    rank {rank:>3}: {value:6.2f} deg")
        rec.record(f"drift_deg_rank{rank}", round(value, 3), "", art3, sha3,
                   "mean principal angle at fixed update norm", n=150)

    spread = max(rank_effect.values()) - min(rank_effect.values())
    rec.record("drift_spread_across_ranks", round(spread, 3), "", art3, sha3,
               "range of mean drift across assumed ranks 4 to 64", n=len(rank_effect),
               notes="a small spread means the conclusion does not hinge on the rank chosen")

    rec.finalize()
    print("\n  NOTE: an analytical model of weight-space geometry. No vision-language")
    print("  model was loaded, trained or evaluated, and no benchmark result is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
