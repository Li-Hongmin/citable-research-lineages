import json
import subprocess
import sys
import tempfile
import threading
from http.server import HTTPServer
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from crl_server import Store, handler_for

ROOT = Path(__file__).resolve().parents[1]


def cli(*args):
    return subprocess.run([sys.executable, str(ROOT / 'crl_client.py'), *args], capture_output=True, text=True)


def test_cli_creates_private_key_and_submits_without_exposing_it():
    with tempfile.TemporaryDirectory() as d:
        keyfile = Path(d) / 'agent.key'
        server = HTTPServer(('127.0.0.1', 0), handler_for(Store(Path(d) / 'events.json')))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            origin = f'http://127.0.0.1:{server.server_port}'
            created = cli('keygen', '--key', str(keyfile))
            assert created.returncode == 0, created.stderr
            assert keyfile.stat().st_mode & 0o777 == 0o600
            assert keyfile.read_bytes().hex() not in created.stdout
            published = cli('publish', '--url', origin, '--key', str(keyfile),
                '--problem', 'demo:cli', '--kind', 'CLAIM', '--content', '{"proposition":"P"}')
            assert published.returncode == 0, published.stderr
            event_id = json.loads(published.stdout)['id']
            exported = cli('export', '--url', origin, '--problem', 'demo:cli', '--root', event_id)
            assert exported.returncode == 0, exported.stderr
            assert json.loads(exported.stdout)['events'][0]['id'] == event_id
            state = cli('state', '--url', origin, '--problem', 'demo:cli', '--root', event_id, '--at', '10')
            assert state.returncode == 0, state.stderr
            assert json.loads(state.stdout)['status'] == 'OPEN'
        finally:
            server.shutdown(); server.server_close(); thread.join()


def test_cli_refuses_permissive_key_file():
    with tempfile.TemporaryDirectory() as d:
        keyfile = Path(d) / 'agent.key'
        keyfile.write_bytes(Ed25519PrivateKey.generate().private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()))
        keyfile.chmod(0o644)
        result = cli('publish', '--url', 'http://127.0.0.1:1', '--key', str(keyfile),
            '--problem', 'demo:cli', '--kind', 'CLAIM', '--content', '{}')
        assert result.returncode != 0
        assert 'permissions' in result.stderr
