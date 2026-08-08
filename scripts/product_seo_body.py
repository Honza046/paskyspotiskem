#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Long-form SEO copy for product detail pages (Czech, B2B)."""

from __future__ import annotations

# Explicit paragraphs per product: (p1, p2). Natural comparisons + use cases + print/MOQ.
PRODUCT_SEO: dict[str, tuple[str, str]] = {
    "BOPP páska HOT MELT": (
        "HOT MELT páska s potiskem je nejčastější volba pro sklady, výrobu a e-commerce expedici. "
        "Syntetické kaučukové lepidlo rychle přilne i na chladnější nebo prašnější karton a hodí se "
        "pro ruční i strojové balení. Pokud hledáte pásky s potiskem od výrobce ALFA IN pro každodenní provoz, "
        "toto je výchozí průmyslový standard.",
        "Oproti akrylové BOPP pásce nabízí HOT MELT okamžitější lepivost v chladu; akryl zase tišší odvíjení "
        "a vyšší UV odolnost při dlouhodobém skladování. Minimální odběr u HOT MELT je typicky od 504 ks "
        "(základ 50 mm × 66 m). Potisk flexotiskem až 8 barev nebo rototiskem až 10 barev včetně spodního tisku.",
    ),
    "BOPP páska Akryl": (
        "Akrylová BOPP páska s potiskem je ideální, když potřebujete tiché odvíjení ve skladu a stabilní lepivost "
        "i při delším skladování. Vodní disperze bez agresivních rozpouštědel je šetrnější k pracovnímu prostředí "
        "a dobře snáší UV zatížení. Dostupné provedení Low noise i Noisy podle provozu.",
        "Ve srovnání s HOT MELT je akryl méně „agresivní“ v chladu, ale lepší pro dlouhodobé skladové zásoby a "
        "ruční balení s důrazem na komfort. Minimální odběr u Akrylu je typicky od 360 ks. Pásku dodáváme "
        "neutrálně i jako pásku s logem na míru.",
    ),
    "BOPP páska TACK+": (
        "TACK+ je HOT MELT páska se zvýšenou lepivostí (+20 %) pro náročné kartony, těžké balíky a prašné prostředí. "
        "Volíte ji, když standardní HOT MELT nestačí a potřebujete jistotu okamžitého přilnutí. "
        "Stejně jako ostatní BOPP pásky s potiskem ji vyrábíme s firemním logem i bez potisku.",
        "Pokud preferujete akrylovou variantu s vyšší vrstvou lepidla, zvažte EXTRA GLUE+. TACK+ zůstává "
        "volbou pro HOT MELT linky a sklady, kde rozhoduje tack a odolnost vůči obtížným povrchům.",
    ),
    "BOPP páska EXTRA GLUE+": (
        "EXTRA GLUE+ je akrylová páska se zesílenou vrstvou lepidla pro obtížné aplikace — nekvalitní kartony, "
        "těžké zásilky nebo prašné prostředí. Drží pevněji než standardní Akryl a přitom zachovává výhody "
        "vodní disperze a možnosti tichého odvíjení.",
        "Hotmeltovou alternativou s vyšším tackem je TACK+. EXTRA GLUE+ volte, když chcete akryl + maximální "
        "lepivost a potisk pásky s logem pro branding zásilek.",
    ),
    "BOPP páska Tamper Evident": (
        "Bezpečnostní Tamper Evident páska s potiskem chrání zásilku před neoprávněným otevřením. "
        "Při odlepení zanechá na kartonu upozornění (VOID / OPEN), které prakticky nelze odstranit. "
        "Hodí se pro e-shopy, farmaceutiku, elektroniku a logistiku s vyšším rizikem manipulace.",
        "Na rozdíl od běžné BOPP pásky není cílem jen uzavření kartonu, ale viditelný důkaz porušení. "
        "Dodáváme ji s firemním potiskem a v barevných variantách podle potřeby identifikace zásilek.",
    ),
    "BOPP páska ecoEVERGREEN": (
        "ecoEVERGREEN kombinuje BOPP výkon s vyšším podílem regenerovaného materiálu — vhodné pro firmy, "
        "které chtějí zelenější balení bez změny balicí linky. Páska s potiskem funguje stejně spolehlivě "
        "jako standardní BOPP a posiluje ESG komunikaci na krabici.",
        "Pro ještě vyšší podíl regenerátu zvažte řadu ECO+ (50 / 80 / 100 %). ecoEVERGREEN 50 % a 100 % "
        "volíte podle cíle uhlíkové stopy a rozpočtu.",
    ),
    "BOPP páska ecoEVERGREEN 100%": (
        "ecoEVERGREEN 100 % míří na maximální podíl regenerovaného obsahu při zachování BOPP pevnosti. "
        "Je to řešení pro zákazníky, kteří chtějí udržitelnou pásku s potiskem bez kompromisů v expedici.",
        "Pokud potřebujete flexibilitu podílu regenerátu a varianty Akryl i HOT MELT, prohlédněte také řadu ECO+.",
    ),
    "Udržitelná páska NOPP": (
        "NOPP je BOPP páska s nosnou fólií z bio-cirkulárního materiálu s certifikací ISCC PLUS. "
        "Nosič využívá obnovitelné suroviny z dřevního odpadu (vedlejší produkt výroby celulózy) a nahrazuje "
        "fosilní plasty bez ztráty pevnosti. Ideální páska s potiskem pro firmy s ESG cíli.",
        "NOPP+ jde ještě dál — certifikaci ISCC PLUS má fólie i lepidlo a nabízí zesílenou přilnavost (Adhesive G1). "
        "NOPP volte jako bio-cirkulární základ; NOPP+ když potřebujete maximum udržitelnosti i tacku.",
    ),
    "Udržitelná páska NOPP+": (
        "NOPP+ posouvá bio-cirkulární pásku na maximum: ISCC PLUS mají fólie i akrylové lepidlo. "
        "Speciální Adhesive G1 zvyšuje lepivost na drsnějších a recyklovaných kartonech. "
        "Pro branding i ESG reporting je to prémiová udržitelná páska s potiskem.",
        "Oproti NOPP získáte plně bio-cirkulární složení včetně lepidla a vyšší okamžitou přilnavost. "
        "Technické parametry (BOPP 28/32 µm, Akryl / Low noise) zůstávají průmyslově srovnatelné.",
    ),
    "Udržitelná páska LOOPP": (
        "LOOPP je cirkulární BOPP páska z polymerů chemicky recyklovaného spotřebitelského plastu "
        "s certifikací ISCC PLUS. Mechanické vlastnosti odpovídají standardní pásce z primárních surovin — "
        "bez kompromisů v pevnosti a lepivosti.",
        "Zatímco NOPP staví na bio-cirkulárním nosiči z obnovitelných surovin, LOOPP uzavírá smyčku "
        "recyklovaného plastu. Obě řady podporují pásky s potiskem pro odpovědné značky.",
    ),
    "Udržitelná páska POLY+": (
        "POLY+ je ekologická a plnohodnotná náhrada PVC pásek s elegantním matným povrchem. "
        "Matná BOPP fólie 35 µm a zesílené akrylové lepidlo (24 µm) dávají prémiový vzhled a pevné uzavření "
        "i těžších kartonů — ideální, když chcete opustit PVC bez ztráty estetického dojmu.",
        "Proti standardní lesklé BOPP pásce vyniká antireflexním povrchem a lepším kontrastem potisku. "
        "Dostupná jako Akryl / Low noise s potiskem firemního loga.",
    ),
    "Udržitelná páska ECO+ 50": (
        "ECO+ 50 obsahuje 50 % postindustriálního regenerátu z vlastní výroby fólií — optimální poměr "
        "ceny a ekologie. Mechanické vlastnosti odpovídají standardní BOPP, bez ekologické přirážky. "
        "Dostupná jako Akryl i HOT MELT, neutrálně i s potiskem.",
        "Pro vyšší podíl regenerátu zvolte ECO+ 80 nebo ECO+ 100. Všechny tři varianty se hodí jako "
        "udržitelné pásky s potiskem pro e-shopy a výrobu.",
    ),
    "Udržitelná páska ECO+ 80": (
        "ECO+ 80 zvyšuje podíl regenerátu na 80 % při stejné pevnosti jako standardní BOPP. "
        "Vhodná pro firmy, které chtějí výrazně snížit spotřebu primárního plastu a zároveň potisknout pásku logem.",
        "ECO+ 50 je levnější vstup do řady; ECO+ 100 je maximum regenerátu. Volba závisí na ESG cílech a rozpočtu.",
    ),
    "Udržitelná páska ECO+ 100": (
        "ECO+ 100 je 100% regenerovaná BOPP fólie z postindustriálního odpadu — maximální ekologický standard "
        "bez kompromisů ve výkonu. Páska s potiskem vypadá a funguje jako běžná BOPP, ale bez nového granulátu.",
        "Pokud potřebujete nižší cenu při stále vysokém podílu regenerátu, zvažte ECO+ 80. Všechny ECO+ varianty "
        "nabízíme s Akryl / HOT MELT lepidlem.",
    ),
    "Udržitelná páska Airtape+": (
        "Airtape+ je tenká a pevná BOPP páska (19 µm), která snižuje spotřebu materiálu a hmotnost zásilek. "
        "Na roli se vejde více metrů bez zvětšení průměru — méně výměn a úspora skladového místa. "
        "Akryl Low noise drží lepivost i při UV zatížení.",
        "Když hledáte maximální efektivitu metráže a nižší plastovou stopu při zachování výkonu, "
        "Airtape+ doplňuje řadu udržitelných pásek s potiskem vedle ECO+ a NOPP.",
    ),
    "Papírová páska C680": (
        "Papírová páska C680 je oblíbená kraftová volba pro plně recyklovatelné balení — páska jde do sběru "
        "spolu s kartonem. FSC certifikovaný nosič a spolehlivé lepidlo ji dělají vhodnou pro e-shopy "
        "i firmy, které chtějí papírové pásky s potiskem bez plastové fólie.",
        "Pro vyšší pevnost zvažte KS165 nebo vyztužené varianty; pro odnímatelné aplikace jiné řady. "
        "Potisk papírové pásky s logem dodává zásilkám přírodní a prémiový vzhled.",
    ),
    "Papírová páska KH80": (
        "KH80 je papírová páska s potiskem pro firmy, které chtějí čistý kraftový vzhled a recyklovatelné balení. "
        "Hodí se na uzavírání kartonů v e-commerce i B2B expedici, kde plastová fólie není žádoucí.",
        "Srovnejte s C680 / C690 podle gramáže a požadované pevnosti. Všechny papírové pásky ALFA IN "
        "umíme potisknout firemním logem.",
    ),
    "Papírová páska KS165": (
        "KS165 je robustnější papírová páska pro těžší balíky a náročnější uzavírání. "
        "Zachovává výhody papírového nosiče (recyklace s kartonem) a hodí se tam, kde standardní kraft nestačí.",
        "Pro lehčí e-shopové zásilky často stačí C680 nebo KH80. KS165 volte při vyšší hmotnosti a požadavku "
        "na pevnost papírové pásky s potiskem.",
    ),
    "BOPET páska ECO HIT19": (
        "ECO HIT19 je BOPET páska s podílem materiálu z recyklovaných PET lahví — pevná, odolná a ekologicky "
        "smysluplná alternativa pro náročné balení. Polyesterový nosič nabízí vysokou odolnost proti roztržení.",
        "Pro silnější fólii zvažte ECO HIT23 nebo klasické AIT/ATE řady. ECO HIT19 je vhodná, když chcete "
        "BOPET výkon a zároveň udržitelnější pásku s potiskem.",
    ),
    "BOPET páska ECO HIT23": (
        "ECO HIT23 kombinuje silnější BOPET fólii s regenerovaným obsahem z PET — pro těžké a náročné aplikace "
        "s ESG požadavky. Páska s potiskem odolává mechanickému namáhání lépe než běžná BOPP.",
        "ECO HIT19 je tenčí varianta stejné filozofie. Klasické HIT/AIT/ATE řady volte, když regenerát není priorita.",
    ),
}


