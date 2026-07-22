#!/usr/bin/env python3
"""Local static server with the same clean URL rewrites as vercel.json."""
from __future__ import annotations

import argparse
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
}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path in REWRITES:
            qs = ""
            if "?" in self.path:
                qs = "?" + self.path.split("?", 1)[1]
            self.path = REWRITES[path] + qs
        return super().do_GET()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), partial(Handler))
    print(f"Serving {ROOT} at http://{args.host}:{args.port}/")
    print("Rewrites: /faq /galerie /sortiment")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
