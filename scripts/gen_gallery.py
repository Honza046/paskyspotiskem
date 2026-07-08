#!/usr/bin/env python3
"""Regenerate galerie.html main content from gallery data (mirrors inc/gallery-data.php)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ITEMS = [
    {
        "id": "alza",
        "image": "gallery/gallery-alza.jpg",
        "title": "Pásky s logem ALZA",
        "category": "vicebarevny",
        "type": "reference",
        "featured": True,
        "client": "Alza",
        "industry": "e-commerce",
        "width": "48 mm",
        "colors": 3,
        "adhesive": "hot-melt",
        "description": "Vícejazyčný brand potisk pro e-commerce balení s opakovaným logem a sloganem na standardní BOPP pásku.",
        "graphic": False,
    },
    {
        "id": "jednobarevny-firemni",
        "image": "gallery/gallery-jednobarevny-firemni.jpg",
        "title": "Jednobarevný firemní potisk",
        "category": "jednobarevny",
        "type": "reference",
        "featured": False,
        "client": "",
        "industry": "vyroba",
        "width": "48 mm",
        "colors": 1,
        "adhesive": "acryl",
        "description": "Klasický jednobarevný potisk loga na průhledné nebo bílé BOPP pásky — ideální pro firemní balení a skladovou logistiku.",
        "graphic": False,
    },
    {
        "id": "flexotisk-8",
        "image": "gallery/gallery-flexotisk-8.jpg",
        "title": "Flexotisk – 8 barev",
        "category": "vicebarevny",
        "type": "reference",
        "featured": True,
        "client": "",
        "industry": "potraviny",
        "width": "48 mm",
        "colors": 8,
        "adhesive": "hot-melt",
        "description": "Plnobarevný flexotisk s vysokým rozlišením — vhodný pro atraktivní brand na balících páskách i potravinářských aplikacích.",
        "graphic": False,
    },
    {
        "id": "rototisk-foto",
        "image": "gallery/gallery-rototisk-foto.jpg",
        "title": "Rototisk ve fotokvalitě",
        "category": "vicebarevny",
        "type": "reference",
        "featured": False,
        "client": "",
        "industry": "potraviny",
        "width": "48 mm",
        "colors": 6,
        "adhesive": "acryl",
        "description": "Rotogravurní tisk s fotografickou kvalitou pro náročné vizuály a dlouhodobou odolnost potisku.",
        "graphic": False,
    },
    {
        "id": "tamper-void",
        "image": "gallery/gallery-tamper-void.jpg",
        "title": "Tamper Evident VOID",
        "category": "bezpecnostni",
        "type": "demo",
        "featured": False,
        "client": "",
        "industry": "bezpecnost",
        "width": "48 mm",
        "colors": 2,
        "adhesive": "acryl",
        "description": "Bezpečnostní páska s VOID efektem — při odlepení zanechá viditelné upozornění, které nelze bez stopy odstranit.",
        "graphic": False,
        "graphic_style": "security",
    },
    {
        "id": "extra-glue",
        "image": "gallery/gallery-extra-glue.jpg",
        "title": "EXTRA GLUE+ bezpečnostní série",
        "category": "bezpecnostni",
        "type": "demo",
        "featured": False,
        "client": "",
        "industry": "bezpecnost",
        "width": "48 mm",
        "colors": 1,
        "adhesive": "hot-melt",
        "description": "Páska se zvýšenou vrstvou lepidla (+33 %) pro obtížné povrchy, těžké balíky a prašné skladové prostředí.",
        "graphic": False,
        "graphic_style": "glue",
    },
    {
        "id": "pecetni",
        "image": "gallery/gallery-pecetni.jpg",
        "title": "Pečetní páska s potiskem",
        "category": "bezpecnostni",
        "type": "reference",
        "featured": False,
        "client": "",
        "industry": "bezpecnost",
        "width": "48 mm",
        "colors": 2,
        "adhesive": "hot-melt",
        "description": "Pečetní páska s vlastním potiskem pro zabezpečení zásilek a dokumentů proti neoprávněnému otevření.",
        "graphic": False,
    },
    {
        "id": "logisticky-kontakty",
        "image": "gallery/gallery-logisticky-kontakty.jpg",
        "title": "Logistický potisk – kontakty",
        "category": "logisticke",
        "type": "reference",
        "featured": False,
        "client": "",
        "industry": "logistika",
        "width": "48 mm",
        "colors": 2,
        "adhesive": "hot-melt",
        "description": "Informační potisk s kontakty, QR kódem nebo instrukcemi pro příjemce zásilky.",
        "graphic": False,
    },
    {
        "id": "neutralni-bopp",
        "image": "gallery/gallery-neutralni-bopp.jpg",
        "title": "Neutrální BOPP 25 mm",
        "category": "jednobarevny",
        "type": "reference",
        "featured": False,
        "client": "",
        "industry": "vyroba",
        "width": "25 mm",
        "colors": 1,
        "adhesive": "acryl",
        "description": "Úzká BOPP páska s jednoduchým potiskem pro ruční balení a lehčí zásilky.",
        "graphic": False,
    },
    {
        "id": "prumyslova-serie",
        "image": "gallery/gallery-prumyslova-serie.jpg",
        "title": "Průmyslová série pro e-shop",
        "category": "vicebarevny",
        "type": "demo",
        "featured": False,
        "client": "",
        "industry": "e-commerce",
        "width": "48 mm",
        "colors": 4,
        "adhesive": "hot-melt",
        "description": "Hromadná výroba potištěných pásek pro e-shopy a fulfillment — konzistentní kvalita v celé sérii.",
        "graphic": False,
        "graphic_style": "industrial",
    },
    {
        "id": "vystrizny-krehke",
        "image": "gallery/gallery-vystrizny-krehke.jpg",
        "title": "Výstražný potisk – křehké",
        "category": "logisticke",
        "type": "demo",
        "featured": False,
        "client": "",
        "industry": "logistika",
        "width": "48 mm",
        "colors": 3,
        "adhesive": "acryl",
        "description": "Výstražné pásky s potiskem „Křehké“, „Neklopit“ nebo vlastním symbolem pro ochranu zboží při přepravě.",
        "graphic": False,
    },
    {
        "id": "bezpecnostni-sklad",
        "image": "gallery/gallery-bezpecnostni-sklad.jpg",
        "title": "Bezpečnostní páska sklad",
        "category": "logisticke",
        "type": "demo",
        "featured": False,
        "client": "",
        "industry": "bezpecnost",
        "width": "48 mm",
        "colors": 1,
        "adhesive": "hot-melt",
        "description": "Kombinace logistického a bezpečnostního potisku pro sklady a distribuční centra.",
        "graphic": False,
        "graphic_style": "security",
    },
]

FILTER_GROUPS = {
    "category": {
        "label": "Typ tisku",
        "options": {
            "jednobarevny": "Jednobarevný tisk",
            "vicebarevny": "Vícebarevný / Rototisk",
            "bezpecnostni": "Bezpečnostní pásky",
            "logisticke": "Logistické / Výstražné",
        },
    },
    "adhesive": {
        "label": "Lepidlo",
        "options": {"hot-melt": "Hot Melt", "acryl": "Acryl"},
    },
    "industry": {
        "label": "Odvětví",
        "options": {
            "e-commerce": "E-commerce",
            "vyroba": "Výroba",
            "logistika": "Logistika",
            "potraviny": "Potraviny",
            "bezpecnost": "Bezpečnost",
        },
    },
    "type": {
        "label": "Typ ukázky",
        "options": {
            "reference": "Reálné reference",
            "demo": "Možnosti tisku",
        },
    },
}

ADHESIVE_LABELS = {"hot-melt": "Hot Melt", "acryl": "Acryl"}
INDUSTRY_LABELS = {
    "e-commerce": "E-commerce",
    "vyroba": "Výroba",
    "logistika": "Logistika",
    "potraviny": "Potraviny",
    "bezpecnost": "Bezpečnost",
}
GRAPHIC_GRADIENTS = {
    "security": "from-rose-50 via-white to-orange-50",
    "glue": "from-amber-50 via-white to-orange-50",
    "industrial": "from-slate-50 via-white to-sky-50",
    "warning": "from-yellow-50 via-white to-orange-50",
}
ICONS = {
    "security": '<svg class="mb-4 h-14 w-14 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"/></svg>',
    "glue": '<svg class="mb-4 h-14 w-14 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"/></svg>',
    "industrial": '<svg class="mb-4 h-14 w-14 text-sky-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z"/></svg>',
}


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def colors_label(n: int) -> str:
    if n == 1:
        return "1 barva"
    if 2 <= n <= 4:
        return f"{n} barvy"
    return f"{n} barev"


def render_card(item: dict, featured_layout: bool = False) -> str:
    img = f"images/{item['image']}"
    adhesive = ADHESIVE_LABELS[item["adhesive"]]
    industry = INDUSTRY_LABELS.get(item.get("industry", ""), "")
    graphic = item.get("graphic", False)
    style = item.get("graphic_style", "security")
    gradient = GRAPHIC_GRADIENTS.get(style, GRAPHIC_GRADIENTS["security"])

    classes = "group overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm transition-all duration-300 hover:border-slate-200 hover:shadow-lg"
    if featured_layout:
        classes += " lg:col-span-2"

    aspect = "aspect-[16/10] lg:aspect-auto lg:min-h-[280px]" if featured_layout else "aspect-[4/3]"
    title_cls = "text-base sm:text-lg" if featured_layout else "text-sm"
    pad = "p-4 sm:p-5" if featured_layout else "p-4"

    attrs = (
        f'data-gallery-item data-id="{esc(item["id"])}" data-category="{esc(item["category"])}" '
        f'data-adhesive="{esc(item["adhesive"])}" data-industry="{esc(item["industry"])}" '
        f'data-type="{esc(item["type"])}" data-featured="{"true" if item.get("featured") else "false"}" '
        f'data-image="{esc(img)}" data-title="{esc(item["title"])}" data-client="{esc(item.get("client", ""))}" '
        f'data-width="{esc(item["width"])}" data-colors="{item["colors"]}" '
        f'data-adhesive-label="{esc(adhesive)}" data-industry-label="{esc(industry)}" '
        f'data-description="{esc(item["description"])}" data-graphic="{"true" if graphic else "false"}" '
        f'data-graphic-style="{esc(style)}"'
    )

    if graphic:
        media = f'''<div class="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br {gradient} p-8 text-center">
                {ICONS.get(style, ICONS["security"])}
                <span class="text-xs font-bold uppercase tracking-widest text-slate-500">Ukázka technologie</span>
            </div>'''
    else:
        media = f'<img src="{esc(img)}" alt="{esc(item["title"])}" class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy">'

    badges = ""
    if item.get("featured"):
        badges += '<span class="absolute left-3 top-3 rounded-full bg-orange-600 px-3 py-1 text-xs font-bold uppercase tracking-wide text-white shadow-md">Vybraná ukázka</span>'
    if item["type"] == "demo":
        badges += '<span class="absolute right-3 top-3 rounded-full border border-slate-200 bg-white/90 px-2.5 py-1 text-xs font-semibold text-slate-600 backdrop-blur-sm">Technologie</span>'

    tags = ""
    if industry:
        tags += f'<span class="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">{esc(industry)}</span>'
    tags += f'<span class="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">{esc(item["width"])}</span>'
    tags += f'<span class="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">{colors_label(item["colors"])}</span>'
    tags += f'<span class="rounded-md bg-orange-50 px-2 py-0.5 text-xs font-semibold text-orange-700">{esc(adhesive)}</span>'

    client = item.get("client", "")
    client_html = f'<p class="text-xs font-semibold uppercase tracking-wide text-orange-600">{esc(client)}</p>' if client else ""

    return f"""<article class="{classes}" {attrs}>
    <button type="button" data-lightbox-trigger class="relative block w-full overflow-hidden text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-orange-500 focus-visible:ring-offset-2 {aspect}" aria-label="Zobrazit detail: {esc(item['title'])}">
        {media}
        <span class="pointer-events-none absolute inset-0 flex items-center justify-center bg-slate-950/0 transition-all duration-300 group-hover:bg-slate-950/40">
            <span class="flex translate-y-2 items-center gap-2 rounded-full bg-white/95 px-4 py-2 text-sm font-semibold text-slate-900 opacity-0 shadow-lg transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100">
                <svg class="h-4 w-4 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35M11 18a7 7 0 100-14 7 7 0 000 14z"/></svg>
                Zobrazit detail
            </span>
        </span>
        {badges}
    </button>
    <div class="{pad}">
        {client_html}
        <h2 class="{title_cls} font-bold text-slate-900">{esc(item['title'])}</h2>
        <div class="mt-2 flex flex-wrap gap-1.5">{tags}</div>
    </div>
