"""Shared reservation, pacing, and single-attempt provider transport."""
import asyncio
from contextlib import contextmanager
from contextvars import ContextVar
from decimal import Decimal
from functools import wraps
import json
import math
import os
import threading
import time

import httpx

from services.spend_ledger import SpendLedger, SpendLimit


class ProviderFailure(RuntimeError):
    def __init__(self, status=None):
        self.code = status
        super().__init__(f'Provider returned HTTP {status}' if status else 'Provider request outcome is uncertain')


_active = ContextVar('paid_execution', default=None)


class ExecutionBudget:
    def __init__(self, seconds, max_calls=100):
        self.deadline = time.monotonic() + seconds
        self.max_calls = max_calls
        self.calls = 0
        self.failure = None
        self.lock = threading.Lock()

    def remaining(self):
        if self.failure:
            raise self.failure
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('Execution deadline exhausted')
        return remaining

    def call(self, provider, reservation, action, reserve=None):
        with self.lock:
            self.remaining()
            if self.calls >= self.max_calls:
                raise SpendLimit('Execution call limit exhausted')
            try:
                if reserve:
                    reserve()
                else:
                    reserve_provider(SpendLedger.configured(), provider, reservation, self.deadline)
                self.calls += 1
                return action(min(self.remaining(), 45))
            except (ProviderFailure, TimeoutError, SpendLimit, httpx.HTTPError) as exc:
                # A network failure can follow an accepted upstream request. Stop this
                # execution even if a caller catches the exception and tries again.
                self.failure = exc
                raise


@contextmanager
def execution_scope(budget):
    token = _active.set(budget)
    try:
        yield budget
    finally:
        _active.reset(token)


def current_budget():
    return _active.get()


def bounded_execution(function):
    @wraps(function)
    def run(*args, **kwargs):
        if current_budget():
            return function(*args, **kwargs)
        with execution_scope(ExecutionBudget(900)) as budget:
            result = function(*args, **kwargs)
            budget.remaining()
            return result
    return run


def reserve_provider(ledger, provider, usd, deadline):
    interval = float(os.getenv('RESEARCHINGOS_GEMINI_MIN_INTERVAL', '13')) if provider == 'gemini' else 0
    if not math.isfinite(interval) or (provider == 'gemini' and not 13 <= interval <= 600):
        raise SpendLimit('Gemini pacing interval must be 13..600 seconds')
    ledger.reserve(usd, provider=provider, interval=interval, deadline=deadline)


def configured_reservation(provider, body, output_tokens):
    # Deployment specifies a verified ceiling for each enabled model/provider.
    ceiling = Decimal(os.getenv(f'RESEARCHINGOS_{provider.upper()}_TOKEN_PRICE_CEILING', '0'))
    minimum = 10 if provider == 'gemini' else 100
    if not ceiling.is_finite() or ceiling < minimum:
        raise SpendLimit(f'Configure a reviewed token price ceiling of at least ${minimum}/million for {provider}')
    return (len(json.dumps(body, ensure_ascii=False).encode()) + 256 + output_tokens) * ceiling / 1_000_000


async def _request(url, headers, body, seconds):
    async def transfer():
        async with httpx.AsyncClient(timeout=seconds, follow_redirects=False, trust_env=False) as client:
            async with client.stream('POST', url, json=body, headers=headers) as response:
                if response.status_code != 200:
                    raise ProviderFailure(response.status_code)
                data = bytearray()
                async for chunk in response.aiter_bytes():
                    data.extend(chunk)
                    if len(data) > 2_000_000:
                        raise ProviderFailure()
                try:
                    return json.loads(data)
                except ValueError as exc:
                    raise ProviderFailure() from exc

    try:
        return await asyncio.wait_for(transfer(), seconds)
    except httpx.TimeoutException as exc:
        raise TimeoutError('Provider request timed out') from exc
    except httpx.HTTPError as exc:
        raise ProviderFailure() from exc


def provider_request(url, headers, body, seconds):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(_request(url, headers, body, seconds))
    # Some legacy synchronous callers run on an API event loop.
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(lambda: asyncio.run(_request(url, headers, body, seconds))).result()


def gemini_request(model, key, body, seconds):
    import re

    if not re.fullmatch(r'gemini-[a-z0-9.-]+', model):
        raise ValueError('Expected an explicit Gemini model ID')
    return provider_request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
                            {'x-goog-api-key': key}, body, seconds)


def gemini_text(response):
    candidates = response.get('candidates') or []
    parts = candidates[0].get('content', {}).get('parts', []) if candidates else []
    return ''.join(part.get('text', '') for part in parts if not part.get('thought'))
