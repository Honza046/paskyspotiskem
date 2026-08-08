#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate SEO guide / landing pages under /pruvodce/."""
from __future__ import annotations

import html
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo import (  # noqa: E402
    apply_page_seo,
    breadcrumb_schema,
    faq_schema,
    page_title,
)

esc = html.escape

GUIDES = [
    {
        "slug": "pasky-s-potiskem",
        "title": "Kompletní průvodce páskami s potiskem",
        "h1": "Pásky s potiskem na míru",
        "description": (
            "Pásky s potiskem a pásky s logem od výrobce ALFA IN: jak vybrat BOPP, papír, ECO+ "
            "nebo speciální pásku, potisk až 8–10 barev, vzorky a kalkulace pro firmy a e-shopy."
        ),
        "intro": (
            "Hledáte pásky s potiskem pro firmu, e-shop nebo sklad? Nabízíme lepicí pásky s logem "
            "na míru: od klasické BOPP přes papírové FSC až po udržitelné ECO+, NOPP a bezpečnostní Tamper Evident."
        ),
        "sections": [
            (
                "Proč pásky s potiskem",
                "Potištěná páska uzavírá karton a zároveň branduje zásilku. Logo, slogan nebo instrukce "
                "cestují s balíkem až k zákazníkovi. Levnější a odolnější než mnoho jiných brandingových prvků.",
            ),
            (
                "Jak vybrat materiál",
                "BOPP HOT MELT pro rychlou expedici a chladnější sklady, Akryl pro tiché odvíjení a UV stabilitu, "
                "papír pro recyklaci s kartonem, ECO+/NOPP pro ESG cíle. Porovnání lepidel najdete v průvodci "
                "HOT MELT vs Akryl.",
            ),
            (
                "Minimální odběr a dodání",
                "U BOPP typicky od 360 ks (Akryl) nebo 504 ks (HOT MELT). Dodání obvykle 3–4 týdny od schválení "
                "grafiky. Vzorky vybraných materiálů zasíláme zdarma.",
            ),
        ],
        "links": [
            ("/sortiment", "Kompletní sortiment"),
            ("/sortiment/bopp-pasky", "BOPP pásky"),
            ("/sortiment/udrzitelne-pasky", "Udržitelné pásky"),
            ("/sortiment/papirove-pasky", "Papírové pásky"),
            ("/faq", "Časté otázky"),
            ("/#gf_1", "Nezávazná kalkulace"),
        ],
        "faqs": [
            (
                "Co jsou pásky s potiskem?",
                "Lepicí balicí pásky s firemním logem nebo textem s potiskem flexotiskem až 8 barev "
                "a rototiskem až 10 barev.",
            ),
            (
                "Jak pásky s potiskem objednat?",
                "Stačí nezávazná poptávka: materiál, šířka, potisk a množství. Připravíme kalkulaci a grafický návrh.",
            ),
        ],
    },
    {
        "slug": "hot-melt-vs-akryl",
        "title": "HOT MELT vs Akryl",
        "h1": "HOT MELT vs Akryl: které lepidlo na pásku s potiskem",
        "description": (
            "Rozdíl mezi HOT MELT a Akryl lepidlem na páskách s potiskem: lepivost v chladu, tiché odvíjení, "
            "UV odolnost a typické použití ve skladu i e-shopu."
        ),
        "intro": (
            "Nejčastější otázka při výběru BOPP pásky s potiskem: HOT MELT, nebo Akryl? "
            "Obě lepidla drží karton. Liší se chováním v chladu, hlukem při odvíjení a odolností vůči UV."
        ),
        "sections": [
            (
                "HOT MELT",
                "Rychlá a silná přilnavost i v chladnějším skladu, vhodný na prašnější a recyklované kartony. "
                "Typická volba pro vysokou expedici. Minimální odběr u potisku obvykle od 504 ks.",
            ),
            (
                "Akryl",
                "Tišší odvíjení (Low noise), vyšší UV stabilita a dlouhodobá lepivost při skladování. "
                "Vodní disperze bez agresivních rozpouštědel. Minimální odběr typicky od 360 ks.",
            ),
            (
                "Kdy zvolit TACK+ nebo EXTRA GLUE+",
                "TACK+ = HOT MELT s vyšším tackem. EXTRA GLUE+ = Akryl se zesílenou vrstvou lepidla. "
                "Obě varianty řeší těžší balíky a obtížné povrchy.",
            ),
        ],
        "links": [
            ("/sortiment/bopp-pasky/bopp-paska-hot-melt", "BOPP HOT MELT"),
            ("/sortiment/bopp-pasky/bopp-paska-acrylic", "BOPP Akryl"),
            ("/sortiment/bopp-pasky/bopp-paska-tack-plus", "TACK+"),
            ("/sortiment/bopp-pasky/bopp-paska-extra-glue-plus", "EXTRA GLUE+"),
            ("/faq", "Další otázky ve FAQ"),
        ],
        "faqs": [
            (
                "Je HOT MELT lepší než Akryl?",
                "Záleží na provozu. HOT MELT vyniká v chladu a rychlé expedici; Akryl v tichém odvíjení a UV odolnosti.",
            ),
        ],
    },
    {
        "slug": "pasky-pro-e-shopy",
        "title": "Pásky pro e-shopy",
        "h1": "Pásky s potiskem pro e-shopy a sklady",
        "description": (
            "Jak vybrat pásky s potiskem pro e-shop: branding zásilek, HOT MELT vs Akryl, papírové FSC, "
            "ECO+ a bezpečnostní Tamper Evident pásky."
        ),
        "intro": (
            "E-shopy potřebují pásku, která drží, vypadá dobře a podporuje značku. "
            "Potištěná páska s logem je často první věc, kterou zákazník na krabici vidí."
        ),
        "sections": [
            (
                "Branding a unboxing",
                "Jednobarevný i vícebarevný potisk, bílá nebo transparentní BOPP, papírový kraft pro přírodní look. "
                "Galerie ukazuje reálné realizace (Alza, Bonami, Notino a další).",
            ),
            (
                "Rychlost skladu",
                "Pro ruční balení zvažte Low noise Akryl. Pro linky a chladné sklady HOT MELT. "
                "Tenčí Airtape+ šetří výměny rolí.",
            ),
            (
                "Bezpečnost zásilky",
                "Tamper Evident páska s potiskem zanechá při odlepení VOID stopu, vhodné pro elektroniku, "
                "kosmetiku a vyšší hodnotu zboží.",
            ),
        ],
        "links": [
            ("/galerie", "Galerie realizací"),
            ("/sortiment/bopp-pasky/bopp-paska-tamper-evident", "Tamper Evident"),
            ("/sortiment/udrzitelne-pasky", "ECO a udržitelné pásky"),
            ("/sortiment/papirove-pasky", "Papírové pásky"),
            ("/#gf_1", "Poptat pásku pro e-shop"),
        ],
        "faqs": [],
    },
    {
        "slug": "papirove-fsc-pasky",
        "title": "Papírové FSC pásky",
        "h1": "Papírové FSC pásky s potiskem",
        "description": (
            "Papírové pásky s potiskem a FSC nosičem: recyklace s kartonem, kraftový vzhled, "
            "varianty C680, KH80, KS165 a další."
        ),
        "intro": (
            "Papírová páska s potiskem je volba pro značky, které chtějí balení bez plastové fólie. "
            "Páska putuje do sběru spolu s kartonem a kraftový povrch působí přírodně a prémiově."
        ),
        "sections": [
            (
                "FSC a recyklace",
                "Nosiče s FSC certifikací a lepidla zvolená pro spolehlivé uzavření kartonu. "
                "Vhodné pro e-commerce i B2B zásilky s ESG požadavky.",
            ),
            (
                "Kterou gramáž",
                "C680 / KH80 pro běžné balíky, KS165 pro vyšší pevnost. Parametry a potisk doladíme podle hmotnosti zásilek.",
            ),
        ],
        "links": [
            ("/sortiment/papirove-pasky", "Všechny papírové pásky"),
            ("/sortiment/papirove-pasky/papirova-paska-c680", "Papírová C680"),
            ("/sortiment/papirove-pasky/papirova-paska-ks165", "Papírová KS165"),
            ("/pruvodce/eco-plus-recyklovane-pasky", "ECO+ recyklované pásky"),
        ],
        "faqs": [],
    },
    {
        "slug": "eco-plus-recyklovane-pasky",
        "title": "ECO+ a recyklované pásky",
        "h1": "ECO+ a recyklované pásky s potiskem",
        "description": (
            "Udržitelné pásky s potiskem: ECO+ 50/80/100 z regenerátu, NOPP/NOPP+ ISCC PLUS, "
            "LOOPP a POLY+ jako náhrada PVC. Bez kompromisů v pevnosti."
        ),
        "intro": (
            "Udržitelná páska s potiskem nemusí znamenat slabší lepivost. Řada ECO+ používá postindustriální "
            "regenerát z výroby BOPP fólií; NOPP a LOOPP přinášejí ISCC PLUS certifikaci."
        ),
        "sections": [
            (
                "ECO+ 50 / 80 / 100",
                "Volíte podíl regenerátu. Mechanické vlastnosti odpovídají standardní BOPP, dostupné jako Akryl i HOT MELT.",
            ),
            (
                "NOPP, NOPP+, LOOPP, POLY+",
                "NOPP = bio-cirkulární nosič, NOPP+ = fólie i lepidlo ISCC PLUS, LOOPP = chemicky recyklovaný plast, "
                "POLY+ = matná náhrada PVC.",
            ),
        ],
        "links": [
            ("/sortiment/udrzitelne-pasky", "Udržitelné pásky"),
            ("/sortiment/udrzitelne-pasky/udrzitelna-paska-eco-100", "ECO+ 100"),
            ("/sortiment/udrzitelne-pasky/udrzitelna-paska-nopp", "NOPP"),
            ("/sortiment/udrzitelne-pasky/udrzitelna-paska-poly-plus", "POLY+"),
        ],
        "faqs": [],
    },
    {
        "slug": "bezpecnostni-tamper-evident",
        "title": "Bezpečnostní Tamper Evident",
        "h1": "Bezpečnostní Tamper Evident pásky s potiskem",
        "description": (
            "Tamper Evident pásky s potiskem: VOID efekt při neoprávněném otevření, branding zásilky "
            "a ochrana elektroniky, kosmetiky i cenného zboží."
        ),
        "intro": (
            "Bezpečnostní páska Tamper Evident uzavře karton a zároveň odhalí manipulaci. "
            "Při odlepení zanechá VOID stopu. Zákazník i sklad ihned vidí, že balík někdo otevíral."
        ),
        "sections": [
            (
                "Jak funguje VOID efekt",
                "Speciální konstrukce pásky při sejmutí zanechá na kartonu permanentní stopu (typicky nápis VOID). "
                "Nelze ji nenápadně přelepit zpět. Vhodné jako pečeť proti krádeži a výměně zboží.",
            ),
            (
                "Kde dává smysl",
                "Elektronika, kosmetika, farmacie, high-value e-commerce a B2B zásilky, kde záleží na důvěře. "
                "Pásku lze potisknout logem: branding i ochrana v jednom kroku balení.",
            ),
            (
                "Kdy stačí běžná BOPP",
                "Pro běžné zásilky bez zvýšeného rizika manipulace často stačí HOT MELT nebo Akryl s potiskem. "
                "Tamper Evident volte tam, kde otevření bez stopy není akceptovatelné.",
            ),
        ],
        "links": [
            ("/sortiment/bopp-pasky/bopp-paska-tamper-evident", "Tamper Evident detail"),
            ("/sortiment/bopp-pasky", "BOPP pásky"),
            ("/pruvodce/pasky-pro-e-shopy", "Pásky pro e-shopy"),
            ("/#gf_1", "Poptat bezpečnostní pásku"),
        ],
        "faqs": [
            (
                "Lze Tamper Evident pásku potisknout logem?",
                "Ano, dostupná je s firemním potiskem i v neutrální variantě, podle vaší grafiky.",
            ),
        ],
    },
]


