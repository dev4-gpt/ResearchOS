import json
import os
import time
from datetime import date, datetime, timezone

import dspy
from google import genai as modern_genai
from openai import OpenAI

# GROQ retired llama-3.1-8b-instant for free/developer-tier keys (ERR-103); its
# own migration doc recommends this replacement. NVIDIA NIM independently
# retired meta/llama-3.1-8b-instruct (410 Gone, EOL 2026-08-26); this is also
# hosted on NIM, so one model covers both providers' defaults instead of
# tracking two separate names. Verified live against both providers'
# /v1/models on 2026-09-11 -- if either 404s again, re-check that endpoint
# before hardcoding a replacement (that live check is what ERR-103 skipped).
_FAST_FALLBACK_MODEL = "openai/gpt-oss-20b"

# Gemini's free tier caps at 20 requests/day, shared across every feature that
# reads GEMINI_API_KEY (graphify semantic extraction, CouncilOrchestrator
# debate/research generation, drafting) -- see ERR-102. This file tracks a
# process-independent daily count so one feature exhausting the budget fails
# fast and falls through to another provider instead of every caller finding
# out separately via a live 429.
_GEMINI_QUOTA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "vault", "00_System", "gemini_quota_state.json"
)
_GEMINI_DAILY_LIMIT = int(os.getenv("GEMINI_DAILY_REQUEST_LIMIT", "20"))


