#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate data/i18n/cs.json, en.json, de.json and it.json from site source strings."""

from __future__ import annotations

import ast
import copy
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_product_builder import (  # noqa: E402
    CATEGORY_IT,
    load_gp_namespace,
    merge_into_gallery,
    merge_into_sortiment,
)

LANG_NAMES = {"cs": "Čeština", "en": "English", "de": "Deutsch", "it": "Italiano"}
HTML_LANG = {"cs": "cs", "en": "en", "de": "de", "it": "it"}

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "i18n"
GEN_PRODUCTS = ROOT / "scripts" / "gen_products.py"


def load_cats() -> list[dict[str, Any]]:
    """Load CATS from gen_products.py without executing that script."""
    source = GEN_PRODUCTS.read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "CATS":
                value = ast.literal_eval(node.value)
                if isinstance(value, list):
                    return value
    raise RuntimeError("CATS not found in gen_products.py")


CATS = load_cats()


# ---------------------------------------------------------------------------
# Sortiment category translations (EN / DE) keyed by slug from gen_products.CATS
# ---------------------------------------------------------------------------
CATEGORY_EN: dict[str, dict[str, Any]] = {
    "papirove-pasky": {
        "title": "Paper tapes",
        "description": "An eco-friendly solution for secure packaging with high adhesion. Ideal for fully recyclable cardboard boxes and clean corporate branding.",
        "intro": "Paper adhesive tapes combine reliable bonding with maximum environmental responsibility. Thanks to the paper carrier, they are fully recyclable together with cardboard and offer an elegant, clean-looking solution for companies that care about sustainability and the visual impact of their shipments.",
        "properties": {
            "Plná recyklovatelnost": "Fully recyclable",
            "Vysoká lepivost": "High adhesion",
            "Čistý design": "Clean design",
        },
        "property_texts": {
            "Plná recyklovatelnost": "Tape and cardboard go into the same bin, no need to separate materials.",
            "Vysoká lepivost": "Reliable bonding even on recycled cardboard and uneven surfaces.",
            "Čistý design": "The matte paper surface looks premium and can be easily printed with your logo.",
        },
        "applications": [
            "E-shops focused on sustainable packaging",
            "Sealing cardboard boxes and parcels",
            "Corporate branding directly on shipments",
            "Manual and semi-automatic packing",
        ],
    },
    "bopp-pasky": {
        "title": "BOPP tapes",
        "description": "The most widely used industrial packaging tapes made from biaxially oriented polypropylene. Outstanding tensile strength and long service life.",
        "intro": "BOPP tapes are the standard for everyday packing in manufacturing, logistics and e-commerce. Biaxially oriented polypropylene film delivers an excellent price-performance ratio, availability in acrylic and hot melt versions, and a wide range of widths and colours.",
        "properties": {
            "Vynikající poměr cena/výkon": "Excellent price/performance ratio",
            "Ekologická šetrnost": "Environmental friendliness",
            "Fyzikální a chemická stálost": "Physical and chemical stability",
        },
        "property_texts": {
            "Vynikající poměr cena/výkon": "Top performance at a favourable price for everyday industrial and e-commerce packing.",
            "Ekologická šetrnost": "Contains no environmentally harmful substances such as PVC.",
            "Fyzikální a chemická stálost": "Stable film and adhesive properties during storage, transport and everyday use.",
        },
        "applications": [
            "Standard carton sealing",
            "Automatic packing machines",
            "Dispatch and warehouse logistics",
            "Printing with company logos and information",
        ],
    },
    "bopet-pasky": {
        "title": "BOPET tapes",
        "description": "Premium polyester tapes with extreme resistance to tearing, chemicals and temperature fluctuations. Designed for the most demanding industrial applications.",
        "intro": "BOPET tapes based on polyester film are made for applications where standard tapes are not enough. They withstand high temperatures, aggressive chemicals and mechanical stress while maintaining their properties in extreme conditions.",
        "properties": {
            "Teplotní odolnost": "Temperature resistance",
            "Chemická odolnost": "Chemical resistance",
            "Odolnost proti roztržení": "Tear resistance",
        },
        "property_texts": {
            "Teplotní odolnost": "Stable performance at high and low temperatures.",
            "Chemická odolnost": "Resistant to solvents, oils and harsh environments.",
            "Odolnost proti roztržení": "Strong polyester film with minimal elongation.",
        },
        "applications": [
            "Demanding industrial operations",
            "Masking in powder coating",
            "Fixation in high-temperature environments",
            "Electrical engineering and specialised manufacturing",
        ],
    },
    "textilni-pasky": {
        "title": "Cloth adhesive tapes",
        "description": "Highly durable, versatile tapes reinforced with a textile mesh. They grip rough surfaces perfectly, tear easily by hand and are ideal for quick repairs and bundling.",
        "intro": "Cloth (duct) tapes are an indispensable all-rounder. Textile reinforcement gives them high strength while allowing easy hand tearing without scissors. They adhere reliably even to coarse and uneven surfaces.",
        "properties": {
            "Textilní výztuž": "Textile reinforcement",
            "Trhání rukou": "Hand tearable",
            "Přilnavost na drsný povrch": "Adhesion on rough surfaces",
        },
        "property_texts": {
            "Textilní výztuž": "High strength and resistance to puncture.",
            "Trhání rukou": "Fast work without tools.",
            "Přilnavost na drsný povrch": "Bonds to metal, wood, concrete and plastic.",
        },
        "applications": [
            "Quick repairs and temporary joints",
            "Bundling and securing items",
            "Reinforcing parcels and packaging",
            "Maintenance, assembly and crafts",
        ],
    },
    "vyztuzene-pasky": {
        "title": "Reinforced tapes",
        "description": "Tapes reinforced with longitudinal or cross-laid glass fibres. Maximum strength for securing heavy loads, pallets and oversized parcels.",
        "intro": "Reinforced (filament) tapes contain glass fibres laid longitudinally or crosswise, dramatically increasing tensile strength. They are designed for securing heavy and oversized shipments where absolute reliability is required.",
        "properties": {
            "Skelná vlákna": "Glass fibres",
            "Nosnost": "Load capacity",
            "Odolnost proti přetržení": "Break resistance",
        },
        "property_texts": {
            "Skelná vlákna": "Longitudinal or cross reinforcement for maximum strength.",
            "Nosnost": "Reliable securing of heavy loads and pallets.",
            "Odolnost proti přetržení": "Withstands high tensile loads.",
        },
        "applications": [
            "Securing heavy and oversized parcels",
            "Stabilising goods on pallets",
            "Bundling pipes, profiles and rods",
            "Demanding transport and export",
        ],
    },
    "mopp-pasky": {
        "title": "MOPP tapes",
        "description": "Monoaxially oriented tapes with extreme strength in one direction and zero elasticity. Specially designed for securing appliances, components or pallet strapping.",
        "intro": "MOPP tapes feature monoaxially oriented film with extreme longitudinal strength and virtually zero elongation. They replace reinforced tapes where firm securing without glass fibres is needed.",
        "properties": {
            "Extrémní pevnost": "Extreme strength",
            "Nulová elasticita": "Zero elasticity",
            "Bez skelných vláken": "No glass fibres",
        },
        "property_texts": {
            "Extrémní pevnost": "High tensile strength in one direction.",
            "Nulová elasticita": "The securing will not loosen under load.",
            "Bez skelných vláken": "Clean securing without loose fibres.",
        },
        "applications": [
            "Securing appliance doors",
            "Stabilising components during transport",
            "Pallet strapping and securing",
            "Bundling without glass fibres",
        ],
    },
    "odstranitelne-pasky": {
        "title": "Removable tapes",
        "description": "Tapes with a special adhesive formulation that leaves no residue after removal. Ideal for temporary marking, protecting sensitive surfaces or logistics processes.",
        "intro": "Removable tapes use a special adhesive that holds firmly yet leaves no residue or surface damage when peeled off. They are ideal for temporary applications and protecting sensitive materials.",
        "properties": {
            "Beze stop": "Residue-free",
            "Šetrné k povrchu": "Surface-friendly",
            "Spolehlivá drživost": "Reliable hold",
        },
        "property_texts": {
            "Beze stop": "No adhesive or residue remains after removal.",
            "Šetrné k povrchu": "Will not damage paint, glass or sensitive materials.",
            "Spolehlivá drživost": "Holds for the entire required application period.",
        },
        "applications": [
            "Temporary marking and labels",
            "Protecting sensitive surfaces",
            "Logistics and manufacturing processes",
            "Fixation that must be removed again",
        ],
    },
    "malirske-pasky": {
        "title": "Masking tapes",
        "description": "Crepe paper tapes designed for precise masking during painting and coating. They protect edges from paint bleed and peel off cleanly after the job is done.",
        "intro": "Masking crepe tapes ensure sharp, clean edges when painting and coating. The crepe paper carrier conforms to the surface, tears easily and removes without adhesive residue after completion.",
        "properties": {
            "Ostré hrany": "Sharp edges",
            "Čisté odlepení": "Clean removal",
            "Snadná aplikace": "Easy application",
        },
        "property_texts": {
            "Ostré hrany": "Prevents paint from bleeding under the tape.",
            "Čisté odlepení": "Leaves no adhesive or marks after use.",
            "Snadná aplikace": "Crepe conforms to shape and tears easily.",
        },
        "applications": [
            "Interior painting and coating",
            "Masking edges and transitions",
            "Paint shops and body shops",
            "DIY and craft work",
        ],
    },
    "udrzitelne-pasky": {
        "title": "Sustainable tapes",
        "description": "Innovative packaging solutions made from recycled materials with minimal environmental impact and support for the circular economy.",
        "intro": "Our sustainable tape range is made from recycled materials and designed to minimise environmental impact. It helps companies meet ESG goals and build a responsible brand image without compromising performance.",
        "properties": {
            "Recyklovaný obsah": "Recycled content",
            "Nižší uhlíková stopa": "Lower carbon footprint",
            "Bez kompromisů": "No compromises",
        },
        "property_texts": {
            "Recyklovaný obsah": "Materials with a high recycled content.",
            "Nižší uhlíková stopa": "More sustainable production and circular approach.",
            "Bez kompromisů": "Eco-friendly without sacrificing reliable bonding.",
        },
        "applications": [
            "Companies with ESG and sustainability goals",
            "Green packaging for e-shops",
            "Circular packaging processes",
            "Building a responsible brand",
        ],
    },
}

