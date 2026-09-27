#!/usr/bin/env python3
"""Generuje samostatne vstupni stranky (kontakt, o nas, reference, komercni landingy).

Kazda stranka cili na jiny vyhledavaci zamer, aby si stranky navzajem nekanibalizovaly:
  /kontakt                     navigacni a lokalni dotazy
  /o-nas                       duveryhodnost znacky
  /reference                   socialni dukaz
  /pasky-s-potiskem-pro-eshopy segment e-commerce
  /pasky-s-logem               branding a technologie potisku
  /cena-pasky-s-potiskem       cenove dotazy
  /vyroba-lepicich-pasek       vyrobni proces a "vyrobce"
"""
from __future__ import annotations

import html
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from seo import (  # noqa: E402
    apply_page_seo,
    breadcrumb_schema,
    faq_schema,
)

esc = html.escape

# ---------------------------------------------------------------------------
# Obsah stranek. Vsechna fakta pochazi z existujiciho webu (homepage, FAQ,
# pruvodci, paticka). Ceny ani udaje, ktere web neuvadi, zde nevymyslime.
# ---------------------------------------------------------------------------

PAGES = [
    {
        "slug": "kontakt",
        "nav": "Kontakt",
        "h1": "Kontakty a nezávazná poptávka",
        "seo_title": "Kontakty a nezávazná poptávka | Pásky s potiskem | ALFA IN",
        "description": (
            "Kontakty na obchodní oddělení pro balicí pásky s potiskem. Telefon, e-mail, "
            "sídlo ALFA IN v Nové Vsi u Třebíče a postup nezávazné poptávky."
        ),
        "intro_parts": [
            "Obraťte se na nás s poptávkou balicích pásek pro váš provoz. Cenovou nabídku obvykle "
            "vypracujeme ",
            ("strong", "ještě v den zadání"),
            ". Pomůžeme vám vybrat ideální materiál, v případě potřeby zajistíme provzorování "
            "ve vašem provozu a připravíme potisk přesně podle potřeb vaší expedice.",
        ],
        "sections": [
            ("Obchodní oddělení", [
                {
                    "type": "person",
                    "name": "Ing. Karel Petrák | Prodej balicích pásek",
                    "phone": "+420 602 746 017",
                    "phone_href": "tel:+420602746017",
                    "email": "karel.petrak@alfain.eu",
                },
                {
                    "type": "person",
                    "name": "Vojtěch Petrák | Asistent prodeje",
                    "phone": "+420 773 216 266",
                    "phone_href": "tel:+420773216266",
                    "email": "vojtech.petrak@alfain.eu",
                },
                {
                    "type": "labeled",
                    "label": "Provozní doba:",
                    "text": "Pracovní dny 7:00 – 15:30 hod.",
                },
            ]),
            ("Sídlo společnosti", [
                {
                    "type": "p_strong_start",
                    "strong": "ALFA IN a.s.",
                    "text": ", Nová Ves 74, 675 21 Nová Ves u Třebíče, Česká republika",
                },
                "Pravidelně zásobujeme provozy po celé ČR. Osobní schůzku nebo vyzvednutí materiálu "
                "lze sjednat po předchozí domluvě.",
            ]),
            ("Co uvést do poptávky pro rychlou kalkulaci", [
                "Pokud máte konkrétní představu, urychlí nám práci tyto údaje:",
                {
                    "type": "ul",
                    "items": [
                        (
                            "Materiál a rozměr:",
                            "Typ nosiče (fólie BOPP, recyklovaný plast, papír), šířka role a návin "
                            "(standardně 50 mm × 66 m pro ruční odvíječe nebo dlouhé strojní náviny "
                            "pro balicí linky).",
                        ),
                        ("Plánovaný odběr:", "Orientační počet rolí nebo kartonů."),
                        (
                            "Podklady pro potisk:",
                            "Počet barev, případně požadavek na celoplošný barevný podklad. Logo "
                            "zašlete nejlépe ve vektorech (PDF, AI, EPS) s uvedením odstínů Pantone.",
                        ),
                    ],
                },
                {
                    "type": "italic",
                    "text": (
                        "Nemáte-li přesné parametry, nevadí. Popište nám, co balíte, v jakém prostředí "
                        "zásilky připravujete a jak jsou těžké. Správnou kombinaci pásky i lepidla "
                        "vybereme za vás."
                    ),
                },
            ]),
            ("Jak probíhá spolupráce", [
                {
                    "type": "ol",
                    "items": [
                        (
                            "Nabídka a doporučení materiálu:",
                            "Na základě vašeho zadání obratem navrhneme optimální pásku a pošleme "
                            "nezávaznou cenovou kalkulaci.",
                        ),
                        (
                            "Bezplatné provzorování:",
                            "Před potvrzením zakázky vám rádi zdarma zašleme vzorky reálných materiálů "
                            "a lepidel ze skladu. Funkčnost a přilnavost si tak sami otestujete přímo "
                            "ve vašem provozu – ať už lepíte na kartony, nebo do stretch fólie.",
                        ),
                        (
                            "Výrobní náhled potisku:",
                            "Připravíme oficiální grafický náhled pásky s vaším logem k finálnímu "
                            "odsouhlasení před spuštěním tiskové přípravy.",
                        ),
                        (
                            "Výroba a dodání:",
                            "Standardně dodáváme během 3 až 4 týdnů od schválení grafiky a potvrzení "
                            "objednávky. Zboží expedujeme bezpečně na nevratných EURO paletách.",
                        ),
                    ],
                },
            ]),
        ],
        "links": [
            ("/sortiment", "Kompletní sortiment"),
            ("/cena-pasky-s-potiskem", "Co ovlivňuje cenu"),
            ("/faq", "Časté otázky"),
            ("/#gf_1", "Nezávazná kalkulace"),
        ],
        "schema_type": "ContactPage",
    },
    {
        "slug": "o-nas",
        "nav": "O nás",
        "h1": "O výrobci lepicích pásek ALFA IN",
        "seo_title": "O nás | Český výrobce lepicích pásek s potiskem | ALFA IN",
        "description": (
            "Vyrábíme lepicí pásky s potiskem více než 30 let. Vlastní výroba fólií, certifikace "
            "ISO 9001 a FSC, přes 300 aktivních odběratelů a důraz na udržitelné materiály."
        ),
        "intro": (
            "Jsme tradiční český dodavatel lepicích pásek s potiskem i bez něj. Více než 30 let pomáháme "
            "firmám bezpečně balit zásilky a budovat značku přímo na obalovém materiálu."
        ),
        "sections": [
            ("Vyrábíme i vlastní fólie", [
                "Nevyrábíme pouze lepicí pásky, ale i samotné fólie, ze kterých pásky vznikají. To nám dává "
                "výhodu v době surovinových výkyvů na trhu, protože nejsme závislí na dodávkách nosiče od "
                "třetích stran.",
                "Vlastní výrobní zázemí zároveň umožňuje pružně reagovat na potřeby malých e-shopů i velkých "
                "průmyslových podniků. Zvládneme jak menší sérii pro začínající obchod, tak opakované dodávky "
                "pro výrobní závod.",
            ]),
            ("Kvalita a certifikace", [
                "Výroba probíhá podle certifikovaných procesů ISO 9001. Papírové pásky vyrábíme z papíru "
                "s certifikací FSC Mix Credit pod licencí FSC-C159046.",
                "Zakládáme si na precizním tisku a na kvalitě použitých lepidel. Nabízíme flexotisk až 8 barev "
                "a rototisk až 10 barev včetně kvalitního spodního tisku.",
                "Používáme akrylátovou disperzi na vodní bázi a technologii HOT MELT bez rozpouštědel. Lepidla "
                "tedy neuvolňují toxické výpary a jsou bezpečná pro pracovníky ve skladu.",
            ]),
            ("Komu dodáváme", [
                "Spolupracujeme s více než 300 aktivními odběrateli napříč obory. Naše pásky používají "
                "e-shopy, výrobní podniky, distribuční sklady i zdravotnická zařízení.",
                "Dodáváme po celé České republice a do zemí Evropské unie. Rozsah zakázek sahá od jednorázových "
                "sérií po dlouhodobé rámcové dodávky.",
            ]),
            ("Udržitelnost není marketing", [
                "V nabídce máme papírové pásky z pevného kraftu, BOPET pásku z recyklovaných PET lahví "
                "a fólie s obsahem PCR a PIR odpadu. Plasty i papír tak vracíme zpět do oběhu.",
                "Řada ECO+ využívá postindustriální regenerát z naší vlastní výroby BOPP fólií. Číslo v názvu "
                "udává podíl recyklovaného materiálu, tedy 50, 80 nebo 100 procent.",
                "Firmám pomáháme snižovat uhlíkovou stopu balení a doložit plnění ESG cílů před auditory "
                "i obchodními partnery.",
            ]),
            ("Jak u nás spolupráce probíhá", [
                "Začínáme vaším zadáním. Zajímá nás, co balíte, v jakém prostředí a jaké množství potřebujete. "
                "Na základě toho doporučíme materiál nosiče i typ lepidla.",
                "Následuje cenová nabídka a grafický náhled pásky. Do výroby jde vždy až podoba, kterou "
                "jste odsouhlasili.",
                "Standardní dodací lhůta je 3 až 4 týdny od schválení návrhu. U opakovaných odběratelů "
                "se domlouváme na rámcových dodávkách s postupným odvoláváním.",
            ]),
            ("Osobní přístup místo formuláře", [
                "Obchodní oddělení pro balicí pásky vedou Ing. Karel Petrák a Vojtěch Petrák. Vaši poptávku "
                "tak řeší konkrétní člověk, který zná výrobu i sortiment.",
                "Díky tomu zvládneme i nestandardní zadání, u kterých by běžný katalogový dodavatel "
                "musel odmítnout. Šířku, délku návinu, barvu podkladu i počet barev přizpůsobíme vašemu provozu.",
            ]),
        ],
        "links": [
            ("/reference", "Reference a zákazníci"),
            ("/vyroba-lepicich-pasek", "Jak pásky vyrábíme"),
            ("/sortiment/udrzitelne-pasky", "Udržitelné pásky"),
            ("/kontakt", "Kontakty"),
        ],
        "schema_type": "AboutPage",
    },
    {
        "slug": "reference",
        "nav": "Reference",
        "h1": "Reference a průmyslové balicí pásky",
        "seo_title": "Reference | Průmyslové balicí pásky s potiskem | ALFA IN",
        "description": (
            "Denně jistíme expedici pro více než 300 aktivních provozů. Pásky s potiskem "
            "i bez něj pro e-commerce, výrobu, automotive i zdravotnictví."
        ),
        "intro_lead": "Denně jistíme expedici pro více než 300 aktivních provozů",
        "intro": (
            "Dodáváme spolehlivá obalová řešení pro rostoucí i zavedené e-commerce firmy, "
            "distribuční sklady i výrobní a automotive provozy. Zajišťujeme zakázkovou výrobu "
            "pásek s vlastním potiskem pro silný branding zásilek i velkoobjemové dodávky "
            "neutrálních pásek bez potisku pro ruční odvíječe i automatizované balicí linky."
        ),
        "sections": [
            ("Proč firmy volí pásky s potiskem?", [
                {
                    "type": "h3p",
                    "h3": "Branding za zlomek ceny",
                    "p": (
                        "Potištěná lepicí páska promění obyčejnou hnědou krabici v plnohodnotný nosič "
                        "značky. Odpadá nutnost objednávat, draze platit a skladovat potištěné kartony "
                        "ve všech rozměrech. Jedna role pásky s logem sjednotí vizuál celého skladu "
                        "a výrazně šetří provozní náklady i místo na paletách."
                    ),
                },
                {
                    "type": "h3p",
                    "h3": "Potisk, který se při přepravě neosetře",
                    "p": (
                        "Využíváme pokročilou technologii spodního sendvičového tisku – barva se nanáší "
                        "na vnitřní stranu nosné fólie ještě před nanesením lepidla. Grafika je tak "
                        "100% chráněná proti mechanickému oděru, poškrábání i vlhkosti při manipulaci "
                        "přepravců."
                    ),
                },
                {
                    "type": "h3p",
                    "h3": "Bezpečnostní pečeť obsahu (Tamper Evident)",
                    "p": (
                        "Vlastní firemní potisk funguje jako okamžitá bezpečnostní pečeť proti vykrádání "
                        "zásilek na depech. Balík nelze nepozorovaně otevřít a přelepit běžnou páskou, "
                        "což výrazně eliminuje ztráty při transportu."
                    ),
                },
                {
                    "type": "h3p",
                    "h3": "Ekologické balení a plnění ESG cílů",
                    "p": (
                        "Pro provozy sledující uhlíkovou stopu dodáváme certifikované papírové pásky "
                        "(100% recyklovatelné přímo s kartonem), inovativní pásky z recyklovaných PET "
                        "lahví i řadu ECO+ využívající recyklovaný materiál z vlastní výroby fólií. "
                        "Všechna udržitelná řešení dodáváme s potiskem i v čistém neutrálním provedení."
                    ),
                },
            ]),
            ("Čím se můžeme doložit: Zázemí, kapacita a certifikace", [
                {
                    "type": "h3p",
                    "h3": "Plně integrované výrobní zázemí",
                    "p": (
                        "Na rozdíl od běžných distributorů, kteří čistou fólii pouze přeprodávají "
                        "od třetích stran, disponujeme zázemím s přímou výrobou BOPP fólií. Fólii "
                        "nemusíme nakupovat od dalších zprostředkovatelů. V případě výkyvů na trhu "
                        "tak držíme stoprocentní kontinuitu dodávek i garantované kapacity, což "
                        "představuje naši zásadní konkurenční výhodu."
                    ),
                },
                {
                    "type": "h3p",
                    "h3": "Špičková kapacita flexotisku i rototisku",
                    "p": (
                        "Zvládáme flexotisk až do 8 barev i průmyslový tisk až do 10 barev. Realizujeme "
                        "precizní jednobarevná i vícebarevná loga, jemné rastry, celoplošné podtisky "
                        "i velkoobjemové série standardních nepotištěných pásek v libovolných šířkách "
                        "a návinech."
                    ),
                },
                {
                    "type": "h3p",
                    "h3": "Certifikovaná kvalita ISO 9001 a auditované standardy",
                    "p": (
                        "Výrobní procesy a laboratorní stálost lepidel podléhají normě ISO 9001. "
                        "Udržitelný sortiment opíráme o mezinárodní certifikace – krepové a kraftové "
                        "papíry s certifikací FSC, fólie s certifikací ISCC PLUS na bázi hmotnostní "
                        "bilance a recyklované materiály s garantovaným původem."
                    ),
                },
                {
                    "type": "h3p",
                    "h3": "Ověřená průmyslová lepidla bez chemických rozpouštědel",
                    "p": (
                        "Stavíme na šetrných a výkonných lepicích systémech bez obsahu těkavých "
                        "chemických rozpouštědel. Dodáváme ekologické akrylátové disperze na vodní "
                        "bázi (s tichým odvíjením, vysokou stálostí a odolností proti UV záření) "
                        "i vysoce přilnavý Hot Melt na bázi syntetického kaučuku, který zaručuje "
                        "okamžitý nátrh a pevné uzavření kartonů i při nižších teplotách pod 18 °C "
                        "a na recyklovaném papíru."
                    ),
                },
            ]),
            ("Řešení na míru pro různé segmenty", [
                {
                    "type": "ul",
                    "items": [
                        (
                            "E-commerce firmy:",
                            "Profesionální unboxing zážitek, okamžitá vizuální identifikace zásilky "
                            "a výrazná úspora expedičních nákladů nahrazením drahých zakázkových krabic.",
                        ),
                        (
                            "Výroba & automotive:",
                            "Vysoká pevnost pásky v tahu, okamžitý silný příchyt a spolehlivé uzavření "
                            "těžkých kartonů i stabilní fixace palet.",
                        ),
                        (
                            "Farmacie & zdravotnictví:",
                            "Čisté technologie lepidel bez zápachu a chemických rozpouštědel, "
                            "certifikovaná stálost materiálů a spolehlivá ochrana citlivých zásilek "
                            "před neoprávněným vniknutím.",
                        ),
                    ],
                },
            ]),
            ("Vyzkoušejte kvalitu na vlastních kartonech", [
                "Nákupčí nepotřebuje sliby, ale jistotu funkčnosti ve svém provozu.",
                "Rádi vám bezplatně zašleme reálné vzorky materiálů a lepidel ze skladu, abyste si "
                "pevnost a přilnavost otestovali přímo na vašich typech krabic.",
            ]),
        ],
        "links": [
            ("/galerie", "Galerie realizací"),
            ("/o-nas", "O výrobci"),
            ("/pasky-s-logem", "Pásky s logem"),
            ("/#gf_1", "Vyžádat vzorky zdarma"),
        ],
        "cta": {
            "title": "Vyzkoušejte kvalitu na vlastních kartonech",
            "text": (
                "Rádi vám bezplatně zašleme reálné vzorky materiálů a lepidel ze skladu, abyste si "
                "pevnost a přilnavost otestovali přímo na vašich typech krabic."
            ),
            "button": "Vyžádat vzorky zdarma",
            "href": "/#gf_1",
        },
        "schema_type": "WebPage",
    },
    {
        "slug": "pasky-s-potiskem-pro-eshopy",
        "nav": "Pásky pro e-shopy",
        "h1": "Pásky s potiskem pro e-shopy",
        "seo_title": "Pásky s potiskem pro e-shopy | Balicí páska s logem",
        "description": (
            "Balicí pásky s potiskem pro e-shopy. Jaký materiál zvolit, kolik pásky spotřebujete, "
            "udržitelné varianty a minimální odběr od 360 kusů."
        ),
        "intro": (
            "Pro e-shop je páska poslední věc, kterou na zásilce vidíte vy, a první věc, kterou uvidí "
            "zákazník. Potištěná páska proto řeší uzavření krabice a budování značky zároveň."
        ),
        "sections": [
            ("Proč e-shopy volí potištěnou pásku", [
                "Zásilka putuje od skladu přes dopravce až ke dveřím zákazníka a po celou dobu ji někdo vidí. "
                "Páska s logem tak funguje jako reklamní plocha, za kterou neplatíte žádné dodatečné umístění.",
                "Oproti potištěné krabici je páska výrazně levnější cestou k jednotnému vzhledu zásilek. "
                "Krabice můžete nakupovat neutrální a vizuální identitu doplnit až páskou.",
                "Potisk zároveň ztěžuje nepozorovanou manipulaci se zásilkou, protože jakýkoli zásah do "
                "pásky je na potištěném motivu snadno viditelný.",
            ]),
            ("Jaký materiál zvolit pro e-shop", [
                "Nejčastější volbou je BOPP páska. Nabízí nejlepší poměr ceny a výkonu pro každodenní balení "
                "běžných zásilek a je dostupná v akrylovém i HOT MELT provedení.",
                "Pokud balíte v nevytápěném skladu nebo expedujete rychle, sáhněte po lepidle HOT MELT. "
                "Přilne okamžitě a pevně i v chladu.",
                "Pro tiché odvíjení ve velké balicí hale a pro dlouhodobé skladování zboží se hodí akryl "
                "s nehlučnou úpravou, který lépe odolává UV záření a stárnutí.",
                "Chcete-li, aby zákazník mohl celou krabici i s páskou vyhodit do papíru, zvolte papírovou "
                "pásku s certifikací FSC.",
            ]),
            ("Kolik pásky vlastně potřebujete", [
                "Minimální odběr u BOPP pásek začíná na 360 kusech u akrylového lepidla a na 504 kusech "
                "u lepidla HOT MELT. U papírových a BOPET pásek se minimální odběr určuje individuálně "
                "podle potisku.",
                "Při odhadu spotřeby pomáhá vynásobit počet expedovaných zásilek za měsíc délkou pásky "
                "na jednu krabici. Rádi vám s propočtem pomůžeme, stačí napsat, kolik balíků měsíčně posíláte.",
                "Standardní dodací lhůta jsou 3 až 4 týdny od schválení návrhu, takže objednávku je dobré "
                "zadat s předstihem před sezónou.",
            ]),
            ("Udržitelné balení pro e-shop", [
                "Zákazníci si stále častěji všímají, v čem zásilka dorazí. Papírová páska s FSC certifikací "
                "umožňuje recyklovat celou krabici najednou bez odlepování.",
                "Alternativou je řada ECO+ z recyklovaného BOPP, která si zachovává mechanické vlastnosti "
                "standardní pásky, ale využívá regenerát z naší vlastní výroby fólií.",
                "Pro ještě vyšší nároky na udržitelnost nabízíme pásky ecoHIT s evropským patentem, "
                "vyrobené z recyklovaných PET lahví, které vynikají extrémní pevností v tahu "
                "a delším návinem na roli.",
            ]),
            ("Bezpečnost zásilek proti nepozorované manipulaci", [
                "U dražšího zboží se vyplatí bezpečnostní páska Tamper Evident. Při pokusu o odlepení "
                "zanechá na kartonu viditelnou stopu, kterou nelze zamaskovat.",
                "Dobře funguje i běžná páska s hustým potiskem. Jakýkoli zásah naruší tištěný motiv "
                "a při přebírání zásilky je okamžitě patrný.",
                "Pokud fixujete zboží stretch fólií, hodí se lepidlo HOT MELT. Z fólie ho nelze snadno "
                "odlepit, takže případná manipulace zůstane zřetelná.",
            ]),
            ("Sezónní špičky a plánování zásob", [
                "Před Vánoci a při výprodejových akcích spotřeba pásky skokově roste. Protože standardní "
                "dodací lhůta jsou 3 až 4 týdny od schválení návrhu, je dobré objednávat s předstihem.",
                "U opakovaných dodávek se osvědčuje domluvit větší sérii dopředu a odebírat ji postupně. "
                "Jednotková cena klesá a nehrozí, že vám páska dojde uprostřed sezóny.",
                "Pásky skladujte v prostředí o teplotě přibližně 14 až 28 stupňů Celsia, aby si lepidlo "
                "udrželo deklarované vlastnosti.",
            ]),
        ],
        "links": [
            ("/sortiment/bopp-pasky", "BOPP pásky"),
            ("/sortiment/papirove-pasky", "Papírové pásky"),
            ("/pruvodce/hot-melt-vs-akryl", "HOT MELT nebo akryl"),
            ("/cena-pasky-s-potiskem", "Co ovlivňuje cenu"),
        ],
        "schema_type": "WebPage",
    },
    {
        "slug": "pasky-s-logem",
        "nav": "Pásky s logem",
        "h1": "Lepicí pásky s logem na míru",
        "seo_title": "Pásky s logem | Potisk lepicích pásek až 10 barev",
        "description": (
            "Lepicí pásky s vlastním logem. Flexotisk až 8 barev, rototisk až 10 barev, "
            "příprava podkladů, odstíny Pantone a grafický náhled před výrobou."
        ),
        "intro": (
            "Páska s logem je jeden z nejlevnějších brandingových prvků, které firma může nasadit. "
            "Cestuje se zásilkou až k zákazníkovi a zaujme dřív, než krabici vůbec otevře."
        ),
        "sections": [
            ("Co páska s logem přináší", [
                "Potištěná páska plní dvě funkce najednou. Spolehlivě uzavře karton a zároveň nese vaši "
                "značku po celou dobu přepravy.",
                "Na rozdíl od tištěné krabice není vázaná na jeden rozměr obalu. Jednu pásku s logem použijete "
                "na všechny velikosti krabic, které expedujete.",
                "Potisk lze využít i prakticky. Kromě loga se na pásku často tisknou manipulační instrukce, "
                "upozornění na křehký obsah nebo kontakt na reklamační oddělení.",
            ]),
            ("Technologie potisku, které nabízíme", [
                "Flexotisk zvládne až 8 barev a je vhodný pro většinu firemních log a jednodušších motivů. "
                "Jde o osvědčenou a cenově dostupnou technologii pro běžné série.",
                "Rototisk umožňuje potisk až 10 barev včetně kvalitního spodního tisku. Volíme jej tam, "
                "kde je potřeba jemný detail, plynulé přechody nebo velmi sytá plocha.",
                "Počet barev patří mezi hlavní faktory ceny. Dvoubarevné logo na jednobarevném podkladu "
                "vyjde znatelně levněji než plnobarevný motiv přes celou šířku pásky.",
            ]),
            ("Jak připravit podklady", [
                "Nejlépe se pracuje s vektorovým logem ve formátu PDF, AI nebo EPS. Vektor lze zvětšit "
                "na jakoukoli šířku pásky bez ztráty ostrosti.",
                "Pokud má vaše značka definované odstíny Pantone, pošlete je s logem. Tisk podle Pantone "
                "zajistí, že barva na pásce bude odpovídat zbytku vaší vizuální identity.",
                "Nemáte logo ve vektoru? Ozvěte se i tak. Podklady umíme připravit a grafický náhled pásky "
                "vám vždy pošleme ke schválení ještě před zahájením výroby.",
            ]),
            ("Na jaký materiál lze tisknout", [
                "Potisk nabízíme na BOPP pásky, BOPET pásky, papírové pásky a na udržitelnou řadu "
                "z recyklovaných materiálů.",
                "Papírové typy C660, C680, C680R, C680RT a C690 lze potisknout až 4 barvami. BOPP a BOPET "
                "pásky zvládnou plný rozsah barev podle zvolené technologie.",
                "Barvu podkladu i šířku a délku návinu volíte podle svého provozu. Na výběr je i bezpečnostní "
                "provedení Tamper Evident, které při odlepení zanechá viditelnou stopu.",
            ]),
            ("Barva podkladu a čitelnost motivu", [
                "Nejlevnější a zároveň nejčitelnější kombinací bývá tmavé logo na světlém podkladu nebo "
                "naopak. Kontrast rozhoduje o tom, jestli logo přečtete na tři metry, nebo na třicet centimetrů.",
                "Papírové pásky C680 a C680R jsou dostupné také v bílé barvě, která dává potisku čistý "
                "a prémiový základ.",
                "Pamatujte, že páska se na krabici částečně překrývá a ohýbá přes hranu. Motiv proto navrhujte "
                "tak, aby dával smysl i v případě, kdy je jeho část zakrytá.",
            ]),
            ("Nejčastější chyby při návrhu potisku", [
                "Příliš mnoho detailu. Páska je úzký pruh a jemné linky ani drobný text se na něm "
                "neuplatní, zvlášť když se motiv čte za pohybu při odvíjení.",
                "Rastrové logo v nízkém rozlišení. Ze skenu nebo z obrázku z webu nelze udělat ostrý tisk. "
                "Vektorový podklad tento problém řeší úplně.",
                "Opomenutá opakovací rozteč. Motiv se na pásce opakuje, takže je dobré vědět, jak často "
                "se má zopakovat a kolik mezery mezi opakováním chcete.",
            ]),
        ],
        "faqs": [
            ("Kolik barev může mít potisk pásky?",
             "Flexotiskem tiskneme až 8 barev, rototiskem až 10 barev včetně spodního tisku. "
             "Papírové pásky potiskujeme až 4 barvami."),
            ("V jakém formátu poslat logo?",
             "Ideální je vektorový formát PDF, AI nebo EPS. Hodí se také uvést odstíny Pantone, "
             "pokud je vaše značka má definované."),
            ("Uvidím návrh před výrobou?",
             "Ano. Před zahájením výroby vždy posíláme grafický náhled pásky ke schválení."),
        ],
        "links": [
            ("/galerie", "Galerie realizací"),
            ("/sortiment", "Materiály k potisku"),
            ("/cena-pasky-s-potiskem", "Co ovlivňuje cenu"),
            ("/#gf_1", "Nezávazná kalkulace"),
        ],
        "schema_type": "WebPage",
    },
    {
        "slug": "cena-pasky-s-potiskem",
        "nav": "Cena a kalkulace",
        "h1": "Cena pásky s potiskem a co ji ovlivňuje",
        "seo_title": "Cena pásky s potiskem | Co ovlivňuje kalkulaci | ALFA IN",
        "description": (
            "Z čeho se skládá cena pásky s potiskem. Vliv materiálu, počtu barev, šířky návinu "
            "a odebraného množství. Minimální odběr od 360 kusů a nezávazná kalkulace."
        ),
        "intro": (
            "Cena potištěné pásky není pevný ceník. Vzniká vždy kalkulací podle konkrétního zadání, "
            "protože každý z níže uvedených faktorů s ní hýbe. Níže shrnujeme, co cenu tvoří."
        ),
        "sections": [
            ("Z čeho se cena skládá", [
                "Základ tvoří materiál nosiče a typ lepidla. Standardní BOPP je nejúspornější volba, "
                "polyesterové BOPET a papírové pásky s certifikací FSC patří do vyšší cenové kategorie.",
                "Druhým faktorem je potisk. Rozhoduje počet barev, plocha pokrytí a zvolená technologie, "
                "tedy flexotisk nebo rototisk.",
                "Poslední a často nejvýraznější položkou je odebrané množství. S rostoucím počtem rolí "
                "klesá jednotková cena, protože se náklady na přípravu tisku rozloží do větší série.",
            ]),
            ("Minimální odběr", [
                "U BOPP pásek začíná minimální odběr na 360 kusech s akrylovým lepidlem a na 504 kusech "
                "s lepidlem HOT MELT.",
                "U papírových a BOPET pásek se minimální množství stanovuje individuálně podle potisku "
                "a krepové vrstvy.",
                "Pásky dodáváme i bez potisku ve stejné kvalitě. Pokud vám branding zatím nedává smysl, "
                "neutrální varianta bývá cenově výhodnější.",
            ]),
            ("Jak ušetřit, aniž byste slevili z kvality", [
                "Nejsnazší úspora vede přes počet barev. Dvoubarevné logo na základním (bílém, "
                "transparentním nebo hnědém) podkladu je výrazně levnější než plnobarevný motiv "
                "a v praxi bývá stejně dobře viditelné.",
                "Pokud odebíráte pravidelně, vyplatí se domluvit větší sérii s postupným odvoláváním "
                "místo opakovaných malých objednávek.",
            ]),
            ("Jak získat konkrétní cenu", [
                "Pošlete nám požadovaný materiál, šířku a délku návinu, orientační množství rolí a počet "
                "barev potisku. Na základě toho připravíme cenovou nabídku.",
                "Pokud si nejste jistí zadáním, stačí popsat, co balíte a v jakém prostředí. Vhodný materiál "
                "i lepidlo doporučíme sami.",
                "Vzorky materiálů a lepidel ze skladu zasíláme zdarma, takže si kvalitu ověříte ještě "
                "před rozhodnutím.",
            ]),
            ("Cena role versus celkové náklady na balení", [
                "Nejlevnější páska nemusí být nejlevnější řešení. Pokud špatně drží, obsluha ji přelepuje "
                "dvakrát a spotřeba i čas balení rostou.",
                "Podobně se chová páska, která se špatně odvíjí. V balicí hale, kde se denně uzavírají "
                "stovky krabic, se každá vteřina navíc promítne do mzdových nákladů.",
                "Do úvahy patří i reklamace. Prasklá páska na kartonu znamená poškozenou zásilku, nový "
                "obal, novou přepravu a nespokojeného zákazníka.",
            ]),
            ("Kdy se vyplatí páska bez potisku", [
                "Pokud pásku používáte na vnitřní přesuny mezi sklady nebo na obaly, které zákazník nikdy "
                "neuvidí, branding žádnou hodnotu nepřidá a neutrální varianta je levnější.",
                "Naopak u zásilek, které jdou přímo ke koncovému zákazníkovi, bývá potisk jedním "
                "z nejlevnějších a nejlepších reklamních nosičů v poměru k počtu zhlédnutí.",
                "Řada firem kombinuje obojí. Potištěnou pásku nasadí na expedici k zákazníkům a neutrální "
                "na interní logistiku.",
            ]),
        ],
        "faqs": [
            ("Kolik stojí páska s potiskem?",
             "Cenu stanovujeme individuální kalkulací. Ovlivňuje ji materiál, počet barev potisku, "
             "šířka a délka návinu a hlavně odebrané množství. Nezávaznou nabídku připravíme zdarma."),
            ("Jaký je minimální odběr?",
             "U BOPP pásek 360 kusů s akrylovým lepidlem nebo 504 kusů s lepidlem HOT MELT. "
             "U papírových a BOPET pásek se určuje individuálně podle potisku."),
            ("Je páska bez potisku levnější?",
             "Ano. Pásky dodáváme ve stejné kvalitě i bez potisku a minimální odběry jsou v tom případě nižší."),
            ("Platím za grafický návrh?",
             "Grafický náhled pásky připravíme a pošleme ke schválení jako součást přípravy zakázky."),
        ],
        "links": [
            ("/faq", "Časté otázky"),
            ("/sortiment", "Přehled materiálů"),
            ("/pasky-s-logem", "Technologie potisku"),
            ("/#gf_1", "Nezávazná kalkulace"),
        ],
        "schema_type": "WebPage",
    },
    {
        "slug": "srovnani-lepicich-pasek",
        "nav": "Srovnání pásek",
        "h1": "Srovnání lepicích pásek podle materiálu",
        "seo_title": "Srovnání lepicích pásek | Jaký materiál vybrat",
        "description": (
            "Přehledné srovnání lepicích pásek podle materiálu. BOPP, BOPET, papírové, MOPP "
            "a vyztužené pásky, jejich silné stránky a typické použití."
        ),
        "intro": (
            "Materiál nosiče rozhoduje o tom, jak páska drží, kolik unese a jestli půjde recyklovat "
            "spolu s krabicí. Níže najdete přehled všech typů, které vyrábíme, a k čemu se každý hodí."
        ),
        "sections": [
            ("Rychlá orientace", [
                "Balíte běžné zásilky a chcete nejlepší poměr ceny a výkonu, sáhněte po BOPP.",
                "Chcete, aby zákazník vyhodil celou krabici i s páskou do papíru, zvolte papírovou "
                "pásku s certifikací FSC.",
                "Posíláte těžké nebo nadrozměrné zásilky a potřebujete extrémní odolnost proti přetržení, "
                "volte TACK+, Extra glue+ nebo vyztužené pásky.",
                "Fixujete palety a komponenty, kde se nic nesmí povolit, jsou na řadě MOPP pásky.",
                "Plníte ESG cíle a řešíte uhlíkovou stopu balení, podívejte se na udržitelnou řadu "
                "nebo ecoHIT.",
            ]),
            ("BOPP je standard pro většinu provozů", [
                "Biaxiálně orientovaný polypropylen je nejrozšířenější nosič balicích pásek. Nabízí "
                "vynikající poměr ceny a výkonu, dobrou pevnost v tahu a dlouhou životnost.",
                "Dostanete jej v akrylovém i HOT MELT provedení, v široké škále šířek a barev. "
                "Neobsahuje PVC ani jiné látky škodlivé prostředí.",
                "Hodí se na standardní uzavírání kartonů, automatické balicí stroje, expedici "
                "a skladovou logistiku. Pro potisk firemním logem je to nejčastější volba.",
            ]),
            ("Papírové pásky pro plnou recyklovatelnost", [
                "Papírový nosič z pevného kraftu umožňuje recyklovat pásku i karton společně "
                "v jednom kontejneru, bez nutnosti cokoli odlepovat.",
                "Matný papírový povrch působí na zákazníka velmi prémiově. Typy C660, C680, C680R, "
                "C680RT a C690 vyrábíme z papíru FSC Mix Credit a lze je potisknout až 4 barvami.",
                "Papír má vysokou lepivost i na recyklovaný karton a členité povrchy. Nevýhodou je "
                "vyšší cena oproti BOPP a nižší odolnost proti vlhkosti.",
            ]),
            ("BOPET tam, kde běžná páska nestačí", [
                "Polyesterová fólie odolává vysokým i nízkým teplotám, rozpouštědlům, olejům "
                "a agresivnímu chemickému prostředí. Má minimální tažnost a vysokou odolnost proti roztržení.",
                "Praktickou výhodou je dvojnásobný návin role oproti běžné pásce. Obsluha méně často "
                "mění roli a ve skladu zabere zásoba méně místa.",
            ]),
            ("MOPP a vyztužené pásky na fixaci", [
                "MOPP je monoaxiálně orientovaná fólie s extrémní pevností v podélném směru a prakticky "
                "nulovou tažností. Fixace se nepovolí ani při zatížení a páska neobsahuje skelná vlákna.",
                "Vyztužené pásky mají podélná nebo křížová skelná vlákna a nabízejí nejvyšší pevnost "
                "v tahu ze všech typů. Použijete je na zajištění zboží na paletách, svazování trubek "
                "a profilů nebo na náročný export.",
                "Rozdíl je v čistotě. Kde vám vadí uvolňující se skelná vlákna, volte MOPP.",
            ]),
            ("Na co ještě myslet kromě materiálu", [
                "Typ lepidla je stejně důležitý jako nosič. HOT MELT přilne okamžitě a zvládá chlad "
                "i recyklované kartony, akryl je tišší při odvíjení a odolnější vůči UV záření.",
                "Šířku a délku návinu volíte podle svého balicího procesu. Delší návin znamená méně "
                "výměn rolí.",
            ]),
        ],
        "faqs": [
            ("Jaká lepicí páska je nejlepší?",
             "Univerzálně nejlepší páska neexistuje. Pro běžné balení zásilek je nejvýhodnější BOPP, "
             "pro plně recyklovatelné balení papírová páska s FSC certifikací a pro těžké nebo náročné "
             "aplikace BOPET či vyztužené pásky."),
            ("Je papírová páska stejně pevná jako BOPP?",
             "Papírová páska má vysokou lepivost a pro běžné zásilky je zcela dostačující. BOPP ale "
             "lépe odolává vlhkosti a u velmi těžkých balíků je spolehlivější."),
            ("Kterou pásku zvolit na recyklovaný karton?",
             "Rozhoduje spíš lepidlo než nosič. Nejlépe drží HOT MELT s vysokou počáteční přilnavostí, "
             "u obzvlášť hrubých kartonů varianta se zvýšenou vrstvou lepidla."),
        ],
        "links": [
            ("/sortiment", "Kompletní sortiment"),
            ("/pruvodce/hot-melt-vs-akryl", "HOT MELT nebo akryl"),
            ("/pruvodce/paska-na-recyklovany-karton", "Páska na recyklovaný karton"),
            ("/cena-pasky-s-potiskem", "Co ovlivňuje cenu"),
        ],
        "schema_type": "WebPage",
    },
    {
        "slug": "bezpecnostni-pasky-proti-kradezi",
        "nav": "Bezpečnostní pásky",
        "h1": "Bezpečnostní pásky proti krádeži zásilek",
        "seo_title": "Bezpečnostní pásky proti krádeži | Tamper Evident",
        "description": (
            "Bezpečnostní pásky Tamper Evident s potiskem. Při odlepení zanechají viditelnou stopu, "
            "takže neoprávněné otevření zásilky nelze zamaskovat. Ochrana cenného zboží."
        ),
        "intro": (
            "Pokud posíláte cenné zboží, potřebujete poznat, jestli s balíkem někdo manipuloval. "
            "Bezpečnostní páska Tamper Evident to řeší tak, že po pokusu o odlepení zůstane na kartonu "
            "trvalá viditelná stopa, kterou nelze vrátit do původního stavu."
        ),
        "sections": [
            ("Jak Tamper Evident funguje", [
                "Páska je konstruovaná tak, aby se při odlepení nevrátila zpět. Na kartonu zůstane "
                "zřetelný otisk a samotná páska se znehodnotí, takže ji nelze znovu nalepit.",
                "Příjemce i dopravce tak vidí na první pohled, zda byla zásilka otevřena. To zásadně "
                "mění situaci při reklamaci, protože máte důkaz, ve které fázi přepravy k zásahu došlo.",
                "Preventivní efekt bývá stejně důležitý jako důkazní. Zásilka, na které je zjevně "
                "bezpečnostní páska, je pro příležitostnou krádež mnohem méně atraktivní.",
            ]),
            ("Kdy se vyplatí", [
                "U elektroniky, mobilních telefonů a dalšího drobného zboží s vysokou hodnotou, "
                "které se snadno odcizí a špatně dohledá.",
                "U zásilek, které procházejí více překladišti nebo jdou do zahraničí. Čím delší "
                "přepravní řetězec, tím víc rukou se zásilky dotkne.",
                "U léčiv, zdravotnického materiálu a všude, kde potřebujete doložit neporušenost "
                "obalu kvůli předpisům nebo auditu.",
                "U reklamačních sporů s dopravci, kde je potřeba prokázat, že zboží bylo odesláno kompletní.",
            ]),
            ("Levnější alternativy, které také fungují", [
                "Pokud plná bezpečnostní páska není v rozpočtu, hodně pomůže i běžná páska s hustým "
                "vlastním potiskem. Jakýkoli zásah naruší tištěný motiv a je při přebírání dobře patrný.",
                "Zároveň se taková páska prakticky nedá nahradit. Útočník by musel mít roli s vaším "
                "konkrétním potiskem, což u cílené krádeže výrazně zvyšuje laťku.",
                "Pokud fixujete zboží stretch fólií, volte lepidlo HOT MELT. Z fólie ho nelze snadno "
                "odlepit, takže případná manipulace zůstane zřetelná.",
            ]),
            ("Jak to zkombinovat s brandingem", [
                "Bezpečnostní pásku lze potisknout stejně jako běžnou. Nemusíte tedy volit mezi ochranou "
                "zásilky a viditelností značky.",
                "Osvědčuje se kombinovat logo s textem, který upozorní na zabezpečení. Příjemce pak ví, "
                "že má obal při převzetí zkontrolovat, a preventivní efekt roste.",
                "Potisk zvládneme flexotiskem až v 8 barvách nebo rototiskem až v 10 barvách. Grafický "
                "náhled vždy posíláme ke schválení před výrobou.",
            ]),
        ],
        "faqs": [
            ("Co je Tamper Evident páska?",
             "Bezpečnostní lepicí páska, která po odlepení zanechá na kartonu viditelnou trvalou stopu "
             "a sama se znehodnotí. Neoprávněné otevření zásilky proto nelze zamaskovat."),
            ("Lze bezpečnostní pásku potisknout logem?",
             "Ano. Bezpečnostní pásku potiskujeme stejně jako běžnou, flexotiskem až v 8 barvách "
             "nebo rototiskem až v 10 barvách."),
            ("Stačí místo ní obyčejná páska s potiskem?",
             "U méně rizikových zásilek často ano. Hustý vlastní potisk se při zásahu naruší a útočník "
             "by musel mít roli s vaším konkrétním motivem. U cenného zboží ale doporučujeme Tamper Evident."),
        ],
        "links": [
            ("/sortiment/bopp-pasky/bopp-paska-tamper-evident", "Páska Tamper Evident"),
            ("/pruvodce/bezpecnostni-tamper-evident", "Jak Tamper Evident funguje"),
            ("/pasky-s-logem", "Potisk pásek"),
            ("/#gf_1", "Nezávazná kalkulace"),
        ],
        "schema_type": "WebPage",
    },
    {
        "slug": "vyroba-lepicich-pasek",
        "nav": "Výroba",
        "h1": "Výroba lepicích pásek na míru",
        "seo_title": "Výroba lepicích pásek | Český výrobce pásek na míru",
        "description": (
            "Jak vzniká lepicí páska na míru. Vlastní výroba BOPP fólií, nanášení lepidla, "
            "potisk až 10 barev, řezání návinu a výstupní kontrola podle ISO 9001."
        ),
        "intro": (
            "Lepicí pásky vyrábíme v Nové Vsi u Třebíče více než 30 let. Na rozdíl od většiny dodavatelů "
            "si vyrábíme i samotné fólie, ze kterých pásky vznikají."
        ),
        "sections": [
            ("Začínáme u vlastní fólie", [
                "Nevyrábíme pouze pásky, ale i BOPP fólie, které slouží jako nosič. Díky tomu nejsme "
                "závislí na externích dodavatelích nosiče a snáz ustojíme surovinové výkyvy na trhu.",
                "Z vlastní výroby fólií vzniká také postindustriální regenerát, který dále používáme "
                "v udržitelné řadě ECO+. Materiál tak zůstává v oběhu místo toho, aby skončil jako odpad.",
            ]),
            ("Nanášení lepidla", [
                "Podle určení pásky nanášíme buď akrylátovou disperzi na vodní bázi, nebo lepidlo HOT MELT "
                "na bázi syntetického kaučuku.",
                "Ani jedna technologie nepoužívá rozpouštědla. Lepidla proto neuvolňují toxické výpary "
                "a jsou bezpečná pro pracovníky, kteří s páskou manipulují celý den.",
                "Tloušťku vrstvy lepidla přizpůsobujeme účelu. Pro náročné a členité povrchy nabízíme "
                "provedení se zvýšenou vrstvou lepidla.",
            ]),
            ("Potisk podle zadání", [
                "Potisk zajišťujeme flexotiskem až v 8 barvách nebo rototiskem až v 10 barvách včetně "
                "kvalitního spodního tisku.",
                "Před zahájením výroby vždy připravíme grafický náhled a odešleme jej ke schválení. "
                "Do výroby jde až podoba, kterou jste potvrdili.",
            ]),
            ("Řezání, návin a kontrola", [
                "Hotový materiál řežeme na požadovanou šířku a navíjíme na zvolenou délku role. Šířku "
                "i návin volíte podle svého balicího procesu, ať už balíte ručně nebo na automatické lince.",
                "Výroba probíhá podle certifikovaných procesů ISO 9001. Papírové pásky navíc vyrábíme "
                "z papíru FSC Mix Credit pod licencí FSC-C159046.",
                "Standardní dodací lhůta je 3 až 4 týdny od schválení grafického návrhu a potvrzení "
                "objednávky. U urgentních zakázek se snažíme dodání urychlit.",
            ]),
            ("Materiály, které zpracováváme", [
                "Nejčastějším nosičem je BOPP, tedy biaxiálně orientovaný polypropylen. Nabízí nejlepší "
                "poměr ceny a pevnosti pro každodenní balení.",
                "Polyesterový BOPET používáme tam, kde běžná páska nestačí. Odolává vysokým i nízkým teplotám, "
                "chemikáliím a mechanickému namáhání a umožňuje dvojnásobný návin role.",
                "Papírový nosič z pevného kraftu volíme pro plně recyklovatelné balení. Páska putuje "
                "do sběru společně s kartonem bez nutnosti odlepování.",
                "Dále zpracováváme monoaxiálně orientovaný MOPP pro pevnou fixaci, textilní nosiče "
                "pro univerzální použití a krepový papír pro malířské pásky.",
            ]),
            ("Co u pásky sledujeme", [
                "Přilnavost k oceli vypovídá o okamžité lepivosti na hladký povrch. U papírových pásek "
                "se běžný standard pohybuje mezi 4,0 a 5,0 N na centimetr, hodnoty nad 6,0 N na centimetr "
                "znamenají extra silnou lepivost.",
                "Pevnost v tahu ukazuje odolnost proti přetržení. Pro běžné balíky do zhruba 15 kilogramů "
                "stačí 30 až 40 N na centimetr, u těžkých zásilek a výztuh jde o 50 N na centimetr a více.",
                "Tažnost udává, o kolik procent se páska natáhne, než praskne. U papírových pásek je "
                "standardem 8 až 12 procent, přičemž nízká tažnost okolo 5 procent drží krabici pevně bez průhybu.",
            ]),
        ],
        "links": [
            ("/o-nas", "O výrobci"),
            ("/sortiment", "Co vyrábíme"),
            ("/pruvodce", "Průvodce výběrem"),
            ("/kontakt", "Kontakty"),
        ],
        "schema_type": "WebPage",
    },
]

