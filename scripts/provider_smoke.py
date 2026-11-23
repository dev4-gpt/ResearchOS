#!/usr/bin/env python3
"""One bounded Gemini request; emits no credentials, prompts or provider errors."""
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from dotenv import dotenv_values
from domain.research_experiments import ExperimentSpec, EngineBudget
from services.research_engines import Meter, Gemini


def run():
    root = Path(__file__).resolve().parents[1]
    if not os.getenv('GEMINI_API_KEY'):
        key = dotenv_values(root / '.env').get('GEMINI_API_KEY')
        if key: os.environ['GEMINI_API_KEY'] = key
    # Required caller configuration; never silently create a fresh spending allowance.
    spec = ExperimentSpec(engine='harness2', mode='live', model='gemini-2.5-flash',
        budget=EngineBudget(calls=1, tokens=256, output_tokens=128, seconds=30,
                            max_usd=.03, usd_per_million_token_ceiling=100))
    meter = Meter(spec)
    result = {'kind': 'provider_connectivity_only', 'model': spec.model,
              'full_integration_validated': False}
    try:
        reply = Gemini(spec, meter).generate('Reply with exactly OK.')
        result.update(passed=reply.strip() == 'OK', response_present=bool(reply))
    except Exception as exc:
        result.update(passed=False, error_type=type(exc).__name__)
        code = getattr(exc, 'code', None)
        if isinstance(code, int): result['http_status'] = code
        status = getattr(exc, 'status', None)
        if status in {'INVALID_ARGUMENT', 'UNAUTHENTICATED', 'PERMISSION_DENIED', 'NOT_FOUND', 'RESOURCE_EXHAUSTED', 'UNAVAILABLE'}:
            result['provider_status'] = status
    result['meter'] = meter.snapshot()
    if meter.spend_ledger: result['cumulative_reservations'] = meter.spend_ledger.status()
    (root / 'docs/provider-smoke-result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1

if __name__ == '__main__': raise SystemExit(run())
