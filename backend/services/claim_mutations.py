"""Break grounded claims on purpose, so the gate's blind spots can be measured.

Every check in this project was written after a defect got past it. That is a
slow way to find holes: the corpus shipped with 726 of 728 claims unbacked, an
audit scored 100.0 on a stub, and each was discovered by a person reading
carefully at the right moment.

This inverts it. Take a manuscript whose claims all resolve, apply a
transformation that *should* make one of them stop resolving, and see whether
the gate notices. The operators are deterministic text or evidence edits -- no
model judges anything, and the verdict is `ClaimProvenanceService`'s own
classification, not an opinion about it.

The operators are ordered by what they test:

    mu_drift        a value moves past its rounding tolerance
    mu_orphan       the measurement a claim rests on is deleted
    mu_rebind       the number stays, the sentence now describes another metric
    mu_transplant   a claim is moved to a paper whose run happens to match it
    mu_attribute    a measured claim becomes an attributed one, citing anything
    mu_unitless     a claim is restated without its unit

The first two should be caught: they are what the gate is for. The rest probe
`_matches_measurement`, which binds a claim to a value and a unit and never
checks the sentence is about the metric it matched, and `_ATTRIBUTION`, which
grants CITATION grounding to any sentence with an attribution verb and a
resolvable key without asking whether the source says it.

Mutants are built in memory and returned as strings. Nothing here writes to a
draft.
"""
from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence


@dataclass
class Mutant:
    """One deliberately broken manuscript, and what was done to it."""

    operator: str
    draft: str
    text: str
    description: str
    #: Measurements the gate should see. mu_orphan removes one; others pass through.
    measurements: List[Dict[str, Any]] = field(default_factory=list)
    #: The claim that was attacked, as it appeared before the edit.
    target: str = ""


def _numeric_claims(claims: Sequence[Any]) -> List[Any]:
    """Claims the gate currently resolves against a measurement."""
    return [c for c in claims
            if getattr(c, "grounding", "") == "EXPERIMENT" and c.value is not None]


def _replace_once(text: str, old: str, new: str) -> Optional[str]:
    """Replace *old* exactly once, refusing when it is not uniquely locatable."""
    if text.count(old) != 1:
        return None
    return text.replace(old, new, 1)


# --------------------------------------------------------------- the operators

def mu_drift(text: str, claims, measurements, rng, **_) -> Optional[Mutant]:
    """Move a value past the precision it was written to.

    `_matches_measurement` accepts a claim when the recorded value rounds to it
    at the claim's own precision, which is correct -- 2.13 for a measured 2.1339
    is rounding, not a different number. The perturbation therefore has to
    exceed that tolerance, or a 'miss' would really be the gate behaving.
    """
    candidates = _numeric_claims(claims)
    if not candidates:
        return None
    claim = rng.choice(candidates)
    raw = claim.raw
    digits = re.search(r"(\d+)\.(\d+)", raw)
    if digits:
        decimals = len(digits.group(2))
        moved = round(claim.value + 10 ** (-decimals) * 3, decimals)
        new_raw = raw.replace(f"{digits.group(1)}.{digits.group(2)}",
                              f"{moved:.{decimals}f}", 1)
    else:
        whole = re.search(r"\d+", raw)
        if not whole:
            return None
        moved = int(whole.group(0)) + max(1, int(abs(claim.value) * 0.1))
        new_raw = raw.replace(whole.group(0), str(moved), 1)

    mutated = _replace_once(text, raw, new_raw)
    if mutated is None:
        return None
    return Mutant("mu_drift", "", mutated,
                  f"{raw} -> {new_raw}", list(measurements), raw)


def mu_orphan(text: str, claims, measurements, rng, **_) -> Optional[Mutant]:
    """Delete the measurement a claim rests on, leaving the sentence untouched."""
    candidates = _numeric_claims(claims)
    if not candidates or len(measurements) < 2:
        return None
    claim = rng.choice(candidates)
    evidence = getattr(claim, "evidence", "") or ""
    artifact = evidence.split("#")[0]

    # Remove every measurement that could satisfy the claim, not only the one it
    # happened to bind to. p9 records both livelock_cycle_with_priority and
    # byzantine_agreement_f3 as 0.0%, so deleting one left the other standing and
    # the claim stayed grounded -- an escape that looked like an instrument
    # failure and was really the value-collision hole mu_rebind targets. An
    # operator whose job is to remove the evidence has to remove all of it, or a
    # "miss" is ambiguous between two very different causes.
    kept = [m for m in measurements if not _rounds_to(m.get("value"), claim)]
    if len(kept) == len(measurements):
        return None
    removed = len(measurements) - len(kept)
    return Mutant("mu_orphan", "", text,
                  f"removed {removed} measurement(s) that could back {claim.raw}",
                  kept, claim.raw)


def mu_rebind(text: str, claims, measurements, rng, metric_vocab=None, **_) -> Optional[Mutant]:
    """Keep the number; say it measures something else entirely.

    The gate matches on value and unit alone, so a sentence claiming a Byzantine
    agreement rate of 100.00% is satisfied by a recorded syntactic-validity of
    100.00%. Nothing connects the words to the metric.
    """
    candidates = [c for c in _numeric_claims(claims) if len(c.sentence) > 40]
    if not candidates or not metric_vocab:
        return None
    claim = rng.choice(candidates)
    sentence = claim.sentence
    replacement = rng.choice(metric_vocab)
    # Re-describe the subject of the sentence while leaving the figure alone.
    mutated_sentence = re.sub(
        r"^[^.]{10,80}?(?=\s+(?:is|are|was|were|reaches|shows|rejects|holds))",
        f"The {replacement}", sentence, count=1)
    if mutated_sentence == sentence:
        mutated_sentence = f"The {replacement} is reported below. {sentence}"
    mutated = _replace_once(text, sentence, mutated_sentence)
    if mutated is None:
        return None
    return Mutant("mu_rebind", "", mutated,
                  f"re-described as '{replacement}'", list(measurements), claim.raw)