</article>"""


def render_filters() -> str:
    parts = []
    for group_key, group in FILTER_GROUPS.items():
        opts = "\n".join(
            f'''                            <button type="button" data-filter-group="{esc(group_key)}" data-tag="{esc(tag)}" data-label="{esc(label)}" aria-pressed="false" class="flex items-center justify-between gap-3 rounded-xl px-3 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50">
                                <span>{esc(label)}</span>
                                <span data-check class="hidden text-orange-600"><svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg></span>
                            </button>'''
            for tag, label in group["options"].items()
        )
        parts.append(
            f'''            <div class="relative" data-dropdown>
                <button type="button" data-dropdown-toggle class="relative flex cursor-pointer items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition-colors hover:border-slate-300 sm:px-5">
                    <span>{esc(group['label'])}</span>
                    <span data-count class="hidden h-5 min-w-[20px] items-center justify-center rounded-full bg-orange-600 px-1.5 text-xs font-bold text-white"></span>
                    <svg data-chevron class="h-4 w-4 text-slate-400 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
                </button>
                <div data-dropdown-menu class="absolute left-0 top-full z-50 mt-2 hidden min-w-[220px] flex-col gap-1 rounded-2xl border border-slate-100 bg-white p-3 shadow-xl">
{opts}
                </div>
            </div>'''
        )
    return "\n".join(parts)


def render_main() -> str:
    featured = [i for i in ITEMS if i.get("featured")]
    references = [i for i in ITEMS if i["type"] == "reference" and not i.get("featured")]
    demos = [i for i in ITEMS if i["type"] == "demo"]

    return f"""<main>

