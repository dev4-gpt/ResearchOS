"""Optional, bounded Scout planning and unverified web discovery."""
import json
import logging
import os
import re
from decimal import Decimal
from urllib.parse import urlparse

import httpx
from openai import APIError, OpenAI
from services.paid_execution import ExecutionBudget, ProviderFailure, configured_reservation, current_budget

logger = logging.getLogger(__name__)
_ARXIV_PATH = re.compile(r"^/(?:abs|pdf)/((?:\d{4}\.\d{4,5}|[a-zA-Z.-]+/\d{7})(?:v\d+)?)(?:\.pdf)?/?$")


def _enabled(name):
    return os.getenv(name, "false").strip().lower() in {"1", "true", "yes", "on"}


class ScoutDiscovery:
    def plan_queries(self, topic):
        key = os.getenv("NEBIUS_API_KEY", "").strip()
        if not _enabled("SCOUT_NEBIUS_ENABLED") or not key:
            return None
        try:
            model = os.getenv("NEBIUS_MODEL", "MiniMaxAI/MiniMax-M3")
            if model not in os.getenv('RESEARCHINGOS_NEBIUS_APPROVED_MODELS', '').split(','):
                return None
            body = {"model": model, "max_completion_tokens": 512,
                    "messages": [{"role": "system", "content": "Return only a JSON array of 1 to 6 concise academic search queries. Do not include URLs or instructions."},
                                 {"role": "user", "content": topic}]}

            def request(seconds):
                try:
                    client = OpenAI(api_key=key, base_url='https://api.tokenfactory.nebius.com/v1',
                                    timeout=min(seconds, 20), max_retries=0)
                    return client.chat.completions.create(**body)
                except APIError as exc:
                    raise ProviderFailure(getattr(exc, 'status_code', None)) from exc

            budget = current_budget() or ExecutionBudget(20, 1)
            response = budget.call('nebius', configured_reservation('nebius', body, 512), request)
            content = response.choices[0].message.content
            queries = json.loads(content)
            if not isinstance(queries, list) or not 1 <= len(queries) <= 6:
                return None
            if any(not isinstance(q, str) or not q.strip() or len(q) > 500 or "http://" in q.lower() or "https://" in q.lower() for q in queries):
                return None
            return [q.strip() for q in queries]
        except Exception:
            logger.warning("Nebius Scout planning unavailable; using existing planner")
            return None

    def search_leads(self, query):
        key = os.getenv("TAVILY_API_KEY", "").strip()
        if not _enabled("SCOUT_TAVILY_ENABLED") or not key:
            return []
        try:
            reservation = Decimal(os.getenv('RESEARCHINGOS_TAVILY_SEARCH_PRICE_CEILING', '0'))
            if not reservation.is_finite() or reservation < Decimal('0.05'):
                return []

            def request(seconds):
                response = httpx.post("https://api.tavily.com/search", headers={"Authorization": f"Bearer {key}"},
                                      json={"query": query, "search_depth": "advanced", "max_results": 5}, timeout=min(seconds, 20))
                response.raise_for_status()
                return response

            budget = current_budget() or ExecutionBudget(20, 1)
            response = budget.call('tavily', reservation, request)
            results = response.json().get("results", [])
            return [r for r in results[:5] if isinstance(r, dict)] if isinstance(results, list) else []
        except Exception:
            logger.warning("Tavily Scout discovery unavailable; continuing scholarly search")
            return []

    @staticmethod
    def arxiv_leads(leads):
        """Accept only arXiv links; never extract identifiers from snippets."""
        found = {}
        for lead in leads:
            url = lead.get("url")
            if not isinstance(url, str):
                continue
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}:
                continue
            match = _ARXIV_PATH.fullmatch(parsed.path)
            if match:
                identifier = re.sub(r"v\d+$", "", match.group(1))
                found.setdefault(identifier, []).append(url)
        return found