ARROW = ('<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" '
         'stroke-width="2" aria-hidden="true"><path stroke-linecap="round" '
         'stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>')


def load_chrome() -> tuple[str, str]:
    """Prevezme hlavicku a paticku ze sortiment.html, aby vzhled zustal jednotny."""
    base = (ROOT / "sortiment.html").read_text(encoding="utf-8")
    start = base.index("<!-- SITE-TOP -->")
    end = base.index("<!-- /SITE-TOP -->") + len("<!-- /SITE-TOP -->")
    header = (
        base[: base.index("</head>") + len("</head>")]
        + base[base.index("<body") : start]
        + base[start:end]
    )
    # Hlavicka pochazi ze sortimentu a nese data-page="sortiment". Bez zmeny by
    # i18n tyto stranky povazoval za sortiment a prepsal jim <title>,
    # nav-active by navic zvyraznil polozku Sortiment.
    header = header.replace('data-page="sortiment"', 'data-page="landing"', 1)
    # Hlavicka ze sortimentu ma polozku Sortiment natvrdo zvyraznenou.
    # Na samostatnych strankach by zustala oranzova, proto ji vratime do klidu.
    header = header.replace(
        '<a href="/sortiment" class="px-2 py-1 text-sm font-semibold text-orange-600 '
        'transition-colors hover:text-orange-600"',
        '<a href="/sortiment" class="px-2 py-1 text-sm font-semibold text-slate-700 '
        'transition-colors hover:text-orange-600"',
        1,
    )
    header = header.replace(
        '<a href="/sortiment" class="block px-2 py-2 font-semibold text-orange-600"',
        '<a href="/sortiment" class="block px-2 py-2 font-semibold text-slate-800"',
        1,
    )
    footer = base[base.index('<footer id="kontakt1"'):]
    return header, footer


