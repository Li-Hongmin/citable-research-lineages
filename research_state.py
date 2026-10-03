"""Snapshot-relative research view; not a scientific verdict."""
from collections import defaultdict
from crl_events import verify_event

VIEW = 'crl-demo-state-v0.1'


def derive_state(packet: dict, *, now: int) -> dict:
    if type(now) is not int or now < 0:
        raise ValueError('Expected nonnegative integer view time')
    events = packet['events']
    by_id = {}
    incoming = defaultdict(list)
    for event in events:
        verify_event(event)
        if event['body']['problem'] != packet['snapshot']['problem']:
            raise ValueError('Problem scope mismatch')
        by_id[event['id']] = event
        for relation in event['body']['relations']:
            incoming[relation['target']].append((relation['type'], event))
    candidates = []
    for event in events:
        body = event['body']
        if body['kind'] != 'CLAIM':
            continue
        claims_resolution = any(r['type'] == 'resolves' for r in body['relations'])
        challenges = [e for relation, e in incoming[event['id']]
                      if relation in ('challenges', 'blocks') and e['body']['kind'] == 'CHALLENGE']
        replications = [e for relation, e in incoming[event['id']]
                        if relation == 'reproduces' and e['body']['kind'] == 'REPLICATION']
        failed = [e for e in replications if e['body']['content'].get('outcome') == 'failed']
        passed = [e for e in replications if e['body']['content'].get('outcome') == 'passed']
        # A response is not automatically a successful resolution of a challenge.
        candidates.append({'id': event['id'], 'claims_resolution': claims_resolution,
                           'challenge_count': len(challenges), 'unresolved_challenges': len(challenges),
                           'replications': len(passed), 'failed_replications': len(failed),
                           'status': 'DISPUTED' if challenges or failed else 'CANDIDATE_SOLUTION' if claims_resolution else 'OPEN'})
    active_work = [e for e in events if e['body']['kind'] == 'WORK'
                   and type(e['body']['content'].get('expires_at')) is int
                   and e['body']['created_at'] <= now < e['body']['content']['expires_at']]
    requests = [e for e in events if e['body']['kind'] == 'REQUEST']
    return {'view_policy': VIEW, 'snapshot_id': packet['snapshot']['id'], 'coverage': packet['coverage'],
            'status': 'DISPUTED' if any(c['status'] == 'DISPUTED' for c in candidates)
                      else 'CANDIDATE_SOLUTION' if any(c['claims_resolution'] for c in candidates) else 'OPEN',
            'candidates': candidates, 'active_work': active_work, 'requests': requests,
            'external_official_status': 'not-provided'}