def load_chrome():
    base = (ROOT / "sortiment.html").read_text(encoding="utf-8")
    start = base.index("<!-- SITE-TOP -->")
    end = base.index("<!-- /SITE-TOP -->") + len("<!-- /SITE-TOP -->")
    header = (
        base[: base.index("</head>") + len("</head>")]
        + base[base.index("<body") : start]
        + base[start:end]
    )
    footer = base[base.index('<footer id="kontakt1"') :]
    return header, footer


def guide_main(g: dict) -> str:
    sections = "\n".join(
        f'''        <section class="mt-10">
            <h2 class="text-2xl font-extrabold tracking-tight text-slate-900">{esc(title)}</h2>
            <p class="mt-3 text-base leading-relaxed text-slate-600">{esc(body)}</p>
        </section>'''
        for title, body in g["sections"]
    )
    links = "\n".join(
        f'''            <a href="{esc(href)}" class="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-orange-200 hover:text-orange-700">
                {esc(label)}
                <span aria-hidden="true" class="text-orange-500">→</span>
            </a>'''
        for href, label in g["links"]
    )
    return f'''
<main>
<section class="mx-auto max-w-3xl px-4 py-12 sm:py-16">
    <nav class="mb-8 text-sm text-slate-500" aria-label="Drobečková navigace">
        <a href="/" class="hover:text-orange-600">Domů</a>
        <span class="mx-2 text-slate-300">/</span>
        <a href="/pruvodce" class="hover:text-orange-600">Průvodce</a>
        <span class="mx-2 text-slate-300">/</span>
        <span class="text-slate-600">{esc(g["title"])}</span>
    </nav>
    <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">{esc(g["h1"])}</h1>
    <p class="mt-5 text-lg leading-relaxed text-slate-600">{esc(g["intro"])}</p>
{sections}
    <nav class="mt-12 border-t border-slate-100 pt-8" aria-label="Související odkazy">
        <p class="mb-4 text-xs font-bold uppercase tracking-widest text-slate-400">Související odkazy</p>
        <div class="flex flex-wrap gap-2">
{links}
        </div>
    </nav>
</section>
</main>
'''