def render_block(block) -> str:
    """Render one section body block: plain string or structured dict."""
    if isinstance(block, str):
        return (
            f'            <p class="mt-3 text-base leading-relaxed text-slate-600">'
            f'{esc(block)}</p>'
        )

    kind = block["type"]
    if kind == "h3p":
        return (
            f'            <h3 class="mt-6 text-base font-bold text-slate-900">{esc(block["h3"])}</h3>\n'
            f'            <p class="mt-2 text-base leading-relaxed text-slate-600">{esc(block["p"])}</p>'
        )
    if kind == "person":
        return (
            '                <div>\n'
            f'                    <p class="text-base font-bold text-slate-900">{esc(block["name"])}</p>\n'
            f'                    <p class="mt-1 text-base leading-relaxed text-slate-600">'
            f'Telefon: <a href="{esc(block["phone_href"])}" class="font-semibold text-orange-700 '
            f'hover:text-orange-600">{esc(block["phone"])}</a> | E-mail: '
            f'<a href="mailto:{esc(block["email"])}" class="font-semibold text-orange-700 '
            f'hover:text-orange-600">{esc(block["email"])}</a></p>\n'
            '                </div>'
        )
    if kind == "labeled":
        return (
            f'                <p class="text-base leading-relaxed text-slate-600">'
            f'<span class="font-bold text-slate-900">{esc(block["label"])}</span> '
            f'{esc(block["text"])}</p>'
        )
    if kind == "p_strong_start":
        return (
            f'            <p class="mt-3 text-base leading-relaxed text-slate-600">'
            f'<strong class="font-bold text-slate-900">{esc(block["strong"])}</strong>'
            f'{esc(block["text"])}</p>'
        )
    if kind == "italic":
        return (
            f'            <p class="mt-4 text-base italic leading-relaxed text-slate-600">'
            f'{esc(block["text"])}</p>'
        )
    if kind in ("ul", "ol"):
        tag = kind
        list_style = "disc" if tag == "ul" else "decimal"
        items = []
        for label, text in block["items"]:
            items.append(
                f'                <li><strong class="font-bold text-slate-900">{esc(label)}</strong> '
                f'{esc(text)}</li>'
            )
        return (
            f'            <{tag} class="mt-4 list-{list_style} '
            f'space-y-3 pl-5 text-base leading-relaxed text-slate-600">\n'
            + "\n".join(items)
            + f'\n            </{tag}>'
        )
    raise ValueError(f"Unknown block type: {kind}")


