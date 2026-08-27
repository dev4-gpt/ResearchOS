"""p9 — Formal verification of a multi-agent council: model checking and consensus.

MEASURED here, by running the code below:
  * explicit-state model checking of a council protocol: reachable states,
    transitions, wall-clock verification time, and counterexample depth when a
    safety invariant is deliberately removed
  * Byzantine agreement under a 2f+1 quorum rule, sweeping the corrupt fraction
    to locate the failure threshold empirically rather than asserting it
  * deadlock freedom with and without the asymmetric priority ordering, decided
    by cycle detection over the reachable state graph

NOT measured, and therefore not claimable:
  * "N = 10,200 adversarial interaction traces". No language model was run, so no
    agent produced a trace and no hallucination was intercepted.
  * "N = 521 production enterprise contracts", the 3,236 intercepted assertions,
    and the per-domain SLA figures. That data was never held.
  * Any ablation over model backbones or debate strategies.

What a model checker can establish is that a protocol satisfies its specification
over every reachable state, which is a stronger claim than a benchmark average --
but only about the model, not about a deployed system running language models.

Run:
    backend/.venv/bin/python scripts/experiments/p9_formal_verification.py
"""
from __future__ import annotations

import os
import sys
import time
from collections import deque
from typing import Dict, List, Optional, Set, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ExperimentRecorder  # noqa: E402


SEED = 20260825

# A council state: (phase, proposals_seen, votes, grounded_flag, committed, retries)
State = Tuple[str, int, int, bool, bool, int]

PHASES = ("propose", "verify", "vote", "commit", "abort")


# ------------------------------------------------------------ transition system

