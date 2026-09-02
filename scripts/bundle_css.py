#!/usr/bin/env python3
"""Slouci render blokujici stylesheety kazde stranky do jednoho souboru.

Proc:
  Kazda stranka nacita 7 az 12 samostatnych CSS souboru. Kazdy z nich blokuje
  vykresleni, takze prohlizec musi cekat na vsechny, nez zobrazi obsah.

Jak to zustava bezpecne:
  - Poradi souboru se zachova presne tak, jak bylo v HTML, takze kaskada je stejna.
  - Pravidla @import se vlozi primo na sve misto. Kdyby zustala uprostred bundlu,
    prohlizec by je ignoroval a soubor by se tise prestal nacitat.
  - Nazev bundlu je odvozeny z hashe obsahu, takze se cache invaliduje sama.
  - Puvodni seznam CSS kazde stranky se uklada do manifestu. Build je proto
    idempotentni a lze ho spustit opakovane, i kdyz uz HTML odkazuje na bundle.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS_DIR = ROOT / 'assets' / 'css'
MANIFEST = CSS_DIR / 'bundles.json'

LINK_RE = re.compile(r'[ \t]*<link rel="stylesheet" href="(/assets/css/[^"]+)"[^>]*>\n?')
IMPORT_RE = re.compile(r'@import\s+url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)\s*;')

SKIP_DIRS = {'node_modules', 'admin', 'scripts', 'api', 'lib', '.git'}


def strip_query(href: str) -> str:
    return href.split('?', 1)[0]


def read_css(href: str, seen: set[str]) -> str:
    """Nacte CSS a rekurzivne vlozi jeho @import pravidla na puvodni misto."""
    rel = strip_query(href).lstrip('/')
    path = ROOT / rel
    if not path.exists():
        print(f'    ! chybi {rel}')
        return ''
    if rel in seen:
        return ''
    seen.add(rel)
    css = path.read_text(encoding='utf-8')

    def inline(m: re.Match) -> str:
        target = m.group(1)
        if target.startswith(('http://', 'https://', '//', 'data:')):
            return m.group(0)  # externi import nechavame byt
        nested = (path.parent / target).resolve()
        try:
            nested_href = '/' + nested.relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        return f'/* vlozeno z {target} */\n' + read_css(nested_href, seen)

    return f'/* ---- {rel} ---- */\n' + IMPORT_RE.sub(inline, css)


def build_bundle(hrefs: list[str]) -> tuple[str, str]:
    """Vrati (nazev souboru, obsah) pro dany seznam CSS."""
    seen: set[str] = set()
    parts = [read_css(h, seen) for h in hrefs]
    content = '\n'.join(p for p in parts if p)
    digest = hashlib.sha1(content.encode('utf-8')).hexdigest()[:12]
    return f'bundle-{digest}.css', content


def html_pages() -> list[Path]:
    pages = []
    for path in ROOT.rglob('*.html'):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        pages.append(path)
    return sorted(pages)


def main() -> int:
    print('Bundling CSS…')
    manifest: dict[str, list[str]] = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))

    written: set[str] = set()
    changed = 0

    for path in html_pages():
        rel = path.relative_to(ROOT).as_posix()
        html = path.read_text(encoding='utf-8')
        head_end = html.find('</head>')
        if head_end == -1:
            continue
        head, rest = html[:head_end], html[head_end:]
        found = LINK_RE.findall(head)

        # Stranka uz je slozena z bundlu. Vezmeme puvodni seznam z manifestu,
        # aby se do bundlu promitly pripadne zmeny ve zdrojovych CSS.
        real = [h for h in found if '/bundle-' not in h]
        stale = [h for h in found if '/bundle-' in h]
        if real:
            manifest[rel] = real
            hrefs = real
        elif rel in manifest:
            hrefs = manifest[rel]
        elif stale:
            # Stranka odkazuje na bundle, ale chybi zaznam v manifestu. Bez nej
            # nelze puvodni seznam CSS obnovit a stranka by zustala bez stylu.
            raise SystemExit(
                f'CHYBA: {rel} odkazuje na {stale[0]}, ale bundles.json nema jeji zaznam.\n'
                f'Obnovte assets/css/bundles.json z gitu, nebo vratte puvodni <link> tagy.'
            )
        else:
            continue

        if len(hrefs) < 2:
            continue

        name, content = build_bundle(hrefs)
        out = CSS_DIR / name
        if name not in written:
            out.write_text(content, encoding='utf-8')
            written.add(name)

        bundle_link = f'    <link rel="stylesheet" href="/assets/css/{name}">\n'
        matches = list(LINK_RE.finditer(head))
        if not matches:
            continue
        # Prvni odkaz nahradime bundlem, zbyle odstranime. Poradi tim zustane zachovane.
        new_head = head[:matches[0].start()] + bundle_link
        prev_end = matches[0].end()
        for m in matches[1:]:
            new_head += head[prev_end:m.start()]
            prev_end = m.end()
        new_head += head[prev_end:]
        new_html = new_head + rest

        if new_html != html:
            path.write_text(new_html, encoding='utf-8')
            changed += 1

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

    # Uklid bundlu, na ktere uz nic neodkazuje.
    for old in CSS_DIR.glob('bundle-*.css'):
        if old.name not in written:
            old.unlink()
            print(f'  smazan zastaraly {old.name}')

    print(f'  {len(written)} bundlu, upraveno {changed} stranek')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
