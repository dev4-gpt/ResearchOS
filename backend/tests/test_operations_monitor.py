import importlib.util
from pathlib import Path

import httpx
import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('monitor_operations', ROOT / 'scripts/monitor_operations.py')
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


@pytest.mark.parametrize('receipt', [[], None, {'healthy': True, 'alerts': ['SecretToken123']},
                                    {'healthy': True, 'alerts': [['nested']]}, {'healthy': 'true', 'alerts': []}])
def test_unknown_monitor_content_is_never_printable(receipt):
    with pytest.raises(ValueError):
        monitor.sanitized_receipt(receipt)


@pytest.mark.parametrize('body,status,expected', [
    (b'{"healthy":true,"alerts":[]}', 200, 0),
    (b'{"healthy":true,"alerts":["backup_stale"]}', 200, 1),
    (b'[]', 200, 1),
    (b'x' * 65537, 200, 1),
    (b'private failure detail', 500, 1),
])
def test_cli_exit_and_redaction(monkeypatch, capsys, body, status, expected):
    original = httpx.Client
    def client(**kwargs):
        assert kwargs['trust_env'] is False
        assert kwargs['follow_redirects'] is False
        return original(**kwargs, transport=httpx.MockTransport(lambda _: httpx.Response(status, content=body)))
    monkeypatch.setattr(monitor.httpx, 'Client', client)
    monkeypatch.setattr('sys.argv', ['monitor_operations.py', '--url', 'https://research.example'])
    assert monitor.main() == expected
    output = capsys.readouterr().out
    assert 'private failure detail' not in output
    assert len(output) < 200
