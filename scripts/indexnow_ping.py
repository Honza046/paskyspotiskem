#!/usr/bin/env python3
"""Ohlasi URL webu do IndexNow (Bing, Seznam, Yandex) po nasazeni.

Seznam URL se cte primo ze sitemap.xml, takze se nove stranky ohlasi samy
a neni potreba udrzovat druhy seznam rucne.

Skript nikdy neshodi build. Kdyz IndexNow nefunguje nebo neni sit,
jen to vypise a skonci s nulou.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.paskyspotiskem.cz"
HOST = "www.paskyspotiskem.cz"
KEY_FILE = ROOT / ".indexnow-key"
SITEMAP = ROOT / "sitemap.xml"
ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls() -> list[str]:
    if not SITEMAP.exists():
        return [f"{SITE}/"]
    xml = SITEMAP.read_text(encoding="utf-8")
    urls = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    return urls or [f"{SITE}/"]


def main() -> int:
    if not KEY_FILE.exists():
        print("IndexNow: chybi .indexnow-key, preskakuji")
        return 0
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not key:
        print("IndexNow: prazdny klic, preskakuji")
        return 0

    urls = sitemap_urls()
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"{SITE}/{key}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"IndexNow: HTTP {resp.status}, ohlaseno {len(urls)} URL")
            body = resp.read().decode("utf-8", errors="replace").strip()
            if body:
                print(f"  {body}")
    except urllib.error.HTTPError as err:
        # 422 typicky znamena, ze klic jeste neni overeny. Build kvuli tomu nepadá.
        print(f"IndexNow: HTTP {err.code} ({err.reason}), pokracuji dal")
    except Exception as err:  # sit, timeout, DNS
        print(f"IndexNow: nepodarilo se ohlasit ({err}), pokracuji dal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