CATEGORY_DE: dict[str, dict[str, Any]] = {
    "papirove-pasky": {
        "title": "Papierklebebänder",
        "description": "Eine umweltfreundliche Lösung für sicheres Verpacken mit hoher Klebkraft. Ideal für vollständig recycelbare Kartonverpackungen und ein sauberes Corporate Design.",
        "intro": "Papierklebebänder verbinden zuverlässige Haftung mit maximaler Umweltverträglichkeit. Dank des Papierträgers sind sie gemeinsam mit dem Karton vollständig recycelbar und bieten eine elegante, saubere Lösung für Unternehmen, die Wert auf Nachhaltigkeit und den visuellen Eindruck ihrer Sendungen legen.",
        "properties": {
            "Plná recyklovatelnost": "Vollständig recycelbar",
            "Vysoká lepivost": "Hohe Klebkraft",
            "Čistý design": "Sauberes Design",
        },
        "property_texts": {
            "Plná recyklovatelnost": "Band und Karton landen in derselben Tonne – kein Trennen der Materialien nötig.",
            "Vysoká lepivost": "Zuverlässige Haftung auch auf Recyclingkarton und unebenen Flächen.",
            "Čistý design": "Die matte Papieroberfläche wirkt hochwertig und lässt sich leicht mit Ihrem Logo bedrucken.",
        },
        "applications": [
            "E-Shops mit Fokus auf nachhaltige Verpackung",
            "Verschließen von Kartons und Verpackungen",
            "Corporate Branding direkt auf der Sendung",
            "Manuelles und halbautomatisches Verpacken",
        ],
    },
    "bopp-pasky": {
        "title": "BOPP-Klebebänder",
        "description": "Die am weitesten verbreiteten Industrie-Verpackungsbänder aus biaxial orientiertem Polypropylen. Hervorragende Zugfestigkeit und lange Lebensdauer.",
        "intro": "BOPP-Klebebänder sind der Standard für den täglichen Einsatz in Produktion, Logistik und E-Commerce. Die Folie aus biaxial orientiertem Polypropylen bietet ein exzellentes Preis-Leistungs-Verhältnis, Verfügbarkeit in Acryl- und Hot-Melt-Ausführung sowie eine breite Palette an Breiten und Farben.",
        "properties": {
            "Vynikající poměr cena/výkon": "Hervorragendes Preis-Leistungs-Verhältnis",
            "Ekologická šetrnost": "Umweltfreundlichkeit",
            "Fyzikální a chemická stálost": "Physikalische und chemische Beständigkeit",
        },
        "property_texts": {
            "Vynikající poměr cena/výkon": "Spitzenleistung zu einem günstigen Preis für den täglichen Einsatz in Industrie und E-Commerce.",
            "Ekologická šetrnost": "Enthält keine umweltschädlichen Stoffe wie PVC.",
            "Fyzikální a chemická stálost": "Stabile Folien- und Klebstoffeigenschaften bei Lagerung, Transport und alltäglichem Einsatz.",
        },
        "applications": [
            "Standard-Kartonverschluss",
            "Automatische Verpackungsmaschinen",
            "Versand und Lagerlogistik",
            "Bedruckung mit Firmenlogo und Informationen",
        ],
    },
    "bopet-pasky": {
        "title": "BOPET-Klebebänder",
        "description": "Premium-Polyesterbänder mit extremer Beständigkeit gegen Reißen, Chemikalien und Temperaturschwankungen. Für die anspruchsvollsten Industrieanwendungen.",
        "intro": "BOPET-Klebebänder auf Polyesterfolienbasis sind dort im Einsatz, wo Standardbänder nicht ausreichen. Sie widerstehen hohen Temperaturen, aggressiven Chemikalien und mechanischer Belastung und behalten ihre Eigenschaften auch unter extremen Bedingungen.",
        "properties": {
            "Teplotní odolnost": "Temperaturbeständigkeit",
            "Chemická odolnost": "Chemische Beständigkeit",
            "Odolnost proti roztržení": "Reißfestigkeit",
        },
        "property_texts": {
            "Teplotní odolnost": "Stabile Leistung bei hohen und niedrigen Temperaturen.",
            "Chemická odolnost": "Beständig gegen Lösungsmittel, Öle und aggressive Umgebungen.",
            "Odolnost proti roztržení": "Starke Polyesterfolie mit minimaler Dehnung.",
        },
        "applications": [
            "Anspruchsvolle Industriebetriebe",
            "Abkleben beim Pulverbeschichten",
            "Fixierung in Hochtemperaturumgebungen",
            "Elektrotechnik und Spezialfertigung",
        ],
    },
    "textilni-pasky": {
        "title": "Gewebe-Klebebänder",
        "description": "Hochfeste, vielseitige Bänder mit Textilgewebe-Verstärkung. Halten perfekt auf rauen Oberflächen, lassen sich per Hand abreißen und eignen sich ideal für schnelle Reparaturen und Bündelung.",
        "intro": "Gewebe- (Duct-) Klebebänder sind unverzichtbare Allrounder. Die textile Verstärkung verleiht hohe Festigkeit und ermöglicht gleichzeitig ein einfaches Abreißen per Hand ohne Schere. Sie haften zuverlässig auch auf groben und unebenen Flächen.",
        "properties": {
            "Textilní výztuž": "Textilverstärkung",
            "Trhání rukou": "Per Hand abreißbar",
            "Přilnavost na drsný povrch": "Haftung auf rauen Oberflächen",
        },
        "property_texts": {
            "Textilní výztuž": "Hohe Festigkeit und Beständigkeit gegen Durchstich.",
            "Trhání rukou": "Schnelle Arbeit ohne Werkzeug.",
            "Přilnavost na drsný povrch": "Haftet auf Metall, Holz, Beton und Kunststoff.",
        },
        "applications": [
            "Schnelle Reparaturen und provisorische Verbindungen",
            "Bündeln und Fixieren von Gegenständen",
            "Verstärkung von Paketen und Verpackungen",
            "Wartung, Montage und Handwerk",
        ],
    },
    "vyztuzene-pasky": {
        "title": "Verstärkte Klebebänder",
        "description": "Bänder mit längs- oder kreuzverlaufenden Glasfasern. Maximale Festigkeit zur Sicherung schwerer Lasten, Paletten und übergroßer Pakete.",
        "intro": "Verstärkte (Filament-) Klebebänder enthalten längs oder kreuz verlaufende Glasfasern, die die Zugfestigkeit erheblich erhöhen. Sie sind für die Sicherung schwerer und übergroßer Sendungen gedacht, bei denen absolute Zuverlässigkeit gefordert ist.",
        "properties": {
            "Skelná vlákna": "Glasfasern",
            "Nosnost": "Tragfähigkeit",
            "Odolnost proti přetržení": "Bruchfestigkeit",
        },
        "property_texts": {
            "Skelná vlákna": "Längs- oder Kreuzverstärkung für maximale Festigkeit.",
            "Nosnost": "Zuverlässige Sicherung schwerer Lasten und Paletten.",
            "Odolnost proti přetržení": "Hält auch hohen Zugbelastungen stand.",
        },
        "applications": [
            "Sicherung schwerer und übergroßer Pakete",
            "Stabilisierung von Waren auf Paletten",
            "Bündeln von Rohren, Profilen und Stäben",
            "Anspruchsvoller Transport und Export",
        ],
    },
    "mopp-pasky": {
        "title": "MOPP-Klebebänder",
        "description": "Monoaxial orientierte Bänder mit extremer Festigkeit in einer Richtung und null Elastizität. Speziell für die Fixierung von Geräten, Komponenten oder Paletten.",
        "intro": "MOPP-Klebebänder haben eine monoaxial orientierte Folie mit extremer Längsfestigkeit und praktisch null Dehnung. Sie ersetzen verstärkte Bänder dort, wo eine feste Fixierung ohne Glasfasern benötigt wird.",
        "properties": {
            "Extrémní pevnost": "Extreme Festigkeit",
            "Nulová elasticita": "Keine Elastizität",
            "Bez skelných vláken": "Ohne Glasfasern",
        },
        "property_texts": {
            "Extrémní pevnost": "Hohe Zugfestigkeit in einer Richtung.",
            "Nulová elasticita": "Die Fixierung lockert sich auch unter Last nicht.",
            "Bez skelných vláken": "Saubere Fixierung ohne sich lösende Fasern.",
        },
        "applications": [
            "Fixierung von Gerätetüren",
            "Sicherung von Komponenten beim Transport",
            "Paletten-Umreifung und -Fixierung",
            "Bündeln ohne Glasfasern",
        ],
    },
    "odstranitelne-pasky": {
        "title": "Abziehbare Klebebänder",
        "description": "Bänder mit spezieller Klebstoffzusammensetzung, die nach dem Abziehen keine Rückstände hinterlassen. Ideal für temporäre Kennzeichnung, Schutz empfindlicher Oberflächen oder Logistikprozesse.",
        "intro": "Abziehbare Klebebänder verwenden einen Spezialklebstoff, der fest haftet, aber beim Abziehen keine Rückstände oder Oberflächenschäden hinterlässt. Sie eignen sich ideal für temporäre Anwendungen und den Schutz empfindlicher Materialien.",
        "properties": {
            "Beze stop": "Rückstandsfrei",
            "Šetrné k povrchu": "Oberflächenschonend",
            "Spolehlivá drživost": "Zuverlässige Haftung",
        },
        "property_texts": {
            "Beze stop": "Nach dem Abziehen bleibt kein Klebstoff oder Rückstand.",
            "Šetrné k povrchu": "Beschädigt weder Lack, Glas noch empfindliche Materialien.",
            "Spolehlivá drživost": "Hält während der gesamten benötigten Einsatzdauer.",
        },
        "applications": [
            "Temporäre Kennzeichnung und Etiketten",
            "Schutz empfindlicher Oberflächen",
            "Logistik- und Fertigungsprozesse",
            "Fixierung, die wieder entfernt werden muss",
        ],
    },
    "malirske-pasky": {
        "title": "Malerklebebänder",
        "description": "Krepp-Papierbänder für präzises Abkleben beim Malen und Lackieren. Schützen Kanten vor Farbaustritt und lassen sich nach der Arbeit rückstandsfrei entfernen.",
        "intro": "Maler-Kreppbänder sorgen für scharfe, saubere Kanten beim Malen und Lackieren. Der Krepp-Papierträger passt sich der Oberfläche an, lässt sich leicht abreißen und entfernt sich nach Abschluss der Arbeit ohne Klebstoffrückstände.",
        "properties": {
            "Ostré hrany": "Scharfe Kanten",
            "Čisté odlepení": "Sauberes Abziehen",
            "Snadná aplikace": "Einfache Anwendung",
        },
        "property_texts": {
            "Ostré hrany": "Verhindert das Unterlaufen der Farbe unter das Band.",
            "Čisté odlepení": "Hinterlässt nach der Arbeit weder Klebstoff noch Spuren.",
            "Snadná aplikace": "Krepp passt sich der Form an und lässt sich leicht abreißen.",
        },
        "applications": [
            "Innenanstrich und Lackierung",
            "Abkleben von Kanten und Übergängen",
            "Lackierereien und Karosseriewerkstätten",
            "Heimwerker- und Handwerksarbeiten",
        ],
    },
    "udrzitelne-pasky": {
        "title": "Nachhaltige Klebebänder",
        "description": "Innovative Verpackungslösungen aus recycelten Materialien mit minimalem ökologischen Fußabdruck und Unterstützung der Kreislaufwirtschaft.",
        "intro": "Unsere nachhaltige Bandserie wird aus recycelten Materialien hergestellt und minimiert die Umweltbelastung. Sie hilft Unternehmen, ESG-Ziele zu erreichen und ein verantwortungsvolles Markenimage aufzubauen – ohne Kompromisse bei der Leistung.",
        "properties": {
            "Recyklovaný obsah": "Recycelter Anteil",
            "Nižší uhlíková stopa": "Geringerer CO₂-Fußabdruck",
            "Bez kompromisů": "Ohne Kompromisse",
        },
        "property_texts": {
            "Recyklovaný obsah": "Materialien mit hohem Rezyklat-Anteil.",
            "Nižší uhlíková stopa": "Schonendere Produktion und zirkulärer Ansatz.",
            "Bez kompromisů": "Ökologie bei zuverlässiger Klebkraft.",
        },
        "applications": [
            "Unternehmen mit ESG- und Nachhaltigkeitszielen",
            "Grüne Verpackung für E-Shops",
            "Zirkuläre Verpackungsprozesse",
            "Aufbau einer verantwortungsvollen Marke",
        ],
    },
}


def build_sortiment_categories_cs() -> dict[str, Any]:
    categories: dict[str, Any] = {}
    for cat in CATS:
        slug = cat["cat"]
        categories[slug] = {
            "title": cat["title"],
            "description": cat["description"],
            "intro": cat["intro"],
            "properties": {title: text for title, text in cat["properties"]},
            "applications": list(cat["apps"]),
        }
    return categories


