from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from crl_events import sign_event, export_context
from research_state import derive_state


def test_disputed_candidate_and_expired_work_are_separate():
    k = Ed25519PrivateKey.generate()
    problem = 'demo:state'
    p = sign_event(k, kind='PROBLEM', problem=problem, created_at=1, content={'title':'P'})
    c = sign_event(k, kind='CLAIM', problem=problem, created_at=2, content={'claim':'proof'}, relations=[{'type':'resolves','target':p['id']}])
    x = sign_event(k, kind='CHALLENGE', problem=problem, created_at=3, content={'objection':'gap'}, relations=[{'type':'challenges','target':c['id']}])
    work = sign_event(k, kind='WORK', problem=problem, created_at=4, content={'objective':'check gap','expires_at':10}, relations=[{'type':'addresses','target':x['id']}])
    request = sign_event(k, kind='REQUEST', problem=problem, created_at=5, content={'request_kind':'verification','description':'verify'}, relations=[{'type':'addresses','target':c['id']}])
    packet = export_context([p,c,x,work,request], [p['id']], problem=problem)
    state = derive_state(packet, now=9)
    assert state['snapshot_id'] == packet['snapshot']['id']
    assert state['status'] == 'DISPUTED'
    assert state['candidates'][0]['unresolved_challenges'] == 1
    assert len(state['active_work']) == 1
    assert len(state['requests']) == 1
    assert derive_state(packet, now=10)['active_work'] == []


def test_partial_export_never_claims_problem_resolved():
    k = Ed25519PrivateKey.generate()
    c = sign_event(k, kind='CLAIM', problem='demo:partial', created_at=1, content={'proof':'maybe'})
    packet = export_context([c], [c['id']], problem='demo:partial')
    assert derive_state(packet, now=2)['status'] == 'OPEN'
    assert derive_state(packet, now=2)['coverage'] == 'provided-snapshot-only'
