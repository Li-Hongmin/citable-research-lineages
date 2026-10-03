import json
import tempfile
import threading
from http.server import HTTPServer
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from crl_events import sign_event
from crl_server import Store, handler_for
from crl_client import Client, ClientError


def test_client_submits_and_exports_with_dispute():
    with tempfile.TemporaryDirectory() as d:
        server = HTTPServer(('127.0.0.1', 0), handler_for(Store(Path(d) / 'events.json')))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            client = Client(f'http://127.0.0.1:{server.server_port}')
            key = Ed25519PrivateKey.generate()
            claim = sign_event(key, kind='CLAIM', problem='demo:client', created_at=1, content={'proposition': 'P'})
            objection = sign_event(key, kind='CHALLENGE', problem='demo:client', created_at=2,
                content={'counterexample': 'not P'}, relations=[{'type': 'challenges', 'target': claim['id']}])
            assert client.submit(claim)['id'] == claim['id']
            client.submit(objection)
            packet = client.export('demo:client', claim['id'])
            assert {e['id'] for e in packet['events']} == {claim['id'], objection['id']}
            assert client.list('demo:client')['coverage'] == 'local-node-only'
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


def test_client_refuses_plaintext_remote_and_ignores_url_credentials():
    with pytest.raises(ClientError, match='HTTPS'):
        Client('http://example.org')
    with pytest.raises(ClientError, match='credentials'):
        Client('https://user:pass@example.org')


def test_client_rejects_tampered_event_before_network():
    client = Client('http://127.0.0.1:1')
    event = sign_event(Ed25519PrivateKey.generate(), kind='CLAIM', problem='demo:client', created_at=1, content={'proposition': 'P'})
    event['body']['content']['proposition'] = 'Q'
    with pytest.raises(ValueError, match='digest'):
        client.submit(event)
