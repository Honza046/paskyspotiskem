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
                "Volba nosiče pásky závisí na hmotnosti zásilek, provozních nárocích i vašich ekologických "
                "cílech. Standardní BOPP je osvědčená a cenově nejefektivnější volba pro každodenní balení "
                "běžných zásilek. Pokud cílíte na plnění ESG cílů, udržitelná řešení ECO+, NOPP a LOOPP staví "
                "na stejném BOPP základu, avšak s certifikovaným obsahem recyklátu či obnovitelných bio-surovin "
                "bez ztráty pevnosti. Polyesterové pásky BOPET nabízejí extrémní odolnost proti přetržení pro "
                "těžké náklady a dvojnásobný návin role, který šetří místo ve skladu. Papírové pásky s FSC "
                "certifikací pak dodávají balíkům prémiový přírodní vzhled a umožňují stoprocentní recyklaci "
                "celé krabice bez nutnosti odlepování. S výběrem optimálního materiálu pro vaše balicí procesy "
                "vám rádi poradíme.",
            ),
            (
                "Jak vybrat správné lepidlo?",
                "Typ lepidla rozhoduje o rychlosti lepení i chování pásky v různých podmínkách. HOT MELT "
                "(syntetický kaučuk) je jasnou volbou pro dynamické provozy a automatické linky díky své "
                "okamžité počáteční lepivosti. Akryl na vodní bázi vyniká dlouhodobou stálostí, UV odolností "
                "a možností tichého odvíjení Low Noise, ideálního pro klidnější pracovní prostředí. Pro "
                "náročné chladírenské podmínky a mrazy pak nabízíme vysoce odolnou řadu EVERGREEN. Podrobné "
                "srovnání vlastností a výhod jednotlivých technologií najdete v Hotmelt, nebo akryl? Jak "
                "vybrat správnou BOPP lepicí pásku.",
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
        "h1": "Papírové FSC pásky",
        "description": (
            "Papírové pásky s FSC certifikací a potiskem: KH80, C660, C680/R/RT, C690 a KS125. "
            "Recyklace s kartonem, hotmelt lepidlo, e-commerce i B2B."
        ),
        "intro": (
            "Papírová lepicí páska představuje ideální volbu pro značky, které chtějí balit ekologicky "
            "a bez použití plastových fólií. Páska putuje do tříděného sběru společně s kartonem a její "
            "přírodní kraftový povrch působí prémiovým i udržitelným dojmem. Naše evropské papírové pásky "
            "jsou standardně opatřeny hotmelt lepidlem ze syntetického kaučuku. Všechny typy disponují "
            "certifikací FSC a umožňují potisk až ve 4 barvách (u řady KH80 dokonce až v 8 barvách)."
        ),
        "sections": [
            (
                "FSC a recyklace",
                "Nosiče s certifikací FSC v kombinaci s kvalitními lepidly zajišťují spolehlivé a trvalé "
                "uzavření kartonu. Všechny využívají ekologické lepidlo hotmelt bez obsahu rozpouštědel. "
                "Výjimkou je pouze model C780 se solventním lepidlem. Papírové pásky jsou plně vhodné "
                "pro e-commerce i B2B zásilky s vysokými ESG požadavky a lze je aplikovat jak ručně, "
                "tak pomocí odvíječů či balicích strojů.",
            ),
            (
                "Který typ a pevnost zvolit?",
                "Široká nabídka materiálů vám umožní vybrat si ideální řešení přesně podle hmotnosti "
                "a náročnosti vašich zásilek:\n\n"
                "KH80: Zosobnění maximální udržitelnosti a zelené evoluce v papírových páskách. Je "
                "vyrobena ze 100% recyklovaného kraftového papíru s certifikací FSC a opatřena "
                "bezrozpouštědlovým hotmelt lepidlem. K dispozici je v hnědé i bílé variantě a technicky "
                "podporuje potisk až v 8 barvách.\n\n"
                "C660: Standardní a cenově dostupná kvalita z krepatého papíru pro běžné balení.\n\n"
                "C680 a C680R / C680RT: Prémiová řada papírových pásek s vynikajícím poměrem ceny "
                "a výkonu. K dispozici je v hnědé i bílé variantě a také v zesílené verzi vyztužené "
                "skelnými vlákny – buď podélně C680R, nebo mřížkově C680RT.\n\n"
                "C690: Mimořádně pevná nezesílená páska s vysokou pevností v tahu a špičkovou přilnavostí "
                "k oceli, která představuje skvělou alternativu k mřížkově zesíleným páskám.\n\n"
                "KS125: Speciální páska z kraftového papíru s extrémně vysokou pevností v tahu. Místo "
                "běžného zalepování krabic slouží k náročným úkolům, jako je pevné zafixování zboží "
                "na paletách před odesláním nebo svazování těžkých produktů do svazků.",
            ),
        ],
        "links": [
            ("/sortiment/papirove-pasky", "Všechny papírové pásky"),
            ("/sortiment/papirove-pasky/papirova-paska-kh80", "Papírová KH80"),
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
            "Udržitelné pásky s potiskem: ECO+ 50/80/100, NOPP/NOPP+ ISCC PLUS, LOOPP, POLY+, "
            "AIRTAPE a ecoHIT. Bez kompromisů v pevnosti a lepivosti."
        ),
        "intro": (
            "Udržitelná lepicí páska s potiskem neznamená kompromis v lepivosti ani pevnosti. Dnešní "
            "ekologické plastové pásky dokáží plně nahradit standardní fólie, zredukovat uhlíkovou stopu "
            "a pomoci vaší firmě plnit ESG cíle. Využívají k tomu buď ztenčenou tloušťku, vysoký podíl "
            "recyklátu, nebo bio-cirkulární suroviny s certifikací ISCC PLUS."
        ),
        "sections": [
            (
                "Redukce plastu a udržitelné technologie",
                "Udržitelnosti lze dosáhnout různými cestami – od snižování tloušťky fólie přes zapojení "
                "recyklovaných plastů až po chemickou recyklaci a bio-materiály:\n\n"
                "ECO+ (50 / 80 / 100): Řada pásek využívající postindustriální regenerát (PIR) z výroby "
                "BOPP fólií. Číslo udává procentuální podíl recyklovaného materiálu (50 %, 80 % nebo 100 %). "
                "Mechanickými vlastnostmi se zcela vyrovná standardním páskám a je k dispozici s akrylovým "
                "i hotmeltovým lepidlem.\n\n"
                "NOPP / NOPP+: Pásky založené na principu hmotnostní bilance (mass balance) certifikované "
                "podle ISCC PLUS. NOPP využívá bio-cirkulární nosič z obnovitelných zdrojů (např. odpadních "
                "olejů). Verze NOPP+ jde ještě dále a certifikaci ISCC PLUS má jak samotná fólie, tak použité "
                "lepidlo.\n\n"
                "LOOPP: Průlomové řešení využívající chemicky recyklovaný plast (PCR). Tento proces vrací "
                "plastový odpad zpět na úroveň primární suroviny, takže páska dosahuje identické kvality, "
                "čirosti a pevnosti jako zcela nová BOPP fólie.\n\n"
                "POLY+: Odolná polypropylenová (BOPP) páska s elegantním matným povrchem, která představuje "
                "ekologičtější a plně recyklovatelnou náhradu za tradiční PVC pásky. Zajišťuje tiché odvíjení "
                "a skvělý vzhled.\n\n"
                "AIRTAPE: Páska se ztenčenou tloušťkou fólie, která při zachování vysoké pevnosti šetří "
                "množství použitého plastu i celkovou hmotnost zásilek.\n\n"
                "ecoHIT: Prémiová ekologická páska chráněná evropským patentem, která obsahuje minimálně "
                "85 % recyklovaného PET odpadu z plastových lahví. Její polyesterový základ jí dává "
                "extrémní mechanickou odolnost proti přetržení, takže se při aplikaci nepraská, nenatahuje "
                "ani nedeformuje. Díky tenčímu profilu pojme role standardního průměru dvojnásobný návin "
                "metrů, což v provozu znamená méně častou výměnu rolí na balicích linkách, vyšší plynulost "
                "balení a výraznou úsporu skladovacího místa.",
            ),
        ],
        "links": [
            ("/sortiment/udrzitelne-pasky", "Udržitelné pásky"),
            ("/sortiment/udrzitelne-pasky/udrzitelna-paska-eco-100", "ECO+ 100"),
            ("/sortiment/udrzitelne-pasky/udrzitelna-paska-nopp", "NOPP"),
            ("/sortiment/udrzitelne-pasky/udrzitelna-paska-poly-plus", "POLY+"),
            ("/sortiment/udrzitelne-pasky/udrzitelna-paska-airtape", "AIRTAPE"),
            ("/sortiment/bopet-pasky/bopet-paska-eco-hit19", "ecoHIT"),
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
            "funguje jako neúprosná kontrola jakékoliv neoprávněné manipulace. Při pokusu o odlepení "
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
                "zanechání stopy absolutně neakceptovatelný a vy potřebujete mít stoprocentní jistotu, "
                "že zásilka dorazí k příjemci v netknutém stavu.",
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
