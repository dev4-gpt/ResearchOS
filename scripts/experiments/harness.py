"""Experiment harness: run a real computation, record what it measured.

Every row this writes is produced by code in this repository that a reader can
re-run. The recorder deliberately makes it awkward to log a number that no
computation produced: a measurement is only accepted alongside the raw artifact
it came from, the artifact is hashed, and the hash is what
:mod:`services.claim_provenance` checks.

Scope, stated plainly: these experiments measure *models and algorithms* on this
machine. They cannot measure GPU cluster behaviour, production telemetry from real
organisations, or benchmark scores that require executing a large model. Any claim
of that kind must be removed from the manuscript rather than backfilled from a
simulation — a simulated number recorded as evidence is fabrication with a
checksum on it.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RUNS_ROOT = os.path.join(REPO_ROOT, "runs")

# iCloud writes a sync-conflict copy beside the original, named "<stem> 2.<ext>"
# (or 3, 4, ...). Four such copies of live modules sit in this working tree. They
# are stale duplicates, not code: an experiment that treats them as corpus members
# double-counts every symbol they define, and a query harvested from one gets a
# gold answer that the rest of the repository never references (ERR-071).
_SYNC_CONFLICT_STEM = re.compile(r" [2-9]$")


def is_sync_conflict_copy(path: str) -> bool:
    """True if *path* is an iCloud sync-conflict duplicate rather than real source."""
    stem = os.path.splitext(os.path.basename(path))[0]
    return bool(_SYNC_CONFLICT_STEM.search(stem))



def _git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
            capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


@dataclass
class Measurement:
    """One measured value, bound to the artifact that produced it."""

    metric: str
    value: float
    unit: str
    artifact: str
    sha256: str
    method: str
    n: Optional[int] = None
    ci95: Optional[List[float]] = None
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "metric": self.metric,
            "value": self.value,
            "unit": self.unit,
            "artifact": self.artifact,
            "sha256": self.sha256,
            "method": self.method,
        }
        if self.n is not None:
            data["n"] = self.n
        if self.ci95 is not None:
            data["ci95"] = self.ci95
        if self.notes:
            data["notes"] = self.notes
        return data


class ExperimentRecorder:
    """Writes artifacts and measurements for one experiment run."""

    def __init__(self, run_id: str, paper: str, description: str, seed: int = 20260825,
                 owns_prefix: str = "", preserves_prefixes: Sequence[str] = ()):
        """Declare which measurements in the shared file belong to this run.

        A paper's measurements live in one file, and finalize() rewrites it, so
        two experiments contributing to the same paper will delete each other's
        rows unless each says what it owns. There are two ways to say it, and a
        pair of experiments needs one of each:

        *owns_prefix* -- "I own exactly this namespace." finalize() replaces the
        metrics starting with it and leaves everything else untouched.

        *preserves_prefixes* -- "I own everything except these." Use it for an
        experiment whose metric names share no common prefix, which is the usual
        case for the first experiment a paper had.

        Both default to the original behaviour: replace the whole file. That is
        correct only while a paper has exactly one experiment behind it, and it
        is how p1 destroyed p1b's nine rows on the first re-run after p1b was
        added -- owns_prefix protected p1 from p1b but not the reverse.
        """
        self.run_id = run_id
        self.paper = paper
        self.description = description
        self.seed = seed
        self.owns_prefix = owns_prefix
        self.preserves_prefixes = tuple(preserves_prefixes)
        self.run_dir = os.path.join(RUNS_ROOT, run_id)
        self.artifact_dir = os.path.join(self.run_dir, "artifacts")
        os.makedirs(self.artifact_dir, exist_ok=True)
        self._measurements: List[Measurement] = []
        self._started = time.time()

    # ---------------------------------------------------------------- artifacts

    def save_artifact(self, name: str, payload: Any) -> tuple:
        """Persist raw experiment output and return (relative_path, sha256).

        The full result set is written, not just the summary, so a reader can
        recompute the reported statistic instead of taking it on trust.
        """
        path = os.path.join(self.artifact_dir, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        blob = json.dumps(payload, indent=2, sort_keys=True, default=str).encode("utf-8")
        with open(path, "wb") as handle:
            handle.write(blob)
        digest = hashlib.sha256(blob).hexdigest()
        return os.path.relpath(path, self.run_dir), digest

    # ------------------------------------------------------------- measurements

    def record(
        self,
        metric: str,
        value: float,
        unit: str,
        artifact: str,
        sha256: str,
        method: str,
        n: Optional[int] = None,
        ci95: Optional[List[float]] = None,
        notes: str = "",
    ) -> Measurement:
        measurement = Measurement(
            metric=metric, value=float(value), unit=unit, artifact=artifact,
            sha256=sha256, method=method, n=n, ci95=ci95, notes=notes,
        )
        self._measurements.append(measurement)
        return measurement

    # ------------------------------------------------------------------ closing

    def finalize(self) -> Dict[str, Any]:
        """Write measurements.jsonl and a manifest describing how they were made."""
        measurements_path = os.path.join(self.run_dir, "measurements.jsonl")

        # A run that recorded nothing is a failed run -- a network timeout, an empty
        # result set -- and must not overwrite the evidence a previous successful run
        # left behind. This clobbered ten p4 measurements with a single row once, and
        # the manuscript silently lost its grounding.
        if not self._measurements and os.path.exists(measurements_path):
            raise RuntimeError(
                f"{self.run_id}: refusing to overwrite existing measurements with an "
                "empty result set. The run produced nothing; investigate before rerunning."
            )

        # A paper can have more than one experiment behind it, and the file is
        # keyed by paper rather than by experiment. Without this, the second
        # script to run silently deletes the first one's rows -- the same
        # data-loss ERR-051 recorded, arriving by a different route: the guard
        # above only catches an *empty* run, not a different experiment.
        #
        # A recorder that declares a namespace owns exactly the metrics whose
        # names begin with it. Everything else in the file is another
        # experiment's evidence and is carried through untouched, while a metric
        # this run stopped producing still disappears from its own namespace.
        preserved: List[str] = []
        dropped: List[str] = []
        if (self.owns_prefix or self.preserves_prefixes) and os.path.exists(measurements_path):
            mine = {m.to_dict()["metric"] for m in self._measurements}
            with open(measurements_path, "r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        metric = json.loads(line).get("metric", "")
                    except json.JSONDecodeError:
                        continue
                    if metric in mine:
                        continue                       # this run re-recorded it
                    if any(metric.startswith(p) for p in self.preserves_prefixes):
                        preserved.append(line)         # explicitly another run's
                    elif self.owns_prefix and not metric.startswith(self.owns_prefix):
                        preserved.append(line)         # outside my namespace
                    else:
                        dropped.append(metric)         # mine to remove, and said so

        with open(measurements_path, "w", encoding="utf-8") as handle:
            for line in preserved:
                handle.write(line + "\n")
            for measurement in self._measurements:
                handle.write(json.dumps(measurement.to_dict(), sort_keys=True) + "\n")

        if preserved:
            print(f"  preserved {len(preserved)} measurement(s) recorded by another "
                  f"experiment for this paper")
        if dropped:
            # Naming a namespace that another experiment already writes into
            # deletes its rows silently. That happened on the first run of p1b:
            # it claimed "swebench_" while p1 was already recording four census
            # metrics under that prefix, and they vanished. Dropping a metric you
            # no longer produce is legitimate; doing it without saying so is how
            # evidence disappears unnoticed.
            namespace = self.owns_prefix or "own"
            print(f"  dropped {len(dropped)} row(s) from the '{namespace}' "
                  f"namespace that this run did not re-record:")
            for metric in sorted(dropped):
                print(f"      - {metric}")
            print("      If any of those belong to a different experiment, this "
                  "run's owns_prefix is wrong.")

        manifest = {
            "run_id": self.run_id,
            "paper": self.paper,
            "description": self.description,
            "seed": self.seed,
            "measurement_count": len(self._measurements),
            "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "duration_s": round(time.time() - self._started, 3),
            "git_commit": _git_commit(),
            "environment": {
                "python": sys.version.split()[0],
                "platform": platform.platform(),
                "machine": platform.machine(),
                "cpu_count": os.cpu_count(),
            },
            "reproduce": f"backend/.venv/bin/python scripts/experiments/{self.paper}*.py",
        }
        with open(os.path.join(self.run_dir, "experiment_manifest.json"), "w",
                  encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2)

        print(f"\n  {len(self._measurements)} measurements -> {measurements_path}")
        return manifest

    # -------------------------------------------------------------------- utils

    @staticmethod
    def bootstrap_ci(samples: List[float], iterations: int = 10000,
                     seed: int = 20260825) -> List[float]:
        """Percentile bootstrap 95% CI actually computed from the samples."""
        import numpy as np

        if not samples:
            return [0.0, 0.0]
        rng = np.random.default_rng(seed)
        data = np.asarray(samples, dtype=float)
        means = data[rng.integers(0, len(data), size=(iterations, len(data)))].mean(axis=1)
        return [round(float(np.percentile(means, 2.5)), 6),
                round(float(np.percentile(means, 97.5)), 6)]

    @staticmethod
    def welch_t(a: List[float], b: List[float]) -> Dict[str, float]:
        """Welch's t-test and Cohen's d, computed rather than asserted."""
        import numpy as np
        from scipy import stats

        x, y = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
        t_stat, p_value = stats.ttest_ind(x, y, equal_var=False)
        pooled = np.sqrt(((len(x) - 1) * x.var(ddof=1) + (len(y) - 1) * y.var(ddof=1))
                         / (len(x) + len(y) - 2))
        cohens_d = float((x.mean() - y.mean()) / pooled) if pooled else 0.0
        return {
            "t": round(float(t_stat), 4),
            "p": float(p_value),
            "cohens_d": round(cohens_d, 4),
            "df": len(x) + len(y) - 2,
        }
