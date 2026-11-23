"""Credential-free writer containers use a bounded, single-provider stdio broker."""
import json
import os
import re

from services.paid_execution import ProviderFailure, configured_reservation, gemini_request

MAX_FRAME = 8_000_000
OUTPUT_TOKENS = 4096


def writer_request(frame, models, budget):
    if set(frame) != {'path', 'body'}:
        raise ValueError('Unexpected writer request envelope')
    route = re.fullmatch(r'/v1beta/models/(gemini-[a-z0-9.-]+):generateContent', frame['path'])
    if not route or route[1] not in models:
        raise ValueError('Writer request outside the approved model routes')
    body = frame['body']
    if not isinstance(body, dict) or not set(body) <= {'contents', 'systemInstruction', 'generationConfig'}:
        raise ValueError('Writer tools, grounding, cached inputs and external files are disabled')
    # Rebuild the config to prevent multiple candidates, paid tools or variable
    # output/THINK budgets being added by the upstream client.
    config = body.get('generationConfig', {})
    body['generationConfig'] = {key: config[key] for key in ('temperature', 'responseMimeType') if key in config}
    body['generationConfig'].update(maxOutputTokens=OUTPUT_TOKENS, candidateCount=1,
                                   thinkingConfig={'thinkingBudget': 0})
    contents = list(body['contents'])
    if 'systemInstruction' in body:
        contents.append(body['systemInstruction'])
    extra_image_tokens = 0
    for content in contents:
        if not set(content) <= {'role', 'parts'}:
            raise ValueError('Unsupported writer content')
        for part in content['parts']:
            if set(part) == {'text'} and isinstance(part['text'], str):
                continue
            if set(part) != {'inlineData'}:
                raise ValueError('Unsupported writer part')
            data = part['inlineData']
            if set(data) != {'mimeType', 'data'} or data['mimeType'] not in {'image/png', 'image/jpeg'}:
                raise ValueError('Only inline PNG or JPEG images are permitted')
            # Reserve more than the maximum tiling overhead for an image; the
            # full serialized image is charged as well.
            extra_image_tokens += 65536
    cost = configured_reservation('gemini', body, OUTPUT_TOKENS + extra_image_tokens)
    return budget.call('gemini', cost, lambda timeout: gemini_request(route[1], os.environ['GEMINI_API_KEY'], body, timeout))


def serve(child, models, budget, failure):
    try:
        while line := child.stdout.readline(MAX_FRAME + 1):
            if len(line) > MAX_FRAME or not line.endswith(b'\n'):
                raise ValueError('Invalid writer frame')
            result = writer_request(json.loads(line), models, budget)
            child.stdin.write(json.dumps(result).encode() + b'\n')
            child.stdin.flush()
    except (BrokenPipeError, OSError):
        if child.poll() is None:
            failure.append('Writer broker transport failed')
    except ProviderFailure as exc:
        failure.append('Writer provider quota exhausted' if exc.code == 429 else 'Writer provider request failed; no replay')
    except TimeoutError:
        failure.append('Writer provider deadline exhausted')
    except Exception as exc:
        failure.append('Writer broker blocked execution (' + type(exc).__name__ + ')')