CATEGORY_SEO_FALLBACK: dict[str, tuple[str, str]] = {
    "bopp-pasky": (
        "BOPP pásky s potiskem jsou průmyslový standard pro uzavírání kartonů ve výrobě, skladech a e-shopech. "
        "Biaxiálně orientovaný polypropylen nabízí výborný poměr pevnosti a ceny a skvěle se potiskuje logem.",
        "Vyberte HOT MELT pro rychlou lepivost v chladu, Akryl pro tiché odvíjení a UV stabilitu, "
        "nebo speciální varianty TACK+ / EXTRA GLUE+ / Tamper Evident podle aplikace. Minimální odběry a potisk "
        "konzultujeme individuálně — typicky stovky kusů podle typu lepidla.",
    ),
    "udrzitelne-pasky": (
        "Udržitelné pásky s potiskem od ALFA IN pokrývají regenerovaný BOPP (ECO+), bio-cirkulární NOPP/NOPP+, "
        "cirkulární LOOPP i matnou náhradu PVC (POLY+). Cílem je snížit ekologickou stopu balení bez ztráty výkonu.",
        "Porovnejte podíly regenerátu, certifikace ISCC PLUS a typ lepidla (Akryl / Low noise / HOT MELT). "
        "Rádi připravíme potisk loga a vzorek zdarma pro ověření v reálném provozu.",
    ),
    "papirove-pasky": (
        "Papírové pásky s potiskem umožňují plně recyklovatelné balení — páska putuje do sběru spolu s kartonem. "
        "Kraftový vzhled působí přírodně a prémiově a hodí se pro e-shopy i značky s důrazem na udržitelnost.",
        "Volte gramáž a pevnost podle hmotnosti zásilek (např. C680 vs KS165). Potisk firemním logem "
        "a FSC nosič patří k nejčastějším požadavkům B2B zákazníků.",
    ),
    "bopet-pasky": (
        "BOPET pásky s potiskem nabízejí polyesterovou pevnost a odolnost pro náročné průmyslové aplikace. "
        "Oproti BOPP lépe vzdorují roztržení a teplotním výkyvům.",
        "Řada ECO HIT přidává regenerovaný obsah z PET lahví. Technické varianty AIT/ATE/HIT volíte podle "
        "tloušťky fólie a lepidla — rádi doporučíme podle vaší linky.",
    ),
    "odstranitelne-pasky": (
        "Odstranitelné pásky s potiskem uzavřou obal a po sejmutí nezanechají lepivé stopy ani poškození povrchu. "
        "Hodí se pro dočasné zajištění, přepravu a aplikace, kde je potřeba pásku znovu odlepit.",
        "Porovnejte R28/32 a ECO RIT19 podle materiálu a udržitelnosti. Potisk loga zajistí branding i u "
        "dočasných uzávěrů.",
    ),
    "vyztuzene-pasky": (
        "Vyztužené pásky s potiskem zvyšují pevnost v tahu pro těžké balíky a náročné fixace. "
        "Jsou řešením, když standardní BOPP nestačí a potřebujete vyšší mechanickou odolnost.",
        "Volte mezi RTPP a RMPP podle konstrukce nosiče. Potisk a šířku připravíme podle specifikace provozu.",
    ),
    "mopp-pasky": (
        "MOPP pásky s potiskem využívají monoaxiálně orientovaný polypropylen pro specifické balicí aplikace "
        "s důrazem na pevnost v jednom směru.",
        "Parametry a lepivost konzultujeme podle vašeho stroje a kartonu. Dodáváme i s firemním potiskem.",
    ),
    "textilni-pasky": (
        "Textilní lepicí pásky s potiskem slouží k opravám, bundlování a specifickým průmyslovým aplikacím, "
        "kde fóliový nosič nestačí.",
        "Vyberte provedení podle nosiče a lepidla. Potisk a šířku připravíme na míru.",
    ),
    "malirske-pasky": (
        "Malířské pásky zajišťují ostré hrany při malování a lakování. Teplotně odolné varianty snesou "
        "náročnější procesy včetně vyšších teplot.",
        "C580 je volba pro běžné malování; CS60-80 pro vyšší teplotní zátěž. Potisk u malířských pásek "
        "řešíme individuálně podle zakázky.",
    ),
}


