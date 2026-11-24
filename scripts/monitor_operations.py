#!/usr/bin/env python3
"""Emit a sanitized operations receipt; exit nonzero for supervisor alerting."""
import argparse
import json
import os
from urllib.parse import urlsplit

import httpx


def sanitized_receipt(receipt):
    queue_alerts = {f'{queue}_{suffix}' for queue in ('research', 'publisher')
                    for suffix in ('queue_age', 'interrupted_jobs', 'recent_failures', 'queue_full', 'worker_unavailable')}
    allowed = queue_alerts | {'low_disk', 'budget_exhausted', 'spending_configuration_invalid',
                             'paid_execution_unconfigured', 'backup_stale', 'backup_receipt_invalid', 'backup_unverified'}
    if type(receipt) is not dict or type(receipt.get('healthy')) is not bool:
        raise ValueError('Invalid monitor response')
    alerts = receipt.get('alerts')
    if type(alerts) is not list or len(alerts) > len(allowed) or any(type(a) is not str or a not in allowed for a in alerts):
        raise ValueError('Invalid monitor response')
    return {'healthy': receipt['healthy'] and not alerts, 'alerts': alerts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True, help='Approved HTTPS origin (or loopback development URL)')
    args = parser.parse_args()
    parsed = urlsplit(args.url)
    if (parsed.scheme not in {'http', 'https'} or not parsed.hostname or parsed.username or parsed.password
            or parsed.query or parsed.fragment or parsed.path not in ('', '/')
            or parsed.scheme == 'http' and parsed.hostname not in {'localhost', '127.0.0.1', '::1'}):
        parser.error('Use an HTTPS origin without embedded credentials, or loopback HTTP')
    password = os.getenv('RESEARCHINGOS_PASSWORD')
    auth = (os.getenv('RESEARCHINGOS_OPERATOR', 'operator'), password) if password else None
    try:
        with httpx.Client(timeout=15, follow_redirects=False, trust_env=False) as client:
            with client.stream('GET', args.url.rstrip('/') + '/api/operations', auth=auth) as response:
                response.raise_for_status()
                body = bytearray()
                for chunk in response.iter_bytes():
                    body.extend(chunk)
                    if len(body) > 65536:
                        raise ValueError('Monitor response exceeds byte limit')
                receipt = json.loads(body)
        # Allowlist output so changed/untrusted server responses cannot expose
        # prompts, file paths, authorization headers or arbitrary exception text.
        result = sanitized_receipt(receipt)
        print(json.dumps(result))
        return 0 if result['healthy'] else 1
    except (httpx.HTTPError, ValueError):
        print(json.dumps({'healthy': False, 'alerts': ['monitor_unavailable']}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