def render_section_body(blocks: list) -> str:
    """Wrap person/labeled blocks in a contact stack; otherwise render sequentially."""
    if blocks and isinstance(blocks[0], dict) and blocks[0].get("type") in ("person", "labeled"):
        inner = "\n".join(render_block(b) for b in blocks)
        return f'            <div class="mt-4 space-y-5">\n{inner}\n            </div>'
    return "\n".join(render_block(b) for b in blocks)


def render_intro(pg: dict) -> str:
    parts = []
    if pg.get("intro_lead"):
        parts.append(
            f'    <p class="mt-4 text-lg font-semibold leading-relaxed text-slate-800">'
            f'{esc(pg["intro_lead"])}</p>'
        )
        intro_cls = "mt-3"
    else:
        intro_cls = "mt-4"

    if pg.get("intro_parts"):
        chunks = []
        for part in pg["intro_parts"]:
            if isinstance(part, tuple) and part[0] == "strong":
                chunks.append(
                    f'<strong class="font-semibold text-slate-800">{esc(part[1])}</strong>'
                )
            else:
                chunks.append(esc(part))
        parts.append(
            f'    <p class="{intro_cls} text-lg leading-relaxed text-slate-600">'
            f'{"".join(chunks)}</p>'
        )
    elif pg.get("intro"):
        parts.append(
            f'    <p class="{intro_cls} text-lg leading-relaxed text-slate-600">'
            f'{esc(pg["intro"])}</p>'
        )
    return "\n".join(parts)


