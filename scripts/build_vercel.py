#!/usr/bin/env python3
"""
Prepare the project for Vercel static deployment.

- Normalizes asset paths to root-absolute (/images/, /assets/, …)
- Ensures header + footer are embedded in every HTML page
- Copies sortiment.html → sortiment/index.html
- Regenerates sortiment subpages via gen_products.py
- Regenerates galerie.html content via gen_gallery.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

from seo import (  # noqa: E402
    FAQ_DESCRIPTION,
    FAQ_TITLE,
    GALLERY_DESCRIPTION,
    GALLERY_TITLE,
    HOME_DESCRIPTION,
    HOME_FAQ,
    HOME_TITLE,
    SORTIMENT_DESCRIPTION,
    SORTIMENT_TITLE,
    apply_page_seo,
    breadcrumb_schema,
    faq_schema,
    organization_schema,
    website_schema,
)


def absolutize_html(html: str) -> str:
    """Convert relative asset and internal links to root-absolute paths."""
    replacements = [
        ('href="index.html#', 'href="/#'),
        ("href='index.html#", "href='/#"),
        ('href="index.html"', 'href="/"'),
        ("href='index.html'", "href='/'"),
        ('href="galerie.html"', 'href="/galerie"'),
        ("href='galerie.html'", "href='/galerie'"),
        ('href="sortiment.html"', 'href="/sortiment"'),
        ("href='sortiment.html'", "href='/sortiment'"),
        ('href="faq.html"', 'href="/faq"'),
        ("href='faq.html'", "href='/faq'"),
        ('href="/index.html#', 'href="/#'),
        ('href="/index.html"', 'href="/"'),
        ('href="/galerie.html"', 'href="/galerie"'),
        ('href="/sortiment.html"', 'href="/sortiment"'),
        ('href="/faq.html"', 'href="/faq"'),
        ('src="./', 'src="/'),
        ('href="./', 'href="/'),
        ('src="images/', 'src="/images/'),
        ('src="loga/', 'src="/loga/'),
        ('src="icons/', 'src="/icons/'),
        ('src="assets/', 'src="/assets/'),
        ('href="icons/', 'href="/icons/'),
        ('href="assets/', 'href="/assets/'),
        ('href="images/', 'href="/images/'),
        ("url('images/", "url('/images/"),
        ('url("images/', 'url("/images/'),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    # Product/category image folders at theme root (encoded URLs from gen_products).
    html = re.sub(
        r'src="(?!https?://|/)([^"]+)"',
        lambda m: f'src="/{m.group(1)}"' if not m.group(1).startswith('/') else m.group(0),
        html,
    )
    return html


# Stranky generovane pres gen_landing.py. Drzime seznam na jednom miste,
# aby ho pouzil patch loop i odkazy v paticce.
LANDING_SLUGS = [
    'kontakt',
    'o-nas',
    'reference',
    'vyroba-lepicich-pasek',
    'pasky-s-logem',
    'pasky-s-potiskem-pro-eshopy',
    'cena-pasky-s-potiskem',
]

FOOTER_LINKS = [
    ('/sortiment', 'Sortiment pásek'),
    ('/pasky-s-logem', 'Pásky s logem'),
    ('/pasky-s-potiskem-pro-eshopy', 'Pásky pro e-shopy'),
    ('/cena-pasky-s-potiskem', 'Cena a kalkulace'),
    ('/vyroba-lepicich-pasek', 'Výroba pásek'),
    ('/pruvodce', 'Průvodce výběrem'),
    ('/galerie', 'Galerie realizací'),
    ('/reference', 'Reference'),
    ('/o-nas', 'O nás'),
    ('/kontakt', 'Kontakt'),
    ('/faq', 'Časté otázky'),
]

FOOTER_LINKS_MARKER = '<!-- FOOTER-LINKS -->'


def ensure_footer_links(html: str) -> str:
    """Prida do paticky radek internich odkazu. Kazda stranka tak odkazuje na vsechny ostatni."""
    if FOOTER_LINKS_MARKER in html:
        return html
    anchor = '    <div class="border-t border-slate-800">'
    if anchor not in html:
        return html
    items = '\n'.join(
        f'                <a href="{href}" class="text-slate-400 transition-colors hover:text-orange-400">{label}</a>'
        for href, label in FOOTER_LINKS
    )
    block = (
        f'    {FOOTER_LINKS_MARKER}\n'
        '    <div class="border-t border-slate-800">\n'
        '        <div class="mx-auto max-w-7xl px-4 py-6">\n'
        '            <nav class="flex flex-wrap justify-center gap-x-6 gap-y-3 text-sm font-medium" aria-label="Odkazy v patičce">\n'
        f'{items}\n'
        '            </nav>\n'
        '        </div>\n'
        '    </div>\n'
    )
    return html.replace(anchor, block + anchor, 1)


def repoint_nav(html: str) -> str:
    """Presmeruje polozky Reference a Kontakty z kotev na samostatne URL."""
    if '<!-- SITE-TOP -->' not in html or '<!-- /SITE-TOP -->' not in html:
        return html
    start = html.index('<!-- SITE-TOP -->')
    end = html.index('<!-- /SITE-TOP -->')
    top = html[start:end]
    for old, new in [
        ('href="/#reference"', 'href="/reference"'),
        ('href="#reference"', 'href="/reference"'),
        ('href="/#kontakt1"', 'href="/kontakt"'),
        ('href="#kontakt1"', 'href="/kontakt"'),
    ]:
        top = top.replace(old, new)
    return html[:start] + top + html[end:]


def ensure_footer_credit(html: str) -> str:
    if 'footer-credit.css' in html:
        return html
    insert = (
        '<link rel="stylesheet" href="/assets/css/footer-credit.css">\n'
        '<script src="/assets/js/footer-credit.js"></script>\n'
    )
    if '</body>' in html:
        return html.replace('</body>', insert + '</body>', 1)
    return html


def ensure_vercel_analytics(html: str) -> str:
    if 'vercel-analytics.js' in html or '/_vercel/insights/script.js' in html:
        return html
    insert = '<script src="/assets/js/vercel-analytics.js" defer></script>\n'
    if '</body>' in html:
        return html.replace('</body>', insert + '</body>', 1)
    return html


def apply_root_seo(path: Path, kind: str | None = None) -> None:
    if not path.exists():
        return
    name = kind or path.name
    if name == 'index.html':
        content = apply_page_seo(
            path.read_text(encoding='utf-8'),
            title=HOME_TITLE,
            description=HOME_DESCRIPTION,
            path='/',
            schemas=[
                organization_schema(),
                website_schema(),
                faq_schema(HOME_FAQ),
            ],
        )
    elif name == 'galerie.html':
        content = apply_page_seo(
            path.read_text(encoding='utf-8'),
            title=GALLERY_TITLE,
            description=GALLERY_DESCRIPTION,
            path='/galerie',
            schemas=[
                breadcrumb_schema([
                    ('/', 'Domů'),
                    ('/galerie', 'Galerie'),
                ]),
            ],
        )
    elif name == 'faq.html':
        content = apply_page_seo(
            path.read_text(encoding='utf-8'),
            title=FAQ_TITLE,
            description=FAQ_DESCRIPTION,
            path='/faq',
            schemas=[
                breadcrumb_schema([
                    ('/', 'Domů'),
                    ('/faq', 'FAQ'),
                ]),
                faq_schema(HOME_FAQ),
            ],
        )
    elif name == 'sortiment.html':
        content = apply_page_seo(
            path.read_text(encoding='utf-8'),
            title=SORTIMENT_TITLE,
            description=SORTIMENT_DESCRIPTION,
            path='/sortiment',
            schemas=[
                breadcrumb_schema([
                    ('/', 'Domů'),
                    ('/sortiment', 'Sortiment'),
                ]),
            ],
        )
    else:
        return
    path.write_text(content, encoding='utf-8')
    print(f'  seo {path.relative_to(ROOT)}')


def patch_file(path: Path) -> None:
    if not path.exists():
        return
    content = absolutize_html(path.read_text(encoding='utf-8'))
    content = repoint_nav(content)
    content = ensure_footer_links(content)
    content = ensure_footer_credit(content)
    content = ensure_vercel_analytics(content)
    path.write_text(content, encoding='utf-8')
    print(f'  patched {path.relative_to(ROOT)}')


def main() -> int:
    print('Building static site for Vercel…')

    # Compile Tailwind once up-front (content files already link tw.css).
    css_cmd = ['npm', 'run', 'build:css']
    print('  running build:css…')
    subprocess.run(css_cmd, cwd=ROOT, check=True)

    root_pages = [
        ROOT / 'index.html',
        ROOT / 'sortiment.html',
        ROOT / 'galerie.html',
        ROOT / 'faq.html',
    ]

    for page in root_pages:
        patch_file(page)

    # Sortiment hub also at /sortiment/
    sortiment_dir = ROOT / 'sortiment'
    sortiment_dir.mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'sortiment.html', sortiment_dir / 'index.html')
    print('  copied sortiment.html → sortiment/index.html')

    # FAQ hub also at /faq/
    faq_dir = ROOT / 'faq'
    faq_dir.mkdir(exist_ok=True)
    if (ROOT / 'faq.html').exists():
        shutil.copy2(ROOT / 'faq.html', faq_dir / 'index.html')
        print('  copied faq.html → faq/index.html')

    # Regenerate gallery + sortiment + guide pages.
    scripts = [
        ROOT / 'scripts' / 'gen_gallery.py',
        ROOT / 'scripts' / 'gen_products.py',
        ROOT / 'scripts' / 'gen_guides.py',
        ROOT / 'scripts' / 'gen_landing.py',
    ]
    for script in scripts:
        if script.exists():
            print(f'  running {script.name}…')
            subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)

    # Rebuild CSS after generators so new utility classes are included.
    print('  running build:css (post-generate)…')
    subprocess.run(css_cmd, cwd=ROOT, check=True)

    # Re-patch after generators (they may write relative paths).
    for page in root_pages:
        patch_file(page)
    patch_file(sortiment_dir / 'index.html')

    for html_path in (ROOT / 'sortiment').rglob('index.html'):
        patch_file(html_path)

    pruvodce_dir = ROOT / 'pruvodce'
    if pruvodce_dir.is_dir():
        for html_path in pruvodce_dir.rglob('index.html'):
            patch_file(html_path)

    for slug in LANDING_SLUGS:
        patch_file(ROOT / slug / 'index.html')

    for page in root_pages:
        apply_root_seo(page)
    apply_root_seo(sortiment_dir / 'index.html', kind='sortiment.html')

    # Kopie /sortiment/ a /faq/ vznikaji drive nez se aplikuje SEO, takze by
    # jinak zustaly se starym <title>. Prekopirujeme je az po SEO kroku.
    shutil.copy2(ROOT / 'sortiment.html', sortiment_dir / 'index.html')
    if (ROOT / 'faq.html').exists():
        shutil.copy2(ROOT / 'faq.html', faq_dir / 'index.html')
    print('  resynced sortiment/index.html + faq/index.html')

    # Slouceni CSS az uplne nakonec, kdyz uz jsou vsechny stranky hotove.
    bundle_script = ROOT / 'scripts' / 'bundle_css.py'
    if bundle_script.exists():
        print('  running bundle_css.py…')
        subprocess.run([sys.executable, str(bundle_script)], cwd=ROOT, check=True)

    sitemap_script = ROOT / 'scripts' / 'gen_sitemap.py'
    if sitemap_script.exists():
        print('  running gen_sitemap.py…')
        subprocess.run([sys.executable, str(sitemap_script)], cwd=ROOT, check=True)

    print('Done.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
