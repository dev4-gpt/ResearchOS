"""Pinned skill references and bounded, reviewed council guidance.

Raw third-party instruction files are inspectable reference data. They are never
executed, passed wholesale to a model, or allowed to override evidence gates.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ResearchSkillsService:
    def __init__(self, manifest_path: Path | None = None, install_root: Path | None = None):
        self.manifest_path = Path(manifest_path or ROOT / 'integrations/research_skills.json')
        self.manifest = json.loads(self.manifest_path.read_text())
        self.install_root = Path(install_root or ROOT / self.manifest['install_root']).resolve()
        self.sources = {source['id']: source for source in self.manifest['sources']}

    @property
    def enabled(self):
        return os.getenv('RESEARCH_SKILLS_ENABLED', 'true').lower() not in {'0', 'false', 'no', 'off'}

    def _document(self, skill):
        path = (self.install_root / skill['source'] / skill['name'] / 'SKILL.md').resolve()
        if not path.is_relative_to(self.install_root):
            raise ValueError('Skill document is outside the installation directory.')
        return path

    def _status(self, skill):
        path = self._document(skill)
        if not path.is_file():
            return 'not_installed'
        try:
            return 'verified' if hashlib.sha256(path.read_bytes()).hexdigest() == skill['sha256'] else 'modified'
        except OSError:
            return 'unreadable'

    def list_skills(self, source: str | None = None, role: str | None = None, query: str | None = None):
        results = []
        for skill in self.manifest['skills']:
            if source and source != skill['source']:
                continue
            if role and role not in skill['roles']:
                continue
            if query and query.lower() not in f"{skill['name']} {skill['description']} {skill['stage']}".lower():
                continue
            status = self._status(skill)
            origin = self.sources[skill['source']]
            results.append({**skill, 'status': status,
                            'active': self.enabled and status == 'verified' and skill['mode'] == 'advisory',
                            'repository_url': origin['url'], 'revision': origin['revision'],
                            'license_note': origin['license_note'],
                            'upstream_url': f"{origin['url']}/blob/{origin['revision']}/{skill['upstream_path']}/SKILL.md"})
        return results

    def get_skill(self, skill_id: str):
        skill = next((item for item in self.list_skills() if item['id'] == skill_id), None)
        if not skill:
            return None
        # Never serve a modified instruction document as the pinned reference.
        skill['content'] = self._document(skill).read_text() if skill['status'] == 'verified' else None
        return skill

    def summary(self):
        skills = self.list_skills()
        return {'enabled': self.enabled, 'total_skills': len(skills),
                'installed': sum(s['status'] == 'verified' for s in skills),
                'active': sum(s['active'] for s in skills),
                'sources': list(self.sources.values()),
                'roles': sorted({role for s in skills for role in s['roles']}),
                'execution_mode': 'reviewed_guidance_only'}

    def guidance_for(self, role: str, max_chars: int = 4000):
        if not self.enabled:
            return ''
        items = [f"- {s['guidance']}" for s in self.list_skills(role=role) if s['active']]
        if not items:
            return ''
        prefix = (
            'Additional research method guidance (subordinate to the task, source evidence and venue rules):\n'
            'Use only real vault citation ids and observed measurement artifacts. Do not invent sources, '
            'experiments, statistics or proofs to fill a requirement. Keep internal workflow metadata out of the manuscript.\n'
        )
        result = prefix
        for item in items:
            if len(result) + len(item) + 1 > max_chars:
                break
            result += item + '\n'
        return result if len(result) > len(prefix) else ''