def mu_transplant(text: str, claims, measurements, rng, foreign_claims=None,
                  **_) -> Optional[Mutant]:
    """Insert another paper's sentence, whose value this run also happens to record."""
    if not foreign_claims:
        return None
    values = {round(float(m.get("value", 0)), 4) for m in measurements}
    matching = [c for c in foreign_claims
                if c.value is not None and round(float(c.value), 4) in values]
    if not matching:
        return None
    claim = rng.choice(matching)
    # Insert before a heading every draft actually has. An earlier version looked
    # for "## Discussion", which none of them contain, so the operator silently
    # produced nothing and reported 0.00% as though it had been measured. An
    # operator that cannot run must say so rather than score zero.
    marker = "\n## Conclusion\n"
    if marker not in text:
        return None
    mutated = text.replace(marker, f"\n{claim.sentence}\n{marker}", 1)
    return Mutant("mu_transplant", "", mutated,
                  f"inserted a claim from another manuscript: {claim.raw}",
                  list(measurements), claim.raw)


def mu_attribute(text: str, claims, measurements, rng, citation_keys=None,
                 **_) -> Optional[Mutant]:
    """Turn a measured claim into an attributed one, citing an arbitrary source.

    This is the shape that let "Vendor specifications report HBM bandwidth of
    2.4 TB/s" pass while citing a paper about research ethics committees.
    """
    candidates = _numeric_claims(claims)
    if not candidates or not citation_keys:
        return None
    claim = rng.choice(candidates)
    key = rng.choice(list(citation_keys))
    invented = _perturb_raw(claim)
    if invented is None:
        return None
    sentence = claim.sentence
    mutated_sentence = (f"Prior work reports {invented} for this quantity "
                        f"[[{key}]].")
    mutated = _replace_once(text, sentence, mutated_sentence)
    if mutated is None:
        return None
    return Mutant("mu_attribute", "", mutated,
                  f"{claim.raw} -> attributed '{invented}' citing {key}",
                  list(measurements), claim.raw)


def mu_unitless(text: str, claims, measurements, rng, **_) -> Optional[Mutant]:
    """Restate a claim without its unit, where no extraction pattern matches it."""
    candidates = [c for c in _numeric_claims(claims) if c.unit in ("%", "time", "n")]
    if not candidates:
        return None
    claim = rng.choice(candidates)
    invented = _perturb_raw(claim)
    if invented is None:
        return None
    bare = re.sub(r"[^\d.]", "", invented)
    mutated_sentence = f"The measured figure was {bare} on this corpus."
    mutated = _replace_once(text, claim.sentence, mutated_sentence)
    if mutated is None:
        return None
    return Mutant("mu_unitless", "", mutated,
                  f"{claim.raw} -> bare '{bare}'", list(measurements), claim.raw)


# ------------------------------------------------------------------- utilities

def _rounds_to(recorded: Any, claim: Any) -> bool:
    try:
        value = float(recorded)
    except (TypeError, ValueError):
        return False
    fraction = re.search(r"\.(\d+)", claim.raw)
    decimals = len(fraction.group(1)) if fraction else 0
    return round(value, decimals) == round(claim.value, decimals)


def _perturb_raw(claim: Any) -> Optional[str]:
    """A version of the claim's text carrying a value nothing recorded."""
    digits = re.search(r"(\d+)\.(\d+)", claim.raw)
    if digits:
        decimals = len(digits.group(2))
        moved = round(claim.value + 10 ** (-decimals) * 7, decimals)
        return claim.raw.replace(f"{digits.group(1)}.{digits.group(2)}",
                                 f"{moved:.{decimals}f}", 1)
    whole = re.search(r"\d+", claim.raw)
    if not whole:
        return None
    return claim.raw.replace(whole.group(0),
                             str(int(whole.group(0)) + 17), 1)


OPERATORS: Dict[str, Callable] = {
    "mu_drift": mu_drift,
    "mu_orphan": mu_orphan,
    "mu_rebind": mu_rebind,
    "mu_transplant": mu_transplant,
    "mu_attribute": mu_attribute,
    "mu_unitless": mu_unitless,
}

#: Operators the gate is built to catch. An escape here is a defect in the
#: harness or in the gate, not an interesting finding about coverage.
MUST_CATCH = ("mu_drift", "mu_orphan")


def generate(operator: str, text: str, claims, measurements,
             seed: int, attempts: int = 12, **context) -> List[Mutant]:
    """Up to *attempts* mutants from one operator, deterministic under *seed*."""
    rng = random.Random(seed)
    made: List[Mutant] = []
    seen: set = set()
    for _ in range(attempts):
        mutant = OPERATORS[operator](text, claims, measurements, rng, **context)
        if mutant is None or mutant.text in seen:
            continue
        seen.add(mutant.text)
        made.append(mutant)
    return made
