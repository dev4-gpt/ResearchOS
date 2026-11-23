"""Pinned engine loading, bounded model calls and durable, fail-closed run evidence."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid

from domain.research_experiments import ExperimentSpec
from services import research_ranking as ranking
from services.paid_execution import ExecutionBudget, ProviderFailure, gemini_request, gemini_text, reserve_provider
from services.spend_ledger import SpendLedger, SpendLimit

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / 'runs/research_engines'
LOCK = ROOT / 'integrations/research_engines.lock.json'


def digest(body):
    return hashlib.sha256(body).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    temp.replace(path)


def pinned_source(engine):
    entry = json.loads(LOCK.read_text())['engines'][engine]
    root = ROOT / '.tools/research-engines' / engine
    for name, expected in entry['files'].items():
        path = root / name
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise RuntimeError(f'Missing pinned source: {engine}/{name}; run scripts/setup_research_engines.py')
        body = path.read_bytes()
        if hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest() != expected:
            raise RuntimeError(f'Modified pinned source: {engine}/{name}')
    return root, entry


def load_upstream(engine):
    root, _ = pinned_source(engine)
    source = root / 'src' if engine == 'alphaevolve' else root
    if str(source) not in sys.path:
        sys.path.insert(0, str(source))
    return root


def status():
    result = {}
    for engine in ('alphaevolve', 'harness2', 'paperorchestra'):
        try:
            _, pin = pinned_source(engine)
            present, error = True, ''
        except RuntimeError as exc:
            pin = json.loads(LOCK.read_text())['engines'][engine]
            present, error = False, str(exc)
        result[engine] = {'sources_verified': present, 'commit': pin['commit'], 'error': error,
                          'enabled': os.getenv('PAPERORCHESTRA_ENABLED' if engine == 'paperorchestra' else 'RESEARCH_ENGINES_ENABLED', '').lower() == 'true',
                          'integration_mode': 'isolated-writer-and-review' if engine == 'paperorchestra' else 'bounded-worker'}
    return {'engines': result, 'gemini_key_configured': bool(os.getenv('GEMINI_API_KEY')),
            'docker_installed': bool(shutil.which('docker')),
            'live_execution_verified': False}


class BudgetExceeded(SpendLimit):
    pass


class Meter:
    def __init__(self, spec):
        self.spec = spec
        self.started = time.monotonic()
        self.execution = ExecutionBudget(spec.budget.seconds, spec.budget.calls)
        self.calls = self.tokens_reserved = self.tokens_reported = 0
        self.reserved_usd = 0.0
        self.lock = threading.Lock()
        self.spend_ledger = None

    def check(self):
        if time.monotonic() - self.started >= self.spec.budget.seconds:
            raise BudgetExceeded('Wall-clock budget exhausted')

    def reserve(self, prompt):
        with self.lock:
            self.check()
            # Conservative byte-bound input reservation plus provider output ceiling.
            tokens = len(prompt.encode('utf-8')) + self.spec.budget.output_tokens
            usd = tokens * self.spec.budget.usd_per_million_token_ceiling / 1e6
            b = self.spec.budget
            if self.calls >= b.calls or self.tokens_reserved + tokens > b.tokens or self.reserved_usd + usd > b.max_usd:
                raise BudgetExceeded('Model call/token/cost reservation budget exhausted')
            if self.spec.mode == 'live':
                if self.spend_ledger is None:
                    self.spend_ledger = SpendLedger.configured()
                reserve_provider(self.spend_ledger, 'gemini', usd, self.execution.deadline)
            self.calls += 1
            self.tokens_reserved += tokens
            self.reserved_usd += usd

    def snapshot(self):
        return {'calls': self.calls, 'tokens_reserved': self.tokens_reserved,
                'tokens_reported': self.tokens_reported, 'cost_ceiling_reserved_usd': self.reserved_usd,
                'seconds': round(time.monotonic() - self.started, 4)}


class Gemini:
    """No tool execution; output is text only. Every provider request is reserved first."""
    def __init__(self, spec, meter):
        if spec.model != 'gemini-2.5-flash' or spec.budget.usd_per_million_token_ceiling < 10:
            raise SpendLimit('Live engines require the reviewed Gemini 2.5 Flash model and a ceiling of at least $10 per million tokens')
        self.spec, self.meter = spec, meter
        self.key = os.environ['GEMINI_API_KEY']

    def generate(self, prompt, schema=None):
        body = {'contents': [{'parts': [{'text': prompt}]}],
                'generationConfig': {'temperature': 0,
                    'maxOutputTokens': self.spec.budget.output_tokens,
                    'thinkingConfig': {'thinkingBudget': 0}}}
        if schema:
            body['generationConfig'].update(responseMimeType='application/json', responseJsonSchema=schema)
        response = self.meter.execution.call('gemini', None,
            lambda seconds: gemini_request(self.spec.model, self.key, body, seconds),
            reserve=lambda: self.meter.reserve(json.dumps(body, ensure_ascii=False)))
        self.meter.tokens_reported += response.get('usageMetadata', {}).get('totalTokenCount', 0)
        self.meter.check()
        text = gemini_text(response)
        if not text:
            raise RuntimeError('Provider returned no text')
        return text


def parse_json(text):
    text = text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text)
    return json.loads(text)


def safe_run(root, run_id):
    if not re.fullmatch(r'[a-zA-Z0-9_-]{1,100}', run_id):
        raise ValueError('Invalid run ID')
    path = Path(root) / run_id
    if path.is_symlink() or path.resolve().parent != Path(root).resolve():
        raise ValueError('Invalid run path')
    return path


def seal_run(path):
    manifest = {}
    for f in sorted(path.rglob('*')):
        if f.is_symlink():
            raise ValueError('Run artifacts must not be symlinks')
        if f.is_file() and f.name not in ('artifacts.json', 'worker.log'):
            manifest[str(f.relative_to(path))] = digest(f.read_bytes())
    write_json(path / 'artifacts.json', manifest)


def verify_run(path):
    """Verify hashes AND recompute each reported metric from raw rankings/labels."""
    try:
        if (path / 'artifacts.json').is_symlink():
            raise ValueError('Unsafe artifact manifest')
        manifest = json.loads((path / 'artifacts.json').read_text())
        required = {'summary.json', 'spec.json', 'dataset.json', 'measurements.json', 'candidate.txt', 'upstream.json', 'evaluator.py'}
        if not required <= set(manifest):
            raise ValueError('Incomplete artifact manifest')
        for name, expected in manifest.items():
            file = path / name
            if file.is_symlink() or not file.resolve().is_relative_to(path.resolve()) or digest(file.read_bytes()) != expected:
                raise ValueError('Artifact integrity failure')
        summary = json.loads((path / 'summary.json').read_text())
        dataset = ranking.load_dataset(path / 'dataset.json')
        if summary.get('evaluator_sha256') != digest((path / 'evaluator.py').read_bytes()):
            raise ValueError('Evaluator provenance mismatch')
        if digest((path / 'evaluator.py').read_bytes()) != digest(Path(ranking.__file__).read_bytes()):
            raise ValueError('Evaluator version changed; explicit migration/replay required')
        if summary.get('dataset_sha256') != digest((path / 'dataset.json').read_bytes()):
            raise ValueError('Dataset provenance mismatch')
        if summary.get('candidate_sha256') != digest((path / 'candidate.txt').read_bytes()):
            raise ValueError('Candidate provenance mismatch')
        pin = json.loads((path / 'upstream.json').read_text())
        if pin != json.loads(LOCK.read_text())['engines'][summary['engine']]:
            raise ValueError('Upstream provenance mismatch')
        tasks = {t['id']: t for t in dataset['tasks']}
        rows = json.loads((path / 'measurements.json').read_text())
        expected_rows = {(t['id'], arm) for t in dataset['tasks'] if t['split'] == 'heldout' for arm in ('baseline', 'candidate')}
        if {(r['task'], r['arm']) for r in rows} != expected_rows or len(rows) != len(expected_rows):
            raise ValueError('Missing/duplicate held-out measurements')
        for row in rows:
            if ranking.measure(row['ranking'], tasks[row['task']]) != row['metrics']:
                raise ValueError('Metric does not match raw ranking')
        metrics = aggregate(rows)
        if metrics != summary['metrics']:
            raise ValueError('Summary does not match measurements')
        # This MVP does NOT auto-admit even live fixture results to publication.
        return {'integrity_verified': True, 'metrics_recomputed': True,
                'publication_eligible': False,
                'reason': 'Synthetic fixture' if dataset['synthetic'] or summary['synthetic'] else 'Independent executable replay and review required'}
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return {'integrity_verified': False, 'metrics_recomputed': False,
                'publication_eligible': False, 'reason': str(exc)}


def aggregate(rows):
    out = {}
    for arm in ('baseline', 'candidate'):
        arm_rows = [r for r in rows if r['arm'] == arm]
        if not arm_rows:
            raise ValueError('Missing measured arm')
        out[arm] = {key: sum(r['metrics'][key] for r in arm_rows) / len(arm_rows)
                    for key in ('ndcg_at_10', 'recall_at_20')}
        out[arm]['tasks'] = len(arm_rows)
    return out


def execute(spec: ExperimentSpec, path: Path):
    """Called in a dedicated CLI worker, never from an HTTP handler."""
    path.mkdir(parents=True, exist_ok=True)
    meter = Meter(spec)
    meter.run_id = path.name
    summary = {'id': path.name, 'engine': spec.engine, 'mode': spec.mode, 'seed': spec.seed,
               'model': spec.model, 'synthetic': True, 'status': 'running', 'metrics': {},
               'parent_run': spec.parent_run, 'publication_eligible': False}
    # The initial summary is also the claim. A crashed run cannot be invoked
    # again under the same ID, including through the internal worker flag.
    with (path / 'summary.json').open('x', encoding='utf-8') as claimed:
        json.dump(summary, claimed, indent=2, allow_nan=False)
    write_json(path / 'spec.json', spec.model_dump())
    try:
        _, pin = pinned_source(spec.engine)
        write_json(path / 'upstream.json', pin)
        data = ranking.load_dataset(spec.dataset_path or ranking.FIXTURE)
        summary['synthetic'] = spec.mode == 'demo' or data['synthetic']
        write_json(path / 'dataset.json', data)
        evaluator = Path(ranking.__file__).read_bytes()
        (path / 'evaluator.py').write_bytes(evaluator)
        summary['evaluator_sha256'] = digest(evaluator)
        summary['dataset_sha256'] = digest((path / 'dataset.json').read_bytes())
        dev = [ranking.public_task(t) for t in data['tasks'] if t['split'] == 'development']
        if spec.mode == 'live':
            if os.getenv('RESEARCH_ENGINES_ENABLED', '').lower() != 'true':
                raise RuntimeError('Live engines disabled; set RESEARCH_ENGINES_ENABLED=true')
            if not os.getenv('GEMINI_API_KEY'):
                raise RuntimeError('GEMINI_API_KEY is not configured')
            if spec.engine == 'alphaevolve':
                docker_preflight()
            model = Gemini(spec, meter)
        else:
            model = None
        if spec.engine == 'alphaevolve':
            from services.alphaevolve import evolve
            run_candidate, candidate = evolve(spec, path, dev, data, model, meter)
        else:
            from services.harness2 import refine
            run_candidate, candidate = refine(spec, path, dev, model, meter)
        (path / 'candidate.txt').write_text(candidate)
        summary['candidate_sha256'] = digest(candidate.encode())
        rows = []
        for task in data['tasks']:
            if task['split'] != 'heldout':
                continue
            for arm in ('baseline', 'candidate'):
                meter.check()
                start = time.monotonic()
                ids = ranking.rrf(task) if arm == 'baseline' else run_candidate(ranking.public_task(task))
                rows.append({'task': task['id'], 'arm': arm, 'ranking': ids,
                             'metrics': ranking.measure(ids, task), 'seconds': time.monotonic() - start})
        write_json(path / 'measurements.json', rows)
        from services.evidence_ledger import EvidenceLedger
        ledger = EvidenceLedger(str(path.parent))
        ledger.create_manifest(path.name, 'Research engine ranking evaluation', synthetic=summary['synthetic'])
        ledger.append_records(path.name, 'measurements.jsonl', rows)
        summary['metrics'] = aggregate(rows)
        summary['status'] = 'completed'
    except (BudgetExceeded, SpendLimit) as exc:
        summary.update(status='budget_exhausted', error=str(exc))
    except TimeoutError as exc:
        summary.update(status='timed_out', error=str(exc))
    except ProviderFailure as exc:
        summary.update(status='quota_exhausted' if exc.code == 429 else 'failed', error=str(exc))
    except KeyboardInterrupt:
        summary.update(status='cancelled', error='Interrupted')
    except Exception as exc:
        summary.update(status='blocked' if isinstance(exc, (RuntimeError, ImportError)) else 'failed',
                       error=f'{type(exc).__name__}: {exc}')
    summary['usage'] = meter.snapshot()
    write_json(path / 'summary.json', summary)
    seal_run(path)
    return summary


def docker_preflight():
    image = os.getenv('RESEARCH_ENGINE_IMAGE', '')
    if not re.fullmatch(r'[^\s]+@sha256:[a-f0-9]{64}', image):
        raise RuntimeError('Set RESEARCH_ENGINE_IMAGE to a locally available Python image pinned by digest')
    result = subprocess.run(['docker', 'image', 'inspect', image], capture_output=True, timeout=10)
    if result.returncode:
        raise RuntimeError('Docker daemon/image unavailable; no unsandboxed fallback')
    return image
