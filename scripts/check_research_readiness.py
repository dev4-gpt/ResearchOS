#!/usr/bin/env python3
"""Probe prerequisites without provider calls, secret output or runtime mutations."""
import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from services.research_engines import status, write_json
from services.openresearch import OpenResearchService
from services.paperorchestra_worker import preflight


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check():
    checks = {}
    backend = os.getenv('RESEARCHINGOS_BACKEND_URL', 'http://127.0.0.1:8000').rstrip('/')
    frontend = os.getenv('RESEARCHINGOS_FRONTEND_URL', 'http://127.0.0.1:3000').rstrip('/')
    opener = build_opener(NoRedirect())
    for name, url in {
        'frontend': frontend + '/',
        'backend': backend + '/api/health',
        'vault': backend + '/api/vault/files',
        'publisher': backend + '/api/vault/files?category=drafts',
    }.items():
        try:
            request = Request(url)
            password = os.getenv('RESEARCHINGOS_PASSWORD')
            if name != 'frontend' and password:
                parsed = urlparse(url)
                if parsed.scheme != 'https' and parsed.hostname not in {'127.0.0.1', 'localhost', '::1'}:
                    raise ValueError('Credentials require HTTPS or loopback')
                encoded = base64.b64encode((os.getenv('RESEARCHINGOS_OPERATOR', 'operator') + ':' + password).encode()).decode()
                request.add_header('Authorization', 'Basic ' + encoded)
            with opener.open(request, timeout=3) as response:
                checks[name] = {'passed': response.status == 200, 'http_status': response.status}
        except Exception as exc:
            checks[name] = {'passed': False, 'error': str(exc)}
    engines = status()
    checks['source_pins'] = {'passed': all(e['sources_verified'] for e in engines['engines'].values())}
    checks['engines_enabled'] = {'passed': all(e['enabled'] for e in engines['engines'].values())}
    checks['engine_provider_configured'] = {'passed': engines['gemini_key_configured']}
    discovery = OpenResearchService().status()
    checks['openresearch'] = {'passed': discovery['available'], 'version': discovery['version']}
    try:
        from services.research_engines import docker_preflight
        docker_preflight()
        checks['candidate_runtime'] = {'passed': True}
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        checks['candidate_runtime'] = {'passed': False, 'error': str(exc)}
    try:
        preflight(os.getenv('PAPERORCHESTRA_IMAGE', ''))
        checks['writer_runtime'] = {'passed': True}
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        checks['writer_runtime'] = {'passed': False, 'error': str(exc)}
    return {'checked_at': datetime.now(timezone.utc).isoformat(), 'checks': checks,
            'prerequisites_ready': all(v['passed'] for v in checks.values()),
            'production_ready': False,
            'release_evidence_required': ['Live provider and Docker isolation tests',
                'Reviewed dataset and independent candidate replay',
                'Locked writer image dependencies and provider spending controls',
                'End-to-end manuscript citation/claim/venue review',
                'Authenticated deployment, backup/restore and recovery validation']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = check()
    if args.output:
        write_json(args.output, report)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['prerequisites_ready'] else 1)