def translate_categories(
    cs_categories: dict[str, Any], lang_map: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for slug, cs_cat in cs_categories.items():
        tr = lang_map[slug]
        props_cs = cs_cat["properties"]
        props_out = {}
        for cs_title, cs_text in props_cs.items():
            en_title = tr["properties"].get(cs_title, cs_title)
            en_text = tr["property_texts"].get(cs_title, cs_text)
            props_out[en_title] = en_text
        out[slug] = {
            "title": tr["title"],
            "description": tr["description"],
            "intro": tr["intro"],
            "properties": props_out,
            "applications": tr["applications"],
        }
    return out


def build_cs() -> dict[str, Any]:
    cs_categories = build_sortiment_categories_cs()
    return {
        "meta": {
            "site_name": "Pásky s potiskem",
            "logo_alt": "Pásky s potiskem",
            "home_title": "Pásky s potiskem | Lepicí pásky s logem na míru | ALFA IN",
            "home_description": "Výroba a prodej lepicích pásek s potiskem – pásky s logem pro firmy, e-shopy a sklady. BOPP, eko a speciální pásky, potisk až 8 barev, dodání po celé ČR. Nezávazná kalkulace.",
            "gallery_title": "Galerie pásek s potiskem | Realizace ALFA IN",
            "gallery_description": "Ukázky lepicích pásek s potiskem – loga firem, bezpečnostní pásky, eko varianty a speciální tisky. Inspirace pro vaši pásku s potiskem na míru.",
            "sortiment_title": "Sortiment lepicích pásek | Pásky s potiskem",
            "sortiment_description": "Kompletní sortiment lepicích pásek s potiskem – BOPP, BOPET, papírové, eko a speciální pásky. Vyberte materiál a poptávejte pásku na míru od výrobce ALFA IN.",
        },
        "nav": {
            "tagline": "ALFA IN - výroba, poradenství, prodej a servis",
            "menu": "Otevřít menu",
            "menu_close": "Zavřít menu",
            "main_nav_label": "Hlavní navigace",
            "home": "Úvod",
            "gallery": "Galerie",
            "sortiment": "Sortiment",
            "references": "Reference",
            "contacts": "Kontakty",
            "facebook": "Facebook",
            "instagram": "Instagram",
            "youtube": "YouTube",
        },
        "info_banner": {
            "aria_label": "Důležité informace",
            "messages": [
                "Srpen: výroba a logistika mají 3týdenní výluku. Objednávky s dodáním před výlukou zašlete nejpozději do <strong>10. 7. 2026</strong>.",
                "U objednávek z července a srpna platí dodací lhůta 3–4 týdny s dodáním v <strong>září 2026</strong>.",
            ],
        },
        "footer": {
            "address_heading": "Najdete nás na adrese",
            "company": "ALFA IN a.s.",
            "street": "č.p. 74",
            "city": "675 21 Nová Ves u Třebíče",
            "country": "Česká republika",
            "show_on_map": "Ukaž na mapě",
            "email_heading": "Napište na e-mail",
            "phone_heading": "Volejte na číslo",
            "phone_hours": "od 7:00 do 15:30 h",
            "more_contacts": "Další kontakty",
            "social_heading": "Sociální sítě",
            "copyright": "Všechna práva vyhrazena",
            "made_by": "vytvořil",
            "made_by_link": "Jan Sedlář",
        },
        "home": {
            "hero": {
                "badge": "ISO 9001 · Přímo od výrobce",
                "slides": [
                    {
                        "title": "LEPICÍ PÁSKY SE SPODNÍM TISKEM",
                        "subtitle": "Spolehlivé BOPP pásky s tiskem chráněným pod folií i eko varianty pro udržitelné balení.",
                    },
                    {
                        "title": "PROČ SI VYBRAT NÁS?",
                        "subtitle": "Více než 20 let zkušeností a spolupráce s e-shopy i průmyslem. Spolehlivost, rychlé dodání a individuální přístup ke každé zakázce.",
                    },
                    {
                        "title": "OTESTUJTE NAŠI KVALITU VE SVÉM PROVOZU",
                        "subtitle": "Bezplatný vzorek nebo nezávazná kalkulace na míru. Přesvědčte se o odolnosti a pevnosti lepidla ještě před objednávkou.",
                    },
                ],
                "cta_offer": "Prohlédnout nabídku",
                "cta_quote": "Nezávazná kalkulace",
                "cta_sample": "Vyžádat vzorky",
            },
            "about": {
                "label": "O nás",
                "title": "Tradiční český dodavatel pásek s potiskem i bez",
                "lead": "Již více než 30 let pomáháme firmám bezpečně balit jejich zásilky a budovat silnou značku přímo na balicích materiálech. Nabízíme lepicí pásky s vlastním potiskem i v neutrální variantě bez potisku.",
                "body1_prefix": "Naše ",
                "body1_highlight": "moderní výrobní zázemí",
                "body1_tooltip": "Nevyrábíme totiž pouze lepicí pásky, ale přímo i samotné fólie, což nám v případě surovinové krize na trhu dává značnou konkurenční výhodu.",
                "body1_suffix": " nám umožňuje flexibilně reagovat na potřeby jak malých e-shopů, tak velkých průmyslových podniků. Zakládáme si na precizním tisku (až 8 barev), špičkové kvalitě použitých lepidel (HOT MELT a Akryl) a rychlém doručení po celé České republice i Evropské unii.",
                "body1": "Naše moderní výrobní zázemí nám umožňuje flexibilně reagovat na potřeby jak malých e-shopů, tak velkých průmyslových podniků. Zakládáme si na precizním tisku (až 8 barev), špičkové kvalitě použitých lepidel (HOT MELT a Akryl) a rychlém doručení po celé České republice i Evropské unii.",
                "body2": "Díky certifikovaným procesům ISO 9001 a používání ekologicky udržitelných materiálů jsme stabilním partnerem pro více než 300 aktivních odběratelů.",
                "image_alt": "Výroba lepicích pásek ALFA IN",
                "team_title": "Tým ALFA IN",
                "team_subtitle": "Tradice, zkušenosti a osobní přístup ke každé zakázce",
            },
            "references": {
                "label": "Reference",
                "title": "Spokojení zákazníci napříč obory",
                "subtitle": "Firmy, které na našich páskách s potiskem spoléhají každý den od e-commerce po výrobu a zdravotnictví.",
                "stat_customers": "aktivních odběratelů",
                "stat_experience": "zkušeností s potiskem",
                "stat_iso": "certifikovaná výroba",
                "carousel_label": "Firmy, které s námi spolupracují",
            },
            "lepidla": {
                "label": "Průvodce výběrem",
                "title": "Jaké lepidlo zvolit?",
                "hot_melt_badge": "Chlad & rychlost",
                "hot_melt_title": "HOT MELT",
                "hot_melt_subtitle": "Syntetický kaučuk",
                "hot_melt_text": "Ideální volba do chladnějšího prostředí a nevytápěných skladů. Vyznačuje se extrémně rychlým a silným přilnutím k podkladu ihned po zalepení. Nelze snadno odlepit z fixační stretch fólie.",
                "acryl_badge": "Ticho & UV odolnost",
                "acryl_title": "Akryl",
                "acryl_subtitle": "S nehlučnou úpravou",
                "acryl_text": "Zajišťuje tiché a komfortní odvíjení, které oceníte ve velkých balicích halách. Je vysoce odolné proti UV záření a stárnutí, což z něj dělá perfektní volbu pro dlouhodobé skladování zboží.",
            },
            "sustainability": {
                "label": "Ekologie & udržitelnost",
                "title": "Udržitelné balení pro Váš e-shop i výrobu",
                "subtitle": "Ekologická stopa obalových materiálů je pro nás prioritou. Nabízíme lepicí pásky vybrané s ohledem na snadnou recyklovatelnost a minimální dopad na životní prostředí.",
                "card1_title": "100% Recyklovatelná fólie",
                "card1_text": "Naše pásky jsou vyrobeny z moderní BOPP fólie, která je plně recyklovatelná. Na rozdíl od starších PVC materiálů při jejím zpracování nevznikají žádné toxické látky a je šetrná k přírodě.",
                "card2_title": "Ekologická lepidla bez rozpouštědel",
                "card2_text": "Používáme výhradně lepidla šetrná k životnímu prostředí. Akrylová lepidla jsou vyrobena na vodní bázi a HOT MELT technologie funguje bez použití jakýchkoliv chemických rozpouštědel či syntetických příměsí.",
                "card3_title": "Bezproblémová recyklace kartonů",
                "card3_text": "Díky pokročilé technologii dokážou moderní recyklační linky naše pásky z papírových krabic snadno oddělit. Vaši zákazníci tak mohou použité krabice bez obav vyhodit přímo do modrého kontejneru.",
            },
            "benefits": {
                "eco_badge": "Udržitelnost",
                "eco_title": "Pásky ECO+ – regenerát z vlastní výroby",
                "eco_text": "Fólie ECO+ vzniká z postindustriálního odpadu při výrobě BOPP fólií – materiál se ihned vrací zpět do oběhu. Volíte podíl regenerátu 50 %, 80 % nebo 100 % při stejné pevnosti jako standardní páska, bez ekologické přirážky. Dostupné jako Akryl i HOT MELT, neutrálně i s potiskem.",
                "eco_link": "Prohlédnout řadu ECO+ →",
                "glue_badge": "Extrémní lepivost",
                "glue_title": "EXTRA GLUE+ (Akryl) a TACK+ (HOT MELT)",
                "glue_text": "Pásky se zvýšenou vrstvou lepidla (33 % resp. 20 %) i s možností pevnější folie oproti standardu, určené i pro velmi obtížné aplikace jako např. velmi těžké balíky, nekvalitní kartony nebo prašné prostředí. Na kartonu drží velmi pevně.",
                "glue_extra_tag": "+33 % lepidla",
            },
            "form": {
                "label": "Poptávka",
                "title": "Mám zájem o kalkulaci",
                "open_3d": "Otevřít interaktivní 3D návrhář",
                "open_3d_hint": "Vyzkoušejte materiál, barvu a potisk v prostorném 3D náhledu",
                "step_label": "Krok {current} ze {total}",
                "steps": ["Specifikace produktu", "Rozměry a množství", "Kontaktní údaje"],
                "step1_title": "Specifikace produktu",
                "step1_hint": "Vyberte materiál a případně konkrétní pásku, typ lepidla, podkladovou barvu a počet barev k tisku.",
                "material_label": "Typ materiálu",
                "material_placeholder": "Vyberte materiál…",
                "product_label": "Konkrétní páska",
                "product_placeholder": "Vyberte pásku (volitelné)…",
                "catalog_error": "Katalog se nepodařilo načíst",
                "tape_type": "Typ lepidla",
                "acryl_no_silent_title": "Bez nehlučného činidla",
                "acryl_no_silent_text": "Standardně je u Akryl pásek tiché odvíjení. Zaškrtněte, pokud preferujete variantu bez této úpravy.",
                "base_color": "Podkladová barva",
                "print_colors": "Počet barev k tisku",
                "hot_melt_hint": "Syntetický kaučuk",
                "acryl_hint": "vodní disperze",
                "colors": {
                    "bila": "bílá",
                    "hneda": "hnědá",
                    "transparentni": "transp.",
                    "jina": "jiná",
                },
                "continue": "Pokračovat",
                "back": "Zpět",
                "step2_title": "Rozměry a množství",
                "step2_hint": "Upřesněte rozměry pásky a plánované objednávky.",
                "design_recap_label": "Váš 3D návrh:",
                "design_recap_empty": "bez textu",
                "width_label": "Šíře pásky v mm",
                "length_label": "Délka pásky v metrech",
                "quantity_label": "Poptávané množství v kusech",
                "quantity_hint": "Zadejte číslo podle zvoleného lepidla.",
                "quantity_min": "Akryl od 360 ks, HOT MELT od 504 ks.",
                "quantity_min_acryl": "Minimální množství od 360 ks (Akryl).",
                "quantity_min_hotmelt": "Minimální množství od 504 ks (HOT MELT).",
                "quantity_tip": "Akryl od 360 ks, HOT MELT od 504 ks. Dodání cca 3–4 týdny.",
                "quantity_tip_acryl": "Minimální množství od 360 ks (Akryl). Dodání cca 3–4 týdny.",
                "quantity_tip_hotmelt": "Minimální množství od 504 ks (HOT MELT). Dodání cca 3–4 týdny.",
                "quantity_success": "🔥 Skvělá volba! Máte dopravu zdarma. Doprava trvá přibližně 3–4 týdny.",
                "validation": {
                    "material_required": "Vyberte materiál ze seznamu.",
                    "required": "Vyplňte toto pole.",
                    "email_required": "Zadejte e-mailovou adresu.",
                    "email_invalid": "Zadejte platný e-mail.",
                    "gdpr_required": "Pro odeslání je nutný souhlas se zpracováním údajů.",
                },
                "sample_note_btn": "Mám zájem o vzorek",
                "sample_note_text": "Mám zájem o testovací vzorek.",
                "order_period_label": "Předpokládaná perioda objednávky",
                "order_periods": {
                    "monthly": "Každý měsíc",
                    "quarterly": "Každé 3 měsíce",
                    "biannual": "Jednou za 6 měsíců",
                    "annual": "Jednou za 1 rok",
                },
                "step3_title": "Firemní a kontaktní údaje",
                "step3_hint": "Doplňte údaje pro zpracování nezávazné kalkulace.",
                "company_label": "Název společnosti",
                "ico_label": "Vložte IČ vaší společnosti",
                "name_label": "Jméno a příjmení (Kontaktní osoba)",
                "email_label": "E-mail",
                "phone_label": "Telefon",
                "note_label": "Poznámka",
                "gdpr": "Odesláním souhlasíte se zpracováním osobních údajů",
                "gdpr_before": "Odesláním souhlasíte se",
                "gdpr_link": "zpracováním osobních údajů",
                "gdpr_modal": {
                    "title": "Zpracování osobních údajů",
                    "close": "Zavřít",
                    "intro": "Informace podle čl. 13 nařízení GDPR k vyplnění a odeslání poptávkového formuláře na této stránce.",
                    "controller_heading": "Správce osobních údajů",
                    "controller": "ALFA IN a.s., IČ 255 35 366, č.p. 74, 675 21 Nová Ves u Třebíče. Kontakt: epo@alfain.eu, tel. +420 568 840 009, www.alfain.eu",
                    "data_heading": "Zpracovávané údaje",
                    "data": "Jméno a příjmení, název společnosti, IČO, e-mail, telefon, poznámka a parametry poptávky uvedené ve formuláři.",
                    "purpose_heading": "Účel a právní základ",
                    "purpose": "Vyřízení poptávky, příprava nezávazné kalkulace a následná komunikace. Právním titulem je váš souhlas (čl. 6 odst. 1 písm. a) GDPR) a jednání před uzavřením smlouvy / plnění smlouvy (čl. 6 odst. 1 písm. b) GDPR).",
                    "retention_heading": "Doba uchovávání",
                    "retention": "Po dobu vyřízení poptávky a nejdéle 4 roky od posledního kontaktu, pokud nedojde k uzavření smlouvy; v případě smluvního vztahu po dobu trvání smlouvy a dále dle zákona.",
                    "recipients_heading": "Příjemci údajů",
                    "recipients": "Údaje mohou být zpřístupněny zpracovatelům (IT správa, hosting, e-mailové služby) na základě smluv o zpracování osobních údajů a příslušným orgánům, pokud to ukládá zákon.",
                    "rights_heading": "Vaše práva",
                    "rights": "Máte právo na přístup, opravu, výmaz, omezení zpracování, přenositelnost údajů, vznesení námitky a podání stížnosti u Úřadu pro ochranu osobních údajů (www.uoou.cz). Žádosti zasílejte na epo@alfain.eu.",
                    "full_link": "Úplné znění zásad ochrany osobních údajů",
                },
                "submit": "Odeslat poptávku",
                "modal_title": "Interaktivní 3D návrhář",
                "modal_subtitle": "Materiál, barva a potisk v reálném čase",
                "modal_bg_label": "Pozadí studia",
                "modal_bg_white": "Bílé pozadí",
                "modal_bg_light": "Světle šedé pozadí",
                "modal_bg_dark": "Tmavě šedé pozadí",
                "modal_box_toggle": "Zobrazit na krabici",
                "modal_rotate_hint": "Tažením myší otočíte model o 360°",
                "accordion_material": "Materiál a podklad",
                "accordion_dimensions": "Rozměry pásky",
                "accordion_print": "Potisk a text",
                "width_short": "Šíře pásky",
                "length_short": "Délka / Návin",
            },
            "contacts": {
                "label": "Tým",
                "title": "KONTAKTY NA ODDĚLENÍ",
                "karel_name": "Ing. Karel Petrák",
                "karel_role": "Zastoupení pro prodej balicích pásek",
                "vojtech_name": "Vojtěch Petrák",
                "vojtech_role": "Asistent prodeje",
                "more_contacts": "Další kontakty",
            },
            "sample": {
                "label": "Testovací vzorek",
                "title": "Nejste si jistí výběrem? Pošleme Vám vzorek zdarma.",
                "text": "Chápeme, že kvalita lepicí pásky je pro hladký chod Vaší logistiky klíčová. Vyplňte poptávku a poznámku o testovací vzorek doplníme za vás.",
                "cta": "Mám zájem o vzorek",
            },
        },
        "gallery": {
            "ui": {
                "label": "Galerie",
                "title": "Ukázky naší práce",
                "subtitle": "Reálné reference z výroby i ukázky technologií tisku, filtrujte podle typu potisku, lepidla nebo odvětví.",
                "cta_custom": "Chci vlastní potisk",
            },
            "filters": {
                "filter": "Filtr",
                "clear_all": "Vymazat vše",
                "groups": {
                    "category": {
                        "label": "Typ tisku",
                        "options": {
                            "jednobarevny": "Jednobarevný tisk",
                            "vicebarevny": "Vícebarevný / Rototisk",
                            "bezpecnostni": "Bezpečnostní pásky",
                            "logisticke": "Logistické / Výstražné",
                            "vyroba": "Výroba / sklad",
                        },
                    },
                    "adhesive": {
                        "label": "Lepidlo",
                        "options": {
                            "hot-melt": "HOT MELT",
                            "acryl": "Akryl",
                        },
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
                            "production": "Výroba a sklad",
                        },
                    },
                },
            },
            "sections": {
                "featured": "Vybrané ukázky",
                "references_title": "Reálné reference",
                "references_subtitle": "",
                "production_title": "Výroba a sklad",
                "production_subtitle": "Automatizované sklady, výrobní linky a suroviny – Empoli a Atessa.",
                "demos_title": "Možnosti tisku a technologie",
                "demos_subtitle": "Ukázky bezpečnostních, logistických a speciálních řešení, ilustrace technologií, které nabízíme.",
                "empty": "Žádná ukázka neodpovídá vybraným filtrům. Zkuste ubrat některý z filtrů.",
            },
            "cards": {
                "view_detail": "Zobrazit detail",
                "view_detail_aria": "Zobrazit detail: {title}",
                "featured_badge": "Vybraná ukázka",
                "technology_badge": "Technologie",
                "technology_demo": "Ukázka technologie",
                "production_badge": "Výroba",
            },
            "lightbox": {
                "close": "Zavřít",
                "prev": "Předchozí",
                "next": "Další",
                "cta": "Chci podobný potisk",
                "meta_industry": "Odvětví",
                "meta_width": "Šířka",
                "meta_colors": "Barvy",
                "meta_adhesive": "Lepidlo",
                "meta_location": "Lokalita",
            },
            "cta": {
                "title": "Máte vlastní logo?",
                "text": "Připravíme vám nezávaznou kalkulaci a vzorek potisku. Stačí nám poslat logo a požadované parametry pásky.",
                "button": "Nezávazně poptat",
            },
        },
        "sortiment": {
            "ui": {
                "label": "Sortiment",
                "title": "Objevte naše lepicí pásky",
                "subtitle": "Vyberte typ produktu podle materiálu a určení. U každé kategorie najdete detailní přehled dostupných variant.",
                "filter": "Filtr",
                "clear_all": "Vymazat vše",
                "results_title": "Nalezené produkty podle filtrů",
                "empty": "Žádná páska neodpovídá vybrané kombinaci filtrů. Zkuste ubrat některý z filtrů.",
                "show_products": "Zobrazit produkty",
                "cta_quote": "Nezávazná kalkulace",
            },
            "filters": {
                "properties": {
                    "label": "Vlastnosti",
                    "ekologicke": "Ekologické",
                    "tiche": "Tiché (Low Noise)",
                    "odstranitelne": "Odstranitelné bez stop",
                    "vyztuzene": "Vyztužené",
                },
                "resistance": {
                    "label": "Odolnost",
                    "mrazuvzdorne": "Mrazuvzdorné (do −70 °C)",
                    "vysoke-teploty": "Vysoké teploty",
                    "chemicka-odolnost": "Chemická odolnost",
                },
                "usage": {
                    "label": "Použití",
                    "rucni": "Ruční aplikace",
                    "stroje": "Stroje a baličky",
                },
            },
            "categories": cs_categories,
        },
        "js": {
            "gallery": {
                "remove_filter": "Odebrat filtr",
                "count_all": "{count} ukázek",
                "count_filtered": "Zobrazeno {visible} z {total}",
                "color_one": "1 barva",
                "color_few": "{n} barvy",
                "color_many": "{n} barev",
            },
            "sortiment": {
                "remove_filter": "Odebrat filtr",
                "product_one": "1 produkt",
                "product_few": "{n} produkty",
                "product_many": "{n} produktů",
                "detail": "Detail",
                "inquire": "Poptat",
            },
            "form": {
                "step_label": "Krok {current} ze {total}",
            },
        },
    }


