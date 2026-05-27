"""
Shared fixtures for ResearchingOS backend tests.

All vault fixtures use tmp_path to guarantee isolation from the real vault.
"""

import os
import sys
import pytest

# Make sure the backend package root is importable regardless of cwd.
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


@pytest.fixture()
def vault(tmp_path):
    """Return a VaultManager rooted at a fresh temp directory."""
    from services.vault import VaultManager
    return VaultManager(str(tmp_path))


@pytest.fixture()
def api_client(tmp_path, monkeypatch):
    """
    Return a FastAPI TestClient with:
    - vault and orchestrator pointed at tmp_path
    - GEMINI_API_KEY unset  (forces dry-run mode)
    - VAULT_PATH set to tmp_path
    """
    # Remove the API key so the app boots in dry-run mode
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("VAULT_PATH", str(tmp_path))

    # The FastAPI app creates its global VaultManager and CouncilOrchestrator at
    # import time, so we must patch the module-level objects after import.
    import main as app_module
    from services.vault import VaultManager
    from agents.council import CouncilOrchestrator

    app_module.vault_manager = VaultManager(str(tmp_path))
    app_module.orchestrator = CouncilOrchestrator(str(tmp_path))

    from fastapi.testclient import TestClient
    return TestClient(app_module.app)