def guide_index_main() -> str:
    cards = "\n".join(
        f'''        <a href="/pruvodce/{esc(g["slug"])}" class="block rounded-2xl border border-slate-100 bg-white p-6 shadow-sm transition hover:border-orange-100 hover:shadow-md">
            <h2 class="text-lg font-bold text-slate-900">{esc(g["title"])}</h2>
            <p class="mt-2 text-sm leading-relaxed text-slate-600">{esc(g["description"])}</p>
        </a>'''
        for g in GUIDES
    )
    return f'''
<main>
<section class="mx-auto max-w-4xl px-4 py-12 sm:py-16">
    <nav class="mb-8 text-sm text-slate-500" aria-label="Drobečková navigace">
        <a href="/" class="hover:text-orange-600">Domů</a>
        <span class="mx-2 text-slate-300">/</span>
        <span class="text-slate-600">Průvodce</span>
    </nav>
    <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">Průvodce páskami s potiskem</h1>
    <p class="mt-4 text-lg leading-relaxed text-slate-600">Praktické srovnání materiálů a lepidel, bez marketingového balastu.</p>
    <div class="mt-10 grid grid-cols-1 gap-5 sm:grid-cols-2">
{cards}
    </div>
</section>
</main>
'''


def prepare_guide_chrome(header: str) -> str:
    """Guides reuse sortiment chrome — fix page marker + active nav styling."""
    header = header.replace('data-page="sortiment"', 'data-page="pruvodce"', 1)
    header = header.replace(
        'href="/sortiment" class="px-2 py-1 text-sm font-semibold text-orange-600 transition-colors hover:text-orange-600"',
        'href="/sortiment" class="px-2 py-1 text-sm font-semibold text-slate-700 transition-colors hover:text-orange-600"',
        1,
    )
    header = header.replace(
        'href="/sortiment" class="block px-2 py-2 font-semibold text-orange-600"',
        'href="/sortiment" class="block px-2 py-2 font-semibold text-slate-800 transition-colors hover:text-orange-600"',
        1,
    )
    header = header.replace(
        'href="/pruvodce" class="px-2 py-1 text-sm font-semibold text-slate-700 transition-colors hover:text-orange-600"',
        'href="/pruvodce" class="px-2 py-1 text-sm font-semibold text-orange-600 transition-colors hover:text-orange-600" data-nav-permanent-active',
        1,
    )
    header = header.replace(
        'href="/pruvodce" class="block px-2 py-2 font-semibold text-slate-800 transition-colors hover:text-orange-600"',
        'href="/pruvodce" class="block px-2 py-2 font-semibold text-orange-600 transition-colors hover:text-orange-600" data-nav-permanent-active',
        1,
    )
    return header


