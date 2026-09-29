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

import os
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
    'srovnani-lepicich-pasek',
    'bezpecnostni-pasky-proti-kradezi',
]

FOOTER_COLUMNS = [
    ('Pásky', [
        ('/sortiment', 'Sortiment pásek'),
        ('/srovnani-lepicich-pasek', 'Srovnání pásek'),
        ('/pasky-s-logem', 'Pásky s logem'),
        ('/bezpecnostni-pasky-proti-kradezi', 'Bezpečnostní pásky'),
        ('/pasky-s-potiskem-pro-eshopy', 'Pásky pro e-shopy'),
    ]),
    ('Poradna', [
        ('/pruvodce', 'Průvodce výběrem'),
        ('/pruvodce/hot-melt-vs-akryl', 'HOT MELT nebo akryl'),
        ('/pruvodce/paska-na-recyklovany-karton', 'Recyklovaný karton'),
        ('/cena-pasky-s-potiskem', 'Cena pásek'),
        ('/faq', 'Časté otázky'),
    ]),
    ('Firma', [
        ('/o-nas', 'O nás'),
        ('/vyroba-lepicich-pasek', 'Výroba pásek'),
        ('/reference', 'Reference'),
        ('/galerie', 'Galerie realizací'),
        ('/kontakt', 'Kontakt'),
    ]),
]

FOOTER_GRID_START = '<!-- FOOTER-GRID -->'
FOOTER_GRID_END = '<!-- /FOOTER-GRID -->'
FOOTER_CONTACT_START = '<!--FC'

FOOTER_GRID_OPEN = '<div class="mx-auto grid max-w-7xl gap-10 px-4 py-16 sm:grid-cols-2 lg:grid-cols-4">'
LEGACY_LINKS_MARKER = '<!-- FOOTER-LINKS -->'
LEGACY_LINKS_END = '<!-- /FOOTER-LINKS -->'


def _match_div(html: str, open_at: int) -> int:
    """Vrati index za uzavíracím </div>, ktery patri k <div> na pozici open_at."""
    depth = 0
    i = open_at
    while i < len(html):
        if html.startswith('<div', i):
            depth += 1
            i += 4
        elif html.startswith('</div>', i):
            depth -= 1
            i += 6
            if depth == 0:
                return i
        else:
            i += 1
    raise ValueError('neuzavreny <div> v paticce')


def _split_top_level_divs(inner: str) -> list[str]:
    blocks, i = [], 0
    while True:
        start = inner.find('<div', i)
        if start == -1:
            return blocks
        end = _match_div(inner, start)
        blocks.append(inner[start:end])
        i = end


def _strip_legacy_links(html: str) -> str:
    """Odstrani drivejsi jednoradkovy pruh odkazu, ktery nahrazuji sloupce."""
    if LEGACY_LINKS_MARKER not in html:
        return html
    if LEGACY_LINKS_END in html:
        a = html.index(LEGACY_LINKS_MARKER)
        b = html.index(LEGACY_LINKS_END) + len(LEGACY_LINKS_END) + 1
        return html[:a].rstrip(' ') + html[b:]
    return re.sub(
        re.escape(LEGACY_LINKS_MARKER) + r'.*?</nav>\s*</div>\s*</div>\s*',
        '', html, count=1, flags=re.DOTALL,
    )


def _footer_link_columns() -> str:
    cols = []
    for heading, links in FOOTER_COLUMNS:
        items = '\n'.join(
            f'                <li><a href="{href}" class="transition-colors hover:text-orange-400">{label}</a></li>'
            for href, label in links
        )
        cols.append(
            '        <div>\n'
            f'            <h4 class="mb-5 text-sm font-bold uppercase tracking-wider text-white">{heading}</h4>\n'
            # Velikost i rozestupy drzime na urovni kontaktnich udaju vlevo,
            # jinak sloupce odkazu vyjdou o sto pixelu kratsi a vpravo zbyde diry.
            '            <ul class="space-y-4 text-base">\n'
            f'{items}\n'
            '            </ul>\n'
            '        </div>'
        )
    return '\n'.join(cols)


