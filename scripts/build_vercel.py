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
        ('href="/index.html#', 'href="/#'),
        ('href="/index.html"', 'href="/"'),
        ('href="/galerie.html"', 'href="/galerie"'),
        ('href="/sortiment.html"', 'href="/sortiment"'),
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


def apply_root_seo(path: Path) -> None:
    if not path.exists():
        return
    name = path.name
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
    content = ensure_footer_credit(content)
    content = ensure_vercel_analytics(content)
    path.write_text(content, encoding='utf-8')
    print(f'  patched {path.relative_to(ROOT)}')


def main() -> int:
    print('Building static site for Vercel…')

    root_pages = [
        ROOT / 'index.html',
        ROOT / 'sortiment.html',
        ROOT / 'galerie.html',
    ]

    for page in root_pages:
        patch_file(page)

    # Sortiment hub also at /sortiment/
    sortiment_dir = ROOT / 'sortiment'
    sortiment_dir.mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'sortiment.html', sortiment_dir / 'index.html')
    print('  copied sortiment.html → sortiment/index.html')

    # Regenerate gallery + sortiment data/pages.
    scripts = [
        ROOT / 'scripts' / 'gen_gallery.py',
        ROOT / 'scripts' / 'gen_products.py',
    ]
    for script in scripts:
        if script.exists():
            print(f'  running {script.name}…')
            subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)

    # Re-patch after generators (they may write relative paths).
    for page in root_pages:
        patch_file(page)
    patch_file(sortiment_dir / 'index.html')

    for html_path in (ROOT / 'sortiment').rglob('index.html'):
        patch_file(html_path)

    for page in root_pages:
        apply_root_seo(page)
    apply_root_seo(sortiment_dir / 'index.html')

    sitemap_script = ROOT / 'scripts' / 'gen_sitemap.py'
    if sitemap_script.exists():
        print('  running gen_sitemap.py…')
        subprocess.run([sys.executable, str(sitemap_script)], cwd=ROOT, check=True)

    print('Done.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
