"""Authenticated operational snapshot with no prompt, secret or file contents."""
import json
import os
from pathlib import Path
import shutil
import time

from services.spend_ledger import SpendLedger, SpendLimit


def snapshot(stores, storage, workers, *, backup_receipt=None):
    alerts = []
    queues = {}
    for name, store in stores.items():
        queues[name] = store.metrics()
        if queues[name]['oldest_queued_seconds'] > 900:
            alerts.append(f'{name}_queue_age')
        if queues[name]['states'].get('interrupted', 0):
            alerts.append(f'{name}_interrupted_jobs')
        if queues[name]['failed_last_hour']:
            alerts.append(f'{name}_recent_failures')
        if queues[name]['states'].get('queued', 0) + queues[name]['states'].get('running', 0) >= store.capacity:
            alerts.append(f'{name}_queue_full')
    for name, ready in workers.items():
        if not ready:
            alerts.append(f'{name}_worker_unavailable')
    # Check each distinct filesystem target; the vault and queue databases may
    # live on separate mounts. Report labels/free bytes rather than private paths.
    disks = {name: shutil.disk_usage(path).free for name, path in storage.items()}
    if any(free < 256 * 1024 * 1024 for free in disks.values()):
        alerts.append('low_disk')
    spending = {'configured': False}
    if os.getenv('RESEARCHINGOS_SPEND_LEDGER'):
        try:
            status = SpendLedger.configured().status()
            remaining = status['cap_usd'] - status['reserved_usd']
            spending = dict(status, configured=True, remaining_usd=remaining)
            if remaining <= 0:
                alerts.append('budget_exhausted')
        except (SpendLimit, OSError):
            alerts.append('spending_configuration_invalid')
    else:
        alerts.append('paid_execution_unconfigured')
    backup = {'verified_receipt': False}
    if backup_receipt:
        try:
            receipt = json.loads(Path(backup_receipt).read_text())
            timestamp = receipt['completed_at_unix']
            if type(timestamp) not in (int, float) or not 0 < timestamp <= time.time():
                raise ValueError('Invalid backup timestamp')
            if receipt.get('verified') is not True:
                raise ValueError('Backup receipt was not verified')
            backup = {'verified_receipt': True, 'age_seconds': time.time() - timestamp}
            if backup['age_seconds'] > 86400:
                alerts.append('backup_stale')
        except (OSError, ValueError, KeyError, TypeError):
            alerts.append('backup_receipt_invalid')
    else:
        alerts.append('backup_unverified')
    return {'checked_at_unix': time.time(), 'workers': workers, 'queues': queues,
            'disk_free_bytes': disks, 'spending': spending, 'backup': backup,
            'alerts': alerts, 'healthy': not alerts}