<!-- HERO -->
<section class="border-b border-slate-100 bg-white">
    <div class="mx-auto max-w-7xl px-4 py-10 sm:py-12">
        <p class="mb-2 text-sm font-bold uppercase tracking-widest text-orange-600">Galerie</p>
        <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div class="max-w-2xl">
                <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">Ukázky naší práce</h1>
                <p class="mt-3 text-base leading-relaxed text-slate-600">Reálné reference z výroby i ukázky technologií tisku — filtrujte podle typu potisku, lepidla nebo odvětví.</p>
            </div>
            <a href="index.html#gf_1" class="inline-flex shrink-0 items-center justify-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-orange-600/20 transition-all hover:scale-[1.02] hover:shadow-xl">Chci vlastní potisk</a>
        </div>
    </div>
</section>

<!-- FILTER -->
<section class="border-b border-slate-100 bg-slate-50">
    <div class="mx-auto max-w-7xl px-4">
        <div id="gallery-filter" class="flex flex-wrap items-center gap-3 py-4 sm:gap-4" data-inquiry="index.html#gf_1">
            <div class="flex items-center gap-2 font-medium text-slate-800">
                <svg class="h-5 w-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M3 4h18M6 8h12M9 12h6M11 16h2"/></svg>
                Filtr
            </div>
{render_filters()}
            <div id="gallery-active" class="flex flex-wrap items-center gap-2"></div>
            <button type="button" id="gallery-clear" class="hidden text-sm font-semibold text-slate-500 transition-colors hover:text-orange-600">Vymazat vše</button>
            <span id="gallery-count" class="ml-auto text-sm font-semibold text-slate-500"></span>
        </div>
    </div>
