"""Small CRL pilot HTTP client. Never transports private keys."""
from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from crl_events import sign_event
from research_state import derive_state
import ipaddress
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from crl_events import verify_event


class ClientError(Exception):
    pass


class Client:
    def __init__(self, base_url: str):
        url = urlsplit(base_url)
        if url.username or url.password:
            raise ClientError('URL credentials are not allowed')
        if url.scheme not in ('http', 'https') or not url.hostname or url.path not in ('', '/') or url.query or url.fragment:
            raise ClientError('Expected an HTTP(S) origin without path, query or fragment')
        if url.scheme != 'https':
            try:
                if not ipaddress.ip_address(url.hostname).is_loopback:
                    raise ClientError('HTTPS is required outside numeric loopback')
            except ValueError as exc:
                raise ClientError('HTTPS is required outside numeric loopback') from exc
        self.base_url = base_url.rstrip('/')

    def _request(self, path: str, event: dict | None = None) -> dict:
        data = json.dumps(event).encode('utf-8') if event is not None else None
        request = Request(self.base_url + path, data=data,
            headers={'Content-Type': 'application/json'} if data is not None else {},
            method='POST' if data is not None else 'GET')
        try:
            with urlopen(request, timeout=10) as response:
                return json.load(response)
        except HTTPError as error:
            raise ClientError(f'HTTP {error.code}: {error.read(1024).decode("utf-8", "replace")}') from error
        except URLError as error:
            raise ClientError(f'Connection failed: {error.reason}') from error

    def submit(self, event: dict) -> dict:
        verify_event(event)
        return self._request('/events', event)

    def list(self, problem: str) -> dict:
        return self._request('/events?' + urlencode({'problem': problem}))

    def export(self, problem: str, root: str) -> dict:
        return self._request('/export?' + urlencode({'problem': problem, 'root': root}))


def _load_key(path: Path) -> Ed25519PrivateKey:
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077:
        raise ClientError('Key file must be regular with permissions 0600')
    if info.st_size != 32:
        raise ClientError('Invalid key length')
    with path.open('rb') as file:
        if os.fstat(file.fileno()).st_ino != info.st_ino:
            raise ClientError('Key file changed during read')
        return Ed25519PrivateKey.from_private_bytes(file.read())


def main() -> None:
    parser = argparse.ArgumentParser(description='Private CRL pilot client (agent keys only)')
    sub = parser.add_subparsers(dest='action', required=True)
    keygen = sub.add_parser('keygen')
    keygen.add_argument('--key', type=Path, required=True)
    publish = sub.add_parser('publish')
    publish.add_argument('--url', required=True)
    publish.add_argument('--key', type=Path, required=True)
    publish.add_argument('--problem', required=True)
    publish.add_argument('--kind', required=True)
    publish.add_argument('--content', required=True, help='JSON object')
    publish.add_argument('--relation-type')
    publish.add_argument('--target')
    export = sub.add_parser('export')
    export.add_argument('--url', required=True)
    export.add_argument('--problem', required=True)
    export.add_argument('--root', required=True)
    state = sub.add_parser('state')
    state.add_argument('--url', required=True)
    state.add_argument('--problem', required=True)
    state.add_argument('--root', required=True)
    state.add_argument('--at', type=int, help='Unix timestamp; defaults to current time')
    args = parser.parse_args()
    try:
        if args.action == 'keygen':
            key = Ed25519PrivateKey.generate()
            fd = os.open(args.key, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_NOFOLLOW', 0), 0o600)
            with os.fdopen(fd, 'wb') as file:
                file.write(key.private_bytes_raw())
            result = {'public_key': key.public_key().public_bytes_raw().hex(), 'key_file': str(args.key)}
        elif args.action == 'publish':
            content = json.loads(args.content)
            if not isinstance(content, dict):
                raise ClientError('Content must be a JSON object')
            if bool(args.relation_type) != bool(args.target):
                raise ClientError('--relation-type and --target must be provided together')
            relations = [{'type': args.relation_type, 'target': args.target}] if args.target else []
            event = sign_event(_load_key(args.key), kind=args.kind, problem=args.problem,
                content=content, created_at=int(time.time()), relations=relations)
            result = Client(args.url).submit(event)
        else:
            result = Client(args.url).export(args.problem, args.root)
            if args.action == 'state':
                result = derive_state(result, now=args.at if args.at is not None else int(time.time()))
        print(json.dumps(result, ensure_ascii=False))
    except (ClientError, ValueError, OSError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == '__main__':
    main()
