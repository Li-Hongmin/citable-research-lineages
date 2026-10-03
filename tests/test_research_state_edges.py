import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from crl_events import sign_event, export_context
from research_state import derive_state


def test_failed_replication_is_not_positive_verification():
    k = Ed25519PrivateKey.generate()
    p = 'demo:replication'
    problem = sign_event(k, kind='PROBLEM', problem=p, created_at=1, content={})
    claim = sign_event(k, kind='CLAIM', problem=p, created_at=2, content={}, relations=[{'type':'resolves','target':problem['id']}])
    failure = sign_event(k, kind='REPLICATION', problem=p, created_at=3, content={'outcome':'failed'}, relations=[{'type':'reproduces','target':claim['id']}])
    state = derive_state(export_context([problem, claim, failure], [problem['id']], problem=p), now=4)
    assert state['status'] == 'DISPUTED'
    assert state['candidates'][0]['failed_replications'] == 1
    assert state['candidates'][0]['replications'] == 0


def test_work_expiry_must_be_bounded_and_after_start():
    k = Ed25519PrivateKey.generate()
    with pytest.raises(ValueError, match='expiry'):
        sign_event(k, kind='WORK', problem='demo:work', created_at=2, content={'objective':'X','expires_at':2})
    with pytest.raises(ValueError, match='expiry'):
        sign_event(k, kind='WORK', problem='demo:work', created_at=2, content={'objective':'X','expires_at':2+8*86400})
