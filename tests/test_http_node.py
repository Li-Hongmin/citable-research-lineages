import json
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
from http.server import HTTPServer
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from crl_events import sign_event
from crl_server import Store, handler_for


def request_json(base, path, event=None):
    body = json.dumps(event).encode() if event is not None else None
    req = urllib.request.Request(base + path, data=body, headers={'Content-Type': 'application/json'}, method='POST' if body else 'GET')
    with urllib.request.urlopen(req) as result:
        return json.load(result)


def test_http_export_import_preserves_later_dispute():
    with tempfile.TemporaryDirectory() as d:
        a = HTTPServer(('127.0.0.1', 0), handler_for(Store(Path(d) / 'a.json')))
        b = HTTPServer(('127.0.0.1', 0), handler_for(Store(Path(d) / 'b.json')))
        threads = [threading.Thread(target=server.serve_forever, daemon=True) for server in (a, b)]
        for thread in threads: thread.start()
        try:
            urls = ['http://127.0.0.1:' + str(server.server_port) for server in (a, b)]
            key = Ed25519PrivateKey.generate()
            claim = sign_event(key, kind='CLAIM', problem='demo:public', created_at=1, content={'proposition': 'All integers are even'})
            challenge = sign_event(key, kind='CHALLENGE', problem='demo:public', created_at=2, content={'counterexample': 1}, relations=[{'type': 'challenges', 'target': claim['id']}])
            for event in (claim, challenge): request_json(urls[0], '/events', event)
            path = '/export?' + urllib.parse.urlencode({'problem':'demo:public', 'root':claim['id']})
            exported = request_json(urls[0], path)
            for event in exported['events']: request_json(urls[1], '/events', event)
            replica = request_json(urls[1], path)
            assert {e['id'] for e in replica['events']} == {claim['id'], challenge['id']}
            assert replica['snapshot']['id'] == exported['snapshot']['id']
        finally:
            for server in (a, b): server.shutdown(); server.server_close()
            for thread in threads: thread.join()