def _gemini_quota_remaining() -> int:
    today = date.today().isoformat()
    try:
        with open(_GEMINI_QUOTA_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        state = {}
    if state.get("date") != today:
        state = {"date": today, "count": 0}
    return max(0, _GEMINI_DAILY_LIMIT - state.get("count", 0))


def _gemini_quota_record_use() -> None:
    today = date.today().isoformat()
    try:
        with open(_GEMINI_QUOTA_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        state = {}
    if state.get("date") != today:
        state = {"date": today, "count": 0}
    state["count"] = state.get("count", 0) + 1
    state["last_used_at"] = datetime.now(timezone.utc).isoformat()
    os.makedirs(os.path.dirname(_GEMINI_QUOTA_PATH), exist_ok=True)
    with open(_GEMINI_QUOTA_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


class LLMRouter:
    def __init__(self):
        # Determine global fallback provider if not specified
        self.active_provider = os.getenv("ACTIVE_LLM_PROVIDER", "GEMINI").strip().upper()

        # Keys
        self.gemini_keys = [k.strip() for k in (os.getenv("GEMINI_API_KEYS", "") or os.getenv("GEMINI_API_KEY", "")).split(",") if k.strip()]
        self.nim_api_key = os.getenv("NVIDIA_NIM_API_KEY", "")
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")

        # Local endpoints
        self.ollama_model = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

        # Init Clients
        self.genai_clients = [modern_genai.Client(api_key=k) for k in self.gemini_keys] if self.gemini_keys else []
        self.ollama_client = OpenAI(base_url=self.ollama_base_url, api_key="ollama")

        self.groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=self.groq_api_key) if self.groq_api_key else None
        self.openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=self.openrouter_api_key) if self.openrouter_api_key else None
        self.nim_client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=self.nim_api_key) if self.nim_api_key else None

        print(f"LLMRouter Initialized. Default Fallback Provider: {self.active_provider}")

    def get_dspy_lm(self, provider: str = None, model: str = None):
        """Returns a configured dspy.LM object for the specified provider."""
        prov = (provider or self.active_provider).upper()

        if prov == "NIM" and self.nim_api_key:
            nim_model = model or os.getenv("NVIDIA_NIM_MODEL", _FAST_FALLBACK_MODEL)
            return dspy.LM(f"openai/{nim_model}", api_key=self.nim_api_key, api_base="https://integrate.api.nvidia.com/v1", max_tokens=4096)

        elif prov == "OLLAMA":
            m = model or self.ollama_model
            return dspy.LM(model=f"openai/{m}", api_key="ollama", api_base=self.ollama_base_url, max_tokens=4096)

        elif prov == "GROQ" and self.groq_api_key:
            m = model or _FAST_FALLBACK_MODEL
            return dspy.LM(model=f"openai/{m}", api_key=self.groq_api_key, api_base="https://api.groq.com/openai/v1", max_tokens=4096)

        elif prov == "OPENROUTER" and self.openrouter_api_key:
            m = model or "meta-llama/llama-3.1-8b-instruct"
            return dspy.LM(model=f"openai/{m}", api_key=self.openrouter_api_key, api_base="https://openrouter.ai/api/v1", max_tokens=4096)

        else: # Default GEMINI
            api_key = self.gemini_keys[0] if self.gemini_keys else ""
            m = model or "gemini-2.5-flash"
            return dspy.LM(f"gemini/{m}", api_key=api_key, max_tokens=4096)

    def generate_content(self, prompt: str, system_instruction: str = "", provider: str = None, model: str = None) -> str:
        """Universal text generation function routing to specific provider."""
        prov = (provider or self.active_provider).upper()

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            if prov == "OLLAMA":
                m = model or self.ollama_model
                response = self.ollama_client.chat.completions.create(model=m, messages=messages, temperature=0.2, max_tokens=2048)
                return response.choices[0].message.content

            elif prov == "GROQ":
                if not self.groq_client: return "[Error] GROQ_API_KEY not set."
                m = model or _FAST_FALLBACK_MODEL
                response = self.groq_client.chat.completions.create(model=m, messages=messages, temperature=0.2, max_tokens=2048)
                return response.choices[0].message.content

            elif prov == "OPENROUTER":
                if not self.openrouter_client: return "[Error] OPENROUTER_API_KEY not set."
                m = model or "meta-llama/llama-3.1-8b-instruct"
                response = self.openrouter_client.chat.completions.create(model=m, messages=messages, temperature=0.2, max_tokens=2048)
                return response.choices[0].message.content

            elif prov == "NIM":
                if not self.nim_client: return "[Error] NVIDIA_NIM_API_KEY not set."
                m = model or os.getenv("NVIDIA_NIM_MODEL", _FAST_FALLBACK_MODEL)
                response = self.nim_client.chat.completions.create(model=m, messages=messages, temperature=0.2, max_tokens=2048)
                return response.choices[0].message.content

            elif prov == "GEMINI":
                if not self.genai_clients: return "[Error] GEMINI_API_KEY not set."
                m = model or "gemini-2.5-flash"
                client = self.genai_clients[0]
                config = {}
                if system_instruction: config["system_instruction"] = system_instruction
                response = client.models.generate_content(model=m, contents=prompt, config=config)
                return response.text if response and response.text else ""

            else:
                return f"[Error] Unknown provider: {prov}"

        except Exception as e:
            print(f"{prov} Error: {e}")
            return ""

    def _provider_available(self, prov: str) -> bool:
        if prov == "GEMINI":
            return bool(self.genai_clients) and _gemini_quota_remaining() > 0
        if prov == "GROQ":
            return bool(self.groq_client)
        if prov == "OPENROUTER":
            return bool(self.openrouter_client)
        if prov == "NIM":
            return bool(self.nim_client)
        if prov == "OLLAMA":
            return True  # local, no key required; a real failure surfaces from the call itself
        return False

    def generate_content_with_fallback(
        self, prompt: str, system_instruction: str = "", preferred_provider: str = None, model: str = None
    ) -> str:
        """Try preferred_provider first, then walk the rest of the chain on failure.

        Centralizes what council.py/meta_review_council.py/venue_advisor.py each
        used to implement separately as a hardcoded single provider (ERR-102/103):
        one broken model ID or one exhausted Gemini quota no longer means every
        call site fails independently and falls back to placeholder text. Skips
        Gemini automatically once its shared daily quota (ERR-102) is spent,
        rather than spending a request finding that out live.
        """
        order = ["GEMINI", "GROQ", "OPENROUTER", "NIM", "OLLAMA"]
        preferred = (preferred_provider or "").upper()
        if preferred in order:
            order = [preferred] + [p for p in order if p != preferred]

        attempted = []
        for prov in order:
            if not self._provider_available(prov):
                continue
            attempted.append(prov)
            if prov == "GEMINI":
                _gemini_quota_record_use()
            result = self.generate_content(prompt, system_instruction, provider=prov, model=model if prov == preferred else None)
            if result and not result.startswith("[Error]"):
                return result

        return f"[Error] All providers exhausted or unavailable (tried: {', '.join(attempted) or 'none configured'})"

# Singleton instance
llm_router = LLMRouter()
