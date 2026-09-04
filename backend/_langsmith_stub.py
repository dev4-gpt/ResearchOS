"""Pre-empt the real `langsmith` package with a "tracing disabled" stub.

Nothing in this backend imports langchain or langsmith directly (grepped:
zero hits under backend/, excluding .venv). langchain_core is pulled in as
an unused transitive dependency of langgraph/dspy, and its
tracers/context.py, tracers/langchain.py, tracers/schemas.py etc. import
several langsmith names (`Client`, `RunTree`, `get_tracing_context`,
`run_trees`, `run_helpers`, `utils`, `evaluation.evaluator.*`) at module
level. The real langsmith package's `_openapi_client/types/` submodule is
hundreds of individually-generated files; on this iCloud-backed repository
each pays the on-demand materialization cost on a cold read, turning an
unused import into a many-minutes startup delay (ERR-097).

This app never invokes LangSmith tracing (confirmed: no LANGCHAIN_TRACING_V2
usage, no langsmith.Client() calls anywhere in backend/). Every name below
is either a documented "tracing is off" value for the few functions
langchain_core actually calls during ordinary (non-tracing) execution, or a
generic no-op placeholder for names that are only ever imported, never
called, on this app's code paths. Returning inert values for those is the
functionally correct behaviour for how this app runs, not a workaround that
changes behaviour.

The no-op placeholder is deliberately generic (any attribute access or call
returns another placeholder) rather than an exhaustive hand-enumeration of
langsmith's API surface -- enumerating it exactly is fragile against
langchain_core/langgraph/dspy version bumps adding new imports; a
placeholder that accepts anything is not.

Import this module before anything that might import langchain_core.
"""

import sys
import types


class _NoOpStub:
    """Inert stand-in for a langsmith name that is imported but never called."""

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return _NoOpStub()

    def __getattr__(self, name):
        return _NoOpStub()

    def __bool__(self):
        return False

    def __repr__(self):
        return "<langsmith-stub-noop>"


def _stub_module(module_name):
    mod = types.ModuleType(module_name)

    def __getattr__(name):
        return _NoOpStub()

    mod.__getattr__ = __getattr__
    return mod


if "langsmith" not in sys.modules:
    langsmith_stub = _stub_module("langsmith")

    run_helpers_stub = _stub_module("langsmith.run_helpers")
    setattr(run_helpers_stub, "get_tracing_context", lambda *args, **kwargs: {})

    utils_stub = _stub_module("langsmith.utils")
    setattr(utils_stub, "tracing_is_enabled", lambda *args, **kwargs: False)
    setattr(utils_stub, "get_tracer_project", lambda *args, **kwargs: "default")

    evaluator_stub = _stub_module("langsmith.evaluation.evaluator")
    setattr(evaluator_stub, "EvaluationResult", _NoOpStub)
    setattr(evaluator_stub, "EvaluationResults", _NoOpStub)

    evaluation_stub = _stub_module("langsmith.evaluation")
    setattr(evaluation_stub, "evaluator", evaluator_stub)

    setattr(langsmith_stub, "run_helpers", run_helpers_stub)
    setattr(langsmith_stub, "utils", utils_stub)
    setattr(langsmith_stub, "evaluation", evaluation_stub)

    sys.modules["langsmith"] = langsmith_stub
    sys.modules["langsmith.run_helpers"] = run_helpers_stub
    sys.modules["langsmith.utils"] = utils_stub
    sys.modules["langsmith.evaluation"] = evaluation_stub
    sys.modules["langsmith.evaluation.evaluator"] = evaluator_stub
