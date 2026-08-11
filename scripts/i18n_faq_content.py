#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAQ page UI copy + Q&A translations (CS / EN / DE / IT)."""

from __future__ import annotations

from typing import Any

# Shared structure: each language fills faq.* including items keyed by data-id.


def _items_cs() -> dict[str, dict[str, str]]:
    return {
        "moq": {
            "q": "Jaké je minimální množství objednávky?",
            "a": "U BOPP pásek 360 ks (Akryl) nebo 504 ks (HOT MELT); u papírových a BOPET pásek závisí minimální odběr individuálně na potisku a krepové vrstvě.",
            "search": "minimum moq odběr množství kusy objednávka bopp hot melt akryl",
        },
        "lead-time": {
            "q": "Jak dlouho trvá výroba pásky s potiskem?",
            "a": "Standardní dodací lhůta je 3 až 4 týdny od schválení grafického návrhu a objednávky. U urgentních zakázek se snažíme dodání urychlit.",
            "search": "dodací lhůta výroba termín týdny urgentní expedice",
        },
        "bez-potisku": {
            "q": "Mohu objednat pásku i bez potisku?",
            "a": "Ano. Pásky dodáváme ve stejné kvalitě i bez potisku, ideální pro skladové zásoby nebo okamžité balení.",
            "search": "bez potisku nepotištěná neutrální páska",
        },
        "lepidlo": {
            "q": "Jaký je rozdíl mezi HOT MELT a Akryl?",
            "a": 'HOT MELT rychle a pevně přilne i v chladu, vhodný do skladů a expedice. Akryl je tišší při odvíjení a odolnější vůči UV, ideální pro dlouhodobé skladování. Více v sekci <a href="/#lepidla">Jaké lepidlo zvolit?</a>.',
            "search": "hot melt akryl lepidlo přilnavost uv tiché odvíjení sklad",
        },
        "vzorky": {
            "q": "Dodáváte vzorky zdarma?",
            "a": "Fyzický vzorek s vaším potiskem nevyrábíme. Rádi vám však zdarma zašleme vzorky materiálů a lepidel, které máme skladem z předchozích realizací. Snadno si tak ještě před objednávkou otestujete kvalitu pásky i její lepivost na vašich kartonech.",
            "search": "vzorek zdarma materiál lepidlo testování trial sample",
        },
        "technologie": {
            "q": "Jaké technologie potisku nabízíte?",
            "a": "Flexotisk až 8 barev a rototisk až 10 barev včetně kvalitního spodního tisku. Vhodnou technologii doporučíme podle nároku na barvy, množství a požadovanou kvalitu tisku.",
            "search": "flexotisk rototisk barvy tisk technologie spodní tisk",
        },
        "grafika": {
            "q": "Připravíte grafický návrh za mě?",
            "a": "Ano. Potřebujeme vaše logo (ideálně ve vektorovém formátu PDF, AI nebo EPS), případně text a představu o barevnosti (přesné odstíny PANTONE). Před samotnou výrobou vám pošleme grafický náhled ke schválení.",
            "search": "grafika návrh logo náhled design pdf ai eps pantone",
        },
        "sirka": {
            "q": "Jaké šířky a délky pásek vyrábíte?",
            "a": "Dodáváme širokou škálu rozměrů pro ruční i strojní balení. Standardní šířky: 25 mm, 38 mm, 50 mm, 75 mm a 100 mm. Náviny pro ruční balení: 66 m, 100 m, 132 m a 180 m. Strojní náviny (pro balicí linky): 330 m, 660 m, 990 m a 1000 m.",
            "search": "šířka délka 25 38 50 75 100 mm 66 132 180 330 660 990 1000 role navíjení",
        },
        "eko": {
            "q": "Máte udržitelné / ECO pásky?",
            "a": "Ano, řada ECO+ (recyklovaný BOPP), papírové pásky a další udržitelné varianty. Podrobnosti najdete v sortimentu Udržitelné pásky.",
            "search": "eco eko recyklace udržitelná papírová fsc cirkulární",
        },
        "stroje": {
            "q": "Hodí se pásky i na strojní balení?",
            "a": "Ano. Podle lepidla a materiálu doporučíme variantu pro ruční odvíjení nebo pro stohovací / automatické balicí linky.",
            "search": "strojní automatizace linka odvíjení dispenser",
        },
        "doprava": {
            "q": "Jak probíhá doprava a fakturace?",
            "a": "Dodáváme po celé ČR i do zahraničí. Podmínky dopravy a splatnosti upřesníme v nabídce podle objemu a místa doručení.",
            "search": "doprava fakturace dodání čr eu cena",
        },
        "skladovani": {
            "q": "Jak pásky správně skladovat?",
            "a": "Ideálně v suchu, mimo přímé slunce, při běžné pokojové teplotě. Akrylové pásky lépe snášejí delší skladování; HOT MELT doporučujeme spotřebovat dříve při intenzivním používání.",
            "search": "skladování teplota vlhkost životnost",
        },
        "opakovat": {
            "q": "Mohu zopakovat objednávku se stejným potiskem?",
            "a": "Ano. Všechny schválené tiskové matrice ukládáme do archivu. Další objednávka se stejným designem tak proběhne okamžitě bez nového schvalování.",
            "search": "opakovaná objednávka reprint stejná grafika matrice archiv",
        },
        "matrice": {
            "q": "Platí se tisková matrice i při opakované objednávce?",
            "a": "Ne. Schválenou tiskovou matrici pro vás uschováváme. Opakovaná výroba se stejným grafickým návrhem probíhá automaticky a bez dalších poplatků za přípravu.",
            "search": "tisková matrice poplatek opakovaná objednávka archiv forma",
        },
        "cena": {
            "q": "Od čeho se odvíjí cena pásky s potiskem?",
            "a": "Cenu ovlivňuje materiál, lepidlo, šířka a délka role, počet barev, technologie tisku a celkový objem. Pošlete poptávku a připravíme konkrétní nabídku.",
            "search": "cena nabídka kalkulace cena za kus",
        },
        "papir-vs-bopp": {
            "q": "Kdy zvolit papírovou pásku místo BOPP?",
            "a": "Papírová páska se hodí pro eko balení, recyklovatelné kartony a brand, kde chcete přírodní vzhled. BOPP je odolnější vůči vlhkosti a často výhodnější při vyšších objemech. Rádi doporučíme podle vašeho procesu.",
            "search": "papírová bopp plast eko karton",
        },
        "bezpecnostni": {
            "q": "Umíte bezpečnostní nebo výstražné pásky?",
            "a": "Ano, potisk varování, Fragile, Vorsicht Glas, VOID / tamper-evident a logistické texty. Návrh připravíme podle vašich instrukcí a jazykových mutací.",
            "search": "bezpečnostní void tamper výstražná fragile",
        },
        "zmena-grafiky": {
            "q": "Co když potřebuji upravit grafiku po schválení?",
            "a": "Dokud nezačne výroba tiskových forem / tisk, změny obvykle stihneme. Po spuštění výroby už úpravy nemusí být možné bez nových nákladů a termínu, proto si náhled pečlivě zkontrolujte.",
            "search": "změna grafiky korekce schválení",
        },
        "jadro": {
            "q": "Jaké jádro / dutinku pásky používáte?",
            "a": "Standardně dodáváme role s běžnou papírovou dutinkou vhodnou pro ruční i strojní odvíječe. Pro naplnění udržitelných a ESG cílů dodáváme také pásky osazené dutinkou z recyklovaného papíru.",
            "search": "jádro dutinka core průměr recyklovaný esg",
        },
        "zahranici": {
            "q": "Dodáváte i mimo Českou republiku?",
            "a": "Ano. Zásilky posíláme do EU i dále, dopravu a podmínky domluvíme podle destinace a objemu.",
            "search": "zahraničí eu export dodání",
        },
        "odstranitelna": {
            "q": "Máte pásky, které jdou čistě odstranit?",
            "a": "Ano, odstranitelné (removable) pásky vhodné tam, kde nechcete zanechat zbytky lepidla. Doporučíme vhodný typ podle povrchu. Více v sortimentu Odstranitelné pásky.",
            "search": "odstranitelná removable clean remove lepidlo",
        },
        "vice-jazyku": {
            "q": "Můžu mít na pásce text ve více jazycích?",
            "a": "Ano. Často kombinujeme logo s logistickými texty v češtině, němčině, angličtině i dalších jazycích, návrh připravíme tak, aby byl čitelný i při opakování po délce pásky.",
            "search": "jazyky mutace text multilingual",
        },
        "prilnavost": {
            "q": "Co znamená přilnavost k oceli?",
            "a": "Udává, jak silně páska přilne k povrchu ihned po nalepení. Vyšší hodnota znamená, že páska pevněji drží na kartonu a nehrozí její samovolné odlepování.",
            "search": "přilnavost adhesion tack ocel karton lepivost",
        },
        "pevnost-tahu": {
            "q": "Co znamená pevnost v tahu?",
            "a": "Měří mechanickou odolnost pásky vůči prasknutí při silném napnutí. Vyšší číslo zaručuje, že se páska nepřetrhne při balení náročných nebo těžkých zásilek.",
            "search": "pevnost tah tensile strength prasknutí odolnost",
        },
        "taznost": {
            "q": "Co znamená tažnost / prodloužení?",
            "a": "Procentuální hodnota udává, o kolik se páska dokáže natáhnout, než praskne. Nízká tažnost drží krabici pevně a bez průhybu, vyšší tažnost umožňuje pásce lépe tlumit rázy při přepravě.",
            "search": "tažnost prodloužení elongation stretch natažení",
        },
    }