def build_en(cs: dict[str, Any], cs_categories: dict[str, Any]) -> dict[str, Any]:
    return {
        "meta": {
            "site_name": "Printed Packaging Tapes",
            "logo_alt": "Printed packaging tapes",
            "home_title": "Home | Printed Packaging Tapes",
            "home_description": "Printed packaging tapes | Manufacturing and supply of custom printed adhesive tapes by ALFA IN a.s.",
            "gallery_title": "Gallery | Printed Packaging Tapes",
            "gallery_description": "Gallery of printed packaging tape samples by ALFA IN a.s., single-colour print, rotogravure, security and logistics tapes.",
            "sortiment_title": "Product Range | Printed Packaging Tapes",
            "sortiment_description": "ALFA IN adhesive tape range, BOPP tapes HOT MELT and Akryl, special lines and ECO products with custom printing.",
        },
        "nav": {
            "tagline": "ALFA IN, manufacturing, consulting, sales and service",
            "menu": "Open menu",
            "menu_close": "Close menu",
            "main_nav_label": "Main navigation",
            "home": "Home",
            "gallery": "Gallery",
            "sortiment": "Products",
            "references": "References",
            "contacts": "Contact",
            "facebook": "Facebook",
            "instagram": "Instagram",
            "youtube": "YouTube",
        },
        "info_banner": {
            "aria_label": "Important information",
            "messages": [
                "August: production and logistics will be shut down for 3 weeks. To receive delivery before the shutdown, place your order by <strong>10 July 2026</strong>.",
                "For July and August orders, the delivery time is 3–4 weeks with delivery in <strong>September 2026</strong>.",
            ],
        },
        "footer": {
            "address_heading": "Visit us at",
            "company": "ALFA IN a.s.",
            "street": "No. 74",
            "city": "675 21 Nová Ves u Třebíče",
            "country": "Czech Republic",
            "show_on_map": "Show on map",
            "email_heading": "Email us",
            "phone_heading": "Call us",
            "phone_hours": "7:00 a.m. – 3:30 p.m.",
            "more_contacts": "More contacts",
            "social_heading": "Social media",
            "copyright": "All rights reserved",
            "made_by": "created by",
            "made_by_link": "Jan Sedlář",
        },
        "home": {
            "hero": {
                "badge": "ISO 9001 · Direct from the manufacturer",
                "slides": [
                    {
                        "title": "ADHESIVE TAPES WITH REVERSE PRINTING",
                        "subtitle": "Reliable BOPP tapes with print protected under the film, plus eco options for sustainable packaging.",
                    },
                    {
                        "title": "WHY CHOOSE US?",
                        "subtitle": "Over 20 years of experience with e-commerce and industry. Reliability, fast delivery and a personal approach to every order.",
                    },
                    {
                        "title": "TEST OUR QUALITY IN YOUR OPERATION",
                        "subtitle": "Request a free sample or a no-obligation custom quote. Check strength and adhesion before you order.",
                    },
                ],
                "cta_offer": "Browse our range",
                "cta_quote": "Request a quote",
                "cta_sample": "Request samples",
            },
            "about": {
                "label": "About us",
                "title": "Traditional Czech supplier of printed and plain tapes",
                "lead": "For more than 30 years we have helped companies pack their shipments securely and build a strong brand directly on packaging materials. We offer custom-printed adhesive tapes as well as plain neutral tapes.",
                "body1_prefix": "Our ",
                "body1_highlight": "modern production facility",
                "body1_tooltip": "We do not only manufacture adhesive tapes, we also produce the films ourselves, which gives us a significant competitive advantage when raw materials are in short supply.",
                "body1_suffix": " allows us to respond flexibly to the needs of both small e-shops and large industrial enterprises. We pride ourselves on precise printing (up to 8 colours), premium adhesive quality (HOT MELT and Akryl) and fast delivery throughout the Czech Republic and the European Union.",
                "body1": "Our modern production facility allows us to respond flexibly to the needs of both small e-shops and large industrial enterprises. We pride ourselves on precise printing (up to 8 colours), premium adhesive quality (Hot Melt, Acrylic) and fast delivery throughout the Czech Republic.",
                "body2": "Thanks to ISO 9001 certified processes and the use of ecological, sustainable materials, we are a reliable partner for more than 300 active customers.",
                "image_alt": "ALFA IN adhesive tape production",
                "team_title": "ALFA IN team",
                "team_subtitle": "Tradition, experience and a personal approach to every order",
            },
            "references": {
                "label": "References",
                "title": "Satisfied customers across industries",
                "subtitle": "Companies that rely on our printed tapes every day, from e-commerce to manufacturing and healthcare.",
                "stat_customers": "active customers",
                "stat_experience": "years of printing experience",
                "stat_iso": "certified production",
                "carousel_label": "Companies we work with",
            },
            "lepidla": {
                "label": "Selection guide",
                "title": "Which adhesive should you choose?",
                "hot_melt_badge": "Cold & speed",
                "hot_melt_title": "HOT MELT",
                "hot_melt_subtitle": "Synthetic rubber",
                "hot_melt_text": "The ideal choice for cooler environments and unheated warehouses. It bonds to the substrate extremely quickly and strongly immediately after application. It cannot be easily removed from stretch wrap.",
                "acryl_badge": "Quiet & UV resistant",
                "acryl_title": "Akryl",
                "acryl_subtitle": "With low-noise unwind",
                "acryl_text": "Ensures quiet, comfortable unwinding appreciated in large packing halls. Highly resistant to UV radiation and ageing, making it the perfect choice for long-term goods storage.",
            },
            "sustainability": {
                "label": "Ecology & sustainability",
                "title": "Sustainable packaging for your e-shop and production",
                "subtitle": "The environmental footprint of packaging materials is our priority. We offer adhesive tapes selected with easy recyclability and minimal environmental impact in mind.",
                "card1_title": "100% recyclable film",
                "card1_text": "Our tapes are made from modern BOPP film that is fully recyclable. Unlike older PVC materials, no toxic substances are released during processing and it is gentle on the environment.",
                "card2_title": "Eco-friendly solvent-free adhesives",
                "card2_text": "We use exclusively environmentally friendly adhesives. Acrylic adhesives are water-based and Hot Melt technology works without any chemical solvents or synthetic additives.",
                "card3_title": "Easy cardboard recycling",
                "card3_text": "Thanks to advanced technology, modern recycling lines can easily separate our tapes from cardboard boxes. Your customers can dispose of used boxes directly in the paper recycling bin without concern.",
            },
            "benefits": {
                "eco_badge": "Sustainability",
                "eco_title": "ECO+ tapes – regenerated from our own production",
                "eco_text": "ECO+ film is made from post-industrial waste from BOPP film production – the material is returned to the loop immediately. Choose 50%, 80% or 100% regenerated content with the same strength as a standard tape, with no eco surcharge. Available as Akryl or HOT MELT, plain or printed.",
                "eco_link": "Browse the ECO+ range →",
                "glue_badge": "Extreme adhesion",
                "glue_title": "EXTRA GLUE+ (Akryl) and TACK+ (HOT MELT)",
                "glue_text": "Tapes with an increased adhesive layer (33% and 20% respectively) and the option of a stronger film than standard, designed for very demanding applications such as heavy parcels, poor-quality cardboard or dusty environments. They bond extremely firmly to cardboard.",
                "glue_extra_tag": "+33% adhesive",
            },
            "form": {
                "label": "Inquiry",
                "title": "I would like a quote",
                "open_3d": "Open interactive 3D designer",
                "open_3d_hint": "Try material, colour and print in a spacious 3D preview",
                "step_label": "Step {current} of {total}",
                "steps": ["Product specification", "Dimensions and quantity", "Contact details"],
                "step1_title": "Product specification",
                "step1_hint": "Select material and optionally a specific tape, adhesive type, base colour and number of print colours.",
                "material_label": "Material type",
                "material_placeholder": "Select material…",
                "product_label": "Specific tape",
                "product_placeholder": "Select tape (optional)…",
                "catalog_error": "Could not load catalogue",
                "tape_type": "Adhesive type",
                "acryl_no_silent_title": "Without low-noise treatment",
                "acryl_no_silent_text": "Akryl tapes normally have quiet unwinding. Check this if you prefer the variant without this treatment.",
                "base_color": "Base colour",
                "print_colors": "Number of print colours",
                "hot_melt_hint": "Synthetic rubber",
                "acryl_hint": "water-based dispersion",
                "colors": {
                    "bila": "white",
                    "hneda": "brown",
                    "transparentni": "transp.",
                    "jina": "other",
                },
                "continue": "Continue",
                "back": "Back",
                "step2_title": "Dimensions and quantity",
                "step2_hint": "Specify tape dimensions and planned order volumes.",
                "design_recap_label": "Your 3D design:",
                "design_recap_empty": "no text",
                "width_label": "Tape width in mm",
                "length_label": "Tape length in metres",
                "quantity_label": "Requested quantity in rolls",
                "quantity_hint": "Enter a number based on the selected adhesive.",
                "quantity_min": "Akryl from 360 pcs, HOT MELT from 504 pcs.",
                "quantity_min_acryl": "Minimum quantity from 360 pcs (Akryl).",
                "quantity_min_hotmelt": "Minimum quantity from 504 pcs (HOT MELT).",
                "quantity_tip": "Akryl from 360 pcs, HOT MELT from 504 pcs. Delivery approx. 3–4 weeks.",
                "quantity_tip_acryl": "Minimum quantity from 360 pcs (Akryl). Delivery approx. 3–4 weeks.",
                "quantity_tip_hotmelt": "Minimum quantity from 504 pcs (HOT MELT). Delivery approx. 3–4 weeks.",
                "quantity_success": "🔥 Great choice! You have free shipping. Delivery takes approximately 3–4 weeks.",
                "validation": {
                    "material_required": "Please select a material from the list.",
                    "required": "Please fill in this field.",
                    "email_required": "Please enter your email address.",
                    "email_invalid": "Please enter a valid email address.",
                    "gdpr_required": "Consent to data processing is required to submit.",
                },
                "sample_note_btn": "I want a sample",
                "sample_note_text": "I am interested in a test sample.",
                "order_period_label": "Expected order frequency",
                "order_periods": {
                    "monthly": "Every month",
                    "quarterly": "Every 3 months",
                    "biannual": "Every 6 months",
                    "annual": "Once a year",
                },
                "step3_title": "Company and contact details",
                "step3_hint": "Provide details for processing your non-binding quote.",
                "company_label": "Company name",
                "ico_label": "Enter your company registration number",
                "name_label": "Full name (contact person)",
                "email_label": "Email",
                "phone_label": "Phone",
                "note_label": "Note",
                "gdpr": "By submitting you agree to the processing of personal data",
                "gdpr_before": "By submitting you agree to the",
                "gdpr_link": "processing of personal data",
                "gdpr_modal": {
                    "title": "Processing of personal data",
                    "close": "Close",
                    "intro": "Information pursuant to Art. 13 GDPR for completing and submitting the inquiry form on this page.",
                    "controller_heading": "Data controller",
                    "controller": "ALFA IN a.s., ID No. 255 35 366, č.p. 74, 675 21 Nová Ves u Třebíče, Czech Republic. Contact: epo@alfain.eu, tel. +420 568 840 009, www.alfain.eu",
                    "data_heading": "Data processed",
                    "data": "Name, company name, company ID, e-mail, phone, note and inquiry parameters entered in the form.",
                    "purpose_heading": "Purpose and legal basis",
                    "purpose": "Handling the inquiry, preparing a non-binding quote and follow-up communication. Legal basis: your consent (Art. 6(1)(a) GDPR) and steps prior to entering into a contract / contract performance (Art. 6(1)(b) GDPR).",
                    "retention_heading": "Retention period",
                    "retention": "For the time needed to handle the inquiry and at most 4 years from the last contact if no contract is concluded; in the case of a contractual relationship for the duration of the contract and thereafter as required by law.",
                    "recipients_heading": "Recipients",
                    "recipients": "Data may be disclosed to processors (IT administration, hosting, e-mail services) under data processing agreements and to relevant authorities where required by law.",
                    "rights_heading": "Your rights",
                    "rights": "You have the right of access, rectification, erasure, restriction of processing, data portability, objection and to lodge a complaint with the Office for Personal Data Protection (www.uoou.cz). Send requests to epo@alfain.eu.",
                    "full_link": "Full privacy policy",
                },
                "submit": "Send inquiry",
                "modal_title": "Interactive 3D designer",
                "modal_subtitle": "Material, colour and print in real time",
                "modal_bg_label": "Studio background",
                "modal_bg_white": "White background",
                "modal_bg_light": "Light grey background",
                "modal_bg_dark": "Dark grey background",
                "modal_box_toggle": "Show on a box",
                "modal_rotate_hint": "Drag with the mouse to rotate the model 360°",
                "accordion_material": "Material and base",
                "accordion_dimensions": "Tape dimensions",
                "accordion_print": "Print and text",
                "width_short": "Tape width",
                "length_short": "Length / Roll",
            },
            "contacts": {
                "label": "Team",
                "title": "DEPARTMENT CONTACTS",
                "karel_name": "Ing. Karel Petrák",
                "karel_role": "Sales representative for packaging tapes",
                "vojtech_name": "Vojtěch Petrák",
                "vojtech_role": "Sales assistant",
                "more_contacts": "More contacts",
            },
            "sample": {
                "label": "Test sample",
                "title": "Not sure which tape to choose? We will send you a free sample.",
                "text": "We understand that tape quality is key to smooth logistics. Fill in the inquiry form and we will add the test sample note for you.",
                "cta": "I want a sample",
            },
        },
        "gallery": {
            "ui": {
                "label": "Gallery",
                "title": "Examples of our work",
                "subtitle": "Real production references and print technology showcases, filter by print type, adhesive or industry.",
                "cta_custom": "I want custom printing",
            },
            "filters": {
                "filter": "Filter",
                "clear_all": "Clear all",
                "groups": {
                    "category": {
                        "label": "Print type",
                        "options": {
                            "jednobarevny": "Single-colour print",
                            "vicebarevny": "Multi-colour / Rotogravure",
                            "bezpecnostni": "Security tapes",
                            "logisticke": "Logistics / Warning tapes",
                            "vyroba": "Production / warehouse",
                        },
                    },
                    "adhesive": {
                        "label": "Adhesive",
                        "options": {
                            "hot-melt": "Hot Melt",
                            "acryl": "Acrylic",
                        },
                    },
                    "industry": {
                        "label": "Industry",
                        "options": {
                            "e-commerce": "E-commerce",
                            "vyroba": "Manufacturing",
                            "logistika": "Logistics",
                            "potraviny": "Food industry",
                            "bezpecnost": "Security",
                        },
                    },
                    "type": {
                        "label": "Sample type",
                        "options": {
                            "reference": "Real references",
                            "production": "Production & warehouse",
                        },
                    },
                },
            },
            "sections": {
                "featured": "Featured samples",
                "references_title": "Real references",
                "references_subtitle": "",
                "production_title": "Production & warehouse",
                "production_subtitle": "Automated warehouses, production lines and raw materials – Empoli and Atessa.",
                "demos_title": "Print options and technologies",
                "demos_subtitle": "Examples of security, logistics and special solutions, illustrations of the technologies we offer.",
                "empty": "No sample matches the selected filters. Try removing one of the filters.",
            },
            "cards": {
                "view_detail": "View details",
                "view_detail_aria": "View details: {title}",
                "featured_badge": "Featured sample",
                "technology_badge": "Technology",
                "technology_demo": "Technology showcase",
            },
            "lightbox": {
                "close": "Close",
                "prev": "Previous",
                "next": "Next",
                "cta": "I want similar printing",
                "meta_industry": "Industry",
                "meta_width": "Width",
                "meta_colors": "Colours",
                "meta_adhesive": "Adhesive",
                "meta_location": "Location",
            },
            "cta": {
                "title": "Have your own logo?",
                "text": "We will prepare a non-binding quote and a print sample. Just send us your logo and the required tape parameters.",
                "button": "Request a quote",
            },
        },
        "sortiment": {
            "ui": {
                "label": "Product range",
                "title": "Discover our adhesive tapes",
                "subtitle": "Choose a product type by material and application. Each category includes a detailed overview of available variants.",
                "filter": "Filter",
                "clear_all": "Clear all",
                "results_title": "Products matching your filters",
                "empty": "No tape matches the selected filter combination. Try removing one of the filters.",
                "show_products": "View products",
                "cta_quote": "Request a quote",
            },
            "filters": {
                "properties": {
                    "label": "Properties",
                    "ekologicke": "Eco-friendly",
                    "tiche": "Low noise",
                    "odstranitelne": "Residue-free removable",
                    "vyztuzene": "Reinforced",
                },
                "resistance": {
                    "label": "Resistance",
                    "mrazuvzdorne": "Cold-resistant (down to −70 °C)",
                    "vysoke-teploty": "High temperatures",
                    "chemicka-odolnost": "Chemical resistance",
                },
                "usage": {
                    "label": "Application",
                    "rucni": "Manual application",
                    "stroje": "Machines and packers",
                },
            },
            "categories": translate_categories(cs_categories, CATEGORY_EN),
        },
        "js": {
            "gallery": {
                "remove_filter": "Remove filter",
                "count_all": "{count} samples",
                "count_filtered": "Showing {visible} of {total}",
                "color_one": "1 colour",
                "color_few": "{n} colours",
                "color_many": "{n} colours",
            },
            "sortiment": {
                "remove_filter": "Remove filter",
                "product_one": "1 product",
                "product_few": "{n} products",
                "product_many": "{n} products",
                "detail": "Details",
                "inquire": "Inquire",
            },
            "form": {
                "step_label": "Step {current} of {total}",
            },
        },
    }