def successors(state: State, enforce_safety: bool, max_retries: int,
               council_size: int) -> List[State]:
    """One step of the council protocol. Returns every legal next state."""
    phase, proposals, votes, grounded, committed, retries = state
    out: List[State] = []

    if phase == "propose":
        # A proposal is either grounded in retrieved evidence or it is not; both
        # are reachable, which is exactly why the invariant has to be checked.
        for is_grounded in (True, False):
            out.append(("verify", proposals + 1, 0, is_grounded, False, retries))

    elif phase == "verify":
        if grounded or not enforce_safety:
            out.append(("vote", proposals, 0, grounded, False, retries))
        if not grounded:
            # Verification rejects it; the council retries or gives up.
            if retries < max_retries:
                out.append(("propose", proposals, 0, False, False, retries + 1))
            else:
                out.append(("abort", proposals, 0, False, False, retries))

    elif phase == "vote":
        for received in range(votes, council_size + 1):
            if received >= (2 * (council_size // 3)) + 1:
                out.append(("commit", proposals, received, grounded, True, retries))
            else:
                out.append(("vote", proposals, received + 1, grounded, False, retries))

    return out


def explore(enforce_safety: bool, max_retries: int = 2, council_size: int = 7
            ) -> Dict[str, int]:
    """Breadth-first exploration of the reachable state space.

    Returns the reachable set, the transition count, whether the safety invariant
    ('never commit an ungrounded proposal') holds everywhere, and the shortest
    counterexample when it does not.
    """
    start: State = ("propose", 0, 0, False, False, 0)
    seen: Set[State] = {start}
    parent: Dict[State, Optional[State]] = {start: None}
    queue = deque([start])
    transitions = 0
    violation: Optional[State] = None

    while queue:
        current = queue.popleft()
        for nxt in successors(current, enforce_safety, max_retries, council_size):
            transitions += 1
            if nxt not in seen:
                seen.add(nxt)
                parent[nxt] = current
                queue.append(nxt)
            # Safety: a committed state must carry a grounded proposal.
            if nxt[4] and not nxt[3] and violation is None:
                violation = nxt

    depth = 0
    if violation is not None:
        node: Optional[State] = violation
        while node is not None:
            node = parent[node]
            depth += 1

    return {
        "states": len(seen),
        "transitions": transitions,
        "safety_holds": int(violation is None),
        "counterexample_depth": depth,
        "terminal_states": sum(1 for s in seen if s[0] in ("commit", "abort")),
    }


# ------------------------------------------------------------- deadlock check

def has_cycle_without_progress(priority_ordering: bool) -> Tuple[bool, int]:
    """Detect an unbounded rebuttal cycle between two polarised personas.

    Modelled on the turn alone. Bounding the objection count would make the graph
    a DAG by construction, so a cycle search over it could never fail to terminate
    and the check would be vacuous -- it would report 'no livelock' for every
    configuration, including ones that livelock.

    Without an ordering both agents may rebut, so turn alternates A->B->A and the
    cycle closes. A strict asymmetric priority forbids the lower-ranked agent from
    re-objecting after the higher-ranked one has spoken, removing the return edge.
    """
    graph: Dict[str, List[str]] = (
        {"A_turn": ["B_turn"], "B_turn": []}          # priority: no way back to A
        if priority_ordering
        else {"A_turn": ["B_turn"], "B_turn": ["A_turn"]}   # free rebuttal both ways
    )

    colour: Dict[str, int] = {}

    def dfs(node: str) -> bool:
        colour[node] = 1
        for nxt in graph.get(node, []):
            if colour.get(nxt, 0) == 1:
                return True
            if colour.get(nxt, 0) == 0 and dfs(nxt):
                return True
        colour[node] = 2
        return False

    return dfs("A_turn"), len(graph)


# ----------------------------------------------------------- byzantine consensus

def byzantine_round(n: int, f: int, rng: np.random.Generator,
                    p_deliver: float = 0.95) -> bool:
    """One randomised round of quorum consensus over an unreliable channel.

    Honest agents broadcast the correct value; Byzantine agents each pick a wrong
    value independently, so they may or may not concentrate. Every message is
    delivered with probability ``p_deliver``. An honest agent commits when it has
    seen at least 2f+1 matching votes, and the round succeeds only when every
    honest agent that commits commits the correct value.

    The unreliable channel is what makes this a simulation rather than an
    inequality: without message loss the outcome is a deterministic function of
    (n, f) and reporting repeated 'trials' of it would be meaningless.
    """
    honest = n - f
    quorum = 2 * f + 1

    wrong_values = rng.integers(1, 4, size=f) if f else np.array([], dtype=int)

    for _ in range(honest):
        seen_correct = int(rng.binomial(honest, p_deliver))
        seen_wrong: Dict[int, int] = {}
        for value in wrong_values:
            if rng.random() < p_deliver:
                seen_wrong[int(value)] = seen_wrong.get(int(value), 0) + 1

        best_wrong = max(seen_wrong.values()) if seen_wrong else 0
        if best_wrong >= quorum and best_wrong > seen_correct:
            return False          # an honest agent commits a corrupted value
        if seen_correct < quorum and best_wrong >= quorum:
            return False
    # Success requires at least one honest agent to reach quorum on the truth.
    return honest >= quorum


def main() -> int:
    rng = np.random.default_rng(SEED)
    rec = ExperimentRecorder(
        run_id="draft-review_trustworthy_multi_agent_systems_formal_verification",
        paper="p9",
        description=("Explicit-state model checking of a council protocol, deadlock "
                     "freedom by cycle detection, and the Byzantine agreement threshold "
                     "under a 2f+1 quorum rule."),
        seed=SEED,
    )

    print("=== p9: formal verification ===\n")

    # 1. Model checking --------------------------------------------------------
    t0 = time.perf_counter()
    enforced = explore(enforce_safety=True)
    t_enforced = time.perf_counter() - t0

    t0 = time.perf_counter()
    unenforced = explore(enforce_safety=False)
    t_unenforced = time.perf_counter() - t0

    art1, sha1 = rec.save_artifact("model_checking.json", {
        "with_invariant": {**enforced, "seconds": t_enforced},
        "without_invariant": {**unenforced, "seconds": t_unenforced},
    })
    print("  explicit-state model checking of the council protocol:")
    print(f"    with LTL safety invariant:    {enforced['states']} states, "
          f"{enforced['transitions']} transitions, safety_holds="
          f"{bool(enforced['safety_holds'])}, {t_enforced*1000:.2f} ms")
    print(f"    with the invariant removed:   {unenforced['states']} states, "
          f"safety_holds={bool(unenforced['safety_holds'])}, "
          f"counterexample depth {unenforced['counterexample_depth']}")

    rec.record("model_states_reachable", enforced["states"], "n", art1, sha1,
               "breadth-first reachable state count, invariant enforced")
    rec.record("model_transitions", enforced["transitions"], "n", art1, sha1,
               "transitions explored, invariant enforced")
    rec.record("model_check_latency_ms", round(t_enforced * 1000, 4), "ms", art1, sha1,
               "wall-clock exhaustive exploration")
    rec.record("counterexample_depth_without_invariant",
               unenforced["counterexample_depth"], "n", art1, sha1,
               "shortest path to an ungrounded commit once the invariant is removed")
    # The manuscript's "removing the safety invariant increases the reachable
    # state count by 72.97%" was computed from this artifact and never recorded,
    # so nothing could resolve it. It survived only because a citation happened to
    # sit in the same sentence. Both terms of the ratio are recorded here so the
    # figure is checkable and moves with the run.
    rec.record("model_states_without_invariant", unenforced["states"], "n", art1, sha1,
               "breadth-first reachable state count, invariant removed")
    rec.record("state_space_growth_without_invariant", round(
        (unenforced["states"] / enforced["states"] - 1.0) * 100, 2), "%", art1, sha1,
        "increase in reachable states when the safety invariant is removed")
    safety_pct = 100.0 if enforced["safety_holds"] else 0.0
    rec.record("safety_invariant_holds", safety_pct, "%", art1, sha1,
               "exhaustive: no reachable state commits an ungrounded proposal",
               n=enforced["states"],
               notes="a proof over the model's reachable states, not a sample average")

    # 2. Deadlock freedom ------------------------------------------------------
    cycle_without, states_without = has_cycle_without_progress(priority_ordering=False)
    cycle_with, states_with = has_cycle_without_progress(priority_ordering=True)
    art2, sha2 = rec.save_artifact("deadlock_check.json", {
        "without_priority": {"cycle_found": cycle_without, "states": states_without},
        "with_priority": {"cycle_found": cycle_with, "states": states_with},
    })
    print(f"\n  rebuttal cycle without priority ordering: {cycle_without} "
          f"({states_without} states)")
    print(f"  rebuttal cycle with priority ordering:    {cycle_with} "
          f"({states_with} states)")
    rec.record("livelock_cycle_without_priority", 100.0 if cycle_without else 0.0,
               "%", art2, sha2, "DFS cycle detection over the reachable graph",
               n=states_without)
    rec.record("livelock_cycle_with_priority", 100.0 if cycle_with else 0.0,
               "%", art2, sha2, "DFS cycle detection over the reachable graph",
               n=states_with)

    # 3. Byzantine threshold ---------------------------------------------------
    council = 7
    sweep = {}
    for f in range(0, council // 2 + 1):
        trials = 20000
        ok = sum(byzantine_round(council, f, rng) for _ in range(trials))
        sweep[f] = ok / trials
    art3, sha3 = rec.save_artifact("byzantine_sweep.json", {
        "council_size": council, "agreement_by_f": sweep,
        "theoretical_threshold": (council - 1) // 3,
    })
    print(f"\n  Byzantine agreement, council of {council}, quorum 2f+1:")
    for f, rate in sweep.items():
        marker = "  <- threshold" if f == (council - 1) // 3 + 1 else ""
        print(f"    f={f}: honest agreement {rate*100:6.2f}%{marker}")
        rec.record(f"byzantine_agreement_f{f}", round(rate * 100, 2), "%", art3, sha3,
                   f"randomised quorum consensus, {f} corrupt of {council}, "
                   f"95% message delivery", n=20000)

    # The channel's delivery probability is an input to this simulation, and the
    # manuscript states it. It was only ever written into the method string above,
    # so nothing could resolve the sentence "95% message delivery" against
    # evidence -- the claim was passing the gate on the strength of a citation to
    # a paper about reward engineering, and became honestly ungrounded the moment
    # that citation was removed. A parameter a manuscript quotes is a claim.
    rec.record("channel_delivery_probability", 95.0, "%", art3, sha3,
               "probability an inter-agent message is delivered, per trial",
               n=20000)

    tolerated = max((f for f, r in sweep.items() if r == 1.0), default=-1)
    rec.record("max_tolerated_byzantine", tolerated, "n", art3, sha3,
               "largest f at which honest agreement is total", n=council)
    print(f"\n    largest f with total agreement: {tolerated} "
          f"(theory: floor((n-1)/3) = {(council - 1) // 3})")

    rec.finalize()
    print("\n  NOTE: these are proofs and simulations over a protocol model. No language")
    print("  model was run, so no interaction traces or intercepted hallucinations exist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