def _items_en() -> dict[str, dict[str, str]]:
    return {
        "moq": {
            "q": "What is the minimum order quantity?",
            "a": "For BOPP tapes 360 pcs (Acrylic) or 504 pcs (HOT MELT); for paper and BOPET tapes the minimum depends individually on the print and crepe layer.",
            "search": "minimum moq quantity order bopp hot melt acrylic",
        },
        "lead-time": {
            "q": "How long does it take to produce printed tape?",
            "a": "The standard lead time is 3 to 4 weeks from approval of the artwork and order. For urgent jobs we try to speed up delivery.",
            "search": "lead time production weeks urgent shipping",
        },
        "bez-potisku": {
            "q": "Can I order tape without printing?",
            "a": "Yes. We supply the same quality tapes without print, ideal for stock or immediate packaging.",
            "search": "unprinted plain neutral tape without print",
        },
        "lepidlo": {
            "q": "What is the difference between HOT MELT and Acrylic?",
            "a": 'HOT MELT bonds quickly and firmly even in the cold, ideal for warehouses and dispatch. Acrylic is quieter when unwinding and more UV-resistant, ideal for longer storage. More in <a href="/#lepidla">Which adhesive to choose?</a>.',
            "search": "hot melt acrylic adhesive tack uv quiet unwind warehouse",
        },
        "vzorky": {
            "q": "Do you provide free samples?",
            "a": "We do not produce a physical sample with your print. We are happy to send free samples of materials and adhesives we keep from previous jobs, so you can test tape quality and adhesion on your cartons before ordering.",
            "search": "sample free material adhesive trial testing",
        },
        "technologie": {
            "q": "Which print technologies do you offer?",
            "a": "Flexo print up to 8 colours and rotogravure up to 10 colours including high-quality reverse print. We recommend the right technology based on colours, volume and print quality needs.",
            "search": "flexo rotogravure colours print technology reverse print",
        },
        "grafika": {
            "q": "Will you prepare the artwork for me?",
            "a": "Yes. We need your logo (ideally vector PDF, AI or EPS), optional text and colour idea (exact Pantone shades). Before production we send a graphic preview for approval.",
            "search": "artwork design logo preview pdf ai eps pantone",
        },
        "sirka": {
            "q": "What tape widths and lengths do you make?",
            "a": "We supply a wide range of sizes for hand and machine packing. Standard widths: 25 mm, 38 mm, 50 mm, 75 mm and 100 mm. Hand-roll lengths: 66 m, 100 m, 132 m and 180 m. Machine lengths (packing lines): 330 m, 660 m, 990 m and 1000 m.",
            "search": "width length 25 38 50 75 100 mm 66 132 180 330 660 990 1000 roll winding",
        },
        "eko": {
            "q": "Do you offer sustainable / ECO tapes?",
            "a": "Yes, the ECO+ range (recycled BOPP), paper tapes and other sustainable options. Details are in the Sustainable tapes assortment.",
            "search": "eco recycled sustainable paper fsc circular",
        },
        "stroje": {
            "q": "Are the tapes suitable for machine packing?",
            "a": "Yes. Based on adhesive and material we recommend a variant for hand dispensers or for automatic packing lines.",
            "search": "machine automatic line unwind dispenser",
        },
        "doprava": {
            "q": "How do shipping and invoicing work?",
            "a": "We deliver across Czechia and abroad. Shipping and payment terms are confirmed in the quote based on volume and destination.",
            "search": "shipping invoicing delivery czech eu price",
        },
        "skladovani": {
            "q": "How should tapes be stored?",
            "a": "Ideally dry, away from direct sun, at normal room temperature. Acrylic tapes handle longer storage better; with intensive use we recommend consuming HOT MELT sooner.",
            "search": "storage temperature humidity shelf life",
        },
        "opakovat": {
            "q": "Can I reorder with the same print?",
            "a": "Yes. We archive all approved printing plates. A repeat order with the same design can therefore proceed immediately without a new approval round.",
            "search": "repeat order reprint same artwork plate archive",
        },
        "matrice": {
            "q": "Do I pay for the printing plate again on a repeat order?",
            "a": "No. We keep your approved printing plate. Repeat production with the same artwork runs automatically with no further prep fees.",
            "search": "printing plate fee repeat order archive forme",
        },
        "cena": {
            "q": "What affects the price of printed tape?",
            "a": "Price depends on material, adhesive, roll width and length, number of colours, print technology and total volume. Send an inquiry and we will prepare a concrete quote.",
            "search": "price quote calculation cost per roll",
        },
        "papir-vs-bopp": {
            "q": "When should I choose paper tape instead of BOPP?",
            "a": "Paper tape suits eco packaging, recyclable cartons and brands that want a natural look. BOPP resists moisture better and is often more cost-effective at higher volumes. We are happy to advise for your process.",
            "search": "paper bopp plastic eco carton",
        },
        "bezpecnostni": {
            "q": "Can you make security or warning tapes?",
            "a": "Yes, warning prints, Fragile, Vorsicht Glas, VOID / tamper-evident and logistics texts. We prepare the design to your instructions and language variants.",
            "search": "security void tamper warning fragile",
        },
        "zmena-grafiky": {
            "q": "What if I need to change artwork after approval?",
            "a": "Until plate-making / printing starts, changes are usually still possible. After production starts, changes may not be possible without extra cost and a new lead time, so check the preview carefully.",
            "search": "artwork change correction approval",
        },
        "jadro": {
            "q": "What core / cardboard tube do you use?",
            "a": "We normally supply rolls with a standard paper core suitable for hand and machine unwinders. For sustainability and ESG goals we also offer tapes with a recycled-paper core.",
            "search": "core tube diameter cardboard recycled esg",
        },
        "zahranici": {
            "q": "Do you deliver outside Czechia?",
            "a": "Yes. We ship to the EU and beyond, shipping and terms are agreed by destination and volume.",
            "search": "abroad eu export delivery international",
        },
        "odstranitelna": {
            "q": "Do you have tapes that remove cleanly?",
            "a": "Yes, removable tapes for cases where you do not want adhesive residue. We recommend the right type for the surface. See Removable tapes in the assortment.",
            "search": "removable clean remove adhesive residue",
        },
        "vice-jazyku": {
            "q": "Can the tape text be in multiple languages?",
            "a": "Yes. We often combine a logo with logistics texts in Czech, German, English and other languages, designed to stay readable when repeated along the tape.",
            "search": "languages multilingual text mutation",
        },
        "prilnavost": {
            "q": "What does adhesion to steel mean?",
            "a": "It shows how strongly the tape sticks to a surface right after application. A higher value means the tape holds more firmly on the carton and is less likely to peel off on its own.",
            "search": "adhesion steel tack carton peel",
        },
        "pevnost-tahu": {
            "q": "What does tensile strength mean?",
            "a": "It measures the tape’s mechanical resistance to breaking under strong tension. A higher number means the tape is less likely to snap when packing demanding or heavy shipments.",
            "search": "tensile strength break resistance packing",
        },
        "taznost": {
            "q": "What does elongation / stretch mean?",
            "a": "The percentage shows how much the tape can stretch before it breaks. Low elongation keeps the box firm without sagging; higher elongation helps the tape absorb shocks during transport.",
            "search": "elongation stretch break shock transport",
        },
    }


