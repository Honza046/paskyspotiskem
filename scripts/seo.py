#!/usr/bin/env python3
"""Shared SEO helpers for static HTML generation."""
from __future__ import annotations

import html
import json
import os
import re
from typing import Any

SITE_URL = os.environ.get('SITE_URL', 'https://www.paskyspotiskem.cz').rstrip('/')
SITE_NAME = 'Pásky s potiskem'
ORG_NAME = 'ALFA IN a.s.'
DEFAULT_OG_IMAGE = '/images/slide-pasky-1920x624.jpg'

SEO_MARKER_START = '<!-- seo:extra -->'
SEO_MARKER_END = '<!-- /seo:extra -->'

HOME_TITLE = 'Pásky s potiskem | Lepicí pásky s logem na míru | ALFA IN'
HOME_DESCRIPTION = (
    'Výroba a prodej lepicích pásek s potiskem – pásky s logem pro firmy, e-shopy a sklady. '
    'BOPP, eko a speciální pásky, potisk až 8 barev, dodání po celé ČR. Nezávazná kalkulace.'
)
SORTIMENT_TITLE = 'Sortiment lepicích pásek | Pásky s potiskem'
SORTIMENT_DESCRIPTION = (
    'Kompletní sortiment lepicích pásek s potiskem – BOPP, BOPET, papírové, eko a speciální pásky. '
    'Vyberte materiál a poptávejte pásku na míru od výrobce ALFA IN.'
)
GALLERY_TITLE = 'Galerie pásek s potiskem | Realizace ALFA IN'
GALLERY_DESCRIPTION = (
    'Ukázky lepicích pásek s potiskem – loga firem, bezpečnostní pásky, eko varianty a speciální tisky. '
    'Inspirace pro vaši pásku s potiskem na míru.'
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def abs_url(path: str) -> str:
    if path.startswith('http://') or path.startswith('https://'):
        return path
    if not path.startswith('/'):
        path = '/' + path
    return SITE_URL + path


def page_title(page: str, brand: str = SITE_NAME) -> str:
    return f'{page} | {brand}'


def extra_head(
    *,
    title: str,
    description: str,
    path: str,
    og_type: str = 'website',
    og_image: str = DEFAULT_OG_IMAGE,
    robots: str = 'index, follow',
    schemas: list[dict[str, Any]] | None = None,
) -> str:
    canonical = abs_url(path)
    image = abs_url(og_image)
    lines = [
        f'<link rel="canonical" href="{esc(canonical)}">',
        f'<meta name="robots" content="{esc(robots)}">',
        f'<meta property="og:type" content="{esc(og_type)}">',
        f'<meta property="og:site_name" content="{esc(SITE_NAME)}">',
        f'<meta property="og:locale" content="cs_CZ">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(description)}">',
        f'<meta property="og:url" content="{esc(canonical)}">',
        f'<meta property="og:image" content="{esc(image)}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(description)}">',
        f'<meta name="twitter:image" content="{esc(image)}">',
    ]
    for schema in schemas or []:
        payload = json.dumps(schema, ensure_ascii=False, separators=(',', ':'))
        lines.append(f'<script type="application/ld+json">{payload}</script>')
    return '\n    '.join(lines)


def apply_page_seo(
    html_doc: str,
    *,
    title: str,
    description: str,
    path: str,
    og_type: str = 'website',
    og_image: str = DEFAULT_OG_IMAGE,
    schemas: list[dict[str, Any]] | None = None,
) -> str:
    out = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', html_doc, count=1, flags=re.DOTALL)
    out = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{esc(description)}">',
        out,
        count=1,
    )
    block = extra_head(
        title=title,
        description=description,
        path=path,
        og_type=og_type,
        og_image=og_image,
        schemas=schemas,
    )
    pattern = re.escape(SEO_MARKER_START) + r'.*?' + re.escape(SEO_MARKER_END)
    replacement = f'{SEO_MARKER_START}\n    {block}\n    {SEO_MARKER_END}'
    if SEO_MARKER_START in out:
        return re.sub(pattern, replacement, out, count=1, flags=re.DOTALL)
    return out.replace(
        '<meta name="description"',
        f'{SEO_MARKER_START}\n    {block}\n    {SEO_MARKER_END}\n    <meta name="description"',
        1,
    )


