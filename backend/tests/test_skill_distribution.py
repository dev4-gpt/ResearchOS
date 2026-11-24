import hashlib
import json

from services.research_skills import ResearchSkillsService


def test_authenticated_mode_does_not_activate_or_serve_uncleared_reference(tmp_path, monkeypatch):
    content = b'# Original test fixture\n'
    source = tmp_path / 'installed/source/example'
    source.mkdir(parents=True)
    (source / 'SKILL.md').write_bytes(content)
    manifest = {'install_root': str(tmp_path / 'installed'),
                'sources': [{'id': 'source', 'url': 'https://example.invalid', 'revision': 'fixed',
                             'license_note': 'Permission not reviewed'}],
                'skills': [{'id': 'fixture', 'source': 'source', 'name': 'example', 'roles': ['Scout'],
                            'description': 'Fixture', 'stage': 'discovery', 'mode': 'advisory',
                            'upstream_path': 'example', 'guidance': 'Original fixture guidance',
                            'sha256': hashlib.sha256(content).hexdigest()}]}
    path = tmp_path / 'manifest.json'
    path.write_text(json.dumps(manifest))
    service = ResearchSkillsService(path)
    monkeypatch.setenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated')
    assert service.get_skill('fixture')['content'] is None
    assert not service.list_skills()[0]['active']
    assert service.guidance_for('Scout') == ''
    monkeypatch.setenv('RESEARCHINGOS_ACCESS_MODE', 'local')
    assert service.list_skills()[0]['active']
    monkeypatch.setenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated')
    service.manifest['skills'][0]['distribution_approved'] = True
    assert service.list_skills()[0]['active']