def render_main(pg: dict) -> str:
    sections = []
    for title, blocks in pg["sections"]:
        body = render_section_body(blocks)
        sections.append(
            f'''        <section class="mt-10">
            <h2 class="text-2xl font-extrabold tracking-tight text-slate-900">{esc(title)}</h2>
{body}
        </section>'''
        )

    faq_html = ""
    if pg.get("faqs"):
        items = "\n".join(
            f'''            <div class="mt-6 rounded-2xl border border-slate-100 bg-white p-6 shadow-sm">
                <h3 class="text-base font-bold text-slate-900">{esc(q)}</h3>
                <p class="mt-2 text-base leading-relaxed text-slate-600">{esc(a)}</p>
            </div>'''
            for q, a in pg["faqs"]
        )
        faq_html = f'''        <section class="mt-12">
            <h2 class="text-2xl font-extrabold tracking-tight text-slate-900">Časté otázky</h2>
{items}
        </section>'''

    links = "\n".join(
        f'''            <a href="{esc(href)}" class="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-orange-200 hover:text-orange-700">
                {esc(label)} {ARROW}
            </a>'''
        for href, label in pg["links"]
    )

    cta = pg.get("cta") or {
        "title": "Nezávazná kalkulace zdarma",
        "text": (
            "Napište nám, co balíte, a my doporučíme vhodný materiál i lepidlo. "
            "Vzorky ze skladu posíláme zdarma."
        ),
        "button": "Chci kalkulaci",
        "href": "/#gf_1",
    }

    return f'''

<main>

<section class="mx-auto max-w-4xl px-4 py-12 sm:py-16">
    <nav class="mb-6 text-sm text-slate-500" aria-label="Drobečková navigace">
        <a href="/" class="hover:text-orange-600">Domů</a>
        <span class="mx-2 text-slate-300">/</span>
        <span class="font-semibold text-orange-600">{esc(pg["nav"])}</span>
    </nav>

    <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">{esc(pg["h1"])}</h1>
{render_intro(pg)}

{chr(10).join(sections)}

{faq_html}

    <section class="mt-12 rounded-3xl border border-slate-100 bg-slate-50 p-7 sm:p-9">
        <h2 class="text-xl font-extrabold tracking-tight text-slate-900">Kam dál</h2>
        <div class="mt-5 flex flex-wrap gap-3">
{links}
        </div>
    </section>

    <section class="mt-10 rounded-3xl bg-gradient-to-r from-orange-600 to-amber-500 p-8 text-center shadow-lg sm:p-10">
        <h2 class="text-2xl font-extrabold tracking-tight text-white">{esc(cta["title"])}</h2>
        <p class="mx-auto mt-3 max-w-xl text-base leading-relaxed text-orange-50">{esc(cta["text"])}</p>
        <a href="{esc(cta["href"])}" class="mt-6 inline-flex items-center gap-2 rounded-2xl bg-white px-8 py-3.5 text-sm font-bold text-orange-700 shadow-md transition-all hover:scale-[1.02]">{esc(cta["button"])} {ARROW}</a>
    </section>

</section>

</main>

'''


