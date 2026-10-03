import hashlib
from copy import deepcopy

import pytest
import rfc8785
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from crl_events import demo, export_context, load_events, sign_event, verify_event


def claim(key=None, **kwargs):
    return sign_event(key or Ed25519PrivateKey.generate(), kind="CLAIM", problem="demo:test",
                      created_at=1, content={"proposition": "P"}, **kwargs)


def test_copied_public_key_cannot_impersonate_signer():
    victim, attacker = Ed25519PrivateKey.generate(), Ed25519PrivateKey.generate()
    event = claim(attacker)
    event["body"]["author_key"] = victim.public_key().public_bytes_raw().hex()
    event["id"] = "crl:event:sha256:" + hashlib.sha256(rfc8785.dumps(event["body"])).hexdigest()
    with pytest.raises(ValueError, match="signature verification"):
        verify_event(event)


def test_changed_contribution_fails_even_when_digest_is_recomputed():
    event = claim()
    event["body"]["content"]["proposition"] = "Different result"
    event["id"] = "crl:event:sha256:" + hashlib.sha256(rfc8785.dumps(event["body"])).hexdigest()
    with pytest.raises(ValueError, match="signature verification"):
        verify_event(event)


def test_canonicalization_ignores_object_property_order():
    event = claim()
    event["body"] = dict(reversed(list(event["body"].items())))
    verify_event(event)


def test_export_keeps_late_disputes_of_ancestors_and_deduplicates_replays():
    key = Ed25519PrivateKey.generate()
    base = claim(key)
    descendant = claim(key, relations=[{"type": "depends-on", "target": base["id"]}])
    objection = sign_event(Ed25519PrivateKey.generate(), kind="CHALLENGE", problem="demo:test",
                           created_at=3, content={"objection": "Failure"},
                           relations=[{"type": "challenges", "target": base["id"]}])
    bundle = export_context([base, descendant, objection, base], [descendant["id"]], problem="demo:test")
    assert {event["id"] for event in bundle["events"]} == {base["id"], descendant["id"], objection["id"]}
    assert len(bundle["events"]) == 3
    assert bundle["coverage"] == "provided-snapshot-only"


def test_missing_dependency_is_declared():
    missing = "crl:event:sha256:" + "0" * 64
    event = claim(relations=[{"type": "depends-on", "target": missing}])
    bundle = export_context([event], [event["id"]], problem="demo:test")
    assert bundle["missing_event_ids"] == [missing]


def test_cross_problem_snapshot_is_rejected():
    event = claim()
    with pytest.raises(ValueError, match="problem scopes"):
        export_context([event], [event["id"]], problem="different:problem")


def test_duplicate_properties_and_unknown_fields_are_rejected():
    with pytest.raises(ValueError, match="Duplicate JSON"):
        load_events('[{"body": {}, "body": {}}]')
    event = claim()
    event["unsigned_author"] = "someone else"
    with pytest.raises(ValueError, match="envelope fields"):
        verify_event(event)


def test_exported_bytes_are_independent_of_later_input_mutation():
    event = claim()
    original = deepcopy(event)
    bundle = export_context([event], [event["id"]], problem="demo:test")
    event["body"]["content"]["proposition"] = "Changed locally"
    assert bundle["events"] == [original]
    assert len(demo()["events"]) == 3
