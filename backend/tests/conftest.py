"""
Shared fixtures for ResearchingOS backend tests.

All vault fixtures use tmp_path to guarantee isolation from the real vault.
"""

import inspect
import os
import sys
import pytest

# Make sure the backend package root is importable regardless of cwd.
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

REPO_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
REAL_HARNESS_MEMORY = os.path.join(REPO_ROOT, "vault", "harness_memory.json")


# ---------------------------------------------------------------------------
# Durable-state isolation guards
#
# vault/harness_memory.json is a git-tracked project data file. Anything that
# runs the council pipeline records telemetry into it, so an unguarded test run
# mutates the working tree. Tests should inject an explicit tmp path (see
# CouncilOrchestrator(memory_file_path=...)); this fixture makes sure that a
# test that forgets to cannot reach the real file.
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _isolate_harness_memory(tmp_path, monkeypatch):
    """
    Two layers, both process-local (so concurrent work in the repo can never
    make this flaky):

      1. Any ContinualMemoryManager built with its *default* path is redirected
         into tmp_path. Explicit paths passed by a caller are left alone.
      2. A save_state() aimed at the real vault/harness_memory.json is refused
         and recorded, then fails the test at teardown.

    Layer 2 records rather than raises because CouncilOrchestrator wraps its
    telemetry call in a bare `except Exception`, which would swallow a raise.
    """
    from harness import continual_memory as cm

    real_init = cm.ContinualMemoryManager.__init__
    real_save = cm.ContinualMemoryManager.save_state
    default_path = inspect.signature(real_init).parameters["memory_file_path"].default
    redirected = str(tmp_path / "harness_memory.json")
    violations = []

    def guarded_init(self, memory_file_path=default_path):
        if os.path.abspath(memory_file_path) == os.path.abspath(default_path):
            memory_file_path = redirected
        real_init(self, memory_file_path)

    def guarded_save(self):
        if os.path.abspath(self.memory_file_path) == REAL_HARNESS_MEMORY:
            violations.append(self.memory_file_path)
            return
        real_save(self)

    monkeypatch.setattr(cm.ContinualMemoryManager, "__init__", guarded_init)
    monkeypatch.setattr(cm.ContinualMemoryManager, "save_state", guarded_save)

    yield

    assert not violations, (
        f"This test tried to write the git-tracked file {REAL_HARNESS_MEMORY}. "
        "Tests must not mutate project data. Inject a tmp path, e.g. "
        "CouncilOrchestrator(vault_path, memory_file_path=str(tmp_path / 'harness_memory.json'))."
    )


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
    monkeypatch.delenv("NVIDIA_NIM_API_KEY", raising=False)
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    monkeypatch.setenv("VAULT_PATH", str(tmp_path))

    # The FastAPI app creates its global VaultManager and CouncilOrchestrator at
    # import time, so we must patch the module-level objects after import.
    import main as app_module
    from services.vault import VaultManager
    from agents.council import CouncilOrchestrator

    app_module.vault_manager = VaultManager(str(tmp_path))
    app_module.orchestrator = CouncilOrchestrator(
        str(tmp_path),
        memory_file_path=str(tmp_path / "harness_memory.json"),
    )

    from fastapi.testclient import TestClient
    return TestClient(app_module.app)
