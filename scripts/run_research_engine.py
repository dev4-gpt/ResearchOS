#!/usr/bin/env python3
"""Run a pinned research engine in a bounded worker; demos never call a model."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from domain.research_experiments import EngineBudget, ExperimentSpec
from services.research_engines import RUNS, execute, safe_run, seal_run, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('engine', choices=['alphaevolve', 'harness2'])
    parser.add_argument('--mode', choices=['demo', 'live'], default='demo')
    parser.add_argument('--model', default='deterministic-fixture')
    parser.add_argument('--dataset', type=Path, help='Versioned labeled dataset; defaults to the synthetic fixture')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--steps', type=int, default=1)
    parser.add_argument('--seconds', type=int, default=120)
    parser.add_argument('--calls', type=int, default=16)
    parser.add_argument('--tokens', type=int, default=200000)
    parser.add_argument('--output-tokens', type=int, default=2048)
    parser.add_argument('--max-usd', type=float, default=1.0)
    parser.add_argument('--token-price-ceiling', type=float, default=100.0,
                        help='Operator supplied USD/million-token upper bound; not a provider quote')
    parser.add_argument('--worker', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        path = args.worker.resolve()
        if path.parent != RUNS.resolve():
            parser.error('Worker must use the dedicated run directory')
        spec = ExperimentSpec.model_validate_json((path / 'spec.json').read_text())
        result = execute(spec, path)
        print(json.dumps(result, indent=2))
        return 0 if result['status'] == 'completed' else 1
    spec = ExperimentSpec(engine=args.engine, mode=args.mode, model=args.model, seed=args.seed,
        steps=args.steps, dataset_path=str(args.dataset.resolve()) if args.dataset else None, budget=EngineBudget(seconds=args.seconds, calls=args.calls, tokens=args.tokens,
            output_tokens=args.output_tokens, max_usd=args.max_usd,
            usd_per_million_token_ceiling=args.token_price_ceiling))
    if spec.engine == 'harness2' and spec.steps != 1:
        parser.error('Harness² research adapter currently supports one recursion step (k=1)')
    path = safe_run(RUNS, f'{spec.engine}-{uuid.uuid4().hex[:12]}')
    path.mkdir(parents=True)
    write_json(path / 'spec.json', spec.model_dump())
    # Only explicitly selected provider credentials enter the worker. Do not load .env.
    allow = {'PATH', 'HOME', 'TMPDIR', 'LANG', 'SYSTEMROOT', 'RESEARCH_ENGINES_ENABLED',
             'GEMINI_API_KEY', 'RESEARCH_ENGINE_IMAGE', 'DOCKER_HOST', 'DOCKER_CONTEXT',
             'RESEARCHINGOS_SPEND_LEDGER', 'RESEARCHINGOS_SPEND_CAP_USD', 'RESEARCHINGOS_GEMINI_MIN_INTERVAL',
             'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY',
             'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy', 'PYTHONPATH'}
    env = {k: v for k, v in os.environ.items() if k in allow}
    with (path / 'worker.log').open('w') as log:
        child = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), spec.engine, '--worker', str(path)],
                                 stdout=log, stderr=subprocess.STDOUT, env=env, start_new_session=True)
        terminal = None
        try:
            code = child.wait(timeout=spec.budget.seconds + 5)
        except subprocess.TimeoutExpired:
            terminal = 'timed_out'
        except KeyboardInterrupt:
            terminal = 'cancelled'
        if terminal:
            try:
                os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try: child.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
            code = 1
            if spec.engine == 'alphaevolve' and spec.mode == 'live':
                try:
                    result = subprocess.run(['docker', 'ps', '-aq', '--filter', 'label=researchingos.engine-run=' + path.name], capture_output=True, text=True, timeout=5)
                    ids = result.stdout.split()
                    if ids:
                        subprocess.run(['docker', 'rm', '-f', *ids], capture_output=True, timeout=10)
                except (OSError, subprocess.TimeoutExpired):
                    pass  # Docker unavailable; candidate containers also have per-call limits.
        summary_file = path / 'summary.json'
        summary = json.loads(summary_file.read_text()) if summary_file.exists() else {
            'id': path.name, 'engine': spec.engine, 'mode': spec.mode, 'synthetic': True, 'metrics': {}}
        if terminal or summary.get('status') == 'running' or not summary_file.exists():
            summary.update(status=terminal or 'failed', publication_eligible=False,
                           error='Worker terminated before completion; inspect worker.log')
            write_json(summary_file, summary)
            seal_run(path)
    print(json.dumps({'run': str(path), 'status': summary['status'], 'error': summary.get('error')}, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