</section>

<!-- FEATURED -->
<section id="gallery-featured-section" class="mx-auto max-w-7xl px-4 pt-8 sm:pt-10">
    <div class="mb-5 flex items-center justify-between gap-3">
        <h2 class="text-xl font-extrabold tracking-tight text-slate-900 sm:text-2xl">Vybrané ukázky</h2>
    </div>
    <div id="gallery-featured" class="grid grid-cols-1 gap-6 lg:grid-cols-4">
{chr(10).join('        ' + render_card(i, True) for i in featured)}
    </div>
</section>

<!-- REFERENCES -->
<section id="gallery-references-section" class="mx-auto max-w-7xl px-4 pb-4 pt-12 sm:pt-16">
    <div class="mb-6 border-b border-slate-100 pb-4">
        <h2 class="text-xl font-extrabold tracking-tight text-slate-900 sm:text-2xl">Reálné reference</h2>
        <p class="mt-1 text-sm text-slate-500">Fotografie skutečných potisků z naší výroby. Po novém focení doplníme další reference.</p>
    </div>
    <div id="gallery-references" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
{chr(10).join('        ' + render_card(i) for i in references)}
    </div>
</section>

<!-- DEMOS -->
<section id="gallery-demos-section" class="mx-auto max-w-7xl px-4 pb-12 pt-8 sm:pb-16 sm:pt-12">
    <div class="mb-6 border-b border-slate-100 pb-4">
        <h2 class="text-xl font-extrabold tracking-tight text-slate-900 sm:text-2xl">Možnosti tisku a technologie</h2>
        <p class="mt-1 text-sm text-slate-500">Ukázky bezpečnostních, logistických a speciálních řešení — ilustrace technologií, které nabízíme.</p>
    </div>
    <div id="gallery-demos" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
{chr(10).join('        ' + render_card(i) for i in demos)}
    </div>
