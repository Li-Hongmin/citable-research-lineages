"""Experimental agent-key signatures and snapshot-relative dispute export.

This module does not implement passkey ownership, delegation or revocation.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict, deque
from copy import deepcopy
from typing import Any

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


PROFILE = "crl/0.1-agent-key-demo"
DOMAIN = b"CRL/0.1/agent-event\x00"
KINDS = {"PROBLEM", "CLAIM", "EVIDENCE", "METHOD", "CHALLENGE", "REPLICATION", "REVISION", "WITHDRAWAL", "ATTESTATION", "WORK", "REQUEST"}
RELATIONS = {"depends-on", "supports", "challenges", "reproduces", "revises", "withdraws", "addresses", "responds-to", "resolves", "blocks"}
REVERSE_CONTEXT = {"challenges", "revises", "withdraws", "reproduces", "responds-to", "blocks", "resolves", "addresses"}  # Context links, not verdicts.
FIELDS = {"protocol", "kind", "problem", "author_key", "created_at", "relations", "content"}
EVENT_ID = re.compile(r"crl:event:sha256:[0-9a-f]{64}\Z")


def _body_bytes(body: dict[str, Any]) -> bytes:
    if not isinstance(body, dict) or set(body) != FIELDS:
        raise ValueError("Unexpected event body fields")
    if body["protocol"] != PROFILE or body["kind"] not in KINDS:
        raise ValueError("Unsupported protocol or event kind")
    if not isinstance(body["problem"], str) or not 1 <= len(body["problem"]) <= 512:
        raise ValueError("Invalid problem identifier")
    key = body["author_key"]
    if not isinstance(key, str) or re.fullmatch(r"[0-9a-f]{64}", key) is None:
        raise ValueError("Invalid agent public key")
    created = body["created_at"]
    if type(created) is not int or not 0 <= created <= 2**53 - 1:
        raise ValueError("Invalid timestamp assertion")
    relations = body["relations"]
    if not isinstance(relations, list) or len(relations) > 256:
        raise ValueError("Invalid relation list")
    for relation in relations:
        if not isinstance(relation, dict) or set(relation) != {"type", "target"}:
            raise ValueError("Invalid relation fields")
        if relation["type"] not in RELATIONS or not isinstance(relation["target"], str):
            raise ValueError("Invalid relation type or target")
        if EVENT_ID.fullmatch(relation["target"]) is None:
            raise ValueError("Invalid referenced event identifier")
    if not isinstance(body["content"], dict):
        raise ValueError("Content must be a JSON object")
    if body["kind"] == "WORK":
        expiry = body["content"].get("expires_at")
        if type(expiry) is not int or not created < expiry <= created + 7 * 86400:
            raise ValueError("WORK expiry must be after start and within seven days")
        if not isinstance(body["content"].get("objective"), str) or not body["content"]["objective"].strip():
            raise ValueError("WORK requires an objective")
    encoded = rfc8785.dumps(body)
    if len(encoded) > 65536:
        raise ValueError("Event body exceeds 64 KiB")
    return encoded


def sign_event(key: Ed25519PrivateKey, *, kind: str, problem: str, created_at: int,
               content: dict[str, Any], relations: list[dict[str, str]] | None = None) -> dict[str, Any]:
    body = {"protocol": PROFILE, "kind": kind, "problem": problem,
            "author_key": key.public_key().public_bytes_raw().hex(), "created_at": created_at,
            "relations": deepcopy(relations or []), "content": deepcopy(content)}
    encoded = _body_bytes(body)
    return {"id": "crl:event:sha256:" + hashlib.sha256(encoded).hexdigest(),
            "body": body, "signature": key.sign(DOMAIN + encoded).hex()}


def verify_event(event: dict[str, Any]) -> None:
    if not isinstance(event, dict) or set(event) != {"id", "body", "signature"}:
        raise ValueError("Unexpected event envelope fields")
    encoded = _body_bytes(event["body"])
    expected = "crl:event:sha256:" + hashlib.sha256(encoded).hexdigest()
    if event["id"] != expected:
        raise ValueError("Event digest mismatch")
    signature = event["signature"]
    if not isinstance(signature, str) or re.fullmatch(r"[0-9a-f]{128}", signature) is None:
        raise ValueError("Invalid signature encoding")
    try:
        key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(event["body"]["author_key"]))
        key.verify(bytes.fromhex(signature), DOMAIN + encoded)
    except InvalidSignature as error:
        raise ValueError("Agent signature verification failed") from error


def export_context(events: list[dict[str, Any]], roots: list[str], *, problem: str) -> dict[str, Any]:
    if len(events) > 10000 or not roots:
        raise ValueError("Expected a bounded snapshot and at least one root")
    by_id: dict[str, dict[str, Any]] = {}
    incoming: dict[str, set[str]] = defaultdict(set)
    for event in events:
        verify_event(event)
        if event["body"]["problem"] != problem:
            raise ValueError("Snapshot mixes problem scopes")
        by_id[event["id"]] = event
        for relation in event["body"]["relations"]:
            if relation["type"] in REVERSE_CONTEXT:
                incoming[relation["target"]].add(event["id"])
    if any(root not in by_id for root in roots):
        raise ValueError("An export root is absent from the snapshot")
    retained: set[str] = set()
    missing: set[str] = set()
    queue = deque(roots)
    # Follow cited dependencies and reverse dispute edges to a fixed point.
    while queue:
        identifier = queue.popleft()
        if identifier in retained or identifier in missing:
            continue
        event = by_id.get(identifier)
        if event is None:
            missing.add(identifier)
            continue
        retained.add(identifier)
        queue.extend(relation["target"] for relation in event["body"]["relations"])
        queue.extend(sorted(incoming[identifier]))
    manifest = {"problem": problem, "event_ids": sorted(by_id)}
    snapshot_id = "crl:snapshot:sha256:" + hashlib.sha256(rfc8785.dumps(manifest)).hexdigest()
    return {"profile": PROFILE, "snapshot": {"id": snapshot_id, **manifest},
            "roots": sorted(set(roots)), "events": [deepcopy(by_id[i]) for i in sorted(retained)],
            "missing_event_ids": sorted(missing), "coverage": "provided-snapshot-only",
            "identity_status": "agent-key-only; owner authorization not implemented"}


def load_events(text: str) -> list[dict[str, Any]]:
    def unique_properties(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON property")
            result[key] = value
        return result

    if len(text.encode("utf-8")) > 8 * 1024 * 1024:
        raise ValueError("Input exceeds the prototype's 8 MiB limit")
    events = json.loads(text, object_pairs_hook=unique_properties)
    if not isinstance(events, list) or len(events) > 10000:
        raise ValueError("Expected a bounded JSON event array")
    for event in events:
        verify_event(event)
    return events


def demo() -> dict[str, Any]:
    proposer, challenger = Ed25519PrivateKey.generate(), Ed25519PrivateKey.generate()
    claim = sign_event(proposer, kind="CLAIM", problem="demo:even-integers", created_at=1,
                       content={"proposition": "Every integer is even"})
    challenge = sign_event(challenger, kind="CHALLENGE", problem="demo:even-integers", created_at=2,
                           content={"counterexample": 1},
                           relations=[{"type": "challenges", "target": claim["id"]}])
    revision = sign_event(proposer, kind="REVISION", problem="demo:even-integers", created_at=3,
                          content={"proposition": "Every integer divisible by two is even"},
                          relations=[{"type": "revises", "target": claim["id"]},
                                     {"type": "depends-on", "target": challenge["id"]}])
    return export_context([claim, challenge, revision, claim], [revision["id"]],
                          problem="demo:even-integers")


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=True, indent=2))