def build_de(cs: dict[str, Any], cs_categories: dict[str, Any]) -> dict[str, Any]:
    return {
        "meta": {
            "site_name": "Bedruckte Verpackungsbänder",
            "logo_alt": "Bedruckte Verpackungsbänder",
            "home_title": "Startseite | Bedruckte Verpackungsbänder",
            "home_description": "Bedruckte Verpackungsbänder | Herstellung und Vertrieb bedruckter Klebebänder von ALFA IN a.s.",
            "gallery_title": "Galerie | Bedruckte Verpackungsbänder",
            "gallery_description": "Galerie bedruckter Verpackungsbänder von ALFA IN a.s. – Einfarbigdruck, Rotogravur, Sicherheits- und Logistikbänder.",
            "sortiment_title": "Sortiment | Bedruckte Verpackungsbänder",
            "sortiment_description": "ALFA IN Klebeband-Sortiment – BOPP-Bänder HOT MELT und Akryl, Spezialserien und ECO-Produkte mit Bedruckung.",
        },
        "nav": {
            "tagline": "ALFA IN – Herstellung, Beratung, Vertrieb und Service",
            "menu": "Menü öffnen",
            "menu_close": "Menü schließen",
            "main_nav_label": "Hauptnavigation",
            "home": "Startseite",
            "gallery": "Galerie",
            "sortiment": "Sortiment",
            "references": "Referenzen",
            "contacts": "Kontakt",
            "facebook": "Facebook",
            "instagram": "Instagram",
            "youtube": "YouTube",
        },
        "info_banner": {
            "aria_label": "Wichtige Informationen",
            "messages": [
                "August: Produktion und Logistik sind 3 Wochen lang geschlossen. Bestellungen mit Lieferung vor der Schließung senden Sie bitte bis spätestens <strong>10. 7. 2026</strong>.",
                "Bei Bestellungen aus Juli und August gilt eine Lieferzeit von 3–4 Wochen mit Lieferung im <strong>September 2026</strong>.",
            ],
        },
        "footer": {
            "address_heading": "Besuchen Sie uns unter",
            "company": "ALFA IN a.s.",
            "street": "č.p. 74",
            "city": "675 21 Nová Ves u Třebíče",
            "country": "Tschechische Republik",
            "show_on_map": "Auf Karte anzeigen",
            "email_heading": "Schreiben Sie uns",
            "phone_heading": "Rufen Sie uns an",
            "phone_hours": "7:00 – 15:30 Uhr",
            "more_contacts": "Weitere Kontakte",
            "social_heading": "Soziale Netzwerke",
            "copyright": "Alle Rechte vorbehalten",
            "made_by": "erstellt von",
            "made_by_link": "Jan Sedlář",
        },
        "home": {
            "hero": {
                "badge": "ISO 9001 · Direkt vom Hersteller",
                "slides": [
                    {
                        "title": "KLEBEBÄNDER MIT RÜCKSEITENDRUCK",
                        "subtitle": "Zuverlässige BOPP-Bänder mit unter der Folie geschütztem Druck und Öko-Varianten für nachhaltige Verpackung.",
                    },
                    {
                        "title": "WARUM UNS WÄHLEN?",
                        "subtitle": "Mehr als 20 Jahre Erfahrung mit E-Commerce und Industrie. Zuverlässigkeit, schnelle Lieferung und individueller Ansatz bei jeder Bestellung.",
                    },
                    {
                        "title": "TESTEN SIE UNSERE QUALITÄT IN IHREM BETRIEB",
                        "subtitle": "Kostenloses Muster oder unverbindliche Kalkulation. Überzeugen Sie sich von Festigkeit und Klebkraft vor der Bestellung.",
                    },
                ],
                "cta_offer": "Angebot ansehen",
                "cta_quote": "Unverbindliche Kalkulation",
                "cta_sample": "Muster anfordern",
            },
            "about": {
                "label": "Über uns",
                "title": "Traditioneller tschechischer Lieferant, Klebebänder mit und ohne Druck",
                "lead": "Seit mehr als 30 Jahren helfen wir Unternehmen, ihre Sendungen sicher zu verpacken und eine starke Marke direkt auf Verpackungsmaterialien aufzubauen. Wir bieten Klebebänder mit individuellem Druck sowie neutrale Varianten ohne Druck.",
                "body1_prefix": "Unsere ",
                "body1_highlight": "moderne Produktionsstätte",
                "body1_tooltip": "Wir produzieren nicht nur Klebebänder, sondern auch die Folien selbst – das verschafft uns bei Rohstoffkrisen am Markt einen deutlichen Wettbewerbsvorteil.",
                "body1_suffix": " ermöglicht es uns, flexibel auf die Bedürfnisse kleiner E-Shops wie auch großer Industrieunternehmen zu reagieren. Wir legen Wert auf präzisen Druck (bis 8 Farben), erstklassige Klebstoffqualität (HOT MELT und Akryl) und schnelle Lieferung in der gesamten Tschechischen Republik und der Europäischen Union.",
                "body1": "Unsere moderne Produktionsstätte ermöglicht es uns, flexibel auf die Bedürfnisse kleiner E-Shops wie auch großer Industrieunternehmen zu reagieren. Wir legen Wert auf präzisen Druck (bis 8 Farben), erstklassige Klebstoffqualität (Hot Melt, Acryl) und schnelle Lieferung in der gesamten Tschechischen Republik.",
                "body2": "Dank ISO-9001-zertifizierter Prozesse und dem Einsatz ökologischer, nachhaltiger Materialien sind wir ein zuverlässiger Partner für mehr als 300 aktive Abnehmer.",
                "image_alt": "ALFA IN Klebeband-Produktion",
                "team_title": "Team ALFA IN",
                "team_subtitle": "Tradition, Erfahrung und persönlicher Ansatz bei jedem Auftrag",
            },
            "references": {
                "label": "Referenzen",
                "title": "Zufriedene Kunden aus allen Branchen",
                "subtitle": "Unternehmen, die täglich auf unsere bedruckten Bänder vertrauen, von E-Commerce über Produktion bis Gesundheitswesen.",
                "stat_customers": "aktive Abnehmer",
                "stat_experience": "Jahre Druckerfahrung",
                "stat_iso": "zertifizierte Produktion",
                "carousel_label": "Unternehmen, mit denen wir zusammenarbeiten",
            },
            "lepidla": {
                "label": "Auswahlhilfe",
                "title": "Welchen Klebstoff wählen?",
                "hot_melt_badge": "Kälte & Schnelligkeit",
                "hot_melt_title": "HOT MELT",
                "hot_melt_subtitle": "Synthetischer Kautschuk",
                "hot_melt_text": "Die ideale Wahl für kühlere Umgebungen und unbeheizte Lager. Er haftet extrem schnell und stark unmittelbar nach dem Aufbringen. Lässt sich nicht leicht von Stretchfolie ablösen.",
                "acryl_badge": "Leise & UV-beständig",
                "acryl_title": "Akryl",
                "acryl_subtitle": "Mit geräuscharmem Abrollen",
                "acryl_text": "Sorgt für leises, komfortables Abrollen in großen Verpackungshallen. Hochbeständig gegen UV-Strahlung und Alterung – die perfekte Wahl für langfristige Lagerung.",
            },
            "sustainability": {
                "label": "Ökologie & Nachhaltigkeit",
                "title": "Nachhaltige Verpackung für Ihren E-Shop und Ihre Produktion",
                "subtitle": "Der ökologische Fußabdruck von Verpackungsmaterialien hat für uns Priorität. Wir bieten Klebebänder, die mit Blick auf einfache Recycelbarkeit und minimale Umweltbelastung ausgewählt wurden.",
                "card1_title": "100 % recycelbare Folie",
                "card1_text": "Unsere Bänder bestehen aus moderner BOPP-Folie, die vollständig recycelbar ist. Im Gegensatz zu älteren PVC-Materialien entstehen bei der Verarbeitung keine giftigen Stoffe.",
                "card2_title": "Ökologische lösemittelfreie Klebstoffe",
                "card2_text": "Wir verwenden ausschließlich umweltfreundliche Klebstoffe. Acrylklebstoffe sind wasserbasiert und die Hot-Melt-Technologie arbeitet ohne chemische Lösungsmittel.",
                "card3_title": "Problemloses Karton-Recycling",
                "card3_text": "Dank moderner Technologie können Recyclinganlagen unsere Bänder leicht von Kartons trennen. Ihre Kunden können verwendete Kartons bedenkenlos in die Papiertonne werfen.",
            },
            "benefits": {
                "eco_badge": "Nachhaltigkeit",
                "eco_title": "ECO+-Bänder – Regenerat aus eigener Produktion",
                "eco_text": "ECO+-Folie entsteht aus postindustriellem Abfall der BOPP-Folienproduktion – das Material wird sofort in den Kreislauf zurückgeführt. Wählen Sie 50 %, 80 % oder 100 % Regeneratanteil bei gleicher Festigkeit wie Standardband, ohne Öko-Aufpreis. Erhältlich als Akryl oder HOT MELT, neutral oder bedruckt.",
                "eco_link": "ECO+-Serie ansehen →",
                "glue_badge": "Extreme Klebkraft",
                "glue_title": "EXTRA GLUE+ (Akryl) und TACK+ (HOT MELT)",
                "glue_text": "Bänder mit erhöhter Klebstoffschicht (33 % bzw. 20 %) und optional stärkerer Folie für anspruchsvolle Anwendungen wie schwere Pakete, minderwertigen Karton oder staubige Umgebungen. Haften extrem fest auf Karton.",
                "glue_extra_tag": "+33 % Klebstoff",
            },
            "form": {
                "label": "Anfrage",
                "title": "Ich interessiere mich für eine Kalkulation",
                "open_3d": "Interaktiven 3D-Designer öffnen",
                "open_3d_hint": "Testen Sie Material, Farbe und Druck in einer großzügigen 3D-Vorschau",
                "step_label": "Schritt {current} von {total}",
                "steps": ["Produktspezifikation", "Abmessungen und Menge", "Kontaktdaten"],
                "step1_title": "Produktspezifikation",
                "step1_hint": "Wählen Sie Material und optional ein konkretes Band, Klebstofftyp, Grundfarbe und Anzahl der Druckfarben.",
                "material_label": "Materialtyp",
                "material_placeholder": "Material wählen…",
                "product_label": "Konkretes Band",
                "product_placeholder": "Band wählen (optional)…",
                "catalog_error": "Katalog konnte nicht geladen werden",
                "tape_type": "Klebstofftyp",
                "acryl_no_silent_title": "Ohne geräuscharme Behandlung",
                "acryl_no_silent_text": "Akryl-Bänder rollen standardmäßig geräuscharm ab. Aktivieren Sie dies, wenn Sie die Variante ohne diese Behandlung bevorzugen.",
                "base_color": "Grundfarbe",
                "print_colors": "Anzahl der Druckfarben",
                "hot_melt_hint": "Synthetischer Kautschuk",
                "acryl_hint": "wässrige Dispersion",
                "colors": {
                    "bila": "weiß",
                    "hneda": "braun",
                    "transparentni": "transp.",
                    "jina": "andere",
                },
                "continue": "Weiter",
                "back": "Zurück",
                "step2_title": "Abmessungen und Menge",
                "step2_hint": "Geben Sie Bandabmessungen und geplante Bestellmengen an.",
                "design_recap_label": "Ihr 3D-Entwurf:",
                "design_recap_empty": "ohne Text",
                "width_label": "Bandbreite in mm",
                "length_label": "Bandlänge in Metern",
                "quantity_label": "Gewünschte Menge in Rollen",
                "quantity_hint": "Geben Sie eine Zahl je nach gewähltem Klebstoff ein.",
                "quantity_min": "Akryl ab 360 Stk., HOT MELT ab 504 Stk.",
                "quantity_min_acryl": "Mindestmenge ab 360 Stk. (Akryl).",
                "quantity_min_hotmelt": "Mindestmenge ab 504 Stk. (HOT MELT).",
                "quantity_tip": "Akryl ab 360 Stk., HOT MELT ab 504 Stk. Lieferzeit ca. 3–4 Wochen.",
                "quantity_tip_acryl": "Mindestmenge ab 360 Stk. (Akryl). Lieferzeit ca. 3–4 Wochen.",
                "quantity_tip_hotmelt": "Mindestmenge ab 504 Stk. (HOT MELT). Lieferzeit ca. 3–4 Wochen.",
                "quantity_success": "🔥 Ausgezeichnete Wahl! Sie haben kostenlosen Versand. Die Lieferung dauert etwa 3–4 Wochen.",
                "validation": {
                    "material_required": "Bitte wählen Sie ein Material aus der Liste.",
                    "required": "Bitte füllen Sie dieses Feld aus.",
                    "email_required": "Bitte geben Sie Ihre E-Mail-Adresse ein.",
                    "email_invalid": "Bitte geben Sie eine gültige E-Mail-Adresse ein.",
                    "gdpr_required": "Zum Absenden ist die Zustimmung zur Datenverarbeitung erforderlich.",
                },
                "sample_note_btn": "Ich möchte ein Muster",
                "sample_note_text": "Ich interessiere mich für ein Testmuster.",
                "order_period_label": "Voraussichtliche Bestellfrequenz",
                "order_periods": {
                    "monthly": "Jeden Monat",
                    "quarterly": "Alle 3 Monate",
                    "biannual": "Alle 6 Monate",
                    "annual": "Einmal pro Jahr",
                },
                "step3_title": "Firmen- und Kontaktdaten",
                "step3_hint": "Ergänzen Sie die Daten für die unverbindliche Kalkulation.",
                "company_label": "Firmenname",
                "ico_label": "Geben Sie Ihre Firmen-ID ein",
                "name_label": "Vor- und Nachname (Ansprechpartner)",
                "email_label": "E-Mail",
                "phone_label": "Telefon",
                "note_label": "Anmerkung",
                "gdpr": "Mit dem Absenden stimmen Sie der Verarbeitung personenbezogener Daten zu",
                "gdpr_before": "Mit dem Absenden stimmen Sie der",
                "gdpr_link": "Verarbeitung personenbezogener Daten",
                "gdpr_modal": {
                    "title": "Verarbeitung personenbezogener Daten",
                    "close": "Schließen",
                    "intro": "Informationen gemäß Art. 13 DSGVO zum Ausfüllen und Absenden des Anfrageformulars auf dieser Seite.",
                    "controller_heading": "Verantwortlicher",
                    "controller": "ALFA IN a.s., ID-Nr. 255 35 366, č.p. 74, 675 21 Nová Ves u Třebíče, Tschechien. Kontakt: epo@alfain.eu, Tel. +420 568 840 009, www.alfain.eu",
                    "data_heading": "Verarbeitete Daten",
                    "data": "Name, Firmenname, Firmen-ID, E-Mail, Telefon, Anmerkung und im Formular angegebene Anfrageparameter.",
                    "purpose_heading": "Zweck und Rechtsgrundlage",
                    "purpose": "Bearbeitung der Anfrage, Erstellung eines unverbindlichen Angebots und anschließende Kommunikation. Rechtsgrundlage: Ihre Einwilligung (Art. 6 Abs. 1 lit. a DSGVO) und Vertragsanbahnung / Vertragserfüllung (Art. 6 Abs. 1 lit. b DSGVO).",
                    "retention_heading": "Speicherdauer",
                    "retention": "Für die Dauer der Bearbeitung der Anfrage und höchstens 4 Jahre ab dem letzten Kontakt, wenn kein Vertrag zustande kommt; bei Vertragsverhältnis für die Dauer des Vertrags und danach gesetzlich vorgeschrieben.",
                    "recipients_heading": "Empfänger",
                    "recipients": "Daten können Auftragsverarbeitern (IT-Verwaltung, Hosting, E-Mail-Dienste) auf Grundlage von Auftragsverarbeitungsverträgen und zuständigen Behörden offengelegt werden, sofern gesetzlich vorgeschrieben.",
                    "rights_heading": "Ihre Rechte",
                    "rights": "Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit, Widerspruch und Beschwerde beim Amt für den Schutz personenbezogener Daten (www.uoou.cz). Anfragen senden Sie an epo@alfain.eu.",
                    "full_link": "Vollständige Datenschutzrichtlinie",
                },
                "submit": "Anfrage senden",
                "modal_title": "Interaktiver 3D-Designer",
                "modal_subtitle": "Material, Farbe und Druck in Echtzeit",
                "modal_bg_label": "Studio-Hintergrund",
                "modal_bg_white": "Weißer Hintergrund",
                "modal_bg_light": "Hellgrauer Hintergrund",
                "modal_bg_dark": "Dunkelgrauer Hintergrund",
                "modal_box_toggle": "Auf Karton anzeigen",
                "modal_rotate_hint": "Mit der Maus ziehen, um das Modell um 360° zu drehen",
                "accordion_material": "Material und Untergrund",
                "accordion_dimensions": "Bandabmessungen",
                "accordion_print": "Druck und Text",
                "width_short": "Bandbreite",
                "length_short": "Länge / Rolle",
            },
            "contacts": {
                "label": "Team",
                "title": "ABTEILUNGSKONTAKTE",
                "karel_name": "Ing. Karel Petrák",
                "karel_role": "Vertretung für den Verkauf von Verpackungsbändern",
                "vojtech_name": "Vojtěch Petrák",
                "vojtech_role": "Verkaufsassistent",
                "more_contacts": "Weitere Kontakte",
            },
            "sample": {
                "label": "Testmuster",
                "title": "Unsicher bei der Auswahl? Wir senden Ihnen ein kostenloses Muster.",
                "text": "Wir wissen, dass die Qualität des Klebebands für reibungslose Logistik entscheidend ist. Füllen Sie die Anfrage aus, den Hinweis auf ein Testmuster ergänzen wir für Sie.",
                "cta": "Ich möchte ein Muster",
            },
        },
        "gallery": {
            "ui": {
                "label": "Galerie",
                "title": "Beispiele unserer Arbeit",
                "subtitle": "Echte Produktionsreferenzen und Drucktechnologie-Beispiele – filtern Sie nach Drucktyp, Klebstoff oder Branche.",
                "cta_custom": "Ich möchte eigenen Druck",
            },
            "filters": {
                "filter": "Filter",
                "clear_all": "Alle löschen",
                "groups": {
                    "category": {
                        "label": "Drucktyp",
                        "options": {
                            "jednobarevny": "Einfarbig",
                            "vicebarevny": "Mehrfarbig / Rotogravur",
                            "bezpecnostni": "Sicherheitsbänder",
                            "logisticke": "Logistik- / Warnbänder",
                            "vyroba": "Produktion / Lager",
                        },
                    },
                    "adhesive": {
                        "label": "Klebstoff",
                        "options": {
                            "hot-melt": "HOT MELT",
                            "acryl": "Akryl",
                        },
                    },
                    "industry": {
                        "label": "Branche",
                        "options": {
                            "e-commerce": "E-Commerce",
                            "vyroba": "Produktion",
                            "logistika": "Logistik",
                            "potraviny": "Lebensmittel",
                            "bezpecnost": "Sicherheit",
                        },
                    },
                    "type": {
                        "label": "Beispieltyp",
                        "options": {
                            "reference": "Echte Referenzen",
                            "production": "Produktion und Lager",
                        },
                    },
                },
            },
            "sections": {
                "featured": "Ausgewählte Beispiele",
                "references_title": "Echte Referenzen",
                "references_subtitle": "",
                "production_title": "Produktion und Lager",
                "production_subtitle": "Automatisierte Lager, Produktionslinien und Rohstoffe – Empoli und Atessa.",
                "demos_title": "Druckmöglichkeiten und Technologien",
                "demos_subtitle": "Beispiele für Sicherheits-, Logistik- und Speziallösungen – Illustrationen der von uns angebotenen Technologien.",
                "empty": "Kein Beispiel entspricht den gewählten Filtern. Versuchen Sie, einen Filter zu entfernen.",
            },
            "cards": {
                "view_detail": "Details anzeigen",
                "view_detail_aria": "Details anzeigen: {title}",
                "featured_badge": "Ausgewähltes Beispiel",
                "technology_badge": "Technologie",
                "technology_demo": "Technologie-Beispiel",
            },
            "lightbox": {
                "close": "Schließen",
                "prev": "Zurück",
                "next": "Weiter",
                "cta": "Ähnlichen Druck anfragen",
                "meta_industry": "Branche",
                "meta_width": "Breite",
                "meta_colors": "Farben",
                "meta_adhesive": "Klebstoff",
                "meta_location": "Standort",
            },
            "cta": {
                "title": "Haben Sie ein eigenes Logo?",
                "text": "Wir erstellen eine unverbindliche Kalkulation und ein Druckmuster. Senden Sie uns einfach Ihr Logo und die gewünschten Bandparameter.",
                "button": "Unverbindlich anfragen",
            },
        },
        "sortiment": {
            "ui": {
                "label": "Sortiment",
                "title": "Entdecken Sie unsere Klebebänder",
                "subtitle": "Wählen Sie den Produkttyp nach Material und Einsatzzweck. In jeder Kategorie finden Sie eine detaillierte Übersicht der verfügbaren Varianten.",
                "filter": "Filter",
                "clear_all": "Alle löschen",
                "results_title": "Produkte nach Filtern",
                "empty": "Kein Band entspricht der gewählten Filterkombination. Versuchen Sie, einen Filter zu entfernen.",
                "show_products": "Produkte anzeigen",
                "cta_quote": "Unverbindliche Kalkulation",
            },
            "filters": {
                "properties": {
                    "label": "Eigenschaften",
                    "ekologicke": "Ökologisch",
                    "tiche": "Leise (Low Noise)",
                    "odstranitelne": "Rückstandsfrei abziehbar",
                    "vyztuzene": "Verstärkt",
                },
                "resistance": {
                    "label": "Beständigkeit",
                    "mrazuvzdorne": "Kältebeständig (bis −70 °C)",
                    "vysoke-teploty": "Hohe Temperaturen",
                    "chemicka-odolnost": "Chemische Beständigkeit",
                },
                "usage": {
                    "label": "Einsatz",
                    "rucni": "Manuelle Anwendung",
                    "stroje": "Maschinen und Packstationen",
                },
            },
            "categories": translate_categories(cs_categories, CATEGORY_DE),
        },
        "js": {
            "gallery": {
                "remove_filter": "Filter entfernen",
                "count_all": "{count} Beispiele",
                "count_filtered": "{visible} von {total} angezeigt",
                "color_one": "1 Farbe",
                "color_few": "{n} Farben",
                "color_many": "{n} Farben",
            },
            "sortiment": {
                "remove_filter": "Filter entfernen",
                "product_one": "1 Produkt",
                "product_few": "{n} Produkte",
                "product_many": "{n} Produkte",
                "detail": "Details",
                "inquire": "Anfragen",
            },
            "form": {
                "step_label": "Schritt {current} von {total}",
            },
        },
    }