</section>

<!-- FILTERED RESULTS -->
<section id="gallery-results-section" class="mx-auto hidden max-w-7xl px-4 py-8 sm:py-10">
    <div id="gallery-empty" class="mb-8 hidden rounded-2xl border border-dashed border-slate-200 bg-white p-12 text-center">
        <p class="text-slate-500">Žádná ukázka neodpovídá vybraným filtrům. Zkuste ubrat některý z filtrů.</p>
    </div>
    <div id="gallery-results" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"></div>
</section>

<!-- CTA -->
<section class="border-t border-slate-100 bg-white">
    <div class="mx-auto max-w-7xl px-4 py-12 sm:py-16">
        <div class="rounded-3xl bg-gradient-to-br from-orange-600 to-amber-500 px-6 py-10 text-center text-white shadow-xl shadow-orange-600/20 sm:px-12 sm:py-14">
            <h2 class="text-2xl font-extrabold tracking-tight sm:text-3xl">Máte vlastní logo?</h2>
            <p class="mx-auto mt-3 max-w-xl text-base text-orange-50">Připravíme vám nezávaznou kalkulaci a vzorek potisku. Stačí nám poslat logo a požadované parametry pásky.</p>
            <a href="index.html#gf_1" class="mt-6 inline-flex items-center gap-2 rounded-2xl bg-white px-8 py-3.5 text-sm font-bold text-orange-600 shadow-lg transition-all hover:scale-[1.02] hover:shadow-xl">
                Nezávazně poptat
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
            </a>
        </div>
    </div>
