# Release runtimes

Build the two independent images from this directory's pinned inputs.

```sh
docker build -f deploy/runtime/tex.Dockerfile -t research-os-tex:release-validation deploy/runtime
docker build -f deploy/runtime/writer.Dockerfile -t research-os-writer:release-validation deploy/runtime
TMPDIR="$PWD/.tools" backend/.venv/bin/python scripts/validate_release_runtime.py
```

The Python build installs only binary wheels whose hashes appear in the lock. The current writer pins the Gemini SDK version used by the stdio transport and uses headless OpenCV for the CLI. To update the dependency graph, review the version changes, regenerate the Python 3.12 lock with `uv pip compile --python-version 3.12 --generate-hashes --universal deploy/runtime/writer-requirements.in -o deploy/runtime/writer-requirements.lock`, and rerun the networkless probes. Validate on the deployment architecture and use the inspected immutable image reference in service configuration.

IEEEtran class 1.8b and bibliography style 1.14 are redistributed unmodified from TeX Live 2024. Their upstream LPPL notices are retained in each file. The [IEEEtran package documentation](https://ctan.org/pkg/ieeetran) describes the class and distribution.

| File | SHA-256 |
| --- | --- |
| `IEEEtran.cls` | `da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7` |
| `IEEEtran.bst` | `314f0ece704568faf827011bac498650691b2b5ee06320720830e782416d5a5f` |