def write_page(path: Path, title: str, description: str, url_path: str, main: str, schemas: list):
    header, footer = load_chrome()
    header = prepare_guide_chrome(header)
    html_doc = header + main + footer
    html_doc = apply_page_seo(
        html_doc,
        title=page_title(title),
        description=description,
        path=url_path,
        schemas=schemas,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_doc, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def main() -> None:
    os.chdir(ROOT)
    print("Generating guide pages…")
    write_page(
        ROOT / "pruvodce" / "index.html",
        "Průvodce páskami s potiskem",
        "Průvodce výběrem pásek s potiskem: HOT MELT vs Akryl, e-shopy, papírové FSC a ECO+ recyklované pásky.",
        "/pruvodce",
        guide_index_main(),
        [breadcrumb_schema([("/", "Domů"), ("/pruvodce", "Průvodce")])],
    )
    for g in GUIDES:
        schemas = [
            breadcrumb_schema([
                ("/", "Domů"),
                ("/pruvodce", "Průvodce"),
                (f"/pruvodce/{g['slug']}", g["title"]),
            ])
        ]
        if g.get("faqs"):
            schemas.append(faq_schema(g["faqs"]))
        write_page(
            ROOT / "pruvodce" / g["slug"] / "index.html",
            g["title"],
            g["description"],
            f"/pruvodce/{g['slug']}",
            guide_main(g),
            schemas,
        )


if __name__ == "__main__":
    main()
