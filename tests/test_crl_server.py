import json
import tempfile
import unittest
from pathlib import Path

from crl_server import Store
from crl_events import sign_event
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


class StoreTest(unittest.TestCase):
    def test_claim_challenge_and_export(self):
        with tempfile.TemporaryDirectory() as d:
            store = Store(Path(d) / 'events.json')
            key = Ed25519PrivateKey.generate()
            claim = sign_event(key, kind='CLAIM', problem='demo:public', content={'proposition': 'Every integer is even'}, created_at=1)
            challenge = sign_event(key, kind='CHALLENGE', problem='demo:public', content={'counterexample': 1},
                                   relations=[{'type': 'challenges', 'target': claim['id']}], created_at=2)
            self.assertEqual(store.submit(claim)['id'], claim['id'])
            store.submit(challenge)
            exported = store.export('demo:public', [claim['id']])
            self.assertEqual({e['id'] for e in exported['events']}, {claim['id'], challenge['id']})
            self.assertEqual(exported['coverage'], 'provided-snapshot-only')
            self.assertEqual(len(Store(Path(d) / 'events.json').list('demo:public')), 2)

    def test_bad_signature_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            store = Store(Path(d) / 'events.json')
            event = sign_event(Ed25519PrivateKey.generate(), kind='CLAIM', problem='demo:public', content={'proposition': 'P'}, created_at=1)
            event['body']['content']['proposition'] = 'Q'
            with self.assertRaises(ValueError):
                store.submit(event)
