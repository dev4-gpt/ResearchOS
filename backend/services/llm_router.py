"""Route text generation through a shared, single-attempt execution boundary."""
from contextlib import nullcontext
import os
from urllib.parse import urlsplit

import dspy
from openai.types.chat import ChatCompletion

from services.paid_execution import (
    ExecutionBudget, ProviderFailure, configured_reservation, current_budget,
    execution_scope, gemini_request, gemini_text, provider_request,
)

_FAST_MODEL = 'openai/gpt-oss-20b'
_PROVIDER_CONFIG = {
    'GEMINI': ('GEMINI_API_KEY', '', 'gemini-2.5-flash'),
    'GROQ': ('GROQ_API_KEY', 'https://api.groq.com/openai/v1', _FAST_MODEL),
    'OPENROUTER': ('OPENROUTER_API_KEY', 'https://openrouter.ai/api/v1', 'meta-llama/llama-3.1-8b-instruct'),
    'NIM': ('NVIDIA_NIM_API_KEY', 'https://integrate.api.nvidia.com/v1', _FAST_MODEL),
}


class RoutedLM(dspy.BaseLM):
    def __init__(self, router, provider, model):
        super().__init__(model=f'{provider.lower()}/{model}', max_tokens=4096, cache=False, num_retries=0)
        self.router, self.provider, self.model_id = router, provider, model

    def forward(self, prompt=None, messages=None, **kwargs):
        text = self.router.generate_messages(messages or [{'role': 'user', 'content': prompt}],
                                             self.provider, self.model_id, 4096)
        return ChatCompletion(id='researchingos', object='chat.completion', created=0, model=self.model_id,
                              choices=[{'index': 0, 'finish_reason': 'stop',
                                        'message': {'role': 'assistant', 'content': text}}])


class LLMRouter:
    def __init__(self):
        self.active_provider = os.getenv('ACTIVE_LLM_PROVIDER', 'GEMINI').strip().upper()
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'qwen3.5:4b')
        self.ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434/v1')

    def _key(self, provider):
        if provider == 'GEMINI':
            return (os.getenv('GEMINI_API_KEYS') or os.getenv('GEMINI_API_KEY', '')).split(',')[0].strip()
        key = os.getenv(_PROVIDER_CONFIG[provider][0], '')
        return key or (os.getenv('NVIDIA_API_KEY', '') if provider == 'NIM' else '')

    def _model(self, provider):
        if provider == 'OLLAMA':
            return self.ollama_model
        if provider == 'NIM':
            return os.getenv('NVIDIA_NIM_MODEL', _FAST_MODEL)
        return _PROVIDER_CONFIG[provider][2]

    def get_dspy_lm(self, provider=None, model=None):
        provider = (provider or self.active_provider).upper()
        return RoutedLM(self, provider, model or self._model(provider))

    def generate_messages(self, messages, provider, model, max_tokens):
        if any(message.get('role') not in {'user', 'assistant', 'system', 'developer'}
               or not isinstance(message.get('content'), str) for message in messages):
            raise ValueError('Only text messages can be submitted by the research router')
        if provider == 'OLLAMA':
            url = urlsplit(self.ollama_base_url)
            # Ollama may relay to a hosted model. Meter it even on loopback.
            if url.scheme != 'http' or url.hostname not in {'127.0.0.1', '::1', 'localhost'}:
                raise ValueError('Ollama must use a loopback HTTP endpoint')
            base, key = self.ollama_base_url, 'ollama'
        else:
            base, key = _PROVIDER_CONFIG[provider][1], self._key(provider)
            if not key:
                return f'[Error] {provider} credential not configured.'
        allowed = os.getenv(f'RESEARCHINGOS_{provider}_APPROVED_MODELS', '').split(',')
        if model not in {entry.strip() for entry in allowed if entry.strip()}:
            return f'[Error] {provider} model is outside the configured paid allowlist.'

        active = current_budget()
        with nullcontext(active) if active else execution_scope(ExecutionBudget(45, 1)) as budget:
            if provider == 'GEMINI':
                system = [m['content'] for m in messages if m['role'] in {'system', 'developer'}]
                body = {'contents': [{'role': 'model' if m['role'] == 'assistant' else 'user',
                                      'parts': [{'text': m['content']}]}
                                     for m in messages if m['role'] in {'assistant', 'user'}],
                        'generationConfig': {'maxOutputTokens': max_tokens, 'temperature': 0.2,
                                             'thinkingConfig': {'thinkingBudget': 0}}}
                if system:
                    body['systemInstruction'] = {'parts': [{'text': '\n'.join(system)}]}
                result = budget.call('gemini', configured_reservation('gemini', body, max_tokens),
                                     lambda seconds: gemini_request(model, key, body, seconds))
                text = gemini_text(result)
            else:
                body = {'model': model, 'messages': messages, 'temperature': 0.2, 'max_tokens': max_tokens}
                def request(seconds):
                    return provider_request(base.rstrip('/') + '/chat/completions',
                                            {'Authorization': f'Bearer {key}'}, body, seconds)
                result = budget.call(provider.lower(), configured_reservation(provider, body, max_tokens), request)
                text = (result.get('choices') or [{}])[0].get('message', {}).get('content')
            return text or '[Error] Provider returned no text.'

    def generate_content(self, prompt, system_instruction='', provider=None, model=None):
        provider = (provider or self.active_provider).upper()
        if provider not in {*_PROVIDER_CONFIG, 'OLLAMA'}:
            return f'[Error] Unknown provider: {provider}'
        messages = [{'role': 'system', 'content': system_instruction}] if system_instruction else []
        messages.append({'role': 'user', 'content': prompt})
        return self.generate_messages(messages, provider, model or self._model(provider), 2048)

    def generate_content_with_fallback(self, prompt, system_instruction='', preferred_provider=None, model=None):
        preferred = (preferred_provider or self.active_provider).upper()
        order = list(dict.fromkeys([preferred, *_PROVIDER_CONFIG, 'OLLAMA']))
        for provider in order:
            try:
                result = self.generate_content(prompt, system_instruction, provider,
                                               model if provider == preferred else None)
            except ProviderFailure:
                # Do not send an ambiguous call again through a fallback provider.
                raise
            if result and not result.startswith('[Error]'):
                return result
        return '[Error] All providers unavailable or returned no text.'


llm_router = LLMRouter()
