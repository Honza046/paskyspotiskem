#!/usr/bin/env python3
"""Ping IndexNow (Bing et al.) with key URLs after deploy."""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.paskyspotiskem.cz"
KEY_FILE = ROOT / ".indexnow-key"

URLS = [
    f"{SITE}/",
    f"{SITE}/sortiment",
    f"{SITE}/pruvodce/pasky-s-potiskem",
    f"{SITE}/pruvodce",
    f"{SITE}/galerie",
    f"{SITE}/faq",
    f"{SITE}/sortiment/bopp-pasky",
    f"{SITE}/sitemap.xml",
]


def main() -> None:
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    host = "www.paskyspotiskem.cz"
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"{SITE}/{key}.txt",
        "urlList": URLS,
    }
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(f"IndexNow HTTP {resp.status}")
        body = resp.read().decode("utf-8", errors="replace")
        if body:
            print(body)


if __name__ == "__main__":
    main()
