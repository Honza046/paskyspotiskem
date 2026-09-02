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

HOME_TITLE = 'Pásky s potiskem na míru | Lepicí pásky s logem | ALFA IN'
HOME_DESCRIPTION = (
    'Vyrábíme lepicí pásky s potiskem a vlastním logem pro firmy, e-shopy a sklady. '
    'Potisk až 10 barev, odběr od 360 ks, vzorky zdarma a kalkulace po celé ČR.'
)
SORTIMENT_TITLE = 'Lepicí pásky s potiskem | Kompletní sortiment | ALFA IN'
SORTIMENT_DESCRIPTION = (
    'Kompletní sortiment lepicích pásek s potiskem. BOPP, BOPET, papírové i udržitelné '
    'pásky s vlastním logem. Vyberte materiál a poptejte pásku na míru.'
)
GALLERY_TITLE = 'Galerie pásek s potiskem | Realizace a reference | ALFA IN'
GALLERY_DESCRIPTION = (
    'Ukázky vyrobených lepicích pásek s potiskem. Loga firem, bezpečnostní pásky '
    'i vícebarevné tisky. Inspirace pro vaši pásku s logem na míru.'
)
FAQ_TITLE = 'Pásky s potiskem | Časté otázky a odpovědi | ALFA IN'
FAQ_DESCRIPTION = (
    'Odpovědi na časté otázky k páskám s potiskem. Minimální odběr, dodací lhůty, '
    'rozdíl mezi HOT MELT a akrylem, technologie potisku a vzorky zdarma.'
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
        '@type': ['Organization', 'LocalBusiness'],
        '@id': SITE_URL + '/#organization',
        'name': f'{ORG_NAME} | {SITE_NAME}',
        'url': SITE_URL,
        'logo': abs_url('/images/logo.svg'),
        'image': abs_url(DEFAULT_OG_IMAGE),
        'description': HOME_DESCRIPTION,
        'email': 'karel.petrak@alfain.eu',
        'telephone': '+420-602-746-017',
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': 'Nová Ves 74',
            'addressLocality': 'Nová Ves u Třebíče',
            'postalCode': '675 21',
            'addressRegion': 'Kraj Vysočina',
            'addressCountry': 'CZ',
        },
        'geo': {
            '@type': 'GeoCoordinates',
            'latitude': 49.2306,
            'longitude': 15.9633,
        },
        'openingHoursSpecification': [
            {
                '@type': 'OpeningHoursSpecification',
                'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'opens': '07:00',
                'closes': '15:30',
            }
        ],
        'areaServed': [
            {'@type': 'Country', 'name': 'Česká republika'},
            {'@type': 'Place', 'name': 'Evropská unie'},
        ],
        'knowsLanguage': ['cs', 'en', 'de', 'it'],
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


def article_schema(*, headline: str, description: str, path: str,
                   image: str = DEFAULT_OG_IMAGE) -> dict[str, Any]:
    """Article schema pro pruvodce. Posiluje signal odbornosti u informacnich dotazu."""
    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': headline,
        'description': description,
        'mainEntityOfPage': {'@type': 'WebPage', '@id': abs_url(path)},
        'image': abs_url(image),
        'inLanguage': 'cs-CZ',
        'author': {'@type': 'Organization', '@id': SITE_URL + '/#organization', 'name': ORG_NAME},
        'publisher': {'@type': 'Organization', '@id': SITE_URL + '/#organization', 'name': ORG_NAME},
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
        'manufacturer': {'@type': 'Organization', '@id': SITE_URL + '/#organization', 'name': ORG_NAME},
        'countryOfOrigin': {'@type': 'Country', 'name': 'CZ'},
        'itemCondition': 'https://schema.org/NewCondition',
        # Zamerne bez 'offers'. B2B cena vznika az kalkulaci podle potisku a mnozstvi,
        # a Offer bez pole 'price' Google odmita jako neplatny (chyba v Search Console).
        # Az budou k dispozici realne cenove hladiny, doplnit AggregateOffer s lowPrice.
    }


def category_meta_description(title: str, description: str) -> str:
    text = f'{title} na míru s vlastním logem. {description}'
    if len(text) > 158:
        text = text[:155].rstrip(' ,.;') + '…'
    return text


def product_meta_description(name: str, tagline: str, extra: str = '') -> str:
    text = f'{name} na míru. {tagline}'
    if extra:
        text = f'{text} {extra}'
    text = f'{text} Lepicí páska s potiskem a vlastním logem od výrobce.'
    if len(text) > 158:
        text = text[:155].rstrip(' ,.;') + '…'
    return text


HOME_FAQ = [
    (
        'Jaké je minimální množství objednávky pásky s potiskem?',
        'U BOPP pásek 360 ks (Akryl) nebo 504 ks (HOT MELT); u papírových a BOPET pásek závisí minimální odběr individuálně na potisku a krepové vrstvě.',
    ),
    (
        'Jak dlouho trvá výroba pásky s potiskem?',
        'Standardní dodací lhůta je 3 až 4 týdny od schválení grafického návrhu a objednávky. U urgentních zakázek se snažíme dodání urychlit.',
    ),
    (
        'Mohu objednat lepicí pásku i bez potisku?',
        'Ano. Pásky dodáváme ve stejné kvalitě i bez potisku.',
    ),
    (
        'Jaký je rozdíl mezi HOT MELT a Akryl lepidlem na páskách?',
        'HOT MELT rychle a pevně přilne i v chladu, vhodný do skladů a expedice. Akryl je tišší při odvíjení a odolnější vůči UV, ideální pro dlouhodobé skladování.',
    ),
    (
        'Dodáváte vzorky lepicích pásek zdarma?',
        'Fyzický vzorek s vaším potiskem nevyrábíme. Rádi vám však zdarma zašleme vzorky materiálů a lepidel ze skladu z předchozích realizací.',
    ),
    (
        'Jaké technologie potisku nabízíte?',
        'Flexotisk až 8 barev a rototisk až 10 barev včetně kvalitního spodního tisku.',
    ),
    (
        'Připravíte grafický návrh za mě?',
        'Ano. Potřebujeme logo (ideálně PDF, AI nebo EPS), případně text a PANTONE. Před výrobou pošleme grafický náhled ke schválení.',
    ),
    (
        'Máte udržitelné / ECO pásky?',
        'Ano, řada ECO+ (recyklovaný BOPP), papírové pásky a další udržitelné varianty.',
    ),
]
