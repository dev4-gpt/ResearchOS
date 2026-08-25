"""p5 — Multi-agent coordination topologies: simulation study.

What this measures, and what it does not.

MEASURED here, by running the code below:
  * exact message counts per topology as agent count N grows, and the fitted
    growth exponent (the O(N) vs O(N^2) claim)
  * cascade failure rates under independent per-agent faults, by Monte Carlo
  * coordination latency as the critical path through each topology
  * steady-state availability from a discrete-time Markov chain, solved exactly
  * context/token growth implied by the message pattern, under a stated model

NOT measured, and therefore not claimable from this run:
  * anything about real organisations, production pipelines or live telemetry
  * dollar costs, payback periods, labour multipliers, security incident rates
  * SLA rates observed in deployment

The manuscript's original framing — 45 enterprises, 318 production pipelines,
121M monthly invocations captured via OpenTelemetry — describes a field study
that did not happen. Those numbers cannot be recovered by simulation and must be
removed. What follows supports the far narrower, true claim: under an explicit
fault and messaging model, hierarchical coordination scales linearly and damps
cascades, while a peer-to-peer mesh does neither.

Run:
    backend/.venv/bin/python scripts/experiments/p5_coordination_topologies.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ExperimentRecorder  # noqa: E402


SEED = 20260825
TOPOLOGIES = ("mesh", "contract_net", "blackboard", "hierarchical")


# --------------------------------------------------------------- message model

def message_count(topology: str, n: int, branching: int = 4) -> int:
    """Exact number of coordination messages to complete one task with n agents.

    Counted from the protocol definition, not estimated:
      mesh          every agent informs every other agent: n(n-1)
      contract_net  announce to n-1, collect n-1 bids, one award: 2(n-1)+1
      blackboard    each agent writes once and reads the board once: 2n
      hierarchical  one message down and one up each tree edge: 2(n-1)
    """
    if topology == "mesh":
        return n * (n - 1)
    if topology == "contract_net":
        return 2 * (n - 1) + 1
    if topology == "blackboard":
        return 2 * n
    if topology == "hierarchical":
        return 2 * (n - 1)
    raise ValueError(topology)


def coordination_depth(topology: str, n: int, branching: int = 4) -> int:
    """Critical-path hop count, which sets latency under equal per-hop cost."""
    if topology == "mesh":
        return 1                      # one broadcast round, but n(n-1) messages
    if topology == "contract_net":
        return 3                      # announce -> bid -> award
    if topology == "blackboard":
        return 2                      # write -> read
    if topology == "hierarchical":
        return 2 * max(1, int(np.ceil(np.log(max(n, 2)) / np.log(branching))))
    raise ValueError(topology)


def fit_growth_exponent(sizes: list, counts: list) -> float:
    """Fit counts ~ N^k in log-log space and return k."""
    log_n = np.log(np.asarray(sizes, dtype=float))
    log_c = np.log(np.asarray(counts, dtype=float))
    slope, _ = np.polyfit(log_n, log_c, 1)
    return float(slope)


# ---------------------------------------------------------------- fault model

def simulate_cascades(topology: str, n: int, p_fail: float, trials: int,
                      rng: np.random.Generator, branching: int = 4) -> np.ndarray:
    """Monte Carlo cascade simulation.

    Each agent fails independently with probability ``p_fail``. A failure then
    propagates to everyone that depends on the failed agent:

      mesh          no supervisor, so a fault reaches every peer it messaged
      contract_net  the failed bidder's task is re-let, containing the fault
      blackboard    a corrupt write is read by all subsequent readers
      hierarchical  the parent retries the child, containing the subtree

    Returns the fraction of agents affected in each trial.
    """
    affected = np.zeros(trials, dtype=float)
    for trial in range(trials):
        failed = rng.random(n) < p_fail
        primary = int(failed.sum())
        if primary == 0:
            affected[trial] = 0.0
            continue

        if topology == "mesh":
            # Unsupervised broadcast: one fault contaminates every peer.
            hit = n if primary else 0
        elif topology == "blackboard":
            # A corrupt entry is visible to every later reader; expected half.
            hit = min(n, primary + int(0.5 * (n - primary)))
        elif topology == "contract_net":
            # Re-letting contains the fault to the failed bidder plus its award.
            hit = min(n, primary * 2)
        else:  # hierarchical
            # Supervisor retry barrier: fault contained to the failed subtree.
            subtree = max(1, int(np.ceil(n / branching)))
            hit = min(n, primary * 1 + (primary * (subtree - 1) if primary > branching else 0))
        affected[trial] = hit / n
    return affected


# ----------------------------------------------------- markov availability

def steady_state_availability(mttf_steps: float, mttr_steps: float) -> float:
    """Exact steady state of a 2-state DTMC {UP, DOWN}, solved by eigenvector.

    Not a closed-form shortcut: the transition matrix is built and its stationary
    distribution is recovered from the left eigenvector for eigenvalue 1, so the
    number reported is the one linear algebra gives.
    """
    lambda_fail = 1.0 / mttf_steps
    mu_repair = 1.0 / mttr_steps
    P = np.array([[1 - lambda_fail, lambda_fail],
                  [mu_repair, 1 - mu_repair]])
    values, vectors = np.linalg.eig(P.T)
    stationary = np.real(vectors[:, np.argmin(np.abs(values - 1.0))])
    stationary = stationary / stationary.sum()
    return float(stationary[0])


def main() -> int:
    rng = np.random.default_rng(SEED)
    rec = ExperimentRecorder(
        run_id="draft-review_enterprise_adoption_of_multi_agent_ai_systems_infr",
        paper="p5",
        description=("Simulation study of four multi-agent coordination topologies: "
                     "message complexity, cascade containment, coordination depth, "
                     "and DTMC steady-state availability."),
        seed=SEED,
    )

    print("=== p5: coordination topology simulation ===\n")

    # 1. Message complexity scaling ------------------------------------------
    sizes = [4, 8, 16, 32, 64, 128, 256]
    scaling = {t: [message_count(t, n) for n in sizes] for t in TOPOLOGIES}
    exponents = {t: fit_growth_exponent(sizes, scaling[t]) for t in TOPOLOGIES}

    art, sha = rec.save_artifact("message_scaling.json",
                                 {"sizes": sizes, "counts": scaling, "exponents": exponents})
    print("  message-count growth exponent (counts ~ N^k):")
    for topology in TOPOLOGIES:
        print(f"    {topology:14} k = {exponents[topology]:.4f}")
        rec.record(f"growth_exponent_{topology}", exponents[topology], "exponent",
                   art, sha, "log-log fit of exact protocol message counts",
                   n=len(sizes),
                   notes="counted from protocol definition, not sampled")

    n_ref = 64
    for topology in TOPOLOGIES:
        rec.record(f"messages_at_n{n_ref}_{topology}", message_count(topology, n_ref),
                   "messages", art, sha, "exact protocol message count", n=n_ref)

    mesh_msgs = message_count("mesh", n_ref)
    hier_msgs = message_count("hierarchical", n_ref)
    reduction = 100.0 * (mesh_msgs - hier_msgs) / mesh_msgs
    rec.record("message_reduction_hier_vs_mesh", round(reduction, 2), "%", art, sha,
               f"exact counts at N={n_ref}: {mesh_msgs} vs {hier_msgs}", n=n_ref)
    print(f"\n  at N={n_ref}: mesh={mesh_msgs} msgs, hierarchical={hier_msgs} msgs "
          f"({reduction:.1f}% fewer)")

    # 2. Cascade containment -------------------------------------------------
    trials, p_fail = 20000, 0.02
    cascade_rates, cascade_samples = {}, {}
    for topology in TOPOLOGIES:
        samples = simulate_cascades(topology, n_ref, p_fail, trials, rng)
        cascade_samples[topology] = samples
        cascade_rates[topology] = float(samples.mean())

    art2, sha2 = rec.save_artifact("cascade_trials.json", {
        "n_agents": n_ref, "p_agent_failure": p_fail, "trials": trials,
        "mean_fraction_affected": cascade_rates,
        "histogram": {t: np.histogram(s, bins=20, range=(0, 1))[0].tolist()
                      for t, s in cascade_samples.items()},
    })
    print(f"\n  cascade containment (N={n_ref}, p_fail={p_fail}, {trials} trials):")
    for topology in TOPOLOGIES:
        pct = cascade_rates[topology] * 100
        ci = rec.bootstrap_ci(cascade_samples[topology].tolist(), iterations=2000)
        print(f"    {topology:14} {pct:6.2f}% of agents affected  "
              f"95% CI [{ci[0]*100:.2f}, {ci[1]*100:.2f}]")
        rec.record(f"cascade_rate_{topology}", round(pct, 2), "%", art2, sha2,
                   "Monte Carlo, independent per-agent faults", n=trials,
                   ci95=[round(ci[0] * 100, 3), round(ci[1] * 100, 3)])

    stats = rec.welch_t(cascade_samples["mesh"].tolist(),
                        cascade_samples["hierarchical"].tolist())
    art3, sha3 = rec.save_artifact("cascade_significance.json", stats)
    print(f"\n    mesh vs hierarchical: t={stats['t']}, p={stats['p']:.3e}, "
          f"d={stats['cohens_d']}")
    rec.record("cascade_cohens_d_mesh_vs_hier", stats["cohens_d"], "d", art3, sha3,
               "Welch t-test on Monte Carlo samples", n=trials)
    rec.record("cascade_t_statistic", stats["t"], "t", art3, sha3,
               "Welch t-test on Monte Carlo samples", n=trials)

    # 3. Coordination depth --------------------------------------------------
    depths = {t: coordination_depth(t, n_ref) for t in TOPOLOGIES}
    art4, sha4 = rec.save_artifact("coordination_depth.json",
                                   {"n_agents": n_ref, "depth_hops": depths})
    print(f"\n  coordination depth at N={n_ref}: " +
          ", ".join(f"{t}={d}" for t, d in depths.items()))
    for topology, depth in depths.items():
        rec.record(f"coordination_depth_{topology}", depth, "hops", art4, sha4,
                   "critical path through protocol", n=n_ref)

    # 4. Availability --------------------------------------------------------
    availability = {}
    for label, (mttf, mttr) in {
        "mesh": (500.0, 20.0),
        "contract_net": (800.0, 12.0),
        "blackboard": (1200.0, 8.0),
        "hierarchical": (2000.0, 4.0),
    }.items():
        availability[label] = {
            "mttf_steps": mttf, "mttr_steps": mttr,
            "availability": steady_state_availability(mttf, mttr),
        }

    art5, sha5 = rec.save_artifact("dtmc_availability.json", availability)
    print("\n  DTMC steady-state availability (from stated MTTF/MTTR, eigenvector solve):")
    for topology, entry in availability.items():
        pct = entry["availability"] * 100
        print(f"    {topology:14} {pct:.4f}%  (MTTF={entry['mttf_steps']}, "
              f"MTTR={entry['mttr_steps']})")
        rec.record(f"availability_{topology}", round(pct, 4), "%", art5, sha5,
                   "2-state DTMC stationary distribution",
                   notes="derived from assumed MTTF/MTTR parameters, not observed uptime")

    # 5. Corollary 1: pipeline reliability with and without supervisor retry ----
    K, p_k, r_k, M = 5, 0.85, 0.90, 2
    mono = p_k ** K
    hier = (1.0 - (1.0 - p_k) * (1.0 - r_k) ** M) ** K
    art6, sha6 = rec.save_artifact("pipeline_reliability.json", {
        "stages_K": K, "worker_accuracy_p": p_k, "supervisor_recovery_r": r_k,
        "retries_M": M, "monolithic": mono, "hierarchical": hier,
    })
    print("\n  pipeline reliability (Corollary 1, evaluated from the stated formula):")
    print(f"    monolithic   R = {mono*100:.2f}%")
    print(f"    hierarchical R = {hier*100:.2f}%")
    rec.record("pipeline_reliability_monolithic", round(mono * 100, 2), "%", art6, sha6,
               f"p^K with p={p_k}, K={K}", n=K)
    rec.record("pipeline_reliability_hierarchical", round(hier * 100, 2), "%", art6, sha6,
               f"[1-(1-p)(1-r)^M]^K with p={p_k}, r={r_k}, M={M}, K={K}", n=K)

    rec.finalize()
    print("\n  NOTE: these are properties of the simulated protocols under the stated")
    print("  fault model. They are not observations of deployed systems, and no")
    print("  cost, payback or enterprise-adoption claim follows from them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
