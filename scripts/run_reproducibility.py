#!/usr/bin/env python3
"""Explicit local entrypoint for live Gemma repair benchmarks and fixture demos."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from services.reproducibility import (  # noqa: E402
    Budget, DockerTests, GemmaClient, MODELS, RUNS, RepairTask, benchmark,
)


class FixtureClient:
    """Scripted plumbing check; never represents Gemma behavior."""
    model = "fixture-no-model"

    def complete(self, messages, output_tokens, timeout):
        edited = any('"edited"' in m["content"] for m in messages)
        action = {"tool": "finish"} if edited else {
            "tool": "edit", "path": "stats.py", "old": "sum(values) / (len(values) + 1)",
            "new": "sum(values) / len(values)"}
        return {"text": json.dumps(action), "usage": {"prompt_tokens": 0, "completion_tokens": 0}}


def fixture_task(repo: Path, image: str) -> RepairTask:
    repo.mkdir(parents=True, exist_ok=True)
    (repo / "stats.py").write_text("def mean(values):\n    return sum(values) / (len(values) + 1)\n")
    (repo / "test_stats.py").write_text(
        "import unittest\nfrom stats import mean\n"
        "class MeanTests(unittest.TestCase):\n"
        "    def test_single(self): self.assertEqual(mean([4]), 4)\n"
        "    def test_pair(self): self.assertEqual(mean([2, 4]), 3)\n"
        "    def test_negative(self): self.assertEqual(mean([-2, -4]), -3)\n")
    def git(*args):
        return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE).decode().strip()
    git("init", "-q")
    git("add", ".")
    git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
        "-c", "core.hooksPath=/dev/null", "commit", "-qm", "Deliberately broken mean fixture")
    return RepairTask(id="mean-denominator-fixture", repository=str(repo), commit=git("rev-parse", "HEAD"),
        question="Does the implementation calculate the arithmetic mean for nonempty input?",
        issue="The denominator includes an extra observation, biasing every mean toward zero.",
        method_excerpt="Arithmetic mean equals the sum of observations divided by their count. Fixture specification, not a paper citation.",
        editable_paths=["stats.py"], test_command=["python", "-m", "unittest", "-v"], image=image)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", type=Path, help="JSON array of pinned task manifests")
    parser.add_argument("--demo", action="store_true", help="Scripted fixture with real Docker tests, no model")
    parser.add_argument("--image", help="Locally installed Python Docker image pinned by @sha256, for --demo")
    parser.add_argument("--model", choices=MODELS, default=MODELS[0])
    parser.add_argument("--seconds", type=int, default=180)
    parser.add_argument("--tokens", type=int, default=32000)
    parser.add_argument("--steps", type=int, default=16)
    parser.add_argument("--output", type=Path, default=RUNS)
    args = parser.parse_args()
    if args.demo == bool(args.tasks):
        parser.error("Choose exactly one of --demo or --tasks")
    budget = Budget(seconds=args.seconds, tokens=args.tokens, steps=args.steps)
    subprocess.run(["docker", "info"], check=True, capture_output=True, timeout=15)
    runner = DockerTests()
    if args.demo:
        if not args.image:
            parser.error("--demo requires --image python@sha256:... (already installed locally)")
        with tempfile.TemporaryDirectory(prefix="researchos-fixture-") as temp:
            task = fixture_task(Path(temp), args.image)
            path = benchmark([task], FixtureClient(), runner, budget, args.output, synthetic=True)
    else:
        endpoint = os.getenv("REPRO_GEMMA_BASE_URL")
        if not endpoint:
            parser.error("Set REPRO_GEMMA_BASE_URL to the approved Gemma OpenAI-compatible /v1 endpoint")
        tasks = [RepairTask.model_validate(t) for t in json.loads(args.tasks.read_text())]
        client = GemmaClient(endpoint, args.model, os.getenv("REPRO_GEMMA_API_KEY", "local"))
        path = benchmark(tasks, client, runner, budget, args.output)
    print(path / "report.md")
    summary = json.loads((path / "summary.json").read_text())
    if any(json.loads(p.read_text())["status"] == "error" for p in path.glob("*/*/result.json")):
        raise SystemExit("Run contains errors; inspect saved logs")
    return summary


if __name__ == "__main__":
    main()
