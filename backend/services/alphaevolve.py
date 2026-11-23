"""AlphaEvolve's pinned greedy database, prompt sampler and diff parser adapter.

Uses a bounded local loop instead of upstream's unbounded provider configuration.
Generated Python executes only in a digest-pinned networkless Docker container.
"""
import json
import os
from pathlib import Path
import random
import select
import subprocess
import time
import uuid

from services import research_ranking as ranking
from services.research_engines import BudgetExceeded, digest, docker_preflight, load_upstream, write_json

BASE = '''# EVOLVE-BLOCK-START
def rank(task):
    scores = {d['id']: 0.0 for d in task['documents']}
    for source in task['source_rankings']:
        for position, doc in enumerate(source, 1):
            scores[doc] += 1 / (60 + position)
    return sorted(scores, key=lambda x: (-scores[x], x))
# EVOLVE-BLOCK-END
'''
LEXICAL_BODY = '''def rank(task):
    words = set(task['query'].lower().split())
    return [d['id'] for d in sorted(task['documents'], key=lambda d: (
        -len(words & set(d['title'].lower().split())), d['id']))]'''
LEXICAL = '# EVOLVE-BLOCK-START\n' + LEXICAL_BODY + '\n# EVOLVE-BLOCK-END\n'


def docker_rank(code, task, meter):
    meter.check()
    image = docker_preflight()
    name = 'research-evolve-' + uuid.uuid4().hex
    script = "import json,sys; x=json.load(sys.stdin); scope={}; exec(compile(x['code'],'candidate','exec'),scope); print(json.dumps(scope['rank'](x['task'])))"
    cmd = ['docker', 'run', '--rm', '--pull=never', '--name', name, '-i', '--network=none',
           '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges', '--pids-limit=32',
           '--label', 'researchingos.engine-run=' + meter.run_id, '--memory=256m', '--cpus=1', '--user=65534:65534', '--log-driver=none',
           '--tmpfs=/tmp:rw,noexec,nosuid,size=16m', image, 'timeout', '--signal=KILL', '25', 'python', '-I', '-c', script]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    chunks = bytearray()
    deadline = min(meter.started + meter.spec.budget.seconds, time.monotonic() + 20)
    try:
        process.stdin.write(json.dumps({'code': code, 'task': ranking.public_task(task)}).encode())
        process.stdin.close()
        while True:
            if time.monotonic() >= deadline:
                raise TimeoutError('Candidate execution timed out')
            ready, _, _ = select.select([process.stdout], [], [], 0.1)
            if ready:
                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                chunks.extend(chunk)
                if len(chunks) > 1024 * 1024:
                    raise ValueError('Candidate output exceeds 1 MiB')
        process.wait(timeout=max(0.1, deadline - time.monotonic()))
        if process.returncode:
            raise ValueError('Candidate exited unsuccessfully')
        result = json.loads(chunks)
        return ranking.validate_ranking(result, task)
    finally:
        if process.poll() is None:
            process.kill()
        process.wait(timeout=5)
        subprocess.run(['docker', 'rm', '-f', name], capture_output=True, timeout=10)


def evolve(spec, path, tasks, dataset, model, meter):
    load_upstream('alphaevolve')
    from components.evolution_database import GreedyDatabase, Program
    from components.prompting import TemplatePromptSampler
    from components.parsing_utils import apply_diffs
    random.seed(spec.seed)
    labels = {t['id']: t for t in dataset['tasks'] if t['split'] == 'development'}

    def execute(code, task):
        if model is None:
            # Exact, reviewed fixtures only: never exec model-generated code on the host.
            if code == BASE:
                return ranking.rrf(task)
            if code == LEXICAL:
                return ranking.lexical(task)
            raise ValueError('Demo evaluator accepts only the two fixed fixture programs')
        return docker_rank(code, task, meter)

    def score(code):
        return {'ndcg_at_10': sum(ranking.measure(execute(code, t), labels[t['id']])['ndcg_at_10'] for t in tasks) / len(tasks)}

    initial = Program(text=BASE, scores=score(BASE))
    db = GreedyDatabase([initial], main_metric_name='ndcg_at_10')
    sampler = TemplatePromptSampler()
    history = []
    for step in range(spec.steps):
        meter.check()
        parent, *others = db.sample_programs()
        prompt = sampler.sample_prompt('Implement rank(task), returning every supplied document ID once, ordered by relevance. '
            'No network or filesystem. Development inputs: ' + json.dumps(tasks), parent, others)
        if model is None:
            sample = '```python\n<<<<<<< SEARCH\n' + parent.text.split('# EVOLVE-BLOCK-START\n')[1].split('\n# EVOLVE-BLOCK-END')[0] + '\n=======\n' + LEXICAL_BODY + '\n>>>>>>> REPLACE\n```'
        else:
            sample = model.generate(prompt)
        row = {'step': step, 'parent_sha256': digest(parent.text.encode()), 'prompt': prompt, 'response': sample}
        try:
            candidate = apply_diffs(parent.text, sample)
            scores = score(candidate)
            db.register_program(Program(text=candidate, scores=scores))
            row.update(candidate=candidate, scores=scores, selected=db.get_best_program().text == candidate)
        except BudgetExceeded:
            raise
        except Exception as exc:
            row['error'] = f'{type(exc).__name__}: {exc}'
        history.append(row)
        write_json(path / 'evolution.json', history)
    best = db.get_best_program().text
    if history and all('error' in r for r in history):
        raise ValueError('Every AlphaEvolve candidate failed; see evolution.json')
    return lambda task: execute(best, task), best