def write_json(path: Path, data: dict[str, Any]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    return len(text.splitlines())


def finalize_locale(data: dict[str, Any], locale: str, ns: dict) -> dict[str, Any]:
    out = copy.deepcopy(data)
    out["meta"]["langNames"] = LANG_NAMES
    out["meta"]["htmlLang"] = HTML_LANG[locale]
    if "sortiment" in out:
        out["sortiment"] = merge_into_sortiment(out["sortiment"], locale, ns)
    if "gallery" in out:
        out["gallery"] = merge_into_gallery(out["gallery"], locale)
    return out


def build_it(cs: dict[str, Any], cs_categories: dict[str, Any]) -> dict[str, Any]:
    """Italian locale, based on EN structure with IT copy and category translations."""
    it = copy.deepcopy(build_en(cs, cs_categories))
    it["meta"].update(
        {
            "site_name": "Nastri adesivi stampati",
            "logo_alt": "Nastri adesivi stampati",
            "home_title": "Home | Nastri adesivi stampati",
            "home_description": "Nastri adesivi stampati | Produzione e fornitura di nastri adesivi personalizzati da ALFA IN a.s.",
            "gallery_title": "Galleria | Nastri adesivi stampati",
            "gallery_description": "Galleria di nastri adesivi stampati di ALFA IN a.s., stampa monocolore, rotocalco, nastri di sicurezza e logistici.",
            "sortiment_title": "Assortimento | Nastri adesivi stampati",
            "sortiment_description": "Gamma di nastri adesivi ALFA IN, nastri BOPP HOT MELT e ACRILICI, linee speciali e prodotti ECO con stampa personalizzata.",
        }
    )
    it["nav"] = {
        "tagline": "ALFA IN, produzione, consulenza, vendita e assistenza",
        "menu": "Apri menu",
        "menu_close": "Chiudi menu",
        "main_nav_label": "Navigazione principale",
        "home": "Home",
        "gallery": "Galleria",
        "sortiment": "Assortimento",
        "references": "Referenze",
        "contacts": "Contatti",
        "facebook": "Facebook",
        "instagram": "Instagram",
        "youtube": "YouTube",
    }
    it["info_banner"] = {
        "aria_label": "Informazioni importanti",
        "messages": [
            "Agosto: produzione e logistica saranno ferme per 3 settimane. Per la consegna prima della pausa, inviate l'ordine entro il <strong>10 luglio 2026</strong>.",
            "Per gli ordini di luglio e agosto, i tempi di consegna sono di 3–4 settimane con consegna a <strong>settembre 2026</strong>.",
        ],
    }
    it["footer"] = {
        "address_heading": "Ci trovate qui",
        "company": "ALFA IN a.s.",
        "street": "n. 74",
        "city": "675 21 Nová Ves u Třebíče",
        "country": "Repubblica Ceca",
        "show_on_map": "Mostra sulla mappa",
        "email_heading": "Scriveteci",
        "phone_heading": "Chiamateci",
        "phone_hours": "7:00 – 15:30",
        "more_contacts": "Altri contatti",
        "social_heading": "Social media",
        "copyright": "Tutti i diritti riservati",
        "made_by": "realizzato da",
        "made_by_link": "Jan Sedlář",
    }
    it["home"]["hero"].update(
        {
            "badge": "ISO 9001 · Direttamente dal produttore",
            "slides": [
                {
                    "title": "NASTRI ADESIVI CON STAMPA PROTETTA",
                    "subtitle": "Nastri BOPP affidabili con stampa protetta sotto pellicola e varianti eco per imballaggi sostenibili.",
                },
                {
                    "title": "PERCHÉ SCEGLIERCI?",
                    "subtitle": "Oltre 20 anni di esperienza con e-commerce e industria. Affidabilità, consegna rapida e approccio personalizzato a ogni ordine.",
                },
                {
                    "title": "TESTATE LA NOSTRA QUALITÀ NEL VOSTRO REPARTO",
                    "subtitle": "Campione gratuito o preventivo senza impegno su misura. Verificate resistenza e adesione prima dell'ordine.",
                },
            ],
            "cta_offer": "Scopri la gamma",
            "cta_quote": "Richiedi un preventivo",
            "cta_sample": "Richiedi campioni",
        }
    )
    it["home"]["about"].update(
        {
            "label": "Chi siamo",
            "title": "Fornitore ceco tradizionale, nastri con e senza stampa",
            "lead": "Da oltre 30 anni aiutiamo le aziende a imballare le spedizioni in modo sicuro e a costruire un marchio forte direttamente sui materiali di imballaggio. Offriamo nastri adesivi con stampa personalizzata e anche in variante neutra senza stampa.",
            "body1_prefix": "Il nostro ",
            "body1_highlight": "moderno stabilimento produttivo",
            "body1_tooltip": "Non produciamo solo nastri adesivi, ma anche le pellicole stesse, il che ci offre un significativo vantaggio competitivo in caso di crisi delle materie prime.",
            "body1_suffix": " ci permette di rispondere in modo flessibile alle esigenze sia dei piccoli e-shop sia delle grandi imprese industriali. Puntiamo su una stampa precisa (fino a 8 colori), adesivi premium (HOT MELT e ACRILICO) e consegne rapide in tutta la Repubblica Ceca e nell'Unione europea.",
            "body1": "Il nostro moderno stabilimento ci permette di rispondere in modo flessibile alle esigenze sia dei piccoli e-shop sia delle grandi imprese industriali. Puntiamo su una stampa precisa (fino a 8 colori), adesivi premium (Hot Melt, Acrilico) e consegne rapide in tutta la Repubblica Ceca.",
            "body2": "Grazie a processi certificati ISO 9001 e all'uso di materiali ecologici e sostenibili, siamo un partner affidabile per oltre 300 clienti attivi.",
            "image_alt": "Produzione di nastri adesivi ALFA IN",
            "team_title": "Team ALFA IN",
            "team_subtitle": "Tradizione, esperienza e approccio personale a ogni ordine",
        }
    )
    it["home"]["references"].update(
        {
            "label": "Referenze",
            "title": "Clienti soddisfatti in diversi settori",
            "subtitle": "Aziende che ogni giorno si affidano ai nostri nastri stampati, dall'e-commerce alla produzione e alla sanità.",
            "stat_customers": "clienti attivi",
            "stat_experience": "anni di esperienza nella stampa",
            "stat_iso": "produzione certificata",
            "carousel_label": "Aziende con cui collaboriamo",
        }
    )
    it["home"]["sample"].update(
        {
            "label": "Campione di prova",
            "title": "Non siete sicuri della scelta? Vi invieremo un campione gratuito.",
            "text": "Comprendiamo che la qualità del nastro è fondamentale per una logistica fluida. Compilate il modulo di richiesta e aggiungeremo noi la nota sul campione di prova.",
            "cta": "Voglio un campione",
        }
    )
    it["home"]["lepidla"].update(
        {
            "label": "Guida alla scelta",
            "title": "Quale adesivo scegliere?",
            "hot_melt_badge": "Freddo e velocità",
            "hot_melt_title": "HOT MELT",
            "hot_melt_subtitle": "Gomma sintetica",
            "hot_melt_text": "La scelta ideale per ambienti più freddi e magazzini non riscaldati. Aderisce al supporto in modo estremamente rapido e forte subito dopo l'applicazione. Non può essere rimosso facilmente dalla pellicola stretch.",
            "acryl_badge": "Silenzioso e resistente ai UV",
            "acryl_title": "Akryl",
            "acryl_subtitle": "Con svolgimento silenzioso",
            "acryl_text": "Garantisce uno svolgimento silenzioso e confortevole, apprezzato nelle grandi sale di imballaggio. Altamente resistente ai raggi UV e all'invecchiamento, perfetto per lo stoccaggio a lungo termine.",
        }
    )
    it["home"]["sustainability"].update(
        {
            "label": "Ecologia e sostenibilità",
            "title": "Imballaggio sostenibile per il vostro e-shop e la produzione",
            "subtitle": "L'impronta ambientale dei materiali di imballaggio è la nostra priorità. Offriamo nastri adesivi selezionati per la facile riciclabilità e il minimo impatto ambientale.",
            "card1_title": "Film riciclabile al 100%",
            "card1_text": "I nostri nastri sono realizzati con moderno film BOPP completamente riciclabile. A differenza dei vecchi materiali PVC, durante la lavorazione non vengono rilasciate sostanze tossiche ed è delicato sull'ambiente.",
            "card2_title": "Adesivi ecologici senza solventi",
            "card2_text": "Utilizziamo esclusivamente adesivi rispettosi dell'ambiente. Gli adesivi acrilici sono a base acquosa e la tecnologia Hot Melt funziona senza solventi chimici o additivi sintetici.",
            "card3_title": "Recycling del cartone senza problemi",
            "card3_text": "Grazie alla tecnologia avanzata, le moderne linee di riciclo possono separare facilmente i nostri nastri dalle scatole di cartone. I vostri clienti possono gettare le scatole usate direttamente nel contenitore della carta.",
        }
    )
    it["home"]["benefits"].update(
        {
            "eco_badge": "Sostenibilità",
            "eco_title": "Nastri ECO+ – materiale rigenerato dalla nostra produzione",
            "eco_text": "Il film ECO+ nasce da scarti postindustriali della produzione di film BOPP: il materiale torna subito in circolo. Scegliete il 50%, 80% o 100% di contenuto rigenerato con la stessa resistenza del nastro standard, senza sovrapprezzo ecologico. Disponibili come Akryl o HOT MELT, neutri o stampati.",
            "eco_link": "Scopri la gamma ECO+ →",
            "glue_badge": "Adesione estrema",
            "glue_title": "EXTRA GLUE+ (Akryl) e TACK+ (HOT MELT)",
            "glue_text": "Nastri con strato adesivo aumentato (33% e 20% rispettivamente) e possibilità di un film più resistente rispetto allo standard, progettati per applicazioni molto impegnative come pacchi pesanti, cartone di scarsa qualità o ambienti polverosi. Aderiscono estremamente bene al cartone.",
            "glue_extra_tag": "+33% adesivo",
        }
    )
    it["home"]["contacts"].update(
        {
            "label": "Team",
            "title": "CONTATTI PER REPARTO",
            "karel_name": "Ing. Karel Petrák",
            "karel_role": "Rappresentante vendite nastri da imballaggio",
            "vojtech_name": "Vojtěch Petrák",
            "vojtech_role": "Assistente vendite",
            "more_contacts": "Altri contatti",
        }
    )
    it["home"]["form"].update(
        {
            "label": "Richiesta",
            "title": "Desidero un preventivo",
            "step_label": "Passo {current} di {total}",
            "steps": ["Specifiche prodotto", "Dimensioni e quantità", "Dati di contatto"],
            "step1_title": "Specifiche prodotto",
            "step1_hint": "Selezionate materiale ed eventualmente un nastro specifico, tipo di adesivo, colore di fondo e numero di colori di stampa.",
            "material_label": "Tipo di materiale",
            "material_placeholder": "Seleziona materiale…",
            "product_label": "Nastro specifico",
            "product_placeholder": "Seleziona nastro (facoltativo)…",
            "catalog_error": "Impossibile caricare il catalogo",
            "tape_type": "Tipo di adesivo",
            "hot_melt_hint": "Gomma sintetica",
            "acryl_hint": "dispersione acquosa",
            "base_color": "Colore di fondo",
            "print_colors": "Numero di colori di stampa",
            "colors": {
                "bila": "bianco",
                "hneda": "marrone",
                "transparentni": "transp.",
                "jina": "altro",
            },
            "acryl_no_silent_title": "Senza trattamento antirumore",
            "acryl_no_silent_text": "I nastri Akryl hanno normalmente svolgimento silenzioso. Selezionate se preferite la variante senza questo trattamento.",
            "continue": "Continua",
            "back": "Indietro",
            "step2_title": "Dimensioni e quantità",
            "step2_hint": "Indicate le dimensioni del nastro e i volumi di ordine previsti.",
            "width_label": "Larghezza del nastro in mm",
            "length_label": "Lunghezza del nastro in metri",
            "quantity_label": "Quantità richiesta in rotoli",
            "quantity_hint": "Inserite un numero in base all'adesivo selezionato.",
            "quantity_min": "Akryl da 360 pz, HOT MELT da 504 pz.",
            "quantity_min_acryl": "Quantità minima da 360 pz (Akryl).",
            "quantity_min_hotmelt": "Quantità minima da 504 pz (HOT MELT).",
            "quantity_tip": "Akryl da 360 pz, HOT MELT da 504 pz. Consegna circa 3–4 settimane.",
            "quantity_tip_acryl": "Quantità minima da 360 pz (Akryl). Consegna circa 3–4 settimane.",
            "quantity_tip_hotmelt": "Quantità minima da 504 pz (HOT MELT). Consegna circa 3–4 settimane.",
            "quantity_success": "🔥 Ottima scelta! Avete la spedizione gratuita. La consegna richiede circa 3–4 settimane.",
            "validation": {
                "material_required": "Selezionate un materiale dall'elenco.",
                "required": "Compilate questo campo.",
                "email_required": "Inserite il vostro indirizzo e-mail.",
                "email_invalid": "Inserite un indirizzo e-mail valido.",
                "gdpr_required": "Per l'invio è necessario il consenso al trattamento dei dati.",
            },
            "order_period_label": "Frequenza di ordine prevista",
            "order_periods": {
                "monthly": "Ogni mese",
                "quarterly": "Ogni 3 mesi",
                "biannual": "Ogni 6 mesi",
                "annual": "Una volta all'anno",
            },
            "step3_title": "Dati aziendali e di contatto",
            "step3_hint": "Completate i dati per l'elaborazione del preventivo non vincolante.",
            "company_label": "Nome dell'azienda",
            "ico_label": "Inserite il numero di registrazione della vostra azienda",
            "name_label": "Nome e cognome (persona di contatto)",
            "email_label": "E-mail",
            "phone_label": "Telefono",
            "note_label": "Nota",
            "sample_note_btn": "Voglio un campione",
            "sample_note_text": "Sono interessato a un campione di prova.",
            "gdpr": "Inviando accettate il trattamento dei dati personali",
            "gdpr_before": "Inviando accettate il",
            "gdpr_link": "trattamento dei dati personali",
            "gdpr_modal": {
                "title": "Trattamento dei dati personali",
                "close": "Chiudi",
                "intro": "Informazioni ai sensi dell'art. 13 GDPR per la compilazione e l'invio del modulo di richiesta su questa pagina.",
                "controller_heading": "Titolare del trattamento",
                "controller": "ALFA IN a.s., ID 255 35 366, č.p. 74, 675 21 Nová Ves u Třebíče, Repubblica Ceca. Contatto: epo@alfain.eu, tel. +420 568 840 009, www.alfain.eu",
                "data_heading": "Dati trattati",
                "data": "Nome e cognome, ragione sociale, ID azienda, e-mail, telefono, nota e parametri della richiesta inseriti nel modulo.",
                "purpose_heading": "Finalità e base giuridica",
                "purpose": "Gestione della richiesta, preparazione di un preventivo non vincolante e comunicazione successiva. Base giuridica: il vostro consenso (art. 6 par. 1 lett. a GDPR) e misure precontrattuali / esecuzione del contratto (art. 6 par. 1 lett. b GDPR).",
                "retention_heading": "Periodo di conservazione",
                "retention": "Per il tempo necessario a gestire la richiesta e al massimo 4 anni dall'ultimo contatto se non viene concluso un contratto; in caso di rapporto contrattuale per la durata del contratto e successivamente come richiesto dalla legge.",
                "recipients_heading": "Destinatari",
                "recipients": "I dati possono essere comunicati a responsabili del trattamento (amministrazione IT, hosting, servizi e-mail) sulla base di accordi di trattamento e alle autorità competenti ove richiesto dalla legge.",
                "rights_heading": "I vostri diritti",
                "rights": "Avete diritto di accesso, rettifica, cancellazione, limitazione del trattamento, portabilità dei dati, opposizione e reclamo all'Ufficio per la protezione dei dati personali (www.uoou.cz). Inviate le richieste a epo@alfain.eu.",
                "full_link": "Testo completo dell'informativa sulla privacy",
            },
            "submit": "Invia richiesta",
        }
    )
    it["sortiment"]["categories"] = translate_categories(cs_categories, CATEGORY_IT)
    it["sortiment"]["ui"].update(
        {
            "label": "Assortimento",
            "title": "Scoprite i nostri nastri adesivi",
            "subtitle": "Scegliete il tipo di prodotto in base al materiale e all'utilizzo. In ogni categoria troverete una panoramica dettagliata delle varianti disponibili.",
            "filter": "Filtro",
            "clear_all": "Cancella tutto",
            "results_title": "Prodotti trovati in base ai filtri",
            "empty": "Nessun nastro corrisponde ai filtri selezionati. Provate a rimuoverne alcuni.",
            "show_products": "Mostra prodotti",
            "cta_quote": "Preventivo non vincolante",
        }
    )
    it["gallery"]["ui"].update(
        {
            "label": "Galleria",
            "title": "Esempi del nostro lavoro",
            "subtitle": "Referenze reali dalla produzione ed esempi di tecnologie di stampa, filtrate per tipo di stampa, adesivo o settore.",
            "cta_custom": "Voglio una stampa personalizzata",
        }
    )
    it["gallery"]["sections"].update(
        {
            "featured": "Esempi selezionati",
            "references_title": "Referenze reali",
            "references_subtitle": "",
            "production_title": "Produzione e magazzino",
            "production_subtitle": "Magazzini automatizzati, linee di produzione e materie prime – Empoli e Atessa.",
            "demos_title": "Possibilità di stampa e tecnologie",
            "demos_subtitle": "Esempi di soluzioni di sicurezza, logistica e speciali, illustrazione delle tecnologie che offriamo.",
            "empty": "Nessun esempio corrisponde ai filtri selezionati. Provate a rimuoverne alcuni.",
        }
    )
    it["gallery"]["cards"].update(
        {
            "view_detail": "Visualizza dettagli",
            "view_detail_aria": "Visualizza dettagli: {title}",
            "featured_badge": "Esempio selezionato",
            "technology_badge": "Tecnologia",
            "technology_demo": "Esempio tecnologico",
        }
    )
    it["gallery"]["filters"].update(
        {
            "filter": "Filtro",
            "clear_all": "Cancella tutto",
        }
    )
    it["gallery"]["filters"]["groups"]["category"].update(
        {
            "label": "Tipo di stampa",
            "options": {
                "jednobarevny": "Stampa monocolore",
                "vicebarevny": "Multicolore / Rotocalco",
                "bezpecnostni": "Nastri di sicurezza",
                "logisticke": "Nastri logistici / di avvertimento",
                "vyroba": "Produzione / magazzino",
            },
        }
    )
    it["gallery"]["filters"]["groups"]["adhesive"].update(
        {
            "label": "Adesivo",
            "options": {
                "hot-melt": "Hot Melt",
                "acryl": "Acrilico",
            },
        }
    )
    it["gallery"]["filters"]["groups"]["industry"].update(
        {
            "label": "Settore",
            "options": {
                "e-commerce": "E-commerce",
                "vyroba": "Produzione",
                "logistika": "Logistica",
                "potraviny": "Alimentare",
                "bezpecnost": "Sicurezza",
            },
        }
    )
    it["gallery"]["filters"]["groups"]["type"].update(
        {
            "label": "Tipo di esempio",
            "options": {
                "reference": "Referenze reali",
                "production": "Produzione e magazzino",
            },
        }
    )
    it["gallery"]["lightbox"].update(
        {
            "close": "Chiudi",
            "prev": "Precedente",
            "next": "Avanti",
            "cta": "Voglio una stampa simile",
            "meta_industry": "Settore",
            "meta_width": "Larghezza",
            "meta_colors": "Colori",
            "meta_adhesive": "Adesivo",
            "meta_location": "Località",
        }
    )
    it["gallery"]["cta"].update(
        {
            "title": "Avete un logo?",
            "text": "Prepareremo un preventivo non vincolante e un campione di stampa. Basta inviarci il logo e i parametri desiderati del nastro.",
            "button": "Richiedi senza impegno",
        }
    )
    it["js"]["gallery"].update(
        {
            "remove_filter": "Rimuovi filtro",
            "count_all": "{count} esempi",
            "count_filtered": "Visualizzati {visible} di {total}",
            "color_one": "1 colore",
            "color_few": "{n} colori",
            "color_many": "{n} colori",
        }
    )
    it["js"]["sortiment"].update(
        {
            "remove_filter": "Rimuovi filtro",
            "product_one": "1 prodotto",
            "product_few": "{n} prodotti",
            "product_many": "{n} prodotti",
            "detail": "Dettagli",
            "inquire": "Richiedi",
        }
    )
    it["js"]["form"]["step_label"] = "Passo {current} di {total}"
    return it


def main() -> None:
    cs = build_cs()
    cs_categories = build_sortiment_categories_cs()
    ns = load_gp_namespace()
    locales = {
        "cs": cs,
        "en": build_en(cs, cs_categories),
        "de": build_de(cs, cs_categories),
        "it": build_it(cs, cs_categories),
    }

    print(f"Writing i18n JSON to {OUT_DIR}/")
    for locale, data in locales.items():
        data = finalize_locale(data, locale, ns)
        path = OUT_DIR / f"{locale}.json"
        lines = write_json(path, data)
        print(f"  {path.name}: {lines} lines")


if __name__ == "__main__":
    main()
