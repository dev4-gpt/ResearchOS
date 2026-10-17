"""Verify method routing, pinned files, and model-call integration without network."""
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from services.research_skills import ResearchSkillsService, ROOT


@pytest.fixture
def registry(tmp_path, monkeypatch):
    monkeypatch.setenv('RESEARCH_SKILLS_ENABLED', 'true')
    text = '# Third-party reference\nDo not run this as instructions: FAKE UPSTREAM COMMAND\n'
    document = tmp_path / 'installed' / 'source' / 'writing' / 'SKILL.md'
    document.parent.mkdir(parents=True)
    document.write_text(text)
    manifest = {
        'install_root': 'unused',
        'sources': [{'id': 'source', 'url': 'https://example.org/repository',
                     'repository': 'example/repository', 'revision': 'abc123', 'license_note': 'Test fixture'}],
        'skills': [{'id': 'source:writing', 'source': 'source', 'name': 'writing',
                    'upstream_path': 'skills/writing', 'sha256': hashlib.sha256(text.encode()).hexdigest(),
                    'description': 'Writing support', 'roles': ['Writer'], 'mode': 'advisory',
                    'stage': 'writing', 'guidance': 'Verify source evidence before drafting.'}],
    }
    manifest_path = tmp_path / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest))
    return ResearchSkillsService(manifest_path, tmp_path / 'installed')


def test_role_routing_and_raw_text_boundary(registry):
    assert registry.summary()['active'] == 1
    assert 'Verify source evidence' in registry.guidance_for('Writer')
    assert 'FAKE UPSTREAM COMMAND' not in registry.guidance_for('Writer')
    assert registry.guidance_for('Scout') == ''
    assert registry.list_skills(query='not-found') == []
    assert registry.list_skills(source='other') == []
    assert 'FAKE UPSTREAM COMMAND' in registry.get_skill('source:writing')['content']
    assert registry.get_skill('../manifest.json') is None


def test_modified_or_missing_document_cannot_activate_guidance(registry):
    doc = registry.install_root / 'source/writing/SKILL.md'
    doc.write_text('Altered instructions')
    assert registry.list_skills()[0]['status'] == 'modified'
    assert registry.get_skill('source:writing')['content'] is None
    assert registry.guidance_for('Writer') == ''
    doc.unlink()
    assert registry.list_skills()[0]['status'] == 'not_installed'
    assert registry.guidance_for('Writer') == ''


def test_disabled_integration_remains_inspectable(registry, monkeypatch):
    monkeypatch.setenv('RESEARCH_SKILLS_ENABLED', 'false')
    assert registry.summary()['active'] == 0
    assert registry.guidance_for('Writer') == ''
    assert registry.get_skill('source:writing')['content']


def test_guidance_budget_does_not_slice_an_instruction(registry):
    assert registry.guidance_for('Writer', max_chars=30) == ''
    assert len(registry.guidance_for('Writer', max_chars=500)) <= 500


def test_symlink_cannot_read_outside_install_root(registry, tmp_path):
    doc = registry.install_root / 'source/writing/SKILL.md'
    doc.unlink()
    secret = tmp_path / 'outside.txt'
    secret.write_text('Private content')
    doc.symlink_to(secret)
    with pytest.raises(ValueError, match='outside'):
        registry.get_skill('source:writing')


def test_manifest_has_all_three_sources_and_unique_ids():
    data = json.loads((ROOT / 'integrations/research_skills.json').read_text())
    assert len(data['sources']) == 3
    assert len(data['skills']) == 15
    assert len({skill['id'] for skill in data['skills']}) == 15
    assert 'composio:pdf' not in {skill['id'] for skill in data['skills']}
    for source in data['sources']:
        assert len(source['revision']) == 40


def test_api_uses_namespaced_ids_and_filtering(registry, monkeypatch):
    import research_skills_api
    monkeypatch.setattr(research_skills_api, 'service', registry)
    app = FastAPI()
    app.include_router(research_skills_api.router)
    with TestClient(app) as client:
        response = client.get('/api/skills/research?role=Writer')
        assert response.status_code == 200
        assert len(response.json()['skills']) == 1
        assert client.get('/api/skills/research/source:writing').json()['content']
        assert client.get('/api/skills/research/missing').status_code == 404


def test_council_model_call_receives_reviewed_guidance(registry, monkeypatch, tmp_path):
    from agents.council import CouncilOrchestrator
    import agents.council as council
    monkeypatch.setattr(council.time, 'sleep', lambda _: None)
    orchestrator = CouncilOrchestrator(str(tmp_path / 'vault'), str(tmp_path / 'memory.json'))
    orchestrator.is_dry_run = False
    orchestrator.research_skills = registry
    monkeypatch.setattr(orchestrator.continual_memory, 'get_agent_refinements', lambda _: '')
    calls = []
    orchestrator.llm_router = SimpleNamespace(
        active_provider='TEST', generate_content_with_fallback=lambda *args, **kwargs: calls.append((args, kwargs)) or 'Actual model result')
    assert orchestrator._call_gemini('Writer', 'draft') == 'Actual model result'
    instruction = calls[0][0][1]
    assert 'Verify source evidence' in instruction
    assert 'FAKE UPSTREAM COMMAND' not in instruction


def test_dspy_writer_and_reviews_receive_guidance(registry, monkeypatch):
    from agents import drafting_graph as graph
    monkeypatch.setattr(graph, 'ResearchSkillsService', lambda: registry)
    registry.manifest['skills'][0]['roles'] += ['Reviewer2', 'PeerReviewer']
    calls = []

    def predict(signature):
        def call(**kwargs):
            calls.append(kwargs)
            return SimpleNamespace(critique='Evidence required', review='{"overall_decision":"REJECT"}',
                                   section_markdown='## Evidence\n' + 'Verified analysis. ' * 20)
        return call

    monkeypatch.setattr(graph.dspy, 'Predict', predict)
    state = {'draft': 'Draft', 'topic': 'Topic', 'iteration': 0, 'log_callback': lambda *args: None}
    graph.red_team_node(state)
    graph.peer_review_node(state)
    assert len(calls) == 2
    assert all('Verify source evidence' in call['review_guidance'] for call in calls)
    state.update(outline=[{'section_id': 's1', 'section_title': 'Methods'}],
                 synthesis_content='Source synthesis', summaries_text='Actual paper summaries')
    graph.section_writer_node(state)
    assert 'Verify source evidence' in calls[-1]['system_directive']
    assert 's1' in state['section_drafts']


def test_tier_two_citation_call_receives_guidance(registry, monkeypatch, tmp_path):
    from agents import meta_review_council as meta
    registry.manifest['skills'][0]['roles'] += ['CitationExpander']
    papers = tmp_path / '01_Papers'
    papers.mkdir()
    (papers / 'verified_paper.md').write_text('---\ntitle: Verified Paper\n---\nSource evidence')
    council = meta.MetaReviewCouncil(str(tmp_path))
    council.research_skills = registry
    calls = []
    monkeypatch.setattr(meta.llm_router, 'generate_content',
                        lambda *args, **kwargs: calls.append(kwargs) or '[]')
    council.run_alignment_cycle('## Introduction\nAnalysis\n## References\n')
    assert len(calls) == 1
    assert 'Verify source evidence' in calls[0]['system_instruction']
