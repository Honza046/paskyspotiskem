#!/usr/bin/env python3
"""Local static server with the same clean URL rewrites as vercel.json.

Proxies /api/* to the local Node API (scripts/local_api_server.js) so admin
and info-banner work on the same origin (cookies, fetch).
"""
from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REWRITES = {
    "/faq": "/faq.html",
    "/faq/": "/faq.html",
    "/galerie": "/galerie.html",
    "/galerie/": "/galerie.html",
    "/sortiment": "/sortiment.html",
    "/sortiment/": "/sortiment.html",
    "/admin": "/admin/index.html",
    "/admin/": "/admin/index.html",
}

API_PORT = int(os.environ.get("LOCAL_API_PORT", "3001"))
API_ORIGIN = f"http://127.0.0.1:{API_PORT}"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _proxy_api(self) -> None:
        target = API_ORIGIN + self.path
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length) if length > 0 else None

        headers = {}
        for key in ("Content-Type", "Cookie", "Accept", "Authorization"):
            val = self.headers.get(key)
            if val:
                headers[key] = val

        req = urllib.request.Request(
            target,
            data=body,
            headers=headers,
            method=self.command,
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = resp.read()
                self.send_response(resp.status)
                hop = {"transfer-encoding", "connection", "content-encoding"}
                for key, value in resp.headers.items():
                    if key.lower() in hop:
                        continue
                    if key.lower() == "set-cookie":
                        # urllib may collapse; also try get_all if available
                        continue
                    self.send_header(key, value)
                # Preserve Set-Cookie for admin session
                raw = getattr(resp.headers, "get_all", None)
                cookies = raw("Set-Cookie") if callable(raw) else None
                if not cookies:
                    one = resp.headers.get("Set-Cookie")
                    cookies = [one] if one else []
                for cookie in cookies:
                    if cookie:
                        self.send_header("Set-Cookie", cookie)
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
        except urllib.error.HTTPError as err:
            payload = err.read()
            self.send_response(err.code)
            for key, value in err.headers.items():
                if key.lower() in {"transfer-encoding", "connection", "content-encoding"}:
                    continue
                if key.lower() == "set-cookie":
                    continue
                self.send_header(key, value)
            raw = getattr(err.headers, "get_all", None)
            cookies = raw("Set-Cookie") if callable(raw) else None
            if not cookies:
                one = err.headers.get("Set-Cookie")
                cookies = [one] if one else []
            for cookie in cookies:
                if cookie:
                    self.send_header("Set-Cookie", cookie)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except Exception as exc:  # noqa: BLE001
            msg = (
                '{"ok":false,"error":"Lokální API neběží. Spusťte npm run dev '
                '(nebo zvlášť node scripts/local_api_server.js). '
                + str(exc).replace('"', "'")
                + '"}'
            ).encode("utf-8")
            self.send_response(502)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)

    def do_GET(self):  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path.startswith("/api/"):
            return self._proxy_api()
        if path in REWRITES:
            qs = ""
            if "?" in self.path:
                qs = "?" + self.path.split("?", 1)[1]
            self.path = REWRITES[path] + qs
        return super().do_GET()

    def do_POST(self):  # noqa: N802
        if self.path.split("?", 1)[0].startswith("/api/"):
            return self._proxy_api()
        self.send_error(405)

    def do_PUT(self):  # noqa: N802
        if self.path.split("?", 1)[0].startswith("/api/"):
            return self._proxy_api()
        self.send_error(405)

    def do_OPTIONS(self):  # noqa: N802
        if self.path.split("?", 1)[0].startswith("/api/"):
            return self._proxy_api()
        self.send_error(405)


def api_port_open() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex(("127.0.0.1", API_PORT)) == 0


def start_api_subprocess() -> subprocess.Popen | None:
    if api_port_open():
        print(f"Using existing API on {API_ORIGIN}")
        return None
    env = os.environ.copy()
    env["LOCAL_API_PORT"] = str(API_PORT)
    proc = subprocess.Popen(
        ["node", str(ROOT / "scripts" / "local_api_server.js")],
        cwd=str(ROOT),
        env=env,
    )
    for _ in range(40):
        if api_port_open():
            print(f"Started local API on {API_ORIGIN} (pid {proc.pid})")
            return proc
        if proc.poll() is not None:
            break
        time.sleep(0.1)
    print("WARNING: local API did not start; /api/* will return 502", file=sys.stderr)
    return proc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-api", action="store_true", help="Do not auto-start local API")
    args = parser.parse_args()

    api_proc = None
    if not args.no_api:
        api_proc = start_api_subprocess()

    server = ThreadingHTTPServer((args.host, args.port), partial(Handler))
    print(f"Serving {ROOT} at http://{args.host}:{args.port}/")
    print("Rewrites: /faq /galerie /sortiment /admin")
    print(f"API proxy: /api/* → {API_ORIGIN}")
    print(f"Admin UI: http://{args.host}:{args.port}/admin")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        if api_proc and api_proc.poll() is None:
            api_proc.terminate()
            try:
                api_proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                api_proc.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