def _items_de() -> dict[str, dict[str, str]]:
    return {
        "moq": {
            "q": "Wie hoch ist die Mindestbestellmenge?",
            "a": "Bei BOPP-Bändern 360 Stück (Akryl) oder 504 Stück (HOT MELT); bei Papier- und BOPET-Bändern hängt die Mindestmenge individuell von Druck und Kreppauflage ab.",
            "search": "mindestmenge moq bestellung stück bopp hot melt akryl",
        },
        "lead-time": {
            "q": "Wie lange dauert die Herstellung von bedrucktem Klebeband?",
            "a": "Die Standardlieferzeit beträgt 3 bis 4 Wochen ab Freigabe des Drucklayouts und der Bestellung. Bei dringenden Aufträgen bemühen wir uns um eine schnellere Lieferung.",
            "search": "lieferzeit produktion wochen dringend versand",
        },
        "bez-potisku": {
            "q": "Kann ich auch unbedrucktes Band bestellen?",
            "a": "Ja. Wir liefern dieselbe Qualität auch ohne Druck, ideal für Lagerbestände oder sofortiges Verpacken.",
            "search": "unbedruckt neutral ohne druck",
        },
        "lepidlo": {
            "q": "Was ist der Unterschied zwischen HOT MELT und Akryl?",
            "a": 'HOT MELT haftet schnell und fest auch bei Kälte, ideal für Lager und Versand. Akryl läuft leiser ab und ist UV-beständiger, ideal für längere Lagerung. Mehr unter <a href="/#lepidla">Welchen Klebstoff wählen?</a>.',
            "search": "hot melt akryl klebstoff haftung uv leise abrollen lager",
        },
        "vzorky": {
            "q": "Liefern Sie kostenlose Muster?",
            "a": "Ein physisches Muster mit Ihrem Aufdruck fertigen wir nicht. Gerne senden wir Ihnen aber kostenlos Material- und Klebstoffmuster aus unserem Bestand früherer Aufträge, damit Sie Qualität und Haftung auf Ihren Kartons vor der Bestellung testen können.",
            "search": "muster gratis material klebstoff test sample",
        },
        "technologie": {
            "q": "Welche Drucktechnologien bieten Sie an?",
            "a": "Flexodruck bis 8 Farben und Rotogravur bis 10 Farben inklusive hochwertigem Unterdruck. Die passende Technologie empfehlen wir nach Farben, Menge und Qualitätsanforderung.",
            "search": "flexo rotogravur farben druck technologie unterdruck",
        },
        "grafika": {
            "q": "Erstellen Sie das Drucklayout für mich?",
            "a": "Ja. Wir brauchen Ihr Logo (idealerweise Vektor PDF, AI oder EPS), optional Text und Farbvorstellung (genaue Pantone-Töne). Vor der Produktion senden wir eine Grafikvorschau zur Freigabe.",
            "search": "layout grafik logo vorschau design pdf ai eps pantone",
        },
        "sirka": {
            "q": "Welche Breiten und Längen fertigen Sie?",
            "a": "Wir liefern ein breites Maßangebot für Hand- und Maschinenverpackung. Standardbreiten: 25 mm, 38 mm, 50 mm, 75 mm und 100 mm. Handwicklungen: 66 m, 100 m, 132 m und 180 m. Maschinenwicklungen (Verpackungslinien): 330 m, 660 m, 990 m und 1000 m.",
            "search": "breite länge 25 38 50 75 100 mm 66 132 180 330 660 990 1000 rolle wicklung",
        },
        "eko": {
            "q": "Haben Sie nachhaltige / ECO-Bänder?",
            "a": "Ja, die ECO+-Serie (recyceltes BOPP), Papierbänder und weitere nachhaltige Varianten. Details finden Sie im Sortiment Nachhaltige Bänder.",
            "search": "eco recycling nachhaltig papier fsc",
        },
        "stroje": {
            "q": "Eignen sich die Bänder auch für Maschinenverpackung?",
            "a": "Ja. Je nach Klebstoff und Material empfehlen wir eine Variante für Handabroller oder für automatische Verpackungslinien.",
            "search": "maschine automatik linie abroller dispenser",
        },
        "doprava": {
            "q": "Wie laufen Versand und Rechnungsstellung?",
            "a": "Wir liefern in ganz Tschechien und ins Ausland. Versand- und Zahlungsbedingungen klären wir im Angebot nach Volumen und Lieferort.",
            "search": "versand rechnung lieferung eu preis",
        },
        "skladovani": {
            "q": "Wie lagere ich die Bänder richtig?",
            "a": "Ideal trocken, ohne direkte Sonne, bei Zimmertemperatur. Akryl-Bänder vertragen längere Lagerung besser; bei intensiver Nutzung empfehlen wir, HOT MELT früher zu verbrauchen.",
            "search": "lagerung temperatur feuchtigkeit haltbarkeit",
        },
        "opakovat": {
            "q": "Kann ich die Bestellung mit demselben Aufdruck wiederholen?",
            "a": "Ja. Alle freigegebenen Druckmatrizen archivieren wir. Eine Nachbestellung mit demselben Design läuft daher sofort ohne erneute Freigabe.",
            "search": "nachbestellung reprint gleiches layout matrix archiv",
        },
        "matrice": {
            "q": "Zahlt man die Druckmatrize auch bei Nachbestellung?",
            "a": "Nein. Die freigegebene Druckmatrize bewahren wir für Sie auf. Die Wiederholung mit demselben Layout läuft automatisch und ohne weitere Vorbereitungskosten.",
            "search": "druckmatrize gebühr nachbestellung archiv forme",
        },
        "cena": {
            "q": "Wovon hängt der Preis für bedrucktes Band ab?",
            "a": "Den Preis beeinflussen Material, Klebstoff, Breite und Länge der Rolle, Farbanzahl, Drucktechnologie und Gesamtmenge. Senden Sie eine Anfrage, wir erstellen ein konkretes Angebot.",
            "search": "preis angebot kalkulation kosten",
        },
        "papir-vs-bopp": {
            "q": "Wann Papierband statt BOPP wählen?",
            "a": "Papierband eignet sich für Öko-Verpackung, recyclingfähige Kartons und Brands mit natürlichem Look. BOPP ist feuchtigkeitsbeständiger und oft günstiger bei höheren Mengen. Gerne beraten wir zu Ihrem Prozess.",
            "search": "papier bopp plastik öko karton",
        },
        "bezpecnostni": {
            "q": "Können Sie Sicherheits- oder Warnbänder fertigen?",
            "a": "Ja, Warnaufdrucke, Fragile, Vorsicht Glas, VOID / Tamper-Evident und Logistiktexte. Das Layout erstellen wir nach Ihren Vorgaben und Sprachversionen.",
            "search": "sicherheit void tamper warnung fragile",
        },
        "zmena-grafiky": {
            "q": "Was, wenn ich das Layout nach Freigabe ändern muss?",
            "a": "Solange Druckformen / Druck noch nicht gestartet sind, sind Änderungen meist möglich. Nach Produktionsstart oft nur mit Mehrkosten und neuem Termin, prüfen Sie die Vorschau daher sorgfältig.",
            "search": "layout änderung korrektur freigabe",
        },
        "jadro": {
            "q": "Welchen Kern / welche Hülse verwenden Sie?",
            "a": "Standardmäßig liefern wir Rollen mit üblicher Papphülse für Hand- und Maschinenabroller. Für Nachhaltigkeits- und ESG-Ziele bieten wir auch Bänder mit Hülse aus Recyclingpapier.",
            "search": "kern hülse durchmesser core recycling esg",
        },
        "zahranici": {
            "q": "Liefern Sie auch außerhalb Tschechiens?",
            "a": "Ja. Wir versenden in die EU und darüber hinaus, Versand und Konditionen stimmen wir nach Ziel und Menge ab.",
            "search": "ausland eu export lieferung",
        },
        "odstranitelna": {
            "q": "Haben Sie sauber ablösbare Bänder?",
            "a": "Ja, entfernbare (removable) Bänder, wenn keine Klebstoffreste bleiben sollen. Wir empfehlen den passenden Typ je nach Untergrund. Mehr im Sortiment Ablösbare Bänder.",
            "search": "ablösbar removable rückstandsfrei klebstoff",
        },
        "vice-jazyku": {
            "q": "Kann der Text auf dem Band mehrsprachig sein?",
            "a": "Ja. Häufig kombinieren wir Logo mit Logistiktexten auf Tschechisch, Deutsch, Englisch und weiteren Sprachen, lesbar auch bei Wiederholung entlang des Bandes.",
            "search": "sprachen mehrsprachig text mutation",
        },
        "prilnavost": {
            "q": "Was bedeutet Klebkraft auf Stahl?",
            "a": "Sie gibt an, wie stark das Band sofort nach dem Aufbringen am Untergrund haftet. Ein höherer Wert bedeutet festeren Halt am Karton und weniger Risiko des selbstständigen Ablösens.",
            "search": "klebkraft adhesion stahl karton haftung",
        },
        "pevnost-tahu": {
            "q": "Was bedeutet Zugfestigkeit?",
            "a": "Sie misst die mechanische Widerstandsfähigkeit des Bandes gegen Reißen bei starker Spannung. Eine höhere Zahl bedeutet, dass das Band bei anspruchsvollen oder schweren Sendungen weniger leicht reißt.",
            "search": "zugfestigkeit tensile reißfestigkeit packung",
        },
        "taznost": {
            "q": "Was bedeutet Dehnung / Verlängerung?",
            "a": "Der Prozentwert gibt an, wie weit sich das Band dehnen kann, bevor es reißt. Geringe Dehnung hält den Karton fest ohne Durchhang; höhere Dehnung hilft, Stöße beim Transport besser abzufangen.",
            "search": "dehnung elongation stretch transport stoß",
        },
    }


