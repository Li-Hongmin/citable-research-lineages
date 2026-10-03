"""Private, loopback-only CRL pilot. Agent signatures only; no owner authorization."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

from crl_events import export_context, load_events, verify_event


class Store:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def list(self, problem: str) -> list[dict]:
        if not self.path.exists():
            return []
        events = load_events(self.path.read_text(encoding="utf-8"))
        return [event for event in events if event["body"]["problem"] == problem]

    def submit(self, event: dict) -> dict:
        verify_event(event)
        # This single-process prototype performs atomic file replacement, not distributed locking.
        events = load_events(self.path.read_text(encoding="utf-8")) if self.path.exists() else []
        if event["id"] not in {e["id"] for e in events}:
            if len(events) >= 10000:
                raise ValueError("Pilot capacity exceeded")
            events.append(event)
            tmp = self.path.with_suffix(".tmp")
            with tmp.open("w", encoding="utf-8") as file:
                json.dump(events, file, ensure_ascii=False)
                file.flush()
                os.fsync(file.fileno())
            os.replace(tmp, self.path)
        return {"id": event["id"], "coverage": "local-node-only", "identity_status": "agent-key-only"}

    def export(self, problem: str, roots: list[str]) -> dict:
        return export_context(self.list(problem), roots, problem=problem)


def handler_for(store: Store):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, status: int, payload: dict):
            body = json.dumps(payload, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            url = urlsplit(self.path)
            query = parse_qs(url.query)
            if url.path == "/health":
                return self.reply(200, {"ok": True, "mode": "private-pilot", "identity_status": "agent-key-only"})
            if url.path == "/events" and query.get("problem"):
                return self.reply(200, {"events": store.list(query["problem"][0]), "coverage": "local-node-only"})
            if url.path == "/export" and query.get("problem") and query.get("root"):
                try:
                    return self.reply(200, store.export(query["problem"][0], query["root"]))
                except ValueError as error:
                    return self.reply(400, {"error": str(error)})
            return self.reply(404, {"error": "Unknown endpoint"})

        def do_POST(self):
            if self.path != "/events":
                return self.reply(404, {"error": "Unknown endpoint"})
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 65536 * 2:
                return self.reply(413, {"error": "Invalid body size"})
            try:
                body = self.rfile.read(size).decode("utf-8")
                # load_events applies duplicate-key rejection and signature verification.
                event = load_events("[" + body + "]")[0]
                return self.reply(201, store.submit(event))
            except (ValueError, UnicodeError, json.JSONDecodeError) as error:
                return self.reply(400, {"error": str(error)})
    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    HTTPServer(("127.0.0.1", args.port), handler_for(Store(args.db))).serve_forever()


if __name__ == "__main__":
    main()