def page_schemas(pg: dict) -> list:
    path = "/" + pg["slug"]
    schemas = [
        breadcrumb_schema([("/", "Domů"), (path, pg["nav"])]),
    ]
    if pg.get("faqs"):
        schemas.append(faq_schema(pg["faqs"]))
    return schemas


NOT_FOUND_LINKS = [
    ("/sortiment", "Kompletní sortiment pásek"),
    ("/srovnani-lepicich-pasek", "Srovnání pásek"),
    ("/pasky-s-logem", "Pásky s logem"),
    ("/cena-pasky-s-potiskem", "Cena a kalkulace"),
    ("/pruvodce", "Průvodce výběrem"),
    ("/kontakt", "Kontakt"),
]

_NF_LINK = (
    '            <a href="{href}" class="inline-flex items-center gap-1.5 rounded-full '
    'border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 '
    'transition hover:border-orange-200 hover:text-orange-700">\n'
    '                {label} {arrow}\n'
    '            </a>'
)


def render_not_found() -> str:
    """Vlastni 404. Vercel ji u statickeho webu servíruje z korenoveho 404.html."""
    links = "\n".join(
        _NF_LINK.format(href=esc(href), label=esc(label), arrow=ARROW)
        for href, label in NOT_FOUND_LINKS
    )
    return (
        '\n\n<main>\n\n'
        '<section class="mx-auto max-w-3xl px-4 py-20 text-center sm:py-28">\n'
        '    <p class="text-sm font-bold uppercase tracking-widest text-orange-600">Chyba 404</p>\n'
        '    <h1 class="mt-3 text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">'
        'Tuhle stránku jsme nenašli</h1>\n'
        '    <p class="mx-auto mt-4 max-w-xl text-lg leading-relaxed text-slate-600">'
        'Adresa možná zanikla nebo je v ní překlep. Zkuste některý z odkazů níže, '
        'nebo nám rovnou napište a poradíme s výběrem pásky.</p>\n'
        '    <div class="mt-9 flex flex-wrap justify-center gap-3">\n'
        f'{links}\n'
        '    </div>\n'
        '    <a href="/#gf_1" class="mt-10 inline-flex items-center gap-2 rounded-2xl '
        'bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3.5 text-sm font-bold text-white '
        'shadow-lg shadow-orange-600/25 transition-all hover:scale-[1.02]">'
        f'Nezávazná kalkulace {ARROW}</a>\n'
        '</section>\n\n'
        '</main>\n\n'
    )


def main() -> None:
    os.chdir(ROOT)
    print("Generating landing pages…")
    header, footer = load_chrome()
    for pg in PAGES:
        doc = header + render_main(pg) + footer
        doc = apply_page_seo(
            doc,
            title=pg["seo_title"],
            description=pg["description"],
            path="/" + pg["slug"],
            schemas=page_schemas(pg),
        )
        out = ROOT / pg["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc, encoding="utf-8")
        print(f"  wrote {out.relative_to(ROOT)}")

    # 404 nesmi byt indexovana, ale ma nabidnout cestu zpatky do webu.
    nf = header + render_not_found() + footer
    nf = apply_page_seo(
        nf,
        title="Stránka nenalezena | Pásky s potiskem",
        description=(
            "Požadovaná stránka neexistuje. Přejděte na sortiment lepicích pásek "
            "s potiskem nebo nám napište."
        ),
        path="/404",
        schemas=[],
    )
    nf = nf.replace(
        '<meta name="robots" content="index, follow">',
        '<meta name="robots" content="noindex, follow">',
        1,
    )
    (ROOT / "404.html").write_text(nf, encoding="utf-8")
    print("  wrote 404.html")


if __name__ == "__main__":
    main()