def _items_it() -> dict[str, dict[str, str]]:
    return {
        "moq": {
            "q": "Qual è la quantità minima d'ordine?",
            "a": "Per i nastri BOPP 360 pz (Akryl) o 504 pz (HOT MELT); per carta e BOPET il minimo dipende individualmente dalla stampa e dallo strato crepato.",
            "search": "minimo moq quantità ordine bopp hot melt akryl",
        },
        "lead-time": {
            "q": "Quanto tempo richiede la produzione di nastro stampato?",
            "a": "Il tempo di consegna standard è di 3–4 settimane dall'approvazione della grafica e dell'ordine. Per urgenze cerchiamo di accelerare la consegna.",
            "search": "tempi consegna produzione settimane urgente",
        },
        "bez-potisku": {
            "q": "Posso ordinare anche nastro senza stampa?",
            "a": "Sì. Forniamo la stessa qualità anche senza stampa, ideale per scorte di magazzino o imballaggio immediato.",
            "search": "senza stampa neutro plain",
        },
        "lepidlo": {
            "q": "Qual è la differenza tra HOT MELT e Akryl?",
            "a": 'HOT MELT aderisce rapidamente e con forza anche a freddo, ideale per magazzini e spedizioni. Akryl è più silenzioso nello svolgimento e più resistente ai UV, ideale per stoccaggio prolungato. Maggiori info in <a href="/#lepidla">Quale adesivo scegliere?</a>.',
            "search": "hot melt akryl adesivo adesione uv silenzioso magazzino",
        },
        "vzorky": {
            "q": "Fornite campioni gratuiti?",
            "a": "Non produciamo un campione fisico con la vostra stampa. Siamo però lieti di inviare gratis campioni di materiali e adesivi a magazzino da realizzazioni precedenti, così potete testare qualità e adesione sui vostri cartoni prima dell'ordine.",
            "search": "campione gratis materiale adesivo test trial",
        },
        "technologie": {
            "q": "Quali tecnologie di stampa offrite?",
            "a": "Flessografia fino a 8 colori e rotocalco fino a 10 colori, incluso sotto-stampa di qualità. Consigliamo la tecnologia in base a colori, quantità e qualità richiesta.",
            "search": "flessografia rotocalco colori stampa tecnologia",
        },
        "grafika": {
            "q": "Preparate voi il progetto grafico?",
            "a": "Sì. Ci servono il logo (idealmente vettoriale PDF, AI o EPS), eventuale testo e idea di colore (tinte Pantone precise). Prima della produzione inviamo un'anteprima grafica da approvare.",
            "search": "grafica logo anteprima design pdf ai eps pantone",
        },
        "sirka": {
            "q": "Quali larghezze e lunghezze producete?",
            "a": "Forniamo un'ampia gamma di misure per imballaggio manuale e automatico. Larghezze standard: 25 mm, 38 mm, 50 mm, 75 mm e 100 mm. Lunghezze manuali: 66 m, 100 m, 132 m e 180 m. Lunghezze macchina (linee): 330 m, 660 m, 990 m e 1000 m.",
            "search": "larghezza lunghezza 25 38 50 75 100 mm 66 132 180 330 660 990 1000 bobina",
        },
        "eko": {
            "q": "Avete nastri sostenibili / ECO?",
            "a": "Sì, linea ECO+ (BOPP riciclato), nastri di carta e altre varianti sostenibili. Dettagli nell'assortimento Nastri sostenibili.",
            "search": "eco riciclo sostenibile carta fsc",
        },
        "stroje": {
            "q": "I nastri vanno bene anche per imballaggio automatico?",
            "a": "Sì. In base ad adesivo e materiale consigliamo la variante per svolgitori manuali o per linee automatiche.",
            "search": "macchina automatica linea svolgitore dispenser",
        },
        "doprava": {
            "q": "Come funzionano spedizione e fatturazione?",
            "a": "Consegniamo in tutta la Repubblica Ceca e all'estero. Condizioni di trasporto e pagamento si definiscono nell'offerta in base a volume e destinazione.",
            "search": "spedizione fattura consegna eu prezzo",
        },
        "skladovani": {
            "q": "Come conservare correttamente i nastri?",
            "a": "Ideale in luogo asciutto, lontano dal sole diretto, a temperatura ambiente. I nastri Akryl tollerano meglio lo stoccaggio lungo; con uso intensivo consigliamo di consumare prima l'HOT MELT.",
            "search": "stoccaggio temperatura umidità durata",
        },
        "opakovat": {
            "q": "Posso ripetere l'ordine con la stessa stampa?",
            "a": "Sì. Archiviamo tutte le matrici di stampa approvate. Un riordino con lo stesso design procede quindi subito senza nuova approvazione.",
            "search": "riordino reprint stessa grafica matrice archivio",
        },
        "matrice": {
            "q": "Si paga di nuovo la matrice di stampa in caso di riordino?",
            "a": "No. Conserviamo la matrice approvata per voi. La produzione ripetuta con lo stesso layout avviene automaticamente e senza ulteriori costi di preparazione.",
            "search": "matrice stampa costo riordino archivio",
        },
        "cena": {
            "q": "Da cosa dipende il prezzo del nastro stampato?",
            "a": "Il prezzo dipende da materiale, adesivo, larghezza e lunghezza della bobina, numero di colori, tecnologia di stampa e volume totale. Inviate una richiesta, prepariamo un'offerta concreta.",
            "search": "prezzo offerta preventivo calcolo",
        },
        "papir-vs-bopp": {
            "q": "Quando scegliere nastro di carta invece del BOPP?",
            "a": "Il nastro di carta è adatto a imballaggi eco, cartoni riciclabili e brand dal look naturale. Il BOPP resiste meglio all'umidità ed è spesso più conveniente a volumi alti. Consigliamo in base al vostro processo.",
            "search": "carta bopp plastica eco cartone",
        },
        "bezpecnostni": {
            "q": "Realizzate nastri di sicurezza o di avvertimento?",
            "a": "Sì, stampe di avviso, Fragile, Vorsicht Glas, VOID / tamper-evident e testi logistici. Prepariamo il layout secondo le vostre istruzioni e le varianti linguistiche.",
            "search": "sicurezza void tamper avviso fragile",
        },
        "zmena-grafiky": {
            "q": "E se devo modificare la grafica dopo l'approvazione?",
            "a": "Finché non partono lastre / stampa, le modifiche di solito sono possibili. Dopo l'avvio della produzione spesso solo con costi e tempi aggiuntivi, controllate quindi attentamente l'anteprima.",
            "search": "modifica grafica correzione approvazione",
        },
        "jadro": {
            "q": "Quale anima / tubetto usate?",
            "a": "Di norma forniamo bobine con tubetto di carta standard adatto a svolgitori manuali e automatici. Per obiettivi di sostenibilità ed ESG offriamo anche nastri con tubetto in carta riciclata.",
            "search": "anima tubetto core diametro riciclato esg",
        },
        "zahranici": {
            "q": "Consegnate anche fuori dalla Repubblica Ceca?",
            "a": "Sì. Spediamo in UE e oltre, trasporto e condizioni si concordano in base a destinazione e volume.",
            "search": "estero eu export consegna",
        },
        "odstranitelna": {
            "q": "Avete nastri che si rimuovono in modo pulito?",
            "a": "Sì, nastri removibili (removable) dove non volete residui di adesivo. Consigliamo il tipo adatto alla superficie. Maggiori info nell'assortimento Nastri removibili.",
            "search": "removibile removable residui adesivo",
        },
        "vice-jazyku": {
            "q": "Il testo sul nastro può essere in più lingue?",
            "a": "Sì. Spesso combiniamo logo e testi logistici in ceco, tedesco, inglese e altre lingue, progettati per restare leggibili anche ripetuti lungo il nastro.",
            "search": "lingue multilingue testo mutazione",
        },
        "prilnavost": {
            "q": "Cosa significa adesione all'acciaio?",
            "a": "Indica quanto fortemente il nastro aderisce alla superficie subito dopo l'applicazione. Un valore più alto significa tenuta più ferma sul cartone e minor rischio di distacco spontaneo.",
            "search": "adesione acciaio tack cartone adesività",
        },
        "pevnost-tahu": {
            "q": "Cosa significa resistenza alla trazione?",
            "a": "Misura la resistenza meccanica del nastro alla rottura sotto forte tensione. Un numero più alto garantisce che il nastro non si spezzi nell'imballaggio di spedizioni impegnative o pesanti.",
            "search": "resistenza trazione tensile rottura imballaggio",
        },
        "taznost": {
            "q": "Cosa significa allungamento / elongazione?",
            "a": "Il valore percentuale indica di quanto il nastro può allungarsi prima di rompersi. Un allungamento basso tiene la scatola ferma senza cedimenti; uno più alto aiuta ad assorbire gli urti durante il trasporto.",
            "search": "allungamento elongazione stretch trasporto urti",
        },
    }