def rebuild_footer(html: str) -> str:
    """Prerovna paticku na pet vyvazenych sloupcu.

    Puvodni rozlozeni melo ctyri kontaktni bloky nad sebou v jednom sloupci,
    ktery byl proti sloupcum odkazu nekolikanasobne vyssi. Kontakty proto
    delime do dvou sloupcu (adresa se sitemi, spojeni) a odkazy do tri.

    Kontaktni bloky se neopisuji do kodu, prebiraji se z existujiciho HTML,
    takze zmena telefonu nebo adresy ve zdroji se propise sama. Cely blok se
    pri kazdem buildu prestavi znovu, aby se do odkazu dostaly i nove stranky.
    """
    html = _strip_legacy_links(html)

    if FOOTER_CONTACT_START in html:
        blocks = re.findall(
            re.escape(FOOTER_CONTACT_START) + r'(\d)-->(.*?)<!--/FC-->',
            html, flags=re.DOTALL,
        )
        contact = [b for _, b in sorted(blocks, key=lambda x: x[0])]
        g = html.index(FOOTER_GRID_START)
        g_end = html.index(FOOTER_GRID_END) + len(FOOTER_GRID_END) + 1
        before, after = html[:g], html[g_end:]
    elif FOOTER_GRID_OPEN in html:
        i = html.index(FOOTER_GRID_OPEN)
        j = _match_div(html, i)
        inner = html[i + len(FOOTER_GRID_OPEN):j - len('</div>')]
        contact = _split_top_level_divs(inner)
        before, after = html[:i], html[j:]
    else:
        return html

    if len(contact) < 4:
        return before + FOOTER_GRID_OPEN + '\n'.join(contact) + '</div>' + after

    def keep(idx: int) -> str:
        block = contact[idx]
        if idx == 0:
            # Nadpis "Najdete nas na adrese" je nadbytecny, adresa se pozna sama.
            # Odstranenim se levy sloupec posune nahoru a spodek ikon socialnich
            # siti sedne na uroven otevirací doby ve vedlejsim sloupci.
            block = re.sub(
                r'\s*<h4[^>]*data-i18n="footer\.address_heading"[^>]*>.*?</h4>',
                '', block, count=1, flags=re.DOTALL,
            )
        return f'{FOOTER_CONTACT_START}{idx}-->{block}<!--/FC-->'

    # 0 adresa, 1 e-mail, 2 telefon, 3 socialni site
    col_address = f'        <div class="space-y-8">\n{keep(0)}\n{keep(3)}\n        </div>'
    col_reach = f'        <div class="space-y-8">\n{keep(1)}\n{keep(2)}\n        </div>'

    grid_open = (
        '<div class="mx-auto grid max-w-7xl gap-x-8 gap-y-10 px-4 py-16 '
        'sm:grid-cols-2 lg:grid-cols-5">'
    )
    grid = (
        f'{FOOTER_GRID_START}\n'
        f'    {grid_open}\n'
        f'{col_address}\n'
        f'{col_reach}\n'
        f'{_footer_link_columns()}\n'
        '    </div>\n'
        f'    {FOOTER_GRID_END}\n'
    )
    return before + grid + after


def repoint_nav(html: str) -> str:
    """Reference → /reference; header Kontakty → /#kontakt1 (footer zůstává /kontakt)."""
    if '<!-- SITE-TOP -->' not in html or '<!-- /SITE-TOP -->' not in html:
        return html
    start = html.index('<!-- SITE-TOP -->')
    end = html.index('<!-- /SITE-TOP -->')
    top = html[start:end]
    for old, new in [
        ('href="/#reference"', 'href="/reference"'),
        ('href="#reference"', 'href="/reference"'),
    ]:
        top = top.replace(old, new)
    # Header Kontakty (desktop + mobile) → homepage sekce #kontakt1
    top = top.replace(
        'href="/kontakt" class="px-2 py-1 text-sm font-semibold text-slate-700 transition-colors hover:text-orange-600" data-i18n="nav.contacts"',
        'href="/#kontakt1" class="px-2 py-1 text-sm font-semibold text-slate-700 transition-colors hover:text-orange-600" data-i18n="nav.contacts"',
    )
    top = top.replace(
        'href="/kontakt" class="block px-2 py-2 font-semibold text-slate-800 transition-colors hover:text-orange-600" data-i18n="nav.contacts"',
        'href="/#kontakt1" class="block px-2 py-2 font-semibold text-slate-800 transition-colors hover:text-orange-600" data-i18n="nav.contacts"',
    )
    top = top.replace(
        'href="/kontakt" class="block px-2 py-2 font-semibold text-slate-800 transition-colors hover:text-orange-600 hover:bg-slate-50" data-i18n="nav.contacts"',
        'href="/#kontakt1" class="block px-2 py-2 font-semibold text-slate-800 transition-colors hover:text-orange-600 hover:bg-slate-50" data-i18n="nav.contacts"',
    )
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
    content = rebuild_footer(content)
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
    patch_file(ROOT / '404.html')

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

    # IndexNow ohlasujeme jen z produkcniho nasazeni, ne z lokalniho buildu
    # ani z preview deploye. Selhani nikdy neshodi build.
    indexnow = ROOT / 'scripts' / 'indexnow_ping.py'
    if indexnow.exists() and os.environ.get('VERCEL_ENV') == 'production':
        print('  running indexnow_ping.py…')
        subprocess.run([sys.executable, str(indexnow)], cwd=ROOT, check=False)

    print('Done.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