def organization_schema() -> dict[str, Any]:
    return {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': f'{ORG_NAME} – {SITE_NAME}',
        'url': SITE_URL,
        'logo': abs_url('/images/logo.svg'),
        'description': HOME_DESCRIPTION,
        'parentOrganization': {
            '@type': 'Organization',
            'name': ORG_NAME,
            'url': 'https://www.alfain.eu/',
        },
        'contactPoint': [
            {
                '@type': 'ContactPoint',
                'telephone': '+420-602-746-017',
                'contactType': 'sales',
                'areaServed': 'CZ',
                'availableLanguage': ['cs', 'en', 'de'],
            }
        ],
        'sameAs': [
            'https://www.facebook.com/AlfaIncz',
            'https://www.instagram.com/AlfaIncz',
            'https://www.youtube.com/AlfaInas',
            'https://www.alfain.eu/',
        ],
    }


def website_schema() -> dict[str, Any]:
    return {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        'name': SITE_NAME,
        'url': SITE_URL,
        'description': HOME_DESCRIPTION,
        'inLanguage': 'cs-CZ',
        'publisher': {'@type': 'Organization', 'name': ORG_NAME},
    }


def faq_schema(items: list[tuple[str, str]]) -> dict[str, Any]:
    return {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': q,
                'acceptedAnswer': {'@type': 'Answer', 'text': a},
            }
            for q, a in items
        ],
    }


def breadcrumb_schema(items: list[tuple[str, str]]) -> dict[str, Any]:
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {
                '@type': 'ListItem',
                'position': i + 1,
                'name': name,
                'item': abs_url(path),
            }
            for i, (path, name) in enumerate(items)
        ],
    }


def product_schema(name: str, description: str, path: str, image_path: str) -> dict[str, Any]:
    return {
        '@context': 'https://schema.org',
        '@type': 'Product',
        'name': name,
        'description': description,
        'image': abs_url(image_path if image_path.startswith('/') else '/' + image_path),
        'brand': {'@type': 'Brand', 'name': ORG_NAME},
        'category': 'Lepicí pásky s potiskem',
        'url': abs_url(path),
        'offers': {
            '@type': 'Offer',
            'url': abs_url('/#gf_1'),
            'priceCurrency': 'CZK',
            'availability': 'https://schema.org/InStock',
            'seller': {'@type': 'Organization', 'name': ORG_NAME},
        },
    }


def category_meta_description(title: str, description: str) -> str:
    text = f'{title} s potiskem na míru. {description}'
    if len(text) > 158:
        text = text[:155].rstrip(' ,.;') + '…'
    return text


def product_meta_description(name: str, tagline: str) -> str:
    text = f'{name} – {tagline} Lepicí páska s potiskem od ALFA IN.'
    if len(text) > 158:
        text = text[:155].rstrip(' ,.;') + '…'
    return text


HOME_FAQ = [
    (
        'Jaké je minimální množství objednávky pásky s potiskem?',
        'Standardně ACRYL od 360 ks a HOT MELT od 504 ks na jednu variantu pásky. U větších objednávek získáte dopravu zdarma v rámci ČR.',
    ),
    (
        'Jak dlouho trvá výroba pásky s potiskem?',
        'Typická dodací lhůta je 3 až 4 týdny od schválení grafického náhledu a objednávky.',
    ),
    (
        'Mohu objednat lepicí pásku i bez potisku?',
        'Ano. Stejný materiál dodáme i v nepotištěném provedení pro okamžité balení nebo skladové zásoby.',
    ),
    (
        'Jaký je rozdíl mezi HOT MELT a ACRYL lepidlem na páskách?',
        'HOT MELT rychle a pevně přilne i v chladu. ACRYL je tišší při odvíjení a odolnější vůči UV.',
    ),
    (
        'Dodáváte vzorky lepicích pásek zdarma?',
        'Ano, vzorek nebo nezávaznou kalkulaci připravíme na vyžádání přes formulář na webu.',
    ),
]
