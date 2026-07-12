#!/usr/bin/env python3
"""Add i18n.js, language switcher and data-i18n attributes to static HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LANG_SWITCHER = '<div data-lang-switcher class="relative shrink-0" aria-label="Language"></div>'

NAV_MAP = [
    ('hover:text-orange-600">Úvod</a>', 'hover:text-orange-600" data-i18n="nav.home">Úvod</a>'),
    ('hover:text-orange-600">Galerie</a>', 'hover:text-orange-600" data-i18n="nav.gallery">Galerie</a>'),
    ('hover:text-orange-600">Sortiment</a>', 'hover:text-orange-600" data-i18n="nav.sortiment">Sortiment</a>'),
    ('hover:text-orange-600">Reference</a>', 'hover:text-orange-600" data-i18n="nav.references">Reference</a>'),
    ('hover:text-orange-600">Kontakty</a>', 'hover:text-orange-600" data-i18n="nav.contacts">Kontakty</a>'),
    ('hover:bg-slate-50">Úvod</a>', 'hover:bg-slate-50" data-i18n="nav.home">Úvod</a>'),
    ('hover:bg-slate-50">Galerie</a>', 'hover:bg-slate-50" data-i18n="nav.gallery">Galerie</a>'),
    ('hover:bg-slate-50">Sortiment</a>', 'hover:bg-slate-50" data-i18n="nav.sortiment">Sortiment</a>'),
    ('hover:bg-slate-50">Reference</a>', 'hover:bg-slate-50" data-i18n="nav.references">Reference</a>'),
    ('hover:bg-slate-50">Kontakty</a>', 'hover:bg-slate-50" data-i18n="nav.contacts">Kontakty</a>'),
    ('text-orange-600">Galerie</a>', 'text-orange-600" data-i18n="nav.gallery">Galerie</a>'),
]

FOOTER_MAP = [
    ('>Najdete nás na adrese<', ' data-i18n="footer.address_heading">Najdete nás na adrese<'),
    ('>Napište na e-mail<', ' data-i18n="footer.email_heading">Napište na e-mail<'),
    ('>Volejte na číslo<', ' data-i18n="footer.phone_heading">Volejte na číslo<'),
    ('>Sociální sítě<', ' data-i18n="footer.social_heading">Sociální sítě<'),
    ('>Ukaž na mapě<', ' data-i18n="footer.show_on_map">Ukaž na mapě<'),
    ('>Další kontakty<', ' data-i18n="footer.more_contacts">Další kontakty<'),
    ('>Všechna práva vyhrazena<', ' data-i18n="footer.copyright">Všechna práva vyhrazena<'),
]

INDEX_MAP = [
    ('<span>ALFA IN - výroba, poradenství, prodej a servis</span>',
     '<span data-i18n="nav.tagline">ALFA IN - výroba, poradenství, prodej a servis</span>'),
    ('alt="Pásky s potiskem"', 'alt="Pásky s potiskem" data-i18n-attr="alt:meta.logo_alt"'),
    ('>Pásky s potiskem</span>', ' data-i18n="meta.site_name">Pásky s potiskem</span>'),
    ('>Menu</button>', ' data-i18n="nav.menu">Menu</button>'),
    ('aria-label="Hlavní navigace"', 'aria-label="Hlavní navigace" data-i18n-attr="aria-label:nav.main_nav_label"'),
    ('>ISO 9001 · Přímo od výrobce</p>', ' data-i18n="home.hero.badge">ISO 9001 · Přímo od výrobce</p>'),
    ('>Prohlédnout nabídku</a>', ' data-i18n="home.hero.cta_offer">Prohlédnout nabídku</a>'),
    ('>Nezávazná kalkulace</a>', ' data-i18n="home.hero.cta_quote">Nezávazná kalkulace</a>'),
    ('>O nás</span>', ' data-i18n="home.about.label">O nás</span>'),
    ('>Tradiční český výrobce lepicích pásek s potiskem</h2>',
     ' data-i18n="home.about.title">Tradiční český výrobce lepicích pásek s potiskem</h2>'),
    ('>Reference</p>', ' data-i18n="home.references.label">Reference</p>'),
    ('>Spokojení zákazníci napříč obory</h2>',
     ' data-i18n="home.references.title">Spokojení zákazníci napříč obory</h2>'),
    ('>Firmy, které s námi spolupracují</p>',
     ' data-i18n="home.references.carousel_label">Firmy, které s námi spolupracují</p>'),
    ('>Bezpečnost</span>', ' data-i18n="home.benefits.security.badge">Bezpečnost</span>'),
    ('>Extrémní lepivost</span>', ' data-i18n="home.benefits.glue.badge">Extrémní lepivost</span>'),
    ('>KONTAKTY NA ODDĚLENÍ</h2>', ' data-i18n="home.contacts.title">KONTAKTY NA ODDĚLENÍ</h2>'),
    ('>Testovací vzorek</p>', ' data-i18n="home.sample.label">Testovací vzorek</p>'),
    ('>Vyplnit poptávku</a>', ' data-i18n="home.sample.cta">Vyplnit poptávku</a>'),
]

GALLERY_MAP = [
    ('>Galerie</p>', ' data-i18n="gallery.ui.label">Galerie</p>'),
    ('>Ukázky naší práce</h1>', ' data-i18n="gallery.ui.title">Ukázky naší práce</h1>'),
    ('>Chci vlastní potisk</a>', ' data-i18n="gallery.ui.cta_own">Chci vlastní potisk</a>'),
    ('>Filtr</div>', ' data-i18n="gallery.ui.filter">Filtr</div>'),
    ('>Vymazat vše</button>', ' data-i18n="gallery.ui.clear_all">Vymazat vše</button>'),
    ('>Vybrané ukázky</h2>', ' data-i18n="gallery.ui.featured_title">Vybrané ukázky</h2>'),
    ('>Reálné reference</h2>', ' data-i18n="gallery.ui.references_title">Reálné reference</h2>'),
    ('>Možnosti tisku a technologie</h2>', ' data-i18n="gallery.ui.demos_title">Možnosti tisku a technologie</h2>'),
    ('>Máte vlastní logo?</h2>', ' data-i18n="gallery.ui.cta_title">Máte vlastní logo?</h2>'),
    ('>Nezávazně poptat</a>', ' data-i18n="gallery.ui.cta_button">Nezávazně poptat</a>'),
]

SORTIMENT_MAP = [
    ('>Sortiment</p>', ' data-i18n="sortiment.ui.label">Sortiment</p>'),
    ('>Objevte naše lepicí pásky</h1>', ' data-i18n="sortiment.ui.title">Objevte naše lepicí pásky</h1>'),
    ('>Filtr</div>', ' data-i18n="sortiment.ui.filter">Filtr</div>'),
    ('>Vymazat vše</button>', ' data-i18n="sortiment.ui.clear_all">Vymazat vše</button>'),
    ('>Nalezené produkty podle filtrů</h2>', ' data-i18n="sortiment.ui.results_title">Nalezené produkty podle filtrů</h2>'),
]


def depth_prefix(path: Path) -> str:
  rel = path.relative_to(ROOT)
  parts = len(rel.parts) - 1
  if parts <= 0:
    return '.'
  return '/'.join(['..'] * parts)


def patch_common(text: str) -> str:
    text = text.replace(
        '<a href="#" class="font-semibold uppercase tracking-wide text-orange-600">cs</a>',
        LANG_SWITCHER,
    )
    text = text.replace(
        '<a href="index.html" class="font-semibold uppercase tracking-wide text-orange-600">cs</a>',
        LANG_SWITCHER,
    )
    for old, new in NAV_MAP:
        text = text.replace(old, new)
    for old, new in FOOTER_MAP:
        text = text.replace(old, new)
    return text


def apply_map(text: str, mapping: list[tuple[str, str]]) -> str:
    for old, new in mapping:
        if old not in text:
            continue
        if 'data-i18n' in new and old.startswith('>'):
            text = text.replace(f'<a href', f'<a href', 1)  # noop
        text = text.replace(old, new)
    return text


BOOT_TAG = '    <script src="/assets/js/i18n-boot.js?v=2"></script>\n'


def inject_i18n_boot(text: str) -> str:
    if 'i18n-boot.js' in text:
        return text
    anchor = '    </script>\n    <meta name="description"'
    if anchor in text:
        return text.replace(anchor, '    </script>\n' + BOOT_TAG + '    <meta name="description"', 1)
    return text


def inject_i18n_script(text: str, prefix: str) -> str:
    i18n_src = f'{prefix}/assets/js/i18n.js?v=7'
    pages_src = f'{prefix}/assets/js/i18n-pages.js?v=6'
    i18n_tag = f'<script src="{i18n_src}"></script>'
    pages_tag = f'<script src="{pages_src}"></script>'
    if 'assets/js/i18n.js' in text:
        text = re.sub(r'<script src="[^"]*assets/js/i18n\.js"></script>\s*', '', text)
    if 'assets/js/i18n-pages.js' in text:
        text = re.sub(r'<script src="[^"]*assets/js/i18n-pages\.js"></script>\s*', '', text)
    bundle = i18n_tag + '\n' + pages_tag + '\n'
    if re.search(r'<script src="[^"]*assets/js/', text):
        text = re.sub(r'(<script src="[^"]*assets/js/)', bundle + '\\1', text, count=1)
    else:
        text = text.replace('</body>', bundle + '</body>')
    return text


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text
    prefix = depth_prefix(path)

    text = patch_common(text)
    text = inject_i18n_boot(text)
    text = inject_i18n_script(text, prefix if prefix != '.' else '.')

    name = path.name
    if name == 'index.html':
        text = apply_map(text, INDEX_MAP)
    elif name == 'galerie.html':
        text = apply_map(text, GALLERY_MAP)
    elif name == 'sortiment.html':
        text = apply_map(text, SORTIMENT_MAP)

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def main() -> None:
    changed = 0
    for html in ROOT.rglob('*.html'):
        if 'node_modules' in html.parts:
            continue
        if patch_file(html):
            changed += 1
            print('patched', html.relative_to(ROOT))
    print(f'Done. {changed} files updated.')


if __name__ == '__main__':
    main()
