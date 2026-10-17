"""Evidence intake must preserve inputs and never promote diagnostics to results."""
import json
from pathlib import Path

import pytest

from services.vault import VaultManager
from services.vlm_research import VLMResearchService, digest


@pytest.fixture
def intake(tmp_path):
    workspace = tmp_path / 'research'
    workspace.mkdir()
    notebook = workspace / 'v2.ipynb'
    notebook.write_text(json.dumps({'cells': [{'cell_type': 'code', 'source': [
        'REFUSAL_MARKERS = ["cannot"]\n',
        'raise RuntimeError("Notebook must never execute")\n'
    ]}]}))
    bundle = workspace / 'pilot'
    bundle.mkdir()
    meta = {'pairs': [['example/model', 'example/text']]}
    (bundle / 'results.json').write_text(json.dumps({'meta': meta}))
    for condition in 'ABCD':
        rows = [{'uid': f'{scenario}|{index}', 'response': 'An answer without a refusal cue.'}
                for scenario in ['s1', 's2'] for index in range(3)]
        (bundle / f'gen_example_model__{condition}.jsonl').write_text(
            '\n'.join(json.dumps(row) for row in rows))
        (bundle / f'lab_example_model__{condition}.json').write_text(json.dumps(['REFUSAL'] * 6))
    service = VLMResearchService(workspace, tmp_path / 'output', VaultManager(str(tmp_path / 'vault')))
    service.profile.update(plan_files=[], notebooks=['v2.ipynb'], refusal_cue_notebook='v2.ipynb',
                           bundles=['pilot'], pdf_folders=[])
    service.connection = lambda: {'exists': True, 'remote_matches': True, 'revision': 'test', 'dirty': False}
    return service


def test_prepare_is_read_only_and_diagnostics_cannot_become_ground_truth(intake):
    before = {str(p): digest(p.read_bytes()) for p in intake.workspace.rglob('*') if p.is_file()}
    report = intake.prepare(3)
    after = {str(p): digest(p.read_bytes()) for p in intake.workspace.rglob('*') if p.is_file()}
    assert before == after
    assert report['status'] == 'MEASUREMENT_VALIDATION_REQUIRED'
    assert report['manuscript_ready'] is False
    assert report['judge_calibration'] == 'NOT_PERFORMED'
    assert report['bundles'][0]['paired_id_order_matches']
    group = report['bundles'][0]['groups'][0]
    assert group['refusal_without_cue_first200'] == 6
    assert group['judge_refusal_rate_unvalidated'] == 1
    assert group['label_binding'] == 'positional_only_not_response_hash_bound'
    assert report['blinded_queue_rows'] == 12
    queue = Path(report['blinded_queue_path']).read_text()
    assert 'REFUSAL' not in queue
    assert 'response_sha256' in queue
    assert intake.status()['latest']['snapshot_current']
    source = intake.workspace / 'pilot/gen_example_model__A.jsonl'
    source.write_text(source.read_text() + '\n')
    assert not intake.status()['latest']['snapshot_current']


def test_mismatched_labels_and_pair_order_are_reported(intake):
    labels = intake.workspace / 'pilot/lab_example_model__B.json'
    labels.write_text('["REFUSAL"]')
    report = intake.prepare(2)
    assert 'label count' in report['bundles'][0]['errors'][0]
    assert not report['bundles'][0]['paired_id_order_matches']
    assert all(g['condition'] != 'B' for g in report['bundles'][0]['groups'])


def test_connection_and_path_boundaries(intake):
    with pytest.raises(ValueError, match='outside'):
        intake._path('../elsewhere')
    intake.connection = lambda: {'exists': True, 'remote_matches': False}
    with pytest.raises(ValueError, match='does not point'):
        intake.prepare()
    with pytest.raises(ValueError, match='between'):
        intake.prepare(101)


def test_later_notebook_cannot_silently_change_pilot_cue_diagnostic(intake):
    later = intake.workspace / 'v3.ipynb'
    later.write_text(json.dumps({'cells': [{'cell_type': 'code', 'source': [
        'REFUSAL_MARKERS = ["answer"]\n'
    ]}]}))
    intake.profile['notebooks'].append('v3.ipynb')
    report = intake.prepare(1)
    assert report['refusal_cue_source'] == 'v2.ipynb'
    assert report['bundles'][0]['groups'][0]['refusal_without_cue_first200'] == 6


def test_api_reports_connection_and_rejects_invalid_sample_size(intake, monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import vlm_research_api
    monkeypatch.setattr(vlm_research_api, 'service', intake)
    app = FastAPI()
    app.include_router(vlm_research_api.router)
    with TestClient(app) as client:
        assert client.get('/api/research/projects/vlm-safety').json()['connection']['remote_matches']
        assert client.post('/api/research/projects/vlm-safety/prepare', json={'sample_per_group': 0}).status_code == 422
        result = client.post('/api/research/projects/vlm-safety/prepare', json={'sample_per_group': 1})
        assert result.status_code == 200
        assert result.json()['manuscript_ready'] is False
