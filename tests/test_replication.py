import tempfile
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from crl_events import sign_event
from crl_server import Store


def test_two_nodes_retain_later_challenge_after_transfer():
    with tempfile.TemporaryDirectory() as tmp:
        source = Store(Path(tmp) / 'a.json')
        destination = Store(Path(tmp) / 'b.json')
        a, b = Ed25519PrivateKey.generate(), Ed25519PrivateKey.generate()
        claim = sign_event(a, kind='CLAIM', problem='demo:public', created_at=1, content={'proposition': 'All integers are even'})
        challenge = sign_event(b, kind='CHALLENGE', problem='demo:public', created_at=2, content={'counterexample': 1}, relations=[{'type': 'challenges', 'target': claim['id']}])
        source.submit(claim)
        source.submit(challenge)
        transfer = source.export('demo:public', [claim['id']])
        for event in transfer['events']:
            destination.submit(event)
        recovered = destination.export('demo:public', [claim['id']])
        assert {event['id'] for event in recovered['events']} == {claim['id'], challenge['id']}
        assert recovered['missing_event_ids'] == []
        assert source.path != destination.path
