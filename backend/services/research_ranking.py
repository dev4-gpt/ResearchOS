"""Trusted ranking measurement. Labels never enter a candidate execution process."""
import math
import re
from pathlib import Path
import json

FIXTURE = Path(__file__).resolve().parents[1] / 'tests/fixtures/research_engines/ranking.json'


def load_dataset(path=FIXTURE):
    data = json.loads(Path(path).read_text())
    ids = set()
    if not isinstance(data.get('synthetic'), bool):
        raise ValueError('Dataset must declare whether it is synthetic')
    for task in data['tasks']:
        if not isinstance(task.get('id'), str) or not re.fullmatch(r'[a-zA-Z0-9_-]{1,100}', task['id']):
            raise ValueError('Unsafe task identifier')
        if not isinstance(task.get('query'), str) or not task['query'].strip():
            raise ValueError('Task query must be nonempty text')
        if not task.get('documents') or any(not isinstance(d.get('id'), str) or not isinstance(d.get('title'), str) for d in task['documents']):
            raise ValueError('Documents need string IDs and titles')
        if task['id'] in ids or task['split'] not in ('development', 'heldout'):
            raise ValueError('Duplicate task or invalid split')
        ids.add(task['id'])
        docs = {d['id'] for d in task['documents']}
        if len(docs) != len(task['documents']) or set(task['labels']) != docs:
            raise ValueError('Document IDs and labels must match exactly')
        if any(type(v) is not int or not 0 <= v <= 3 for v in task['labels'].values()):
            raise ValueError('Labels must be integer grades 0..3')
        for ranking in task['source_rankings']:
            validate_ranking(ranking, task)
    if {t['split'] for t in data['tasks']} != {'development', 'heldout'}:
        raise ValueError('Both development and heldout splits required')
    return data


def public_task(task):
    return {k: task[k] for k in ('id', 'query', 'documents', 'source_rankings')}


def validate_ranking(ids, task):
    if not isinstance(ids, list) or any(not isinstance(x, str) for x in ids):
        raise ValueError('Ranking must be a list of document IDs')
    allowed = {d['id'] for d in task['documents']}
    if len(ids) != len(set(ids)) or set(ids) != allowed:
        raise ValueError('Ranking must be a permutation of all supplied IDs')
    return ids


def rrf(task):
    scores = {d['id']: 0.0 for d in task['documents']}
    for ranking in task['source_rankings']:
        for rank, doc in enumerate(ranking, 1):
            scores[doc] += 1 / (60 + rank)
    return sorted(scores, key=lambda x: (-scores[x], x))


def lexical(task):
    query = set(task['query'].lower().split())
    return [d['id'] for d in sorted(task['documents'], key=lambda d: (
        -len(query & set(d['title'].lower().split())), d['id']))]


def measure(ids, task):
    validate_ranking(ids, task)
    labels = task['labels']
    def dcg(values):
        return sum((2 ** value - 1) / math.log2(i + 2) for i, value in enumerate(values[:10]))
    ideal = dcg(sorted(labels.values(), reverse=True))
    relevant = {k for k, v in labels.items() if v > 0}
    return {'ndcg_at_10': dcg([labels[x] for x in ids]) / ideal if ideal else 0.0,
            'recall_at_20': len(set(ids[:20]) & relevant) / len(relevant) if relevant else 0.0}