def product_seo_paragraphs(cat_slug: str, product_name: str) -> tuple[str, str]:
    if product_name in PRODUCT_SEO:
        return PRODUCT_SEO[product_name]
    if product_name.startswith("BOPP páska ecoEVERGREEN"):
        return PRODUCT_SEO["BOPP páska ecoEVERGREEN"]
    if product_name.startswith("Papírová páska"):
        return CATEGORY_SEO_FALLBACK["papirove-pasky"]
    if product_name.startswith("BOPET páska"):
        return CATEGORY_SEO_FALLBACK["bopet-pasky"]
    return CATEGORY_SEO_FALLBACK.get(
        cat_slug,
        (
            f"{product_name} od výrobce ALFA IN je lepicí páska s potiskem určená pro firemní balení, "
            "sklady a e-commerce expedici. Parametry a lepivost přizpůsobíme vašemu provozu.",
            "Připravíme potisk loga, šířku i návin a rádi pošleme vzorek k otestování před objednávkou. "
            "Nezávaznou kalkulaci pásky s potiskem vyřídíte přímo na webu.",
        ),
    )


def product_seo_body_html(cat_slug: str, product_name: str) -> str:
    p1, p2 = product_seo_paragraphs(cat_slug, product_name)
    return (
        f'<div class="product-seo-body mt-5 space-y-3 text-sm leading-relaxed text-slate-600 sm:text-base">'
        f"<p>{_esc(p1)}</p>"
        f"<p>{_esc(p2)}</p>"
        f"</div>"
    )


def _esc(s: str) -> str:
    import html

    return html.escape(s, quote=True)
