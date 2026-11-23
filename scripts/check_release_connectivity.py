#!/usr/bin/env python3
"""Check the four release surfaces with local or authenticated HTTP requests."""
import argparse
import json
import os

import httpx


def check(frontend, backend, auth=None):
    checks = {
        'frontend': (frontend, '/'),
        'backend_health': (backend, '/api/health'),
        'vault_listing': (backend, '/api/vault/files'),
        'draft_listing': (backend, '/api/vault/files?category=drafts'),
    }
    result = {}
    with httpx.Client(timeout=15, follow_redirects=False) as client:
        for name, (base, path) in checks.items():
            try:
                response = client.get(base.rstrip('/') + path, auth=auth if name != 'frontend' else None)
                result[name] = response.status_code
            except httpx.HTTPError:
                result[name] = None
        if auth:
            result['anonymous_rejected'] = client.get(backend.rstrip('/') + '/api/health').status_code == 401
            refused = client.get(backend.rstrip('/') + '/api/health', auth=auth,
                                 headers={'Origin': 'https://untrusted.invalid'})
            result['foreign_origin_rejected'] = refused.status_code == 403
            login = client.post(backend.rstrip('/') + '/api/session', auth=auth)
            cookie = login.headers.get('set-cookie', '').lower()
            result['secure_cookie'] = login.status_code == 200 and all(
                attr in cookie for attr in ('httponly', 'secure', 'samesite=strict'))
    return {'passed': all(value is True or type(value) is int and value == 200 for value in result.values()),
            'checks': result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frontend', default='http://127.0.0.1:3000')
    parser.add_argument('--backend', default='http://127.0.0.1:18000')
    parser.add_argument('--authenticated', action='store_true')
    args = parser.parse_args()
    auth = None
    if args.authenticated:
        if not args.backend.startswith('https://'):
            parser.error('Authentication checks require a verified HTTPS endpoint')
        password = os.getenv('RESEARCHINGOS_PASSWORD')
        if not password:
            parser.error('Load RESEARCHINGOS_PASSWORD from a private environment')
        auth = (os.getenv('RESEARCHINGOS_OPERATOR', 'operator'), password)
    result = check(args.frontend, args.backend, auth)
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
