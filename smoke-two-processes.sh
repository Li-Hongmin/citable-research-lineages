#!/usr/bin/env bash
set -euo pipefail
cd /opt/crl-pilot
/opt/crl-pilot/venv/bin/python - <<'PY'
import json, urllib.request, urllib.parse
from crl_events import demo
from crl_server import Store
from pathlib import Path
source = Store(Path('/var/lib/crl-pilot/events.json'))
destination = Store(Path('/var/lib/crl-pilot/events-second.json'))
problem = 'demo:even-integers'
claim = next(e for e in source.list(problem) if e['body']['kind'] == 'CLAIM')
base = 'http://127.0.0.1:8765'
query = urllib.parse.urlencode({'problem': problem, 'root': claim['id']})
with urllib.request.urlopen(base + '/export?' + query) as r:
    packet = json.load(r)
assert any(e['body']['kind'] == 'CHALLENGE' for e in packet['events'])
for event in packet['events']:
    req = urllib.request.Request('http://127.0.0.1:8766/events', data=json.dumps(event).encode(), headers={'Content-Type':'application/json'}, method='POST')
    with urllib.request.urlopen(req) as r:
        assert r.status == 201
with urllib.request.urlopen('http://127.0.0.1:8766/export?' + query) as r:
    recovered = json.load(r)
assert recovered['snapshot']['id'] == packet['snapshot']['id']
assert {e['id'] for e in recovered['events']} == {e['id'] for e in packet['events']}
print(json.dumps({'source_events': len(packet['events']), 'destination_events': len(recovered['events']), 'challenge_preserved': True, 'snapshot_match': True, 'same_vm': True}))
PY