</section>

</main>

<!-- LIGHTBOX -->
<div id="gallery-lightbox" class="gallery-lightbox" role="dialog" aria-modal="true" aria-labelledby="lightbox-title" hidden>
    <div id="lightbox-backdrop" class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm"></div>
    <button type="button" id="lightbox-prev" class="absolute left-2 top-[35%] z-20 flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full border border-white/20 bg-white/90 text-slate-700 shadow-lg transition hover:bg-white hover:text-orange-600 sm:left-4 lg:top-1/2 lg:left-6" aria-label="Předchozí">
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
    </button>
    <button type="button" id="lightbox-next" class="absolute right-2 top-[35%] z-20 flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full border border-white/20 bg-white/90 text-slate-700 shadow-lg transition hover:bg-white hover:text-orange-600 sm:right-4 lg:top-1/2 lg:right-6" aria-label="Další">
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
    </button>
    <div class="relative z-10 w-full max-w-5xl overflow-hidden rounded-2xl bg-white shadow-2xl">
        <button type="button" id="lightbox-close" class="absolute right-3 top-3 z-20 flex h-10 w-10 items-center justify-center rounded-full bg-white/90 text-slate-700 shadow-md transition hover:bg-white hover:text-orange-600" aria-label="Zavřít">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
        <div class="flex flex-col lg:flex-row">
            <div id="lightbox-media" class="relative flex min-h-[220px] items-center justify-center bg-slate-100 lg:w-3/5">
                <img id="lightbox-image" src="" alt="" class="hidden max-h-[50vh] w-full object-contain lg:max-h-[65vh]">
                <div id="lightbox-graphic" class="hidden flex h-full min-h-[220px] w-full flex-col items-center justify-center bg-gradient-to-br from-rose-50 via-white to-orange-50 p-10 text-center lg:min-h-[320px]">
                    <div id="lightbox-graphic-icon" class="mb-4"></div>
                    <span class="text-xs font-bold uppercase tracking-widest text-slate-500">Ukázka technologie</span>
                </div>
            </div>
            <div class="flex flex-col border-t border-slate-100 p-5 sm:p-6 lg:w-2/5 lg:border-l lg:border-t-0">
                <p id="lightbox-client" class="hidden text-xs font-semibold uppercase tracking-wide text-orange-600"></p>
                <h3 id="lightbox-title" class="text-lg font-bold text-slate-900 sm:text-xl"></h3>
                <dl id="lightbox-meta" class="mt-4 space-y-2 text-sm"></dl>
                <p id="lightbox-description" class="mt-4 flex-1 text-sm leading-relaxed text-slate-600"></p>
                <a id="lightbox-cta" href="index.html#gf_1" class="mt-6 inline-flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-orange-600/20 transition-all hover:scale-[1.02] hover:shadow-xl">
                    Chci podobný potisk
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
                </a>
            </div>
        </div>
    </div>
</div>
"""


def main() -> None:
    html_path = ROOT / "galerie.html"
    content = html_path.read_text(encoding="utf-8")
    new_block = render_main()
    updated = re.sub(
        r"<main>.*?</main>\s*(?:<!-- LIGHTBOX -->.*?</div>\s*)*<!-- FOOTER -->",
        new_block + "\n<!-- FOOTER -->",
        content,
        count=1,
        flags=re.DOTALL,
    )
    if updated == content:
        raise SystemExit("Failed to patch galerie.html — pattern not found")
    html_path.write_text(updated, encoding="utf-8")
    print(f"Updated {html_path}")


if __name__ == "__main__":
    main()