def faq_ui(lang: str) -> dict[str, Any]:
    if lang == "cs":
        return {
            "label": "Časté dotazy",
            "title": "Otázky a odpovědi",
            "subtitle": "Najděte odpověď na potisk, termíny, lepidla i vzorky. Filtrujte podle tématu nebo hledejte klíčové slovo.",
            "hero_cta": "Napsat zprávu",
            "search_label": "Hledat v otázkách",
            "search_placeholder": "Hledat… např. HOT MELT, vzorek, dodací lhůta",
            "filters_label": "Filtr témat",
            "filters": {
                "all": "Vše",
                "objednavka": "Objednávka",
                "vyroba": "Výroba a termíny",
                "material": "Materiál a lepidlo",
                "potisk": "Potisk a grafika",
                "vzorky": "Vzorky",
            },
            "more": "Zobrazit dalších {n} otázek",
            "count_preview": "Zobrazeno {shown} z {total}",
            "count_all": "{n} otázek",
            "count_filtered": "Zobrazeno {visible} z {total}",
            "empty_title": "Nic jsme nenašli",
            "empty_text": "Zkuste jiné klíčové slovo nebo vyberte jiný filtr. Případně nám napište a poradíme.",
            "empty_cta": "Napsat zprávu →",
            "contact_label": "Kontakt",
            "cta_title": "Nenašli jste odpověď?",
            "cta_text": "Napište nám krátkou zprávu a ozveme se s odpovědí nebo doporučením materiálu a potisku.",
            "cta_button": "Odeslat zprávu",
            "form": {
                "name": "Jméno a příjmení",
                "email": "E-mail",
                "phone": "Telefon",
                "message": "Vaše otázka / zpráva",
                "message_placeholder": "Napište, s čím potřebujete poradit…",
                "gdpr": "Odesláním souhlasíte se zpracováním osobních údajů za účelem vyřízení zprávy.",
                "sending": "Odesílám…",
                "success": "Děkujeme, zpráva byla odeslána. Ozveme se co nejdřív.",
                "error": "Odeslání se nezdařilo. Napište nám prosím na karel.petrak@alfain.eu.",
            },
            "items": _items_cs(),
        }
    if lang == "en":
        return {
            "label": "FAQ",
            "title": "Questions and answers",
            "subtitle": "Find answers about printing, lead times, adhesives and samples. Filter by topic or search a keyword.",
            "hero_cta": "Write a message",
            "search_label": "Search questions",
            "search_placeholder": "Search… e.g. HOT MELT, sample, lead time",
            "filters_label": "Topic filter",
            "filters": {
                "all": "All",
                "objednavka": "Ordering",
                "vyroba": "Production & lead times",
                "material": "Material & adhesive",
                "potisk": "Print & artwork",
                "vzorky": "Samples",
            },
            "more": "Show {n} more questions",
            "count_preview": "Showing {shown} of {total}",
            "count_all": "{n} questions",
            "count_filtered": "Showing {visible} of {total}",
            "empty_title": "No results",
            "empty_text": "Try another keyword or filter. Or send us a message and we will help.",
            "empty_cta": "Write a message →",
            "contact_label": "Contact",
            "cta_title": "Didn’t find your answer?",
            "cta_text": "Send us a short message and we will reply with an answer or a material and print recommendation.",
            "cta_button": "Send message",
            "form": {
                "name": "Full name",
                "email": "E-mail",
                "phone": "Phone",
                "message": "Your question / message",
                "message_placeholder": "Tell us what you need help with…",
                "gdpr": "By submitting you agree to the processing of personal data for handling this message.",
                "sending": "Sending…",
                "success": "Thank you, your message was sent. We will get back to you soon.",
                "error": "Sending failed. Please e-mail us at karel.petrak@alfain.eu.",
            },
            "items": _items_en(),
        }
    if lang == "de":
        return {
            "label": "FAQ",
            "title": "Fragen und Antworten",
            "subtitle": "Finden Sie Antworten zu Druck, Terminen, Klebstoffen und Mustern. Filtern Sie nach Thema oder suchen Sie ein Stichwort.",
            "hero_cta": "Nachricht schreiben",
            "search_label": "In Fragen suchen",
            "search_placeholder": "Suchen… z. B. HOT MELT, Muster, Lieferzeit",
            "filters_label": "Themenfilter",
            "filters": {
                "all": "Alle",
                "objednavka": "Bestellung",
                "vyroba": "Produktion & Termine",
                "material": "Material & Klebstoff",
                "potisk": "Druck & Grafik",
                "vzorky": "Muster",
            },
            "more": "{n} weitere Fragen anzeigen",
            "count_preview": "Angezeigt {shown} von {total}",
            "count_all": "{n} Fragen",
            "count_filtered": "Angezeigt {visible} von {total}",
            "empty_title": "Keine Treffer",
            "empty_text": "Versuchen Sie ein anderes Stichwort oder einen anderen Filter. Oder schreiben Sie uns und wir helfen.",
            "empty_cta": "Nachricht schreiben →",
            "contact_label": "Kontakt",
            "cta_title": "Keine passende Antwort gefunden?",
            "cta_text": "Schreiben Sie uns eine kurze Nachricht und wir melden uns mit einer Antwort oder Empfehlung zu Material und Druck.",
            "cta_button": "Nachricht senden",
            "form": {
                "name": "Vor- und Nachname",
                "email": "E-Mail",
                "phone": "Telefon",
                "message": "Ihre Frage / Nachricht",
                "message_placeholder": "Schreiben Sie, wobei wir helfen sollen…",
                "gdpr": "Mit dem Absenden stimmen Sie der Verarbeitung personenbezogener Daten zur Bearbeitung der Nachricht zu.",
                "sending": "Wird gesendet…",
                "success": "Danke, Ihre Nachricht wurde gesendet. Wir melden uns bald.",
                "error": "Senden fehlgeschlagen. Bitte schreiben Sie an karel.petrak@alfain.eu.",
            },
            "items": _items_de(),
        }
    # it
    return {
        "label": "Domande frequenti",
        "title": "Domande e risposte",
        "subtitle": "Trovate risposte su stampa, tempi, adesivi e campioni. Filtrate per tema o cercate una parola chiave.",
        "hero_cta": "Scrivi un messaggio",
        "search_label": "Cerca nelle domande",
        "search_placeholder": "Cerca… es. HOT MELT, campione, tempi di consegna",
        "filters_label": "Filtro temi",
        "filters": {
            "all": "Tutte",
            "objednavka": "Ordine",
            "vyroba": "Produzione e tempi",
            "material": "Materiale e adesivo",
            "potisk": "Stampa e grafica",
            "vzorky": "Campioni",
        },
        "more": "Mostra altre {n} domande",
        "count_preview": "Visualizzate {shown} di {total}",
        "count_all": "{n} domande",
        "count_filtered": "Visualizzate {visible} di {total}",
        "empty_title": "Nessun risultato",
        "empty_text": "Provate un'altra parola chiave o un altro filtro. Oppure scriveteci e vi aiutiamo.",
        "empty_cta": "Scrivi un messaggio →",
        "contact_label": "Contatto",
        "cta_title": "Non avete trovato la risposta?",
        "cta_text": "Scriveteci un breve messaggio e vi risponderemo con una risposta o un consiglio su materiale e stampa.",
        "cta_button": "Invia messaggio",
        "form": {
            "name": "Nome e cognome",
            "email": "E-mail",
            "phone": "Telefono",
            "message": "La vostra domanda / messaggio",
            "message_placeholder": "Scrivete di cosa avete bisogno…",
            "gdpr": "Inviando accettate il trattamento dei dati personali per la gestione del messaggio.",
            "sending": "Invio in corso…",
            "success": "Grazie, il messaggio è stato inviato. Vi risponderemo al più presto.",
            "error": "Invio non riuscito. Scriveteci a karel.petrak@alfain.eu.",
        },
        "items": _items_it(),
    }


