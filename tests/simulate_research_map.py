"""Synthetic end-to-end rehearsal; no historical research or public network."""
import json
import tempfile
import threading
from http.server import HTTPServer
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from crl_client import Client
from crl_events import sign_event
from crl_server import Store, handler_for
from research_state import derive_state


def run():
    with tempfile.TemporaryDirectory() as directory:
        servers = [HTTPServer(('127.0.0.1', 0), handler_for(Store(Path(directory) / f'node{i}.json'))) for i in range(2)]
        threads = [threading.Thread(target=s.serve_forever, daemon=True) for s in servers]
        for t in threads: t.start()
        try:
            a, b = [Client(f'http://127.0.0.1:{s.server_port}') for s in servers]
            keys = [Ed25519PrivateKey.generate() for _ in range(3)]
            problem = 'demo:synthetic-lemma'
            events = []
            def add(actor, kind, at, content, relations=()):
                e = sign_event(keys[actor], kind=kind, problem=problem, created_at=at,
                               content=content, relations=list(relations))
                assert a.submit(e)['id'] == e['id']
                events.append(e)
                return e['id']
            p = add(0, 'PROBLEM', 1, {'title': 'Synthetic integer property'})
            claim = add(0, 'CLAIM', 2, {'proof': 'Deliberately incomplete'}, [{'type':'resolves','target':p}])
            add(1, 'REPLICATION', 3, {'outcome':'failed'}, [{'type':'reproduces','target':claim}])
            challenge = add(2, 'CHALLENGE', 4, {'gap':'Missing step'}, [{'type':'challenges','target':claim}])
            add(0, 'REVISION', 5, {'proof':'Revised draft'}, [{'type':'revises','target':claim}])
            add(1, 'REQUEST', 6, {'request_kind':'independent-verification'}, [{'type':'addresses','target':claim}])
            add(2, 'WORK', 7, {'objective':'Check the missing step','expires_at':20}, [{'type':'addresses','target':challenge}])
            packet = a.export(problem, p)
            during = derive_state(packet, now=10)
            after = derive_state(packet, now=20)
            assert during['status'] == after['status'] == 'DISPUTED'
            assert during['candidates'][0]['unresolved_challenges'] == 1
            assert during['candidates'][0]['failed_replications'] == 1
            assert len(during['active_work']) == 1 and not after['active_work']
            assert len(during['requests']) == 1
            for event in packet['events']: b.submit(event)
            replicated = b.export(problem, p)
            assert replicated['snapshot']['id'] == packet['snapshot']['id']
            assert {e['id'] for e in replicated['events']} == {e['id'] for e in packet['events']}
            print(json.dumps({'scenario':'synthetic-multi-agent', 'submitted':len(events),
                  'exported':len(packet['events']), 'status':during['status'],
                  'failed_replications':during['candidates'][0]['failed_replications'],
                  'open_challenges':during['candidates'][0]['unresolved_challenges'],
                  'active_work_before_expiry':len(during['active_work']),
                  'active_work_after_expiry':len(after['active_work']),
                  'requests':len(during['requests']), 'second_node_snapshot_match':True,
                  'coverage':during['coverage']}, ensure_ascii=False))
        finally:
            for s in servers: s.shutdown(); s.server_close()
            for t in threads: t.join()

if __name__ == '__main__':
    run()
