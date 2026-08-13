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
        "title": "Pásky s potiskem na míru",
        "h1": "Pásky s potiskem na míru",
        "description": (
            "Pásky s potiskem na míru od ALFA IN: branding zásilek, výběr BOPP HOT MELT / Akryl, "
            "papírové FSC a ECO+, minimální odběr a dodání 3–4 týdny."
        ),
        "intro": (
            "Hledáte potištěné lepicí pásky pro firmu, e-shop nebo sklad? Nabízíme řešení na míru přesně "
            "podle vašich potřeb: od klasických BOPP pásek přes ekologické papírové varianty s certifikací "
            "FSC až po udržitelné materiály ECO+, NOPP či bezpečnostní pásky Tamper Evident."
        ),
        "sections": [
            (
                "Proč zvolit pásky s potiskem?",
                "Potištěná páska plní dvě funkce najednou – spolehlivě uzavře karton a zároveň buduje značku "
                "přímo při přepravě. Vaše logo, slogan nebo manipulační instrukce cestují spolu s balíkem až "
                "k zákazníkovi. Jde o cenově výhodný a mimořádně odolný brandingový prvek, který zaujme "
                "na první pohled.",
            ),
            (
                "Jak vybrat správný materiál?",
                "Volba materiálu závisí na vašich provozních potřebách. Pro bleskovou expedici a okamžitou "
                "lepivost je ideální BOPP HOT MELT, zatímco Akryl vyniká tichým odvíjením a vysokou UV "
                "stabilitou. Papírové pásky umožňují snadnou recyklaci společně s kartonem a řešení ECO+/NOPP "
                "vám pomohou naplnit vaše firemní ESG cíle. Podrobné srovnání vlastností jednotlivých lepidel "
                "najdete v našem průvodci Hotmelt vs. Akryl.",
            ),
            (
                "Minimální odběr a termín dodání",
                "U BOPP pásek začíná minimální odběr typicky na 360 ks (Akryl) nebo 504 ks (HOT MELT). "
                "Standardní doba dodání se pohybuje mezi 3 a 4 týdny od finálního schválení grafického návrhu. "
                "Vzorky vybraných materiálů vám rádi zašleme zdarma na ukázku.",
            ),
        ],
        "links": [
            ("/sortiment", "Kompletní sortiment"),
            ("/pruvodce/hot-melt-vs-akryl", "Hotmelt vs. Akryl"),
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
        "title": "Hotmelt, nebo akryl?",
        "h1": "Hotmelt, nebo akryl? Jak vybrat správnou BOPP lepicí pásku",
        "description": (
            "Hotmelt vs Akryl u BOPP pásek s potiskem: okamžitá lepivost, UV odolnost, skladování "
            "a ideální použití pro e-commerce i průmyslové linky."
        ),
        "intro": (
            "Při výběru ideální BOPP lepicí pásky se nejčastěji setkáte s klíčovou otázkou: Sáhnout po "
            "hotmeltu, nebo raději po akrylu? Ačkoliv obě varianty na první pohled vypadají podobně, každá "
            "využívá zcela odlišný typ lepidla. To zásadně ovlivňuje jejich chování při balení, rychlost "
            "přilnutí i odolnost vůči okolním podmínkám. Abychom vám rozhodování usnadnili, připravili jsme "
            "přehledné srovnání vlastností i ideálního využití obou typů."
        ),
        "sections": [
            (
                "Akryl",
                "Pásky s akrylovým lepidlem představují ideální řešení všude tam, kde je prioritou vysoká "
                "odolnost proti stárnutí a působení UV záření. Skvěle se osvědčují při dlouhodobém uskladnění "
                "i při aplikaci ve venkovním prostředí. Charakteristickou vlastností akrylu je pozvolnější "
                "nástup lepicího účinku – lepidlo jednoduše potřebuje určitý čas, aby k povrchu plně přilnulo. "
                "Pokud tedy vyžadujete okamžitou a silnou fixaci ihned po nalepení, nemusí jít o nejvhodnější "
                "volbu. Jakmile však proces přilnutí proběhne, vytvoří se mimořádně pevný a trvanlivý spoj.\n\n"
                "V praxi se akrylové pásky nejčastěji uplatňují ve skladech a při balení zásilek, které nejsou "
                "vystaveny okamžitému extrémnímu zatížení. Pro své vlastnosti jsou velmi oblíbené také "
                "v kancelářích – díky odolnosti vůči žloutnutí si totiž uchovávají čistý a estetický vzhled "
                "i po delší době.",
            ),
            (
                "HOT MELT",
                "Hledáte-li pásku, která se okamžitě přichytí a zajistí pevné spojení bez čekání, je pro vás "
                "hotmelt správnou volbou. Toto lepidlo na bázi syntetického kaučuku vyniká mimořádnou lepivostí "
                "a vysokou počáteční přilnavostí. Velkou výhodou je jeho univerzálnost – spolehlivě drží "
                "na široké škále materiálů včetně méně standardních, prašnějších nebo recyklovaných kartonů. "
                "Zajišťuje maximálně efektivní a rychlé lepení bez rizika odlepování.\n\n"
                "Hotmelt je perfektním řešením pro rychlé balení v e-commerce, expedici zboží a náročné "
                "průmyslové provozy s automatickými balícími linkami. Skvěle si poradí i s náročnějšími typy "
                "povrchů či recyklovanými kartonovými krabicemi. Své nenahraditelné místo má v logistice "
                "a skladování, kde je klíčová okamžitá pevnost a bezproblémová manipulace se zásilkami ihned "
                "po zabalení.",
            ),
        ],
        "links": [
            ("/sortiment/bopp-pasky/bopp-paska-hot-melt", "BOPP HOT MELT"),
            ("/sortiment/bopp-pasky/bopp-paska-acrylic", "BOPP Akryl"),
            ("/sortiment/bopp-pasky/bopp-paska-tack-plus", "TACK+"),
            ("/sortiment/bopp-pasky/bopp-paska-extra-glue-plus", "EXTRA GLUE+"),
            ("/pruvodce/skladovani-aplikace-teplota", "Skladování a aplikace"),
            ("/faq", "Další otázky ve FAQ"),
        ],
        "faqs": [
            (
                "Je HOT MELT lepší než Akryl?",
                "Záleží na provozu. HOT MELT vyniká okamžitou lepivostí a rychlou expedicí; Akryl v UV "
                "odolnosti, dlouhodobém skladování a čistém vzhledu bez žloutnutí.",
            ),
        ],
    },
    {
        "slug": "skladovani-aplikace-teplota",
        "title": "Skladování, aplikace a teplota",
        "h1": "Skladování, aplikace a teplotní odolnost lepicích pásek",
        "description": (
            "Jak skladovat lepicí pásky (6–12 měsíců, 14–28 °C), proč je důležitý přítlak při lepení "
            "a jak pásky drží od mrazíren po zámořské kontejnery."
        ),
        "intro": (
            "Správné skladování a aplikace rozhodují o tom, jak páska drží v praxi – stejně jako výběr "
            "hotmeltu nebo akrylu. Níže najdete doporučené podmínky, roli přítlaku a teplotní odolnost "
            "od mrazíren po zámořské kontejnery."
        ),
        "sections": [
            (
                "Správné podmínky skladování a trvanlivost",
                "Standardní trvanlivost lepicích pásek se v závislosti na konkrétním typu a použitém lepidle "
                "pohybuje v rozmezí 6 až 12 měsíců od data odeslání. Pro zachování stoprocentních vlastností "
                "lepidla doporučujeme pásky skladovat v čistých a suchých prostorách, chránit je před "
                "nadměrnou vlhkostí a zamezit přímému působení slunečního záření.\n\n"
                "Ideální teplota pro skladování i samotné balení se pohybuje mezi 14 °C a 28 °C. Pokud jsou "
                "pásky krátkodobě vystaveny nižším teplotám (například při přepravě nebo v nevytápěném skladu), "
                "je nezbytné je před použitím přemístit do temperovaného prostředí a nechat materiál plně "
                "přizpůsobit doporučené pracovní teplotě.",
            ),
            (
                "Důležitost přítlaku při lepení",
                "Uvědomte si prosím, že balicí pásky využívají lepidla citlivá na tlak. Výsledná pevnost spoje "
                "proto nezávisí pouze na kvalitě lepidla, ale také na správné technice aplikace. Při odvíjení "
                "je potřeba na pásku vyvinout dostatečný a rovnoměrný přítlak po celé její délce, čímž dojde "
                "k dokonalému spojení lepidla s povrchem kartonu.",
            ),
            (
                "Teplotní odolnost v praxi: Od mrazíren po zámořské kontejnery",
                "Chování lepicí pásky v reálném provozu ovlivňuje řada faktorů – od konkrétní kombinace teploty "
                "a vlhkosti prostředí až po zásadní proměnnou, kterou je kvalita a povrch samotného kartonu. "
                "Výsledná pevnost spoje je tak vždy výsledkem souhry kvalitního lepidla a odpovídajícího podkladu.\n\n"
                "Mnohaleté zkušenosti z praxe u našich zákazníků ukazují, že jak akrylová, tak hotmeltová lepidla "
                "podávají vynikající výsledky. Pokud pásku aplikujete při běžných provozních či pokojových "
                "teplotách a vyvinete dostatečný přítlak, získáte spoj s mimořádnou odolností. Takto zalepené "
                "krabice si zachovávají plnou spolehlivost i ve velmi náročných podmínkách.",
            ),
        ],
        "links": [
            ("/pruvodce/hot-melt-vs-akryl", "Hotmelt vs. Akryl"),
            ("/faq", "FAQ – přilnavost, pevnost, tažnost"),
            ("/sortiment/bopp-pasky", "BOPP pásky"),
            ("/#gf_1", "Nezávazná kalkulace"),
        ],
        "faqs": [
            (
                "Jak dlouho pásky vydrží na skladě?",
                "Obvykle 6 až 12 měsíců od odeslání, podle typu pásky a lepidla, při skladování v suchu "
                "a při 14–28 °C mimo přímé slunce.",
            ),
        ],
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
            "Bezpečnostní páska Tamper Evident plní dvojí funkci – spolehlivě uzavře karton a zároveň "
            "funguje jako neúprosná kontrola jakéhokoliv neoprávněné manipulace. Při pokusu o odlepení "
            "zanechá na povrchu nesmazatelnou stopu, takže sklad i zákazník okamžitě poznají, že balík "
            "někdo neoprávněně otevíral."
        ),
        "sections": [
            (
                "Jak funguje VOID efekt",
                "Tato páska využívá speciální vícevrstvou konstrukci lepidla. Při jakémkoliv pokusu "
                "o sejmutí či odlepení se vrstvy oddělí a na kartonu zanechají permanentní bezpečnostní "
                "otisk (nejčastěji ve formě viditelného nápisu VOID). Pásku již nelze nenápadně přilepit "
                "zpět ani nahradit, což z ní dělá dokonalou bezpečnostní pečeť proti krádežím obsahu "
                "nebo nepozorované výměně zboží během přepravy.",
            ),
            (
                "Kde dává bezpečnostní páska největší smysl",
                "Tamper Evident pásky jsou ideální volbou pro zásilky s vysokou hodnotou nebo citlivým "
                "obsahem, kde je klíčová absolutní důvěra a ochrana. Typicky se využívají při expedici "
                "elektroniky, luxusní kosmetiky, farmaceutických výrobků, cenného e-commerce zboží nebo "
                "u důležitých B2B balíků. Díky možnosti vlastního potisku logem získáte prémiový branding "
                "i maximální zabezpečení zásilky v jediném kroku.",
            ),
            (
                "Kdy zvolit Tamper Evident a kdy stačí běžná BOPP?",
                "Pro standardní zásilky bez zvýšeného rizika odcizení plně postačí klasické BOPP pásky "
                "s akrylovým nebo hotmeltovým lepidlem a vlastním potiskem. Po bezpečnostní pásce "
                "Tamper Evident sáhněte v momentech, kdy je jakýkoliv neoprávněný vstup do balíku bez "
                "zanechání stopy absolutně neakceptovatelný a vy potřebujete mít stoprocentní jistotu.",
            ),
        ],
        "links": [
            ("/sortiment/bopp-pasky/bopp-paska-tamper-evident", "Tamper Evident detail"),
            ("/sortiment/bopp-pasky", "BOPP pásky"),
            ("/pruvodce/pasky-s-potiskem", "Pásky s potiskem na míru"),
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
    section_blocks = []
    for title, body in g["sections"]:
        paras = [p.strip() for p in body.split("\n\n") if p.strip()]
        paras_html = "\n".join(
            f'            <p class="mt-3 text-base leading-relaxed text-slate-600">{esc(p)}</p>'
            for p in paras
        )
        section_blocks.append(
            f'''        <section class="mt-10">
            <h2 class="text-2xl font-extrabold tracking-tight text-slate-900">{esc(title)}</h2>
{paras_html}
        </section>'''
        )
    sections = "\n".join(section_blocks)
    links = "\n".join(
        f'''            <a href="{esc(href)}" class="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-orange-200 hover:text-orange-700">
                {esc(label)}
                <span aria-hidden="true" class="text-orange-500">→</span>
            </a>'''
        for href, label in g["links"]
    )
    intro_paras = [p.strip() for p in g["intro"].split("\n\n") if p.strip()]
    intro_html = "\n".join(
        f'    <p class="mt-5 text-lg leading-relaxed text-slate-600">{esc(p)}</p>'
        for p in intro_paras
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
{intro_html}
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