def faq_meta(lang: str) -> dict[str, str]:
    if lang == "cs":
        return {
            "faq_title": "FAQ | Pásky s potiskem: otázky a odpovědi",
            "faq_description": "Časté otázky k páskám s potiskem: minimální odběr, dodací lhůty, HOT MELT vs Akryl, potisk, vzorky a doprava. Odpovědi od výrobce ALFA IN.",
        }
    if lang == "en":
        return {
            "faq_title": "FAQ | Printed tapes: questions and answers",
            "faq_description": "Common questions about printed tapes: minimum order, lead times, HOT MELT vs Acrylic, print, samples and shipping. Answers from manufacturer ALFA IN.",
        }
    if lang == "de":
        return {
            "faq_title": "FAQ | Bedruckte Klebebänder: Fragen und Antworten",
            "faq_description": "Häufige Fragen zu bedruckten Klebebändern: Mindestmenge, Lieferzeiten, HOT MELT vs Akryl, Druck, Muster und Versand. Antworten vom Hersteller ALFA IN.",
        }
    return {
        "faq_title": "FAQ | Nastri stampati: domande e risposte",
        "faq_description": "Domande frequenti sui nastri stampati: quantità minima, tempi, HOT MELT vs Akryl, stampa, campioni e spedizione. Risposte dal produttore ALFA IN.",
    }


def apply_faq_i18n(tree: dict[str, Any], lang: str) -> None:
    """Replace/merge FAQ page strings + meta into a locale tree."""
    tree["faq"] = faq_ui(lang)
    meta = tree.setdefault("meta", {})
    meta.update(faq_meta(lang))
    # Homepage FAQ item keys used in index.html
    home = tree.setdefault("home", {}).setdefault("faq", {})
    items = tree["faq"]["items"]
    home_ids = ["moq", "lead-time", "bez-potisku", "lepidlo", "vzorky", "technologie"]
    home["items"] = {
        str(i): {"q": items[fid]["q"], "a": items[fid]["a"]} for i, fid in enumerate(home_ids)
    }
