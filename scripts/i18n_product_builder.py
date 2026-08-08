#!/usr/bin/env python3
"""Build sortiment product translation data for i18n JSON files."""
from __future__ import annotations

import copy
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN_PRODUCTS = ROOT / "scripts" / "gen_products.py"
SAMPLE_CATEGORIES = frozenset({"bopp-pasky", "bopet-pasky", "papirove-pasky", "udrzitelne-pasky"})
CATEGORY_IT: dict[str, dict] = {
    "papirove-pasky": {
        "title": "Nastri in carta",
        "description": "Una soluzione ecologica per un imballaggio elegante con elevata adesione, ideale per un aspetto pulito e scatole in cartone completamente riciclabili.",
        "intro": "I nastri adesivi in carta combinano un incollaggio affidabile con la massima attenzione all'ambiente. Grazie al supporto in carta, sono completamente riciclabili insieme al cartone e rappresentano una soluzione elegante e ordinata per le aziende attente alla sostenibilità e all'immagine delle proprie spedizioni.",
        "series_note": "C660, C680, C680R, C680RT e C690 sono disponibili per uso manuale e macchine nastratrici e sono prodotti con carta FSC Mix Credit. Tutti questi, insieme al C780, possono essere personalizzati con stampa (fino a 4 colori). C680 e C680R sono disponibili anche in bianco. Licenza FSC®: FSC-C159046.",
        "param_hints": [
            {
                "title": "Adesione sull'acciaio",
                "body": "Misura l'adesione immediata sulla superficie.",
                "highlight": "Standard tipico: 4,0–5,0 N/cm. Valori sopra 6,0 N/cm indicano adesione extra forte.",
            },
            {
                "title": "Resistenza alla trazione",
                "body": "Resistenza alla rottura sotto tensione.",
                "highlight": "Standard per pacchi comuni (fino a ~15 kg): 30–40 N/cm. Spedizioni pesanti e rinforzi: 50+ N/cm.",
            },
            {
                "title": "Allungamento / estensione",
                "body": "Di quanti % il nastro si allunga prima di rompersi.",
                "highlight": "Standard per la carta: 8–12 %. Un allungamento basso (circa 5 %) tiene ferma la scatola senza cedimenti.",
            },
        ],
        "properties": {"Plná recyklovatelnost": "Completamente riciclabile", "Vysoká lepivost": "Elevata adesione", "Čistý design": "Design pulito"},
        "property_texts": {"Plná recyklovatelnost": "Nastro e cartone possono essere conferiti nello stesso contenitore, senza separare i materiali.", "Vysoká lepivost": "Incollaggio affidabile anche su cartone riciclato e superfici irregolari.", "Čistý design": "La superficie opaca della carta ha un aspetto premium e può essere facilmente stampata con il vostro logo."},
        "applications": ["E-shop orientati al packaging sostenibile", "Chiusura di scatole e imballaggi in cartone", "Branding aziendale direttamente sulle spedizioni", "Imballaggio manuale e semiautomatico"],
    },
    "bopp-pasky": {
        "title": "Nastri BOPP",
        "description": "I nastri per imballaggio industriale più diffusi, realizzati in polipropilene biorientato. Offrono eccellente resistenza alla trazione e lunga durata.",
        "intro": "I nastri BOPP sono lo standard per l'imballaggio quotidiano nella produzione, nella logistica e nell'e-commerce. Il film in polipropilene biorientato offre un eccellente rapporto qualità-prezzo, versioni acriliche e hot melt e un'ampia scelta di larghezze e colori.",
        "properties": {"Vynikající poměr cena/výkon": "Eccellente rapporto qualità/prezzo", "Ekologická šetrnost": "Rispetto per l'ambiente", "Fyzikální a chemická stálost": "Stabilità fisica e chimica"},
        "property_texts": {"Vynikající poměr cena/výkon": "Prestazioni elevate a un prezzo conveniente per l'imballaggio quotidiano in industria ed e-commerce.", "Ekologická šetrnost": "Non contiene sostanze dannose per l'ambiente come il PVC.", "Fyzikální a chemická stálost": "Proprietà stabili del film e dell'adesivo durante stoccaggio, trasporto e uso quotidiano."},
        "applications": ["Chiusura standard dei cartoni", "Macchine automatiche per imballaggio", "Spedizioni e logistica di magazzino", "Stampa di loghi e informazioni aziendali"],
    },
    "bopet-pasky": {
        "title": "Nastri BOPET",
        "description": "Nastri in poliestere premium con estrema resistenza allo strappo, agli agenti chimici e alle variazioni di temperatura. Progettati per le applicazioni industriali più impegnative.",
        "intro": "I nastri BOPET a base di film in poliestere sono destinati alle applicazioni in cui i nastri standard non sono sufficienti. Resistono alle alte temperature, agli agenti chimici aggressivi e alle sollecitazioni meccaniche, mantenendo le proprie caratteristiche anche in condizioni estreme.",
        "properties": {"Teplotní odolnost": "Resistenza alla temperatura", "Chemická odolnost": "Resistenza chimica", "Odolnost proti roztržení": "Resistenza allo strappo"},
        "property_texts": {"Teplotní odolnost": "Prestazioni stabili alle alte e alle basse temperature.", "Chemická odolnost": "Resistente a solventi, oli e ambienti aggressivi.", "Odolnost proti roztržení": "Robusto film in poliestere con allungamento minimo."},
        "applications": ["Impianti industriali impegnativi", "Mascheratura nella verniciatura a polvere", "Fissaggio in ambienti ad alta temperatura", "Elettrotecnica e produzione specializzata"],
    },
    "textilni-pasky": {
        "title": "Nastri adesivi telati",
        "description": "Nastri molto resistenti e versatili rinforzati con una rete tessile. Aderiscono perfettamente alle superfici ruvide, si strappano facilmente a mano e sono ideali per riparazioni rapide e fascettatura.",
        "intro": "I nastri telati sono un indispensabile prodotto universale. Il rinforzo tessile conferisce elevata resistenza e consente allo stesso tempo di strapparli facilmente a mano senza forbici. Aderiscono in modo affidabile anche alle superfici ruvide e irregolari.",
        "properties": {"Textilní výztuž": "Rinforzo tessile", "Trhání rukou": "Strappabile a mano", "Přilnavost na drsný povrch": "Adesione su superfici ruvide"},
        "property_texts": {"Textilní výztuž": "Elevata resistenza e protezione dalla perforazione.", "Trhání rukou": "Lavoro rapido senza utensili.", "Přilnavost na drsný povrch": "Aderisce a metallo, legno, cemento e plastica."},
        "applications": ["Riparazioni rapide e giunzioni provvisorie", "Fascettatura e fissaggio di oggetti", "Rinforzo di colli e imballaggi", "Manutenzione, montaggio e lavori artigianali"],
    },
    "vyztuzene-pasky": {
        "title": "Nastri rinforzati",
        "description": "Nastri rinforzati con fibre di vetro longitudinali o incrociate. Offrono la massima resistenza per fissare carichi pesanti, pallet e colli fuori sagoma.",
        "intro": "I nastri rinforzati contengono fibre di vetro disposte longitudinalmente o incrociate che aumentano sensibilmente la resistenza alla trazione. Sono progettati per fissare spedizioni pesanti e fuori sagoma, dove è richiesta la massima affidabilità.",
        "properties": {"Skelná vlákna": "Fibre di vetro", "Nosnost": "Capacità di carico", "Odolnost proti přetržení": "Resistenza alla rottura"},
        "property_texts": {"Skelná vlákna": "Rinforzo longitudinale o incrociato per la massima resistenza.", "Nosnost": "Fissaggio affidabile di carichi pesanti e pallet.", "Odolnost proti přetržení": "Resiste anche a elevati carichi di trazione."},
        "applications": ["Fissaggio di colli pesanti e fuori sagoma", "Messa in sicurezza delle merci sui pallet", "Fascettatura di tubi, profili e barre", "Trasporti ed esportazioni impegnativi"],
    },
    "mopp-pasky": {
        "title": "Nastri MOPP",
        "description": "Nastri mono-orientati con estrema resistenza in una direzione ed elasticità pressoché nulla. Specificamente progettati per fissare elettrodomestici, componenti o pallet.",
        "intro": "I nastri MOPP hanno un film mono-orientato con estrema resistenza longitudinale e allungamento praticamente nullo. Sostituiscono i nastri rinforzati dove è necessario un fissaggio solido senza fibre di vetro.",
        "properties": {"Extrémní pevnost": "Resistenza estrema", "Nulová elasticita": "Elasticità nulla", "Bez skelných vláken": "Senza fibre di vetro"},
        "property_texts": {"Extrémní pevnost": "Elevata resistenza alla trazione in una direzione.", "Nulová elasticita": "Il fissaggio non si allenta nemmeno sotto carico.", "Bez skelných vláken": "Fissaggio pulito senza rilascio di fibre."},
        "applications": ["Fissaggio delle porte degli elettrodomestici", "Messa in sicurezza dei componenti durante il trasporto", "Reggiatura e fissaggio dei pallet", "Fascettatura senza fibre di vetro"],
    },
    "odstranitelne-pasky": {
        "title": "Nastri rimovibili",
        "description": "Nastri con una speciale formulazione adesiva che non lascia residui dopo la rimozione. Ideali per marcature temporanee, protezione di superfici sensibili o processi logistici.",
        "intro": "I nastri rimovibili utilizzano un adesivo speciale che tiene saldamente ma non lascia residui né danneggia la superficie quando viene rimosso. Sono ideali per applicazioni temporanee e per la protezione di materiali delicati.",
        "properties": {"Beze stop": "Senza residui", "Šetrné k povrchu": "Delicato sulle superfici", "Spolehlivá drživost": "Tenuta affidabile"},
        "property_texts": {"Beze stop": "Dopo la rimozione non restano adesivo né residui.", "Šetrné k povrchu": "Non danneggia vernice, vetro o materiali sensibili.", "Spolehlivá drživost": "Tiene per tutta la durata necessaria dell'applicazione."},
        "applications": ["Marcature ed etichette temporanee", "Protezione di superfici sensibili", "Processi logistici e produttivi", "Fissaggi che devono essere rimossi"],
    },
    "malirske-pasky": {
        "title": "Nastri per mascheratura",
        "description": "Nastri in carta crespata progettati per una mascheratura precisa durante la pittura e la verniciatura. Proteggono i bordi dalle sbavature di colore e si rimuovono pulitamente al termine del lavoro.",
        "intro": "I nastri di carta crespata per mascheratura garantiscono bordi netti e puliti durante la pittura e la verniciatura. Il supporto in carta crespata si adatta alla superficie, si strappa facilmente e si rimuove senza residui di adesivo al termine del lavoro.",
        "properties": {"Ostré hrany": "Bordi netti", "Čisté odlepení": "Rimozione pulita", "Snadná aplikace": "Applicazione semplice"},
        "property_texts": {"Ostré hrany": "Impedisce al colore di infiltrarsi sotto il nastro.", "Čisté odlepení": "Non lascia adesivo né segni dopo l'uso.", "Snadná aplikace": "La carta crespata si adatta alla forma e si strappa facilmente."},
        "applications": ["Pittura e verniciatura di interni", "Mascheratura di bordi e passaggi", "Verniciature industriali e carrozzerie", "Lavori fai da te e artigianali"],
    },
    "udrzitelne-pasky": {
        "title": "Nastri sostenibili",
        "description": "Soluzioni di imballaggio innovative realizzate con materiali riciclati, con un impatto ambientale minimo e a sostegno dell'economia circolare.",
        "intro": "La nostra gamma di nastri sostenibili è realizzata con materiali riciclati e progettata per ridurre al minimo l'impatto ambientale. Aiuta le aziende a raggiungere gli obiettivi ESG e a costruire un'immagine di marca responsabile senza compromettere le prestazioni.",
        "properties": {"Recyklovaný obsah": "Contenuto riciclato", "Nižší uhlíková stopa": "Minore impronta di carbonio", "Bez kompromisů": "Senza compromessi"},
        "property_texts": {"Recyklovaný obsah": "Materiali con un'elevata percentuale di riciclato.", "Nižší uhlíková stopa": "Produzione più sostenibile e approccio circolare.", "Bez kompromisů": "Sostenibilità senza rinunciare a un incollaggio affidabile."},
        "applications": ["Aziende con obiettivi ESG e di sostenibilità", "Imballaggi sostenibili per e-shop", "Processi di imballaggio circolari", "Costruzione di un marchio responsabile"],
    },
}

CATEGORY_TITLES = {
    "cs": {slug: data["title"] for slug, data in {
        "udrzitelne-pasky": {"title": "Udržitelné pásky"}, "bopp-pasky": {"title": "BOPP pásky"},
        "bopet-pasky": {"title": "BOPET pásky"}, "papirove-pasky": {"title": "Papírové pásky"},
        "odstranitelne-pasky": {"title": "Odstranitelné pásky"}, "vyztuzene-pasky": {"title": "Vyztužené pásky"},
        "mopp-pasky": {"title": "MOPP pásky"}, "textilni-pasky": {"title": "Textilní lepicí pásky"},
        "malirske-pasky": {"title": "Malířské pásky"},
    }.items()},
    "en": {slug: data["title"] for slug, data in {
        "udrzitelne-pasky": {"title": "Sustainable tapes"}, "bopp-pasky": {"title": "BOPP tapes"},
        "bopet-pasky": {"title": "BOPET tapes"}, "papirove-pasky": {"title": "Paper tapes"},
        "odstranitelne-pasky": {"title": "Removable tapes"}, "vyztuzene-pasky": {"title": "Reinforced tapes"},
        "mopp-pasky": {"title": "MOPP tapes"}, "textilni-pasky": {"title": "Cloth adhesive tapes"},
        "malirske-pasky": {"title": "Masking tapes"},
    }.items()},
    "de": {slug: data["title"] for slug, data in {
        "udrzitelne-pasky": {"title": "Nachhaltige Klebebänder"}, "bopp-pasky": {"title": "BOPP-Klebebänder"},
        "bopet-pasky": {"title": "BOPET-Klebebänder"}, "papirove-pasky": {"title": "Papierklebebänder"},
        "odstranitelne-pasky": {"title": "Abziehbare Klebebänder"}, "vyztuzene-pasky": {"title": "Verstärkte Klebebänder"},
        "mopp-pasky": {"title": "MOPP-Klebebänder"}, "textilni-pasky": {"title": "Gewebe-Klebebänder"},
        "malirske-pasky": {"title": "Malerklebebänder"},
    }.items()},
    "it": {slug: data["title"] for slug, data in CATEGORY_IT.items()},
}

SORTIMENT_PAGE = {
    "cs": {
        "breadcrumb_home": "Domů",
        "breadcrumb_sortiment": "Sortiment",
        "breadcrumb_aria": "Drobečková navigace",
        "section_key_properties": "Klíčové vlastnosti",
        "section_products": "Produkty v této kategorii",
        "section_typical_use": "Typické použití",
        "section_technical_params": "Technické parametry",
        "section_benefits": "Hlavní výhody a použití",
        "section_uses_label": "Typické použití",
        "view_detail": "Zobrazit detail",
        "back_to_sortiment": "Zpět na sortiment",
        "back_to_category": "Zpět na kategorii",
        "back_to_category_short": "Zpět na {category}",
        "params_note": "Uvedené hodnoty jsou orientační a mohou se lišit podle konkrétní šířky, návinu a provedení. Rádi vám připravíme přesnou specifikaci na míru.",
        "tailor_title": "Na míru vašemu provozu",
        "tailor_bullet_width": "Volitelná šířka a délka návinu",
        "tailor_bullet_print": "Barva podkladu a počet barev potisku",
        "tailor_bullet_sample": "Otestování kvality před objednáním",
        "tailor_bullet_consult": "Konzultace parametrů před objednávkou",
        "tailor_bullet_params": "Různé provedení lepidla a nosiče",
        "no_print_note": "Pásku lze objednat i bez potisku.",
        "no_print_body": "Neutrální (nepotištěná) verze stejného materiálu, ideální pro okamžité balení nebo skladové zásoby.",
        "no_print_link": "Zeptejte se na dostupnost",
        "product_card_detail": "Zobrazit detail",
    },
    "en": {
        "breadcrumb_home": "Home",
        "breadcrumb_sortiment": "Product range",
        "breadcrumb_aria": "Breadcrumb navigation",
        "section_key_properties": "Key properties",
        "section_products": "Products in this category",
        "section_typical_use": "Typical applications",
        "section_technical_params": "Technical specifications",
        "section_benefits": "Key benefits and applications",
        "section_uses_label": "Typical applications",
        "view_detail": "View details",
        "back_to_sortiment": "Back to product range",
        "back_to_category": "Back to category",
        "back_to_category_short": "Back to {category}",
        "params_note": "The stated values are indicative and may vary depending on the specific width, roll length and version. We will be happy to prepare an exact specification tailored to your requirements.",
        "tailor_title": "Tailored to your operation",
        "tailor_bullet_width": "Custom width and roll length",
        "tailor_bullet_print": "Base colour and number of print colours",
        "tailor_bullet_sample": "Quality testing before ordering",
        "tailor_bullet_consult": "Parameter consultation before ordering",
        "tailor_bullet_params": "Various adhesive and carrier options",
        "no_print_note": "This tape is also available without printing.",
        "no_print_body": "Neutral (unprinted) version of the same material, ideal for immediate packing or stock.",
        "no_print_link": "Ask about availability",
        "product_card_detail": "View details",
    },
    "de": {
        "breadcrumb_home": "Startseite",
        "breadcrumb_sortiment": "Sortiment",
        "breadcrumb_aria": "Brotkrümelnavigation",
        "section_key_properties": "Wichtige Eigenschaften",
        "section_products": "Produkte dieser Kategorie",
        "section_typical_use": "Typische Anwendungen",
        "section_technical_params": "Technische Daten",
        "section_benefits": "Wichtigste Vorteile und Anwendungen",
        "section_uses_label": "Typische Anwendungen",
        "view_detail": "Details anzeigen",
        "back_to_sortiment": "Zurück zum Sortiment",
        "back_to_category": "Zurück zur Kategorie",
        "back_to_category_short": "Zurück zu {category}",
        "params_note": "Die angegebenen Werte sind Richtwerte und können je nach Breite, Rollenlänge und Ausführung variieren. Gerne erstellen wir Ihnen eine genaue Spezifikation nach Ihren Anforderungen.",
        "tailor_title": "Passend für Ihren Betrieb",
        "tailor_bullet_width": "Wählbare Breite und Rollenlänge",
        "tailor_bullet_print": "Grundfarbe und Anzahl der Druckfarben",
        "tailor_bullet_sample": "Qualitätsprüfung vor der Bestellung",
        "tailor_bullet_consult": "Beratung zu den Parametern vor der Bestellung",
        "tailor_bullet_params": "Verschiedene Klebstoff- und Trägerausführungen",
        "no_print_note": "Dieses Band ist auch ohne Bedruckung erhältlich.",
        "no_print_body": "Neutrale (unbedruckte) Version desselben Materials – ideal für den sofortigen Einsatz oder Lagerbestand.",
        "no_print_link": "Verfügbarkeit anfragen",
        "product_card_detail": "Details anzeigen",
    },
    "it": {
        "breadcrumb_home": "Home",
        "breadcrumb_sortiment": "Assortimento",
        "breadcrumb_aria": "Navigazione a breadcrumb",
        "section_key_properties": "Caratteristiche principali",
        "section_products": "Prodotti di questa categoria",
        "section_typical_use": "Applicazioni tipiche",
        "section_technical_params": "Parametri tecnici",
        "section_benefits": "Vantaggi principali e applicazioni",
        "section_uses_label": "Applicazioni tipiche",
        "view_detail": "Visualizza dettagli",
        "back_to_sortiment": "Torna all'assortimento",
        "back_to_category": "Torna alla categoria",
        "back_to_category_short": "Torna a {category}",
        "params_note": "I valori indicati sono orientativi e possono variare in base alla larghezza, alla lunghezza della bobina e alla versione specifica. Saremo lieti di preparare una specifica precisa su misura per voi.",
        "tailor_title": "Su misura per la vostra attività",
        "tailor_bullet_width": "Larghezza e lunghezza della bobina personalizzabili",
        "tailor_bullet_print": "Colore di fondo e numero di colori di stampa",
        "tailor_bullet_sample": "Test della qualità prima dell'ordine",
        "tailor_bullet_consult": "Consulenza sui parametri prima dell'ordine",
        "tailor_bullet_params": "Diverse versioni di adesivo e supporto",
        "no_print_note": "Il nastro è disponibile anche senza stampa.",
        "no_print_body": "Versione neutra (non stampata) dello stesso materiale, ideale per imballaggio immediato o scorte di magazzino.",
        "no_print_link": "Chiedete la disponibilità",
        "product_card_detail": "Visualizza dettagli",
    },
}

PARAM_FIELD_KEYS = [
    ("carrier", "Nosič / materiál"),
    ("thickness", "Tloušťka"),
    ("adhesive", "Typ lepidla"),
    ("adhesion", "Přilnavost (ocel)"),
    ("temperature", "Teplotní odolnost"),
    ("strength", "Pevnost v tahu"),
]

MIN_QTY_NOTE_MAP = {
    "Minimální množství od 360 ks (Akryl).": {
        "en": "Minimum quantity from 360 pcs (Akryl).",
        "de": "Mindestmenge ab 360 Stk. (Akryl).",
        "it": "Quantità minima da 360 pz (Akryl).",
    },
    "Minimální množství od 504 ks (HOT MELT).": {
        "en": "Minimum quantity from 504 pcs (HOT MELT).",
        "de": "Mindestmenge ab 504 Stk. (HOT MELT).",
        "it": "Quantità minima da 504 pz (HOT MELT).",
    },
    "Dostupné jako Akryl i HOT MELT. Min. množství: Akryl od 360 ks, HOT MELT od 504 ks.": {
        "en": "Available as Akryl and HOT MELT. Min. quantity: Akryl from 360 pcs, HOT MELT from 504 pcs.",
        "de": "Erhältlich als Akryl und HOT MELT. Mindestmenge: Akryl ab 360 Stk., HOT MELT ab 504 Stk.",
        "it": "Disponibile come Akryl e HOT MELT. Quantità min.: Akryl da 360 pz, HOT MELT da 504 pz.",
    },
}

# Akryl / HOT MELT detailed tech-spec schema (same value keys, different CS labels).
TECH_SPEC_PARAM_FIELD_KEYS = [
    ("carrier", "Nosič"),
    ("thickness", "Tloušťka fólie"),
    ("adhesive", "Typ lepidla"),
    ("adhesion", "Tloušťka lepidla"),
    ("strength", "Skladovací a aplikační teplota"),
    ("temperature", "Provozní teplota po nalepení"),
    ("min_qty", "Minimální množství"),
]

PAPER_SPEC_PARAM_FIELD_KEYS = [
    ("carrier", "Nosič"),
    ("grammage", "Gramáž nosiče"),
    ("adhesive", "Lepidlo"),
    ("thickness", "Celková tloušťka"),
    ("adhesion", "Přilnavost k oceli"),
    ("strength", "Pevnost v tahu"),
    ("elongation", "Tažnost / Prodloužení"),
    ("temperature", "Aplikační a skladovací teplota"),
]

PAPER_SPEC_PARAM_LABELS = {
    "cs": {
        "carrier": "Nosič",
        "grammage": "Gramáž nosiče",
        "adhesive": "Lepidlo",
        "thickness": "Celková tloušťka",
        "adhesion": "Přilnavost k oceli",
        "strength": "Pevnost v tahu",
        "elongation": "Tažnost / Prodloužení",
        "temperature": "Aplikační a skladovací teplota",
    },
    "en": {
        "carrier": "Carrier",
        "grammage": "Carrier grammage",
        "adhesive": "Adhesive",
        "thickness": "Total thickness",
        "adhesion": "Adhesion to steel",
        "strength": "Tensile strength",
        "elongation": "Elongation / stretch",
        "temperature": "Application and storage temperature",
    },
    "de": {
        "carrier": "Träger",
        "grammage": "Trägergrammatur",
        "adhesive": "Klebstoff",
        "thickness": "Gesamtdicke",
        "adhesion": "Haftung auf Stahl",
        "strength": "Zugfestigkeit",
        "elongation": "Dehnung / Verlängerung",
        "temperature": "Verarbeitungs- und Lagertemperatur",
    },
    "it": {
        "carrier": "Supporto",
        "grammage": "Grammatura del supporto",
        "adhesive": "Adesivo",
        "thickness": "Spessore totale",
        "adhesion": "Adesione sull'acciaio",
        "strength": "Resistenza alla trazione",
        "elongation": "Allungamento / estensione",
        "temperature": "Temperatura di applicazione e stoccaggio",
    },
}

TECH_SPEC_PARAM_LABELS = {
    "cs": {
        "carrier": "Nosič",
        "thickness": "Tloušťka fólie",
        "adhesive": "Typ lepidla",
        "adhesion": "Tloušťka lepidla",
        "strength": "Skladovací a aplikační teplota",
        "temperature": "Provozní teplota po nalepení",
        "min_qty": "Minimální množství",
    },
    "en": {
        "carrier": "Carrier",
        "thickness": "Film thickness",
        "adhesive": "Adhesive type",
        "adhesion": "Adhesive thickness",
        "strength": "Storage and application temperature",
        "temperature": "Operating temperature after application",
        "min_qty": "Minimum quantity",
    },
    "de": {
        "carrier": "Träger",
        "thickness": "Foliendicke",
        "adhesive": "Klebstofftyp",
        "adhesion": "Klebstoffdicke",
        "strength": "Lager- und Verarbeitungstemperatur",
        "temperature": "Betriebstemperatur nach dem Aufkleben",
        "min_qty": "Mindestmenge",
    },
    "it": {
        "carrier": "Supporto",
        "thickness": "Spessore del film",
        "adhesive": "Tipo di adesivo",
        "adhesion": "Spessore dell'adesivo",
        "strength": "Temperatura di stoccaggio e applicazione",
        "temperature": "Temperatura di esercizio dopo l'applicazione",
        "min_qty": "Quantità minima",
    },
}

PARAM_VALUE_MAP: dict[str, dict[str, str]] = {'matná BOPP': {'en': 'matte BOPP', 'de': 'mattes BOPP', 'it': 'BOPP opaco'}, 
    'od 1080 ks, základ 50 mm × 132 m; 3 barvy od 1 palety (2376 ks)': {'en': 'from 1080 pcs, base 50 mm × 132 m; 3 colours from 1 pallet (2376 pcs)', 'de': 'ab 1080 Stk., Basis 50 mm × 132 m; 3 Farben ab 1 Palette (2376 Stk.)', 'it': 'da 1080 pz, base 50 mm × 132 m; 3 colori da 1 pallet (2376 pz)'},
    'Akryl (NOISY)': {'en': 'Acrylic (NOISY)', 'de': 'Acryl (NOISY)', 'it': 'Acrilico (NOISY)'},
    '0–25 °C': {'en': '0–25 °C', 'de': '0–25 °C', 'it': '0–25 °C'},
    '−20 až +50 °C': {'en': '−20 to +50 °C', 'de': '−20 bis +50 °C', 'it': '−20 a +50 °C'},
    '1 paleta (2376 ks), základ 50 mm × 66 m': {'en': '1 pallet (2376 pcs), base 50 mm × 66 m', 'de': '1 Palette (2376 Stk.), Basis 50 mm × 66 m', 'it': '1 pallet (2376 pz), base 50 mm × 66 m'},'Akryl / Low noise': {'en': 'Acrylic / Low noise', 'de': 'Acryl / Low noise', 'it': 'Acrilico / Low noise'}, 'Akrylové': {'en': 'Acrylic', 'de': 'Acryl', 'it': 'Acrilico'}, 'Akrylové (bez rozpouštědel)': {'en': 'Acrylic (solvent-free)', 'de': 'Acryl (lösungsmittelfrei)', 'it': 'Acrilico (senza solventi)'}, 'Akrylové (disperzní)': {'en': 'Acrylic (dispersion)', 'de': 'Acryl (Dispersion)', 'it': 'Acrilico (dispersione)'}, 'Akrylové (vodní disperze)': {'en': 'Acrylic (water-based dispersion)', 'de': 'Acryl (wässrige Dispersion)', 'it': 'Acrilico (dispersione acquosa)'}, 'BOPP fólie': {'en': 'BOPP film', 'de': 'BOPP-Folie', 'it': 'Film BOPP'}, 'BOPP fólie (barevná)': {'en': 'BOPP film (coloured)', 'de': 'BOPP-Folie (farbig)', 'it': 'Film BOPP (colorato)'}, 'Hot melt': {'en': 'Hot melt', 'de': 'Hot Melt', 'it': 'Hot melt'}, 'HOT MELT': {'en': 'Hot melt', 'de': 'Hot Melt', 'it': 'Hot melt'}, 'Hot melt (syntetický kaučuk)': {'en': 'Hot melt (synthetic rubber)', 'de': 'Hot Melt (Synthesekautschuk)', 'it': 'Hot melt (gomma sintetica)'}, 'HOT MELT (syntetický kaučuk)': {'en': 'Hot melt (synthetic rubber)', 'de': 'Hot Melt (Synthesekautschuk)', 'it': 'Hot melt (gomma sintetica)'}, 'Kaučukové': {'en': 'Rubber-based', 'de': 'Kautschuk', 'it': 'Gomma'}, 'Kaučukové (odolné teplu)': {'en': 'Rubber-based (heat-resistant)', 'de': 'Kautschuk (hitzebeständig)', 'it': 'Gomma (resistente al calore)'}, 'Kaučukové (solvent)': {'en': 'Rubber-based (solvent)', 'de': 'Kautschuk (Lösungsmittel)', 'it': 'Gomma (solvente)'}, 'Kaučukové (syntetické)': {'en': 'Rubber-based (synthetic)', 'de': 'Kautschuk (synthetisch)', 'it': 'Gomma (sintetica)'}, 'Krepový papír': {'en': 'Crepe paper', 'de': 'Krepppapier', 'it': 'Carta crespa'}, 'MOPP + křížová skelná vlákna': {'en': 'MOPP + cross-laid glass fibres', 'de': 'MOPP + kreuzweise Glasfasern', 'it': 'MOPP + fibre di vetro incrociate'}, 'MOPP + podélná skelná vlákna': {'en': 'MOPP + longitudinal glass fibres', 'de': 'MOPP + längs verlaufende Glasfasern', 'it': 'MOPP + fibre di vetro longitudinali'}, 'MOPP fólie': {'en': 'MOPP film', 'de': 'MOPP-Folie', 'it': 'Film MOPP'}, 'Odstranitelné akrylové': {'en': 'Removable acrylic', 'de': 'Abziehbares Acryl', 'it': 'Acrilico rimovibile'}, 'Papír (FSC)': {'en': 'Paper (FSC)', 'de': 'Papier (FSC)', 'it': 'Carta (FSC)'}, 'Papírový nosič': {'en': 'Paper carrier', 'de': 'Papierträger', 'it': 'Supporto in carta'}, 'Papírový nosič (kraft)': {'en': 'Paper carrier (kraft)', 'de': 'Papierträger (Kraft)', 'it': 'Supporto in carta kraft'}, 'Krepový papír (FSC certifikace)': {'en': 'Crepe paper (FSC certified)', 'de': 'Krepppapier (FSC-zertifiziert)', 'it': 'Carta crespa (certificata FSC)'}, 'Krepový papír s podélným skelným vláknem (FSC)': {'en': 'Crepe paper with longitudinal glass fibre (FSC)', 'de': 'Krepppapier mit längs verlaufender Glasfaser (FSC)', 'it': 'Carta crespa con fibra di vetro longitudinale (FSC)'}, 'Krepový papír s křížovým skelným vláknem (FSC)': {'en': 'Crepe paper with cross-laid glass fibre (FSC)', 'de': 'Krepppapier mit kreuzweise Glasfaser (FSC)', 'it': 'Carta crespa con fibra di vetro a croce (FSC)'}, 'Zesílený krepový papír (FSC certifikace)': {'en': 'Reinforced crepe paper (FSC certified)', 'de': 'Verstärktes Krepppapier (FSC-zertifiziert)', 'it': 'Carta crespa rinforzata (certificata FSC)'}, 'Hladký Kraftový papír (FSC certifikace)': {'en': 'Smooth kraft paper (FSC certified)', 'de': 'Glattes Kraftpapier (FSC-zertifiziert)', 'it': 'Carta kraft liscia (certificata FSC)'}, 'Recyklovaný Kraftový papír (100% recyklovaný, FSC certifikace)': {'en': 'Recycled kraft paper (100% recycled, FSC certified)', 'de': 'Recyceltes Kraftpapier (100 % recycelt, FSC-zertifiziert)', 'it': 'Carta kraft riciclata (100% riciclata, certificata FSC)'}, 'Syntetický kaučuk (Hot Melt)': {'en': 'Synthetic rubber (Hot Melt)', 'de': 'Synthesekautschuk (Hot Melt)', 'it': 'Gomma sintetica (Hot Melt)'}, 'Přírodní kaučuk (Solvent)': {'en': 'Natural rubber (Solvent)', 'de': 'Naturkautschuk (Solvent)', 'it': 'Gomma naturale (Solvent)'}, '60 g/m²': {'en': '60 g/m²', 'de': '60 g/m²', 'it': '60 g/m²'}, '72 g/m²': {'en': '72 g/m²', 'de': '72 g/m²', 'it': '72 g/m²'}, '165 g/m²': {'en': '165 g/m²', 'de': '165 g/m²', 'it': '165 g/m²'}, '80 g/m²': {'en': '80 g/m²', 'de': '80 g/m²', 'it': '80 g/m²'}, '4,5 N/cm': {'en': '4.5 N/cm', 'de': '4,5 N/cm', 'it': '4,5 N/cm'}, '6,0 N/cm': {'en': '6.0 N/cm', 'de': '6,0 N/cm', 'it': '6,0 N/cm'}, '7,0 N/cm': {'en': '7.0 N/cm', 'de': '7,0 N/cm', 'it': '7,0 N/cm'}, '>7 N/cm (při odtržení papíru)': {'en': '>7 N/cm (paper tear)', 'de': '>7 N/cm (Papierriss)', 'it': '>7 N/cm (strappo della carta)'}, '2,4 N/cm': {'en': '2.4 N/cm', 'de': '2,4 N/cm', 'it': '2,4 N/cm'}, '33 N/cm': {'en': '33 N/cm', 'de': '33 N/cm', 'it': '33 N/cm'}, '150 N/cm': {'en': '150 N/cm', 'de': '150 N/cm', 'it': '150 N/cm'}, '50 N/cm (±10 %)': {'en': '50 N/cm (±10%)', 'de': '50 N/cm (±10 %)', 'it': '50 N/cm (±10 %)'}, '10 %': {'en': '10%', 'de': '10 %', 'it': '10 %'}, '6,2 %': {'en': '6.2%', 'de': '6,2 %', 'it': '6,2 %'}, '8 %': {'en': '8%', 'de': '8 %', 'it': '8 %'}, '14 %': {'en': '14%', 'de': '14 %', 'it': '14 %'}, '2 % (±15 %)': {'en': '2% (±15%)', 'de': '2 % (±15 %)', 'it': '2 % (±15 %)'}, '15–25 °C': {'en': '15–25 °C', 'de': '15–25 °C', 'it': '15–25 °C'}, '120 µm': {'en': '120 µm', 'de': '120 µm', 'it': '120 µm'}, '125 µm': {'en': '125 µm', 'de': '125 µm', 'it': '125 µm'}, '130 µm': {'en': '130 µm', 'de': '130 µm', 'it': '130 µm'}, '225 µm': {'en': '225 µm', 'de': '225 µm', 'it': '225 µm'}, '135 µm (±15 %)': {'en': '135 µm (±15%)', 'de': '135 µm (±15 %)', 'it': '135 µm (±15 %)'}, '110 µm': {'en': '110 µm', 'de': '110 µm', 'it': '110 µm'}, '140 µm': {'en': '140 µm', 'de': '140 µm', 'it': '140 µm'}, '35 N/cm': {'en': '35 N/cm', 'de': '35 N/cm', 'it': '35 N/cm'}, '50 N/cm': {'en': '50 N/cm', 'de': '50 N/cm', 'it': '50 N/cm'}, '60 N/cm': {'en': '60 N/cm', 'de': '60 N/cm', 'it': '60 N/cm'}, '5,0 N/cm': {'en': '5.0 N/cm', 'de': '5,0 N/cm', 'it': '5,0 N/cm'}, '5 %': {'en': '5%', 'de': '5 %', 'it': '5 %'}, 'Polyesterová (PET) fólie': {'en': 'Polyester (PET) film', 'de': 'Polyester- (PET-) Folie', 'it': 'Film in poliestere (PET)'}, 'Recyklovaná PET fólie': {'en': 'Recycled PET film', 'de': 'Recycelte PET-Folie', 'it': 'Film PET riciclato'}, 'Recyklovaná PP fólie': {'en': 'Recycled PP film', 'de': 'Recycelte PP-Folie', 'it': 'Film PP riciclato'}, '100% regenerovaná BOPP fólie': {'en': '100% regenerated BOPP film', 'de': '100 % regenerierte BOPP-Folie', 'it': 'Film BOPP rigenerato al 100%'}, 'BOPP fólie (matná, 35 µm)': {'en': 'BOPP film (matte, 35 µm)', 'de': 'BOPP-Folie (matt, 35 µm)', 'it': 'Film BOPP (opaco, 35 µm)'}, 'Akrylové (tiché, bez rozpouštědel)': {'en': 'Acrylic (quiet, solvent-free)', 'de': 'Acryl (leise, lösungsmittelfrei)', 'it': 'Acrilico (silenzioso, senza solventi)'}, 'Akrylové (zvýšená vrstva +33 %)': {'en': 'Acrylic (increased adhesive layer +33%)', 'de': 'Acryl (erhöhte Klebstoffschicht +33 %)', 'it': 'Acrilico (strato adesivo aumentato +33%)'}, 'Hot melt (super tack, +20 %)': {'en': 'Hot melt (super tack, +20%)', 'de': 'Hot Melt (Super-Tack, +20 %)', 'it': 'Hot melt (super tack, +20%)'}, 'HOT MELT (super tack, +20 %)': {'en': 'Hot melt (super tack, +20%)', 'de': 'Hot Melt (Super-Tack, +20 %)', 'it': 'Hot melt (super tack, +20%)'}, 'HOT MELT (tack+)': {'en': 'HOT MELT (tack+)', 'de': 'HOT MELT (tack+)', 'it': 'HOT MELT (tack+)'}, '28 / 32 µm': {'en': '28 / 32 µm', 'de': '28 / 32 µm', 'it': '28 / 32 µm'}, 'Recyklovaný papír': {'en': 'Recycled paper', 'de': 'Recyclingpapier', 'it': 'Carta riciclata'}, 'Silikonové': {'en': 'Silicone', 'de': 'Silikon', 'it': 'Silicone'}, 'BOPP': {'en': 'BOPP', 'de': 'BOPP', 'it': 'BOPP'}, 'Akryl (Low noise / Noisy)': {'en': 'Akryl (Low noise / Noisy)', 'de': 'Akryl (Low noise / Noisy)', 'it': 'Akryl (Low noise / Noisy)'}, 'Akryl': {'en': 'Akryl', 'de': 'Akryl', 'it': 'Akryl'}, 'Bezpečnostní (VOID)': {'en': 'Security (VOID)', 'de': 'Sicherheit (VOID)', 'it': 'Sicurezza (VOID)'}, '28 µm': {'en': '28 µm', 'de': '28 µm', 'it': '28 µm'}, '28 / 32 / 35 µm': {'en': '28 / 32 / 35 µm', 'de': '28 / 32 / 35 µm', 'it': '28 / 32 / 35 µm'}, 'Akryl (Low noise)': {'en': 'Akryl (Low noise)', 'de': 'Akryl (Low noise)', 'it': 'Akryl (Low noise)'}, 'Akryl (Noisy)': {'en': 'Akryl (Noisy)', 'de': 'Akryl (Noisy)', 'it': 'Akryl (Noisy)'}, 'Akryl (Low noise / Noisy) / HOT MELT': {'en': 'Akryl (Low noise / Noisy) / HOT MELT', 'de': 'Akryl (Low noise / Noisy) / HOT MELT', 'it': 'Akryl (Low noise / Noisy) / HOT MELT'}, '0 až +60 °C': {'en': '0 to +60 °C', 'de': '0 bis +60 °C', 'it': '0 a +60 °C'}, '−10 až +60 °C': {'en': '−10 to +60 °C', 'de': '−10 bis +60 °C', 'it': '−10 a +60 °C'}, '25 / 28 / 32 µm': {'en': '25 / 28 / 32 µm', 'de': '25 / 28 / 32 µm', 'it': '25 / 28 / 32 µm'}, '21 µm': {'en': '21 µm', 'de': '21 µm', 'it': '21 µm'}, '18 µm': {'en': '18 µm', 'de': '18 µm', 'it': '18 µm'}, '21 µm (Akryl) / 18 µm (HOT MELT)': {'en': '21 µm (Akryl) / 18 µm (HOT MELT)', 'de': '21 µm (Akryl) / 18 µm (HOT MELT)', 'it': '21 µm (Akryl) / 18 µm (HOT MELT)'}, 'od 360 ks': {'en': 'from 360 pcs', 'de': 'ab 360 Stk.', 'it': 'da 360 pz'}, 'od 504 ks': {'en': 'from 504 pcs', 'de': 'ab 504 Stk.', 'it': 'da 504 pz'}, 'Akryl od 360 ks / HOT MELT od 504 ks': {'en': 'Akryl from 360 pcs / HOT MELT from 504 pcs', 'de': 'Akryl ab 360 Stk. / HOT MELT ab 504 Stk.', 'it': 'Akryl da 360 pz / HOT MELT da 504 pz'}, '50 % regenerát': {'en': '50% regenerated', 'de': '50 % regeneriert', 'it': '50% rigenerato'}, '80 % regenerát': {'en': '80% regenerated', 'de': '80 % regeneriert', 'it': '80% rigenerato'}, '100 % regenerát': {'en': '100% regenerated', 'de': '100 % regeneriert', 'it': '100% rigenerato'}, 'Akryl / HOT MELT': {'en': 'Akryl / HOT MELT', 'de': 'Akryl / HOT MELT', 'it': 'Akryl / HOT MELT'}, '14–28 °C': {'en': '14–28 °C', 'de': '14–28 °C', 'it': '14–28 °C'}, 'Textilní výztuž + PE laminát': {'en': 'Textile reinforcement + PE laminate', 'de': 'Textilverstärkung + PE-Laminat', 'it': 'Rinforzo tessile + laminato PE'}, 'BOPET': {'en': 'BOPET', 'de': 'BOPET', 'it': 'BOPET'}, '35 µm': {'en': '35 µm', 'de': '35 µm', 'it': '35 µm'}, '29 µm': {'en': '29 µm', 'de': '29 µm', 'it': '29 µm'}, '22 µm': {'en': '22 µm', 'de': '22 µm', 'it': '22 µm'}, '19 µm': {'en': '19 µm', 'de': '19 µm', 'it': '19 µm'}, '0–28 °C': {'en': '0–28 °C', 'de': '0–28 °C', 'it': '0–28 °C'}, '−20 až +60 °C': {'en': '−20 to +60 °C', 'de': '−20 bis +60 °C', 'it': 'da −20 a +60 °C'}, '0 až +50 / 0 až +60 / −10 až +60 °C': {'en': '0 to +50 / 0 to +60 / −10 to +60 °C', 'de': '0 bis +50 / 0 bis +60 / −10 bis +60 °C', 'it': 'da 0 a +50 / da 0 a +60 / da −10 a +60 °C'}, 'od 180 ks': {'en': 'from 180 pcs', 'de': 'ab 180 Stk.', 'it': 'da 180 pz'}, 'od 1 palety (2376 ks)': {'en': 'from 1 pallet (2376 pcs)', 'de': 'ab 1 Palette (2376 Stk.)', 'it': 'da 1 pallet (2376 pz)'}, 'od 1080 ks': {'en': 'from 1080 pcs', 'de': 'ab 1080 Stk.', 'it': 'da 1080 pz'}, '0 až +60 / −10 až +60 °C': {'en': '0 to +60 / −10 to +60 °C', 'de': '0 bis +60 / −10 bis +60 °C', 'it': 'da 0 a +60 / da −10 a +60 °C'}}

PARAM_LABELS = {
    "cs": {"carrier": "Nosič / materiál", "thickness": "Tloušťka", "adhesive": "Typ lepidla", "adhesion": "Přilnavost (ocel)", "temperature": "Teplotní odolnost", "strength": "Pevnost v tahu"},
    "en": {"carrier": "Carrier / material", "thickness": "Thickness", "adhesive": "Adhesive type", "adhesion": "Adhesion (steel)", "temperature": "Temperature resistance", "strength": "Tensile strength"},
    "de": {"carrier": "Träger / Material", "thickness": "Dicke", "adhesive": "Klebstofftyp", "adhesion": "Haftung (Stahl)", "temperature": "Temperaturbeständigkeit", "strength": "Zugfestigkeit"},
    "it": {"carrier": "Supporto / materiale", "thickness": "Spessore", "adhesive": "Tipo di adesivo", "adhesion": "Adesione (acciaio)", "temperature": "Resistenza alla temperatura", "strength": "Resistenza alla trazione"},
}

GALLERY_ITEMS = {
    "cs": {
        "bonami": {"title": "Pásky s logem Bonami", "description": "Jednobarevný brand potisk na bílé BOPP pásce – logo a ilustrace nábytku pro e-commerce balení.", "industry_label": "E-commerce"},
        "notino": {"title": "Pásky s logem Notino", "description": "Kontrastní bílý potisk loga na černé pásce – výrazný branding zásilek v beauty e-commerce.", "industry_label": "E-commerce"},
        "fenske": {"title": "Pásky s logem Fenske", "description": "Dvoubarevný potisk FENSKE / Weine und Feinkost na balicí pásce – branding zásilek vína a delikates.", "industry_label": "Potraviny"},
        "just-nahrin": {"title": "Pásky Just+ / nahrin", "description": "Vícebarevný potisk log a logistického textu včetně symbolu křehké – branding i instrukce pro příjemce.", "industry_label": "E-commerce"},
        "vorsicht-glas": {"title": "Výstražná páska Vorsicht Glas", "description": "Výstražný potisk „Vorsicht Glas!“ / „Do not drop“ na balicí pásce – ochrana křehkých zásilek při přepravě.", "industry_label": "Logistika"},
        "alfain": {"title": "Pásky s logem ALFA IN", "description": "Oranžová BOPP páska s bílým logem ALFA IN – branding zásilek přímo ve skladu.", "industry_label": "Logistika"},
        "papir-fsc": {"title": "Papírová páska FSC / 22 PAP", "description": "Ekologická papírová páska s potiskem FSC a symbolem 22 PAP – udržitelné balení e-commerce zásilek.", "industry_label": "E-commerce"},
        "alfain-sklad": {"title": "ALFA IN páska ve skladu", "description": "Ruční balení na paletě s oranžovou páskou ALFA IN – potisk v praxi logistického provozu.", "industry_label": "Logistika"},
        "irplast-warehouse": {"title": "Automatizovaný sklad Empoli", "description": "Automatizovaný sklad v Empoli – logistika hotových pásek a fólií.", "industry_label": "Výroba"},
        "irplast-warehouse-2": {"title": "Just in Time dodávky", "description": "Když objednáte dopředu, nejdřív potiskneme fólii. Těsně před dodáním ji teprve nařežeme, naneseme lepidlo a pásku odešleme. Just in Time — čerstvý produkt přesně včas, bez zbytečných zásob hotových rolí.", "industry_label": "Výroba"},
        "irplast-shuttle": {"title": "Výroba – automated shuttle", "description": "Výrobní oddělení se automatickým shuttle systémem v závodě Empoli.", "industry_label": "Výroba"},
        "irplast-silos": {"title": "Sila na suroviny Atessa", "description": "Sila pro skladování surovin (polypropylen) ve filmovém závodě Atessa.", "industry_label": "Výroba"},
        "irplast-lisim": {"title": "Linka STILANSOL® LISIM", "description": "Simultánní orientace BOPP fólie – výrobní linka Brückner LISIM / STILANSOL®.", "industry_label": "Výroba"},
        "irplast-slitter": {"title": "Řezací linka (taglierina)", "description": "Průmyslová řezací linka pro dělení fólie a pásek.", "industry_label": "Výroba"},
        "irplast-carriages": {"title": "Automatické vozíky ve výrobě", "description": "Automatické manipulační vozíky zajišťující tok materiálu ve výrobě.", "industry_label": "Výroba"},
        "irplast-reels": {"title": "Sklad BOPP rolí", "description": "Skladování hotových BOPP rolí před konverzí na pásky a etikety.", "industry_label": "Výroba"},
        "alza": {"title": "Pásky s logem ALZA", "description": "Vícejazyčný brand potisk pro e-commerce balení s opakovaným logem a sloganem na standardní BOPP pásku.", "industry_label": "E-commerce"},
        "flexotisk-8": {"title": "Flexotisk – 8 barev", "description": "Plnobarevný flexotisk s vysokým rozlišením, vhodný pro atraktivní brand na balících páskách i potravinářských aplikacích.", "industry_label": "Potraviny"},
        "jednobarevny-firemni": {"title": "Jednobarevný firemní potisk", "description": "Klasický jednobarevný potisk loga na průhledné nebo bílé BOPP pásky, ideální pro firemní balení a skladovou logistiku.", "industry_label": "Výroba"},
        "rototisk-foto": {"title": "Rototisk ve fotokvalitě", "description": "Rotogravurní tisk s fotografickou kvalitou pro náročné vizuály a dlouhodobou odolnost potisku.", "industry_label": "Potraviny"},
        "pecetni": {"title": "Pečetní páska s potiskem", "description": "Pečetní páska s vlastním potiskem pro zabezpečení zásilek a dokumentů proti neoprávněnému otevření.", "industry_label": "Bezpečnost"},
        "logisticky-kontakty": {"title": "Logistický potisk – kontakty", "description": "Informační potisk s kontakty, QR kódem nebo instrukcemi pro příjemce zásilky.", "industry_label": "Logistika"},
        "neutralni-bopp": {"title": "Neutrální BOPP 25 mm", "description": "Úzká BOPP páska s jednoduchým potiskem pro ruční balení a lehčí zásilky.", "industry_label": "Výroba"},
        "tamper-void": {"title": "Tamper Evident VOID", "description": "Bezpečnostní páska s VOID efektem, při odlepení zanechá viditelné upozornění, které nelze bez stopy odstranit.", "industry_label": "Bezpečnost"},
        "extra-glue": {"title": "EXTRA GLUE+ bezpečnostní série", "description": "Páska se zvýšenou vrstvou lepidla (+33 %) pro obtížné povrchy, těžké balíky a prašné skladové prostředí.", "industry_label": "Bezpečnost"},
        "prumyslova-serie": {"title": "Průmyslová série pro e-shop", "description": "Hromadná výroba potištěných pásek pro e-shopy a fulfillment, konzistentní kvalita v celé sérii.", "industry_label": "E-commerce"},
        "vystrizny-krehke": {"title": "Výstražný potisk – křehké", "description": "Výstražné pásky s potiskem „Křehké“, „Neklopit“ nebo vlastním symbolem pro ochranu zboží při přepravě.", "industry_label": "Logistika"},
        "bezpecnostni-sklad": {"title": "Bezpečnostní páska sklad", "description": "Kombinace logistického a bezpečnostního potisku pro sklady a distribuční centra.", "industry_label": "Bezpečnost"},
    },
    "en": {
        "bonami": {"title": "Bonami logo tapes", "description": "Single-colour brand print on white BOPP tape – logo and furniture illustrations for e-commerce packaging.", "industry_label": "E-commerce"},
        "notino": {"title": "Notino logo tapes", "description": "High-contrast white logo print on black tape – bold shipment branding for beauty e-commerce.", "industry_label": "E-commerce"},
        "fenske": {"title": "Fenske logo tapes", "description": "Two-colour FENSKE / Weine und Feinkost print on packing tape – branding for wine and gourmet shipments.", "industry_label": "Food industry"},
        "just-nahrin": {"title": "Just+ / nahrin tapes", "description": "Multi-colour print of logos and logistics text with a fragile symbol – branding plus instructions for the recipient.", "industry_label": "E-commerce"},
        "vorsicht-glas": {"title": "Warning tape Vorsicht Glas", "description": "Warning print “Vorsicht Glas!” / “Do not drop” on packing tape – protecting fragile shipments in transit.", "industry_label": "Logistics"},
        "alfain": {"title": "ALFA IN logo tapes", "description": "Orange BOPP tape with a white ALFA IN logo – shipment branding directly in the warehouse.", "industry_label": "Logistics"},
        "papir-fsc": {"title": "Paper tape FSC / 22 PAP", "description": "Eco-friendly paper tape printed with FSC and 22 PAP symbols – sustainable e-commerce packaging.", "industry_label": "E-commerce"},
        "alfain-sklad": {"title": "ALFA IN tape in the warehouse", "description": "Manual packing on a pallet with orange ALFA IN tape – print in real logistics operations.", "industry_label": "Logistics"},
        "irplast-warehouse": {"title": "Automated warehouse Empoli", "description": "Automated warehouse in Empoli – logistics for finished tapes and films.", "industry_label": "Manufacturing"},
        "irplast-warehouse-2": {"title": "Just-in-time delivery", "description": "When you order ahead, we print the film first. Only shortly before delivery do we slit it, apply adhesive and ship the tape. Just in time — a fresh product exactly when you need it, without surplus stock of finished rolls.", "industry_label": "Manufacturing"},
        "irplast-shuttle": {"title": "Production – automated shuttle", "description": "Production department with an automated shuttle system at the Empoli plant.", "industry_label": "Manufacturing"},
        "irplast-silos": {"title": "Raw material silos Atessa", "description": "Silos for storing raw materials (polypropylene) at the Atessa film plant.", "industry_label": "Manufacturing"},
        "irplast-lisim": {"title": "STILANSOL® LISIM line", "description": "Simultaneous BOPP film orientation – Brückner LISIM / STILANSOL® production line.", "industry_label": "Manufacturing"},
        "irplast-slitter": {"title": "Slitting line", "description": "Industrial slitting line for cutting film and tapes.", "industry_label": "Manufacturing"},
        "irplast-carriages": {"title": "Automatic carriages in production", "description": "Automatic handling carriages ensuring material flow in production.", "industry_label": "Manufacturing"},
        "irplast-reels": {"title": "BOPP reel stock", "description": "Storage of finished BOPP reels before converting into tapes and labels.", "industry_label": "Manufacturing"},
        "alza": {"title": "ALZA logo tapes", "description": "Multilingual brand printing for e-commerce packaging, featuring a repeated logo and slogan on standard BOPP tape.", "industry_label": "E-commerce"},
        "flexotisk-8": {"title": "Flexographic printing – 8 colours", "description": "High-resolution full-colour flexographic printing, suitable for impactful tape branding and food-industry applications.", "industry_label": "Food industry"},
        "jednobarevny-firemni": {"title": "Single-colour corporate print", "description": "Classic single-colour logo printing on clear or white BOPP tapes, ideal for corporate packaging and warehouse logistics.", "industry_label": "Manufacturing"},
        "rototisk-foto": {"title": "Photographic-quality rotogravure", "description": "Rotogravure printing with photographic quality for demanding visuals and long-lasting print durability.", "industry_label": "Food industry"},
        "pecetni": {"title": "Printed sealing tape", "description": "Sealing tape with custom printing to protect shipments and documents against unauthorised opening.", "industry_label": "Security"},
        "logisticky-kontakty": {"title": "Logistics print – contacts", "description": "Informational printing with contact details, a QR code or instructions for the shipment recipient.", "industry_label": "Logistics"},
        "neutralni-bopp": {"title": "Plain BOPP 25 mm", "description": "Narrow BOPP tape with simple printing for manual packing and lighter shipments.", "industry_label": "Manufacturing"},
        "tamper-void": {"title": "Tamper Evident VOID", "description": "Security tape with a VOID effect that leaves a visible warning when removed and cannot be removed without evidence.", "industry_label": "Security"},
        "extra-glue": {"title": "EXTRA GLUE+ security series", "description": "Tape with an increased adhesive layer (+33%) for difficult surfaces, heavy parcels and dusty warehouse environments.", "industry_label": "Security"},
        "prumyslova-serie": {"title": "Industrial e-commerce series", "description": "Volume production of printed tapes for e-shops and fulfilment operations, with consistent quality across the entire run.", "industry_label": "E-commerce"},
        "vystrizny-krehke": {"title": "Warning print – fragile", "description": "Warning tapes printed with “Fragile”, “Do not tilt” or a custom symbol to protect goods during transport.", "industry_label": "Logistics"},
        "bezpecnostni-sklad": {"title": "Warehouse security tape", "description": "A combination of logistics and security printing for warehouses and distribution centres.", "industry_label": "Security"},
    },
    "de": {
        "bonami": {"title": "Klebebänder mit Bonami-Logo", "description": "Einfarbiger Markendruck auf weißem BOPP-Band – Logo und Möbelillustrationen für E-Commerce-Verpackungen.", "industry_label": "E-Commerce"},
        "notino": {"title": "Klebebänder mit Notino-Logo", "description": "Kontrastreicher weißer Logodruck auf schwarzem Band – starkes Sendungsbranding für Beauty-E-Commerce.", "industry_label": "E-Commerce"},
        "fenske": {"title": "Klebebänder mit Fenske-Logo", "description": "Zweifarbiger Druck FENSKE / Weine und Feinkost auf Klebeband – Branding für Wein- und Feinkostsendungen.", "industry_label": "Lebensmittel"},
        "just-nahrin": {"title": "Just+ / nahrin Klebebänder", "description": "Mehrfarbiger Druck von Logos und Logistiktext inkl. Zerbrechlich-Symbol – Branding und Hinweise für den Empfänger.", "industry_label": "E-Commerce"},
        "vorsicht-glas": {"title": "Warnband Vorsicht Glas", "description": "Warndruck „Vorsicht Glas!“ / „Do not drop“ auf Klebeband – Schutz zerbrechlicher Sendungen beim Transport.", "industry_label": "Logistik"},
        "alfain": {"title": "Klebebänder mit ALFA IN-Logo", "description": "Oranges BOPP-Band mit weißem ALFA IN-Logo – Sendungsbranding direkt im Lager.", "industry_label": "Logistik"},
        "papir-fsc": {"title": "Papierklebeband FSC / 22 PAP", "description": "Ökologisches Papierklebeband mit FSC- und 22-PAP-Aufdruck – nachhaltige E-Commerce-Verpackung.", "industry_label": "E-Commerce"},
        "alfain-sklad": {"title": "ALFA IN-Band im Lager", "description": "Manuelles Verpacken auf Palette mit orangem ALFA IN-Band – Druck im realen Logistikbetrieb.", "industry_label": "Logistik"},
        "irplast-warehouse": {"title": "Automatisiertes Lager Empoli", "description": "Automatisiertes Lager in Empoli – Logistik für fertige Bänder und Folien.", "industry_label": "Produktion"},
        "irplast-warehouse-2": {"title": "Just-in-Time-Lieferung", "description": "Bei Vorausbestellung bedrucken wir zuerst die Folie. Erst kurz vor der Lieferung schneiden wir sie zu, tragen den Klebstoff auf und versenden das Band. Just in Time — frisches Produkt genau dann, wenn Sie es brauchen, ohne unnötige Bestände fertiger Rollen.", "industry_label": "Produktion"},
        "irplast-shuttle": {"title": "Produktion – Automated Shuttle", "description": "Produktionsbereich mit automatischem Shuttle-System im Werk Empoli.", "industry_label": "Produktion"},
        "irplast-silos": {"title": "Rohstoffsilos Atessa", "description": "Silos zur Lagerung von Rohstoffen (Polypropylen) im Folienwerk Atessa.", "industry_label": "Produktion"},
        "irplast-lisim": {"title": "STILANSOL® LISIM-Linie", "description": "Simultane BOPP-Folienorientierung – Brückner LISIM / STILANSOL® Produktionslinie.", "industry_label": "Produktion"},
        "irplast-slitter": {"title": "Schneidlinie (Taglierina)", "description": "Industrielle Schneidlinie zum Teilen von Folie und Bändern.", "industry_label": "Produktion"},
        "irplast-carriages": {"title": "Automatische Wagen in der Produktion", "description": "Automatische Handhabungswagen für den Materialfluss in der Produktion.", "industry_label": "Produktion"},
        "irplast-reels": {"title": "BOPP-Rollenlager", "description": "Lagerung fertiger BOPP-Rollen vor der Konvertierung zu Bändern und Etiketten.", "industry_label": "Produktion"},
        "alza": {"title": "Klebebänder mit ALZA-Logo", "description": "Mehrsprachiger Markendruck für E-Commerce-Verpackungen mit wiederholtem Logo und Slogan auf Standard-BOPP-Klebeband.", "industry_label": "E-Commerce"},
        "flexotisk-8": {"title": "Flexodruck – 8 Farben", "description": "Hochauflösender Vollfarb-Flexodruck für aufmerksamkeitsstarke Markenauftritte auf Klebebändern und Lebensmittelanwendungen.", "industry_label": "Lebensmittel"},
        "jednobarevny-firemni": {"title": "Einfarbiger Firmendruck", "description": "Klassischer einfarbiger Logodruck auf transparenten oder weißen BOPP-Bändern, ideal für Firmenverpackungen und Lagerlogistik.", "industry_label": "Produktion"},
        "rototisk-foto": {"title": "Rotogravur in Fotoqualität", "description": "Rotogravurdruck in fotografischer Qualität für anspruchsvolle Motive und dauerhaft beständige Bedruckung.", "industry_label": "Lebensmittel"},
        "pecetni": {"title": "Bedrucktes Siegelband", "description": "Siegelband mit individuellem Druck zur Sicherung von Sendungen und Dokumenten gegen unbefugtes Öffnen.", "industry_label": "Sicherheit"},
        "logisticky-kontakty": {"title": "Logistikdruck – Kontakte", "description": "Informationsdruck mit Kontaktdaten, QR-Code oder Anweisungen für den Empfänger der Sendung.", "industry_label": "Logistik"},
        "neutralni-bopp": {"title": "Neutrales BOPP 25 mm", "description": "Schmales BOPP-Band mit einfachem Druck für manuelles Verpacken und leichtere Sendungen.", "industry_label": "Produktion"},
        "tamper-void": {"title": "Tamper Evident VOID", "description": "Sicherheitsband mit VOID-Effekt, das beim Abziehen einen sichtbaren Hinweis hinterlässt.", "industry_label": "Sicherheit"},
        "extra-glue": {"title": "EXTRA GLUE+ Sicherheitsserie", "description": "Band mit erhöhter Klebstoffschicht (+33 %) für schwierige Oberflächen, schwere Pakete und staubige Lagerumgebungen.", "industry_label": "Sicherheit"},
        "prumyslova-serie": {"title": "Industrieserie für E-Shops", "description": "Serienfertigung bedruckter Bänder für E-Shops und Fulfillment mit gleichbleibender Qualität über die gesamte Serie.", "industry_label": "E-Commerce"},
        "vystrizny-krehke": {"title": "Warndruck – zerbrechlich", "description": "Warnbänder mit „Zerbrechlich“, „Nicht kippen“ oder einem individuellen Symbol zum Schutz von Waren beim Transport.", "industry_label": "Logistik"},
        "bezpecnostni-sklad": {"title": "Sicherheitsband für Lager", "description": "Kombination aus Logistik- und Sicherheitsdruck für Lager und Vertriebszentren.", "industry_label": "Sicherheit"},
    },
    "it": {
        "bonami": {"title": "Nastri con logo Bonami", "description": "Stampa del marchio monocolore su nastro BOPP bianco – logo e illustrazioni di arredi per imballaggi e-commerce.", "industry_label": "E-commerce"},
        "notino": {"title": "Nastri con logo Notino", "description": "Stampa bianca ad alto contrasto del logo su nastro nero – branding evidente delle spedizioni nel beauty e-commerce.", "industry_label": "E-commerce"},
        "fenske": {"title": "Nastri con logo Fenske", "description": "Stampa bicolore FENSKE / Weine und Feinkost sul nastro da imballaggio – branding per spedizioni di vini e gastronomia.", "industry_label": "Industria alimentare"},
        "just-nahrin": {"title": "Nastri Just+ / nahrin", "description": "Stampa multicolore di loghi e testo logistico con simbolo fragile – branding e istruzioni per il destinatario.", "industry_label": "E-commerce"},
        "vorsicht-glas": {"title": "Nastro di avvertimento Vorsicht Glas", "description": "Stampa di avvertimento “Vorsicht Glas!” / “Do not drop” sul nastro – protezione delle spedizioni fragili in transito.", "industry_label": "Logistica"},
        "alfain": {"title": "Nastri con logo ALFA IN", "description": "Nastro BOPP arancione con logo ALFA IN bianco – branding delle spedizioni direttamente in magazzino.", "industry_label": "Logistica"},
        "papir-fsc": {"title": "Nastro di carta FSC / 22 PAP", "description": "Nastro di carta ecologico con stampa FSC e simbolo 22 PAP – imballaggio e-commerce sostenibile.", "industry_label": "E-commerce"},
        "alfain-sklad": {"title": "Nastro ALFA IN in magazzino", "description": "Imballaggio manuale su pallet con nastro arancione ALFA IN – stampa nella pratica logistica.", "industry_label": "Logistica"},
        "irplast-warehouse": {"title": "Magazzino automatizzato Empoli", "description": "Magazzino automatizzato di Empoli – logistica di nastri e film finiti.", "industry_label": "Produzione"},
        "irplast-warehouse-2": {"title": "Consegne Just in Time", "description": "Con un ordine anticipato stampiamo prima il film. Solo poco prima della consegna lo tagliamo, applichiamo l’adesivo e spediamo il nastro. Just in Time — prodotto fresco al momento giusto, senza scorte inutili di bobine finite.", "industry_label": "Produzione"},
        "irplast-shuttle": {"title": "Produzione – automated shuttle", "description": "Reparto produttivo con sistema shuttle automatico nello stabilimento di Empoli.", "industry_label": "Produzione"},
        "irplast-silos": {"title": "Silos materie prime Atessa", "description": "Silos per lo stoccaggio delle materie prime (polipropilene) nello stabilimento film di Atessa.", "industry_label": "Produzione"},
        "irplast-lisim": {"title": "Linea STILANSOL® LISIM", "description": "Orientamento simultaneo del film BOPP – linea di produzione Brückner LISIM / STILANSOL®.", "industry_label": "Produzione"},
        "irplast-slitter": {"title": "Linea di taglio (taglierina)", "description": "Linea industriale di taglio per film e nastri.", "industry_label": "Produzione"},
        "irplast-carriages": {"title": "Carrelli automatici in produzione", "description": "Carrelli automatici di movimentazione che garantiscono il flusso dei materiali in produzione.", "industry_label": "Produzione"},
        "irplast-reels": {"title": "Stock bobine BOPP", "description": "Stoccaggio delle bobine BOPP finite prima della conversione in nastri ed etichette.", "industry_label": "Produzione"},
        "alza": {"title": "Nastri con logo ALZA", "description": "Stampa del marchio multilingue per imballaggi e-commerce, con logo e slogan ripetuti su nastro BOPP standard.", "industry_label": "E-commerce"},
        "flexotisk-8": {"title": "Stampa flessografica – 8 colori", "description": "Stampa flessografica in quadricromia ad alta risoluzione, adatta a un branding d'impatto sui nastri e alle applicazioni alimentari.", "industry_label": "Industria alimentare"},
        "jednobarevny-firemni": {"title": "Stampa aziendale monocolore", "description": "Classica stampa del logo a un colore su nastri BOPP trasparenti o bianchi, ideale per imballaggi aziendali e logistica di magazzino.", "industry_label": "Produzione"},
        "rototisk-foto": {"title": "Rotocalco in qualità fotografica", "description": "Stampa rotocalco in qualità fotografica per immagini complesse e una lunga durata della stampa.", "industry_label": "Industria alimentare"},
        "pecetni": {"title": "Nastro sigillante stampato", "description": "Nastro sigillante con stampa personalizzata per proteggere spedizioni e documenti da aperture non autorizzate.", "industry_label": "Sicurezza"},
        "logisticky-kontakty": {"title": "Stampa logistica – contatti", "description": "Stampa informativa con recapiti, codice QR o istruzioni per il destinatario della spedizione.", "industry_label": "Logistica"},
        "neutralni-bopp": {"title": "BOPP neutro 25 mm", "description": "Nastro BOPP stretto con stampa semplice per l'imballaggio manuale e le spedizioni più leggere.", "industry_label": "Produzione"},
        "tamper-void": {"title": "Tamper Evident VOID", "description": "Nastro di sicurezza con effetto VOID che, quando viene rimosso, lascia un avviso visibile.", "industry_label": "Sicurezza"},
        "extra-glue": {"title": "Serie di sicurezza EXTRA GLUE+", "description": "Nastro con strato adesivo maggiorato (+33%) per superfici difficili, colli pesanti e ambienti di magazzino polverosi.", "industry_label": "Sicurezza"},
        "prumyslova-serie": {"title": "Serie industriale per e-commerce", "description": "Produzione in serie di nastri stampati per e-shop e centri di fulfilment, con qualità costante per l'intera fornitura.", "industry_label": "E-commerce"},
        "vystrizny-krehke": {"title": "Stampa di avvertimento – fragile", "description": "Nastri di avvertimento stampati con “Fragile”, “Non capovolgere” o un simbolo personalizzato per proteggere le merci durante il trasporto.", "industry_label": "Logistica"},
        "bezpecnostni-sklad": {"title": "Nastro di sicurezza per magazzino", "description": "Combinazione di stampa logistica e di sicurezza per magazzini e centri di distribuzione.", "industry_label": "Sicurezza"},
    },
}

TAGLINES: dict[str, dict[str, str]] = {'udrzitelna-paska-airtape': {'en': 'Thin and strong BOPP tape for maximum efficiency and less waste.', 'de': 'Dünnes und festes BOPP-Klebeband für maximale Effizienz und weniger Abfall.', 'it': 'Nastro BOPP sottile e resistente per massima efficienza e meno rifiuti.'}, 'udrzitelna-paska-eco-50': {'en': 'Efficient packaging with 50% regenerated material. The optimal balance of ecology and best price.', 'de': 'Effizientes Verpacken mit 50 % regeneriertem Material. Optimale Balance aus Ökologie und bestem Preis.', 'it': 'Imballaggio efficiente con il 50% di materiale rigenerato. Il giusto equilibrio tra ecologia e miglior prezzo.'}, 'udrzitelna-paska-eco-80': {'en': 'BOPP film with 80% regenerated material. Combines a high ecological standard with full strength.', 'de': 'BOPP-Folie mit 80 % regeneriertem Material. Verbindet hohen ökologischen Standard mit voller Festigkeit.', 'it': 'Film BOPP con l’80% di materiale rigenerato. Unisce un elevato standard ecologico e piena resistenza.'}, 'udrzitelna-paska-eco-100': {'en': '100% regenerated BOPP film from post-industrial waste. Maximum ecological standard without compromising performance.', 'de': '100 % regenerierte BOPP-Folie aus postindustriellen Abfällen. Maximaler ökologischer Standard ohne Kompromisse bei der Leistung.', 'it': 'Film BOPP rigenerato al 100% da scarti post-industriali. Massimo standard ecologico senza compromessi sulle prestazioni.'}, 'udrzitelna-paska-poly-plus': {'en': 'Ecological full replacement for PVC tapes with an elegant matte surface.', 'de': 'Ökologischer und vollwertiger Ersatz für PVC-Klebebänder mit elegantem mattem Finish.', 'it': 'Sostituto ecologico e completo dei nastri in PVC con elegante superficie opaca.'}, 'udrzitelna-paska-loopp': {'en': 'Premium eco tape from recycled plastics with no compromise on strength.', 'de': 'Premium-Öko-Klebeband aus recycelten Kunststoffen ohne Kompromisse bei der Festigkeit.', 'it': 'Nastro eco premium da plastica riciclata senza compromessi sulla resistenza.'}, 'udrzitelna-paska-nopp': {'en': 'Tape with a bio-circular carrier film certified ISCC PLUS.', 'de': 'Klebeband mit Trägerfolie aus biozirkulärem Material mit ISCC-PLUS-Zertifizierung.', 'it': 'Nastro con film di supporto bio-circolare certificato ISCC PLUS.'}, 'udrzitelna-paska-nopp-plus': {'en': 'Tape with certified bio-circular film and adhesive for maximum carbon footprint reduction.', 'de': 'Klebeband mit zertifizierter biozirkulärer Folie und Klebstoff für maximale Reduktion des CO₂-Fußabdrucks.', 'it': 'Nastro con film e adesivo bio-circolari certificati per la massima riduzione dell’impronta di carbonio.'}, 'bopp-paska-acrylic': {'en': 'Reliable BOPP tape with long service life.', 'de': 'Zuverlässiges BOPP-Klebeband mit langer Lebensdauer.', 'it': 'Nastro BOPP affidabile con lunga durata.'}, 'bopp-paska-evergreen': {'en': 'Sustainable packing tape made from 50% recycled post-industrial material.', 'de': 'Nachhaltiges Verpackungsklebeband aus 50 % recyceltem postindustriellem Material.', 'it': 'Nastro da imballaggio sostenibile realizzato con il 50% di materiale riciclato post-industriale.'}, 'bopp-paska-evergreen-100': {'en': 'Sustainable packing tape made from 100% recycled post-industrial material.', 'de': 'Nachhaltiges Verpackungsklebeband aus 100 % recyceltem postindustriellem Material.', 'it': 'Nastro da imballaggio sostenibile realizzato con il 100% di materiale riciclato post-industriale.'}, 'bopp-paska-tamper-evident': {'en': 'BOPP tape with security print for immediate detection of unauthorized parcel opening.', 'de': 'BOPP-Klebeband mit Sicherheitsdruck zur sofortigen Erkennung unbefugten Öffnens.', 'it': 'Nastro BOPP con stampa di sicurezza per rilevare subito aperture non autorizzate.'}, 'bopp-paska-hot-melt': {'en': 'BOPP tape with hot melt adhesive for fast, strong bonding.', 'de': 'BOPP-Klebeband mit Hot-Melt-Klebstoff für schnelle, feste Haftung.', 'it': "Nastro BOPP con adesivo hot melt per un'adesione rapida e resistente."}, 'bopp-paska-extra-glue-plus': {'en': 'Acrylic tape with an increased adhesive layer for demanding surfaces.', 'de': 'Acrylklebeband mit erhöhter Klebstoffschicht für anspruchsvolle Oberflächen.', 'it': 'Nastro acrilico con strato adesivo aumentato per superfici impegnative.'}, 'bopp-paska-tack-plus': {'en': 'HOT MELT tape with extreme adhesion and instant tack. For demanding applications.', 'de': 'HOT-MELT-Klebeband mit extremer Haftung und sofortigem Tack. Für anspruchsvolle Anwendungen.', 'it': 'Nastro HOT MELT con adesione estrema e effetto tack immediato. Per applicazioni impegnative.'}, 'bopet-paska-ait23': {'en': 'Strong packing tape with a polyester carrier and acrylic adhesive.', 'de': 'Festes Verpackungsklebeband mit Polyesterträger und Acrylklebstoff.', 'it': 'Nastro da imballaggio resistente con supporto in poliestere e adesivo acrilico.'}, 'bopet-paska-ate23': {'en': 'Security BOPET tape that reveals unauthorized tampering.', 'de': 'Sicherheits-BOPET-Klebeband, das unbefugte Manipulation erkennbar macht.', 'it': 'Nastro BOPET di sicurezza che rivela manipolazioni non autorizzate.'}, 'bopet-paska-eco-hit19': {'en': 'BOPET tape made from 90% recycled PET bottles.', 'de': 'BOPET-Klebeband aus 90 % recycelten PET-Flaschen.', 'it': 'Nastro BOPET da PET riciclato di bottiglie al 90%.'}, 'bopet-paska-eco-hit23': {'en': 'Stronger BOPET tape made from 90% recycled PET bottles.', 'de': 'Stärkeres BOPET-Klebeband aus 90 % recycelten PET-Flaschen.', 'it': 'Nastro BOPET più resistente da PET riciclato di bottiglie al 90%.'}, 'bopet-paska-hit17': {'en': 'High-strength packing tape with a polyester carrier.', 'de': 'Hochfestes Verpackungsklebeband mit Polyesterträger.', 'it': 'Nastro da imballaggio ad alta resistenza con supporto in poliestere.'}, 'papirova-paska-c660': {'en': 'An eco-friendly solution for elegant packaging with high adhesion.', 'de': 'Eine umweltfreundliche Lösung für elegantes Verpacken mit hoher Klebkraft.', 'it': 'Una soluzione ecologica per un imballaggio elegante con elevata adesione.'}, 'papirova-paska-c680': {'en': 'Thinner profile with higher tensile strength for efficient packaging.', 'de': 'Dünneres Profil mit höherer Zugfestigkeit für effizientes Verpacken.', 'it': 'Profilo più sottile con maggiore resistenza alla trazione per un imballaggio efficiente.'}, 'papirova-paska-c680-rt': {'en': 'Cross-reinforced glass-fibre tape for the most demanding shipments.', 'de': 'Kreuzweise glasfaserverstärktes Band für anspruchsvollste Sendungen.', 'it': 'Nastro con rinforzo a croce in fibra di vetro per le spedizioni più impegnative.'}, 'papirova-paska-c680r': {'en': 'Glass-fibre reinforced tape for secure packing of heavier cartons.', 'de': 'Glasfaserverstärktes Band für sicheres Verpacken schwererer Kartons.', 'it': 'Nastro rinforzato con fibra di vetro per imballare in sicurezza cartoni più pesanti.'}, 'papirova-paska-c690': {'en': 'Heavy crepe paper for the most demanding cartons.', 'de': 'Schweres Krepppapier für anspruchsvollste Kartons.', 'it': 'Carta crespa pesante per i cartoni più impegnativi.'}, 'papirova-paska-c780': {'en': 'Premium combination of crepe and natural rubber for demanding temperature conditions.', 'de': 'Premium-Kombination aus Krepp und Naturkautschuk für anspruchsvolle Temperaturbedingungen.', 'it': 'Combinazione premium di carta crespa e gomma naturale per condizioni di temperatura impegnative.'}, 'papirova-paska-kh80': {'en': 'Exclusive paper tape from 100% recycled material – the perfect blend of high aesthetics, instant adhesion and care for nature.', 'de': 'Exklusives Papierklebeband aus 100 % recyceltem Material – die perfekte Verbindung aus hoher Ästhetik, Soforthaftung und Rücksicht auf die Natur.', 'it': 'Nastro di carta esclusivo in materiale riciclato al 100%: il connubio perfetto tra estetica elevata, adesione immediata e rispetto per la natura.'}, 'papirova-paska-ks165': {'en': 'Uncompromising paper solution with extreme load capacity for the heaviest industrial packing, pallet securing and strapping.', 'de': 'Kompromisslose Papierlösung mit extremer Tragfähigkeit für schwerstes Industrieverpacken, Palettenfixierung und Umreifung.', 'it': 'Soluzione in carta senza compromessi con capacità di carico estrema per imballaggi industriali pesanti, fissaggio pallet e reggiatura.'}, 'odstranitelna-paska-eco-rit19': {'en': 'Gentle removable tape with recycled content.', 'de': 'Schonendes abziehbares Klebeband mit recyceltem Anteil.', 'it': 'Nastro rimovibile delicato con contenuto riciclato.'}, 'odstranitelna-paska-r28-32': {'en': 'Removable tape that leaves no trace after peeling.', 'de': 'Abziehbares Klebeband, das nach dem Entfernen keine Spuren hinterlässt.', 'it': 'Nastro rimovibile che non lascia tracce dopo la rimozione.'}, 'vyztuzena-paska-rmpp32': {'en': 'Reinforced tape with glass fibres for securing heavy loads.', 'de': 'Verstärktes Klebeband mit Glasfasern zur Sicherung schwerer Lasten.', 'it': 'Nastro rinforzato con fibre di vetro per fissare carichi pesanti.'}, 'vyztuzena-paska-rtpp32': {'en': 'Cross-reinforced tape for maximum strength in all directions.', 'de': 'Kreuzverstärktes Klebeband für maximale Festigkeit in alle Richtungen.', 'it': 'Nastro rinforzato incrociato per la massima resistenza in ogni direzione.'}, 'mopp-paska-s45-50': {'en': 'Monoaxial MOPP tape with extreme strength and zero stretch.', 'de': 'Monoaxiales MOPP-Band mit extremer Festigkeit und null Dehnung.', 'it': 'Nastro MOPP monoassiale con resistenza estrema e allungamento nullo.'}, 'textilni-paska-bc': {'en': 'Strong cloth (duct) tape for repairs and universal use.', 'de': 'Starkes Gewebeband (Duct Tape) für Reparaturen und universellen Einsatz.', 'it': 'Nastro telato resistente (duct tape) per riparazioni e uso universale.'}, 'textilni-paska-bc2': {'en': 'Extra-strong cloth tape with high tensile strength.', 'de': 'Extra starkes Gewebeband mit hoher Zugfestigkeit.', 'it': 'Nastro telato extra resistente con elevata resistenza alla trazione.'}, 'textilni-paska-nu': {'en': 'Universal cloth tape for quick bundling and fixing.', 'de': 'Universelles Gewebeband für schnelles Bündeln und Fixieren.', 'it': 'Nastro telato universale per fascettatura e fissaggio rapidi.'}, 'malirska-paska-c580': {'en': 'Crepe masking tape for sharp edges in everyday painting.', 'de': 'Krepp-Malerklebeband für saubere Kanten beim regulären Streichen.', 'it': 'Nastro per mascheratura in carta crespata per bordi netti nella pittura quotidiana.'}, 'malirska-paska-cs60-80': {'en': 'Heat-resistant masking tape for painting and demanding masking.', 'de': 'Hitzebeständiges Malerklebeband für Lackierung und anspruchsvolles Abkleben.', 'it': 'Nastro per mascheratura resistente al calore per verniciatura e mascherature impegnative.'}}
USE_MAP: dict[str, dict[str, str]] = {'Zabezpečení zásilek proti neoprávněnému otevření': {'en': 'Securing shipments against unauthorized opening', 'de': 'Sicherung von Sendungen gegen unbefugtes Öffnen', 'it': 'Protezione delle spedizioni contro l’apertura non autorizzata'}, 'E-commerce a cenné balíky': {'en': 'E-commerce and valuable parcels', 'de': 'E-Commerce und wertvolle Pakete', 'it': 'E-commerce e pacchi di valore'}, 'Aplikace s důrazem na udržitelnější materiál': {'en': 'Applications with a focus on more sustainable materials', 'de': 'Anwendungen mit Fokus auf nachhaltigere Materialien', 'it': 'Applicazioni con attenzione a materiali più sostenibili'}, 'Automatické balicí linky s ESG cíli': {'en': 'Automatic packing lines with ESG goals', 'de': 'Automatische Verpackungslinien mit ESG-Zielen', 'it': 'Linee di imballaggio automatiche con obiettivi ESG'}, 'Automatické balicí stroje': {'en': 'Automatic packing machines', 'de': 'Automatische Verpackungsmaschinen', 'it': 'Macchine automatiche per imballaggio'}, 'Budování zodpovědné značky': {'en': 'Building a responsible brand', 'de': 'Aufbau einer verantwortungsvollen Marke', 'it': 'Costruzione di un marchio responsabile'}, 'Cirkulární obalové procesy': {'en': 'Circular packaging processes', 'de': 'Zirkuläre Verpackungsprozesse', 'it': 'Processi di imballaggio circolari'}, 'Dočasné značení a etikety': {'en': 'Temporary marking and labels', 'de': 'Temporäre Kennzeichnung und Etiketten', 'it': 'Marcature ed etichette temporanee'}, 'E-shopy s důrazem na udržitelné balení': {'en': 'E-shops focused on sustainable packaging', 'de': 'E-Shops mit Fokus auf nachhaltige Verpackung', 'it': 'E-shop orientati al packaging sostenibile'}, 'Elektrotechnika a specializovaná výroba': {'en': 'Electronics and specialised manufacturing', 'de': 'Elektrotechnik und spezialisierte Fertigung', 'it': 'Elettrotecnica e produzione specializzata'}, 'Expedice a skladová logistika': {'en': 'Dispatch and warehouse logistics', 'de': 'Versand und Lagerlogistik', 'it': 'Spedizione e logistica di magazzino'}, 'Firemní branding přímo na zásilce': {'en': 'Corporate branding directly on shipments', 'de': 'Firmen-Branding direkt auf der Sendung', 'it': 'Branding aziendale direttamente sulle spedizioni'}, 'Firmy s ESG a udržitelnými cíli': {'en': 'Companies with ESG and sustainability goals', 'de': 'Unternehmen mit ESG- und Nachhaltigkeitszielen', 'it': 'Aziende con obiettivi ESG e di sostenibilità'}, 'Fixace dveří elektrospotřebičů': {'en': 'Securing appliance doors', 'de': 'Fixierung von Gerätetüren', 'it': 'Fissaggio delle porte degli elettrodomestici'}, 'Fixace těžkých a nadrozměrných balíků': {'en': 'Securing heavy and oversized parcels', 'de': 'Sicherung schwerer und übergroßer Pakete', 'it': 'Fissaggio di colli pesanti e fuori sagoma'}, 'Fixace v prostředí s vysokými teplotami': {'en': 'Fixing in high-temperature environments', 'de': 'Fixierung in Umgebungen mit hohen Temperaturen', 'it': 'Fissaggio in ambienti ad alta temperatura'}, 'Fixace, která se musí opět odstranit': {'en': 'Fixing that must be removed again', 'de': 'Fixierungen, die wieder entfernt werden müssen', 'it': 'Fissaggi che devono essere rimossi'}, 'Kutilské a řemeslné práce': {'en': 'DIY and craft work', 'de': 'Heimwerker- und Handwerksarbeiten', 'it': 'Lavori fai da te e artigianali'}, 'Lakovny a autolakovny': {'en': 'Paint shops and body shops', 'de': 'Lackierereien und Autolackierereien', 'it': 'Verniciature industriali e carrozzerie'}, 'Logistické a výrobní procesy': {'en': 'Logistics and production processes', 'de': 'Logistische und Produktionsprozesse', 'it': 'Processi logistici e produttivi'}, 'Malování a lakování interiérů': {'en': 'Interior painting and coating', 'de': 'Innenanstrich und Lackierung', 'it': 'Pittura e verniciatura di interni'}, 'Maskování při práškovém lakování': {'en': 'Masking during powder coating', 'de': 'Abkleben bei der Pulverbeschichtung', 'it': 'Mascheratura nella verniciatura a polvere'}, 'Náročné průmyslové provozy': {'en': 'Demanding industrial operations', 'de': 'Anspruchsvolle Industriebetriebe', 'it': 'Impianti industriali impegnativi'}, 'Ochrana citlivých povrchů': {'en': 'Protection of sensitive surfaces', 'de': 'Schutz empfindlicher Oberflächen', 'it': 'Protezione di superfici sensibili'}, 'Potisk až 10 barev (reverse printing)': {'en': 'Printing up to 10 colours (reverse printing)', 'de': 'Bedruckung bis zu 10 Farben (Reverse-Druck)', 'it': 'Stampa fino a 10 colori (reverse printing)'}, 'Potisk firemním logem a informacemi': {'en': 'Printing with company logos and information', 'de': 'Bedruckung mit Firmenlogo und Informationen', 'it': 'Stampa con logo e informazioni aziendali'}, 'Recyklovaný karton a náročné povrchy': {'en': 'Recycled cardboard and demanding surfaces', 'de': 'Recyclingkarton und anspruchsvolle Oberflächen', 'it': 'Cartone riciclato e superfici difficili'}, 'Provoz v chladírenských a mrazicích skladech': {'en': 'Use in chilled and frozen warehouses', 'de': 'Einsatz in Kühl- und Tiefkühllagern', 'it': 'Utilizzo in magazzini refrigerati e congelati'}, 'Práškové lakování a vysokoteplotní procesy': {'en': 'Powder coating and high-temperature processes', 'de': 'Pulverbeschichtung und hochtemperaturfähige Prozesse', 'it': 'Verniciatura a polvere e processi ad alta temperatura'}, 'Ruční balení a uzavírání e-commerce zásilek': {'en': 'Manual packing and sealing of e-commerce shipments', 'de': 'Manuelles Verpacken und Verschließen von E-Commerce-Sendungen', 'it': 'Imballaggio manuale e chiusura di spedizioni e-commerce'}, 'Ruční i poloautomatické balení': {'en': 'Manual and semi-automatic packing', 'de': 'Manuelles und halbautomatisches Verpacken', 'it': 'Imballaggio manuale e semiautomatico'}, 'Rychlé opravy a provizorní spoje': {'en': 'Quick repairs and temporary joints', 'de': 'Schnelle Reparaturen und provisorische Verbindungen', 'it': 'Riparazioni rapide e giunzioni provvisorie'}, 'Stahování a fixace palet': {'en': 'Strapping and securing pallets', 'de': 'Umreifung und Fixierung von Paletten', 'it': 'Reggiatura e fissaggio dei pallet'}, 'Standardní uzavírání kartonů': {'en': 'Standard carton sealing', 'de': 'Standard-Kartonverschluss', 'it': 'Chiusura standard dei cartoni'}, 'Strojové balení těžkých zásilek': {'en': 'Machine packing of heavy shipments', 'de': 'Maschinelles Verpacken schwerer Sendungen', 'it': 'Imballaggio automatico di spedizioni pesanti'}, 'Svazování a fixace předmětů': {'en': 'Bundling and securing items', 'de': 'Bündeln und Fixieren von Gegenständen', 'it': 'Fascettatura e fissaggio di oggetti'}, 'Svazování bez skelných vláken': {'en': 'Bundling without glass fibres', 'de': 'Bündeln ohne Glasfasern', 'it': 'Fascettatura senza fibre di vetro'}, 'Svazování trubek, profilů a tyčí': {'en': 'Bundling pipes, profiles and rods', 'de': 'Bündeln von Rohren, Profilen und Stäben', 'it': 'Fascettatura di tubi, profili e barre'}, 'Tiché ruční odvíjení ve skladech a expedici': {'en': 'Quiet manual unwinding in warehouses and dispatch', 'de': 'Leises manuelles Abrollen in Lagern und im Versand', 'it': 'Svolgimento manuale silenzioso in magazzino e spedizione'}, 'Uzavírání kartonových krabic a obalů': {'en': 'Sealing cardboard boxes and packaging', 'de': 'Verschließen von Kartonschachteln und Verpackungen', 'it': 'Chiusura di scatole e imballaggi in cartone'}, 'Uzavírání kartonů všech typů povrchů': {'en': 'Sealing cartons of all surface types', 'de': 'Verschließen von Kartons aller Oberflächentypen', 'it': 'Chiusura di cartoni su tutti i tipi di superficie'}, 'Zajištění komponentů během přepravy': {'en': 'Securing components during transport', 'de': 'Sicherung von Komponenten während des Transports', 'it': 'Messa in sicurezza dei componenti durante il trasporto'}, 'Zajištění zboží na paletách': {'en': 'Securing goods on pallets', 'de': 'Sicherung von Waren auf Paletten', 'it': 'Messa in sicurezza delle merci sui pallet'}, 'Zakrývání hran a přechodů': {'en': 'Masking edges and transitions', 'de': 'Abkleben von Kanten und Übergängen', 'it': 'Mascheratura di bordi e passaggi'}, 'Zelené balení pro e-shopy': {'en': 'Green packaging for e-shops', 'de': 'Grüne Verpackung für E-Shops', 'it': 'Imballaggi verdi per e-shop'}, 'Zpevnění balíků a obalů': {'en': 'Reinforcing parcels and packaging', 'de': 'Verstärkung von Paketen und Verpackungen', 'it': 'Rinforzo di colli e imballaggi'}, 'Údržba, montáže a řemeslo': {'en': 'Maintenance, assembly and craft work', 'de': 'Wartung, Montage und Handwerk', 'it': 'Manutenzione, montaggio e lavori artigianali'}, 'Ruční balení s tichým (low noise) odvíjením': {'en': 'Manual packing with quiet (low noise) unwinding', 'de': 'Manuelles Verpacken mit leisem (Low-Noise) Abrollen', 'it': 'Imballaggio manuale con svolgimento silenzioso (low noise)'}, 'Automatické balicí stroje – hlučná (noisy) verze': {'en': 'Automatic packing machines – noisy version', 'de': 'Automatische Verpackungsmaschinen – laute (Noisy) Version', 'it': 'Macchine automatiche per imballaggio – versione noisy'}, 'Recyklované kartony a prašné prostředí': {'en': 'Recycled cartons and dusty environments', 'de': 'Recyclingkartons und staubige Umgebungen', 'it': 'Cartoni riciclati e ambienti polverosi'}, 'Zabezpečení zásilek na stretch fólii': {'en': 'Securing shipments on stretch film', 'de': 'Sicherung von Sendungen auf Stretchfolie', 'it': 'Sicurezza delle spedizioni su film stretch'}}

CTA_MAP: dict[str, dict[str, str]] = {
    'Chci vzorek zdarma': {'en': 'I want a free sample', 'de': 'Ich möchte ein kostenloses Muster', 'it': 'Voglio un campione gratuito'},
    'Kalkulace s potiskem': {'en': 'Quote with printing', 'de': 'Kalkulation mit Bedruckung', 'it': 'Preventivo con stampa'},
    'Vyžádat kalkulaci': {'en': 'Request a quote', 'de': 'Kalkulation anfordern', 'it': 'Richiedi un preventivo'},
    'Konzultace parametrů před objednávkou': {'en': 'Parameter consultation before ordering', 'de': 'Beratung zu den Parametern vor der Bestellung', 'it': "Consulenza sui parametri prima dell'ordine"},
    'Nezávazně konzultovat': {'en': 'Request a consultation', 'de': 'Unverbindlich beraten lassen', 'it': 'Richiedi una consulenza'},
    'Poptat MOPP pásku': {'en': 'Enquire about MOPP tape', 'de': 'MOPP-Band anfragen', 'it': 'Richiedi nastro MOPP'},
    'Poptat malířskou pásku': {'en': 'Enquire about masking tape', 'de': 'Malerklebeband anfragen', 'it': 'Richiedi nastro per mascheratura'},
    'Poptat odstranitelnou pásku': {'en': 'Enquire about removable tape', 'de': 'Abziehbares Klebeband anfragen', 'it': 'Richiedi nastro rimovibile'},
    'Poptat textilní pásku': {'en': 'Enquire about cloth tape', 'de': 'Gewebeband anfragen', 'it': 'Richiedi nastro telato'},
    'Poptat vyztuženou pásku': {'en': 'Enquire about reinforced tape', 'de': 'Verstärktes Klebeband anfragen', 'it': 'Richiedi nastro rinforzato'},
    'Poptat udržitelnou pásku s potiskem': {'en': 'Enquire about sustainable printed tape', 'de': 'Nachhaltiges bedrucktes Band anfragen', 'it': 'Richiedi nastro sostenibile stampato'},
    'Poptat BOPP pásku s logem': {'en': 'Enquire about BOPP tape with logo', 'de': 'BOPP-Band mit Logo anfragen', 'it': 'Richiedi nastro BOPP con logo'},
    'Poptat BOPET pásku na míru': {'en': 'Enquire about custom BOPET tape', 'de': 'Maßgeschneidertes BOPET-Band anfragen', 'it': 'Richiedi nastro BOPET su misura'},
    'Poptat eko pásku s potiskem': {'en': 'Enquire about eco printed tape', 'de': 'Öko-Band mit Bedruckung anfragen', 'it': 'Richiedi nastro ecologico stampato'},
    'Poptat z této kategorie': {'en': 'Enquire from this category', 'de': 'Aus dieser Kategorie anfragen', 'it': 'Richiedi da questa categoria'},
    'Vyžádat cenovou nabídku': {'en': 'Request a quote', 'de': 'Angebot anfordern', 'it': 'Richiedi un preventivo'},
    'Vzorek nebo kalkulace zdarma': {'en': 'Free sample or quote', 'de': 'Kostenloses Muster oder Kalkulation', 'it': 'Campione o preventivo gratuito'},
    'Otestování kvality před objednáním': {'en': 'Quality testing before ordering', 'de': 'Qualitätsprüfung vor der Bestellung', 'it': "Test della qualità prima dell'ordine"},
    'Vzorek s vaším logem před objednávkou': {'en': 'Quality testing before ordering', 'de': 'Qualitätsprüfung vor der Bestellung', 'it': "Test della qualità prima dell'ordine"},
}

BENEFIT_TITLE_MAP: dict[str, dict[str, str]] = {'Prémiový matný vzhled': {'en': 'Premium matte look', 'de': 'Premium-Mattoptik', 'it': 'Aspetto opaco premium'}, 'Robustní 35µm nosič se zesíleným lepidlem': {'en': 'Robust 35 µm carrier with reinforced adhesive', 'de': 'Robuster 35-µm-Träger mit verstärktem Klebstoff', 'it': 'Supporto robusto da 35 µm con adesivo rinforzato'}, 'Plnohodnotná ekologická náhrada za PVC pásky': {'en': 'Full ecological replacement for PVC tapes', 'de': 'Vollwertiger ökologischer Ersatz für PVC-Klebebänder', 'it': 'Sostituto ecologico completo dei nastri in PVC'}, 'Zesílená přilnavost pro náročné kartony': {'en': 'Enhanced adhesion for demanding cartons', 'de': 'Verstärkte Haftung für anspruchsvolle Kartons', 'it': 'Adesione rafforzata per cartoni impegnativi'}, 'Plně bio-cirkulární složení fólie i lepidla': {'en': 'Fully bio-circular film and adhesive composition', 'de': 'Vollständig biozirkuläre Zusammensetzung von Folie und Klebstoff', 'it': 'Composizione completamente bio-circolare di film e adesivo'}, 'Certifikovaný nosič z borovicového oleje': {'en': 'Certified carrier from pine oil', 'de': 'Zertifizierter Träger aus Kiefernholzöl', 'it': 'Supporto certificato da olio di pino'}, 'VOID efekt při odlepení': {'en': 'VOID effect on removal', 'de': 'VOID-Effekt beim Abziehen', 'it': 'Effetto VOID alla rimozione'}, 'Neutrální vzhled': {'en': 'Neutral appearance', 'de': 'Neutrales Erscheinungsbild', 'it': 'Aspetto neutro'}, 'Kartony i stretch fólie': {'en': 'Cardboard and stretch film', 'de': 'Karton und Stretchfolie', 'it': 'Cartone e film stretch'}, 'Akrylové lepidlo': {'en': 'Acrylic adhesive', 'de': 'Acrylklebstoff', 'it': 'Adesivo acrilico'}, 'Barevné odlišení zásilek': {'en': 'Colour-coded shipment identification', 'de': 'Farbliche Kennzeichnung von Sendungen', 'it': 'Identificazione visiva delle spedizioni'}, 'Bez skelných vláken': {'en': 'No glass fibres', 'de': 'Ohne Glasfasern', 'it': 'Senza fibre di vetro'}, 'Beze stop po odlepení': {'en': 'No residue after removal', 'de': 'Keine Rückstände nach dem Abziehen', 'it': 'Senza residui dopo la rimozione'}, 'Bezplastový papírový nosič': {'en': 'Plastic-free paper carrier', 'de': 'Plastikfreier Papierträger', 'it': 'Supporto in carta senza plastica'}, 'Chemická odolnost': {'en': 'Chemical resistance', 'de': 'Chemische Beständigkeit', 'it': 'Resistenza chimica'}, 'Dlouhá životnost': {'en': 'Long service life', 'de': 'Lange Lebensdauer', 'it': 'Lunga durata'}, 'Ekologická alternativa k PVC': {'en': 'Eco-friendly PVC alternative', 'de': 'Ökologische PVC-Alternative', 'it': 'Alternativa ecologica al PVC'}, 'Extrémní teploty': {'en': 'Extreme temperatures', 'de': 'Extreme Temperaturen', 'it': 'Temperature estreme'}, 'Fixace těžkých břemen': {'en': 'Securing heavy loads', 'de': 'Sicherung schwerer Lasten', 'it': 'Fissaggio di carichi pesanti'}, 'HOT MELT lepidlo': {'en': 'Hot melt adhesive', 'de': 'Hot-Melt-Klebstoff', 'it': 'Adesivo hot melt'}, 'Hot melt lepidlo': {'en': 'Hot melt adhesive', 'de': 'Hot-Melt-Klebstoff', 'it': 'Adesivo hot melt'}, 'Kaučukové lepidlo': {'en': 'Rubber adhesive', 'de': 'Kautschukklebstoff', 'it': 'Adesivo in gomma'}, 'Křížová skelná vlákna': {'en': 'Cross-laid glass fibres', 'de': 'Kreuzweise Glasfasern', 'it': 'Fibre di vetro incrociate'}, 'Ostré hrany bez protečení': {'en': 'Sharp edges without bleed-through', 'de': 'Saubere Kanten ohne Auslaufen', 'it': 'Bordi netti senza sbavature'}, 'Plná recyklovatelnost': {'en': 'Fully recyclable', 'de': 'Vollständig recycelbar', 'it': 'Completamente riciclabile'}, 'Krepový nosič FSC': {'en': 'FSC crepe carrier', 'de': 'FSC-Kreppträger', 'it': 'Supporto crespo FSC'}, 'Hladký Kraft papír 165 g/m²': {'en': 'Smooth kraft paper 165 g/m²', 'de': 'Glattes Kraftpapier 165 g/m²', 'it': 'Carta kraft liscia 165 g/m²'}, 'Recyklovaný Kraft papír 80 g/m²': {'en': 'Recycled kraft paper 80 g/m²', 'de': 'Recyceltes Kraftpapier 80 g/m²', 'it': 'Carta kraft riciclata 80 g/m²'}, 'Snadná recyklace PAP22': {'en': 'Easy recycling PAP22', 'de': 'Einfaches Recycling PAP22', 'it': 'Riciclo facile PAP22'}, 'Extrémní pevnost v tahu (150 N/cm)': {'en': 'Extreme tensile strength (150 N/cm)', 'de': 'Extreme Zugfestigkeit (150 N/cm)', 'it': 'Estrema resistenza alla trazione (150 N/cm)'}, 'Rychlá přilnavost': {'en': 'Fast adhesion', 'de': 'Schnelle Haftung', 'it': 'Adesione rapida'}, 'Extrémní přilnavost': {'en': 'Extreme adhesion', 'de': 'Extreme Haftung', 'it': 'Adesione estrema'}, 'Lepidlo z přírodního kaučuku (Solvent)': {'en': 'Natural rubber adhesive (Solvent)', 'de': 'Naturkautschukkleber (Solvent)', 'it': 'Adesivo in gomma naturale (Solvent)'}, 'Silnější gramáž nosiče (72 g/m²)': {'en': 'Heavier carrier grammage (72 g/m²)', 'de': 'Höhere Trägergrammatur (72 g/m²)', 'it': 'Grammatura del supporto più elevata (72 g/m²)'}, 'Zvýšená pevnost v tahu': {'en': 'Increased tensile strength', 'de': 'Erhöhte Zugfestigkeit', 'it': 'Maggiore resistenza alla trazione'}, 'Podélná skelná výztuž': {'en': 'Longitudinal glass-fibre reinforcement', 'de': 'Längs verlaufende Glasfaserverstärkung', 'it': 'Rinforzo longitudinale in fibra di vetro'}, 'Křížová mřížková výztuž': {'en': 'Cross-woven mesh reinforcement', 'de': 'Kreuzweise Gitterverstärkung', 'it': 'Rinforzo a maglia incrociata'}, 'Podélná skelná vlákna': {'en': 'Longitudinal glass fibres', 'de': 'Längs verlaufende Glasfasern', 'it': 'Fibre di vetro longitudinali'}, 'Přilnavost na drsný povrch': {'en': 'Adhesion on rough surfaces', 'de': 'Haftung auf rauen Oberflächen', 'it': 'Adesione su superfici ruvide'}, 'Recyklovaný papírový nosič': {'en': 'Recycled paper carrier', 'de': 'Recycelter Papierträger', 'it': 'Supporto in carta riciclato'}, 'Recyklovaný polyester': {'en': 'Recycled polyester', 'de': 'Recyceltes Polyester', 'it': 'Poliestere riciclato'}, 'Recyklovaný polypropylen': {'en': 'Recycled polypropylene', 'de': 'Recyceltes Polypropylen', 'it': 'Polipropilene riciclato'}, 'Rychlé přilnutí': {'en': 'Fast bonding', 'de': 'Schnelle Haftung', 'it': 'Adesione rapida'}, 'Silikonové lepidlo': {'en': 'Silicone adhesive', 'de': 'Silikonklebstoff', 'it': 'Adesivo siliconico'}, 'Snadné odvíjení pro stroje': {'en': 'Easy unwinding for machines', 'de': 'Leichtes Abrollen für Maschinen', 'it': 'Svolgimento facile per macchine'}, 'Spolehlivá drživost': {'en': 'Reliable hold', 'de': 'Zuverlässige Haftung', 'it': 'Tenuta affidabile'}, 'Super tack (+20 % lepivost)': {'en': 'Super tack (+20% adhesion)', 'de': 'Super-Tack (+20 % Klebkraft)', 'it': 'Super tack (+20% adesione)'}, 'Partner pro obtížné aplikace': {'en': 'Partner for demanding applications', 'de': 'Partner für anspruchsvolle Anwendungen', 'it': 'Partner per applicazioni impegnative'}, 'Tiché odvíjení a snadné trhání': {'en': 'Quiet unwinding and easy tear', 'de': 'Leises Abrollen und leichtes Abreißen', 'it': 'Svolgimento silenzioso e strappo facile'}, 'Tiché odvíjení a UV odolnost': {'en': 'Quiet unwinding and UV resistance', 'de': 'Leises Abrollen und UV-Beständigkeit', 'it': 'Svolgimento silenzioso e resistenza UV'}, 'Zvýšená vrstva lepidla (+33 %)': {'en': 'Increased adhesive layer (+33%)', 'de': 'Erhöhte Klebstoffschicht (+33 %)', 'it': 'Strato adesivo aumentato (+33%)'}, '100% regenerovaná BOPP fólie': {'en': '100% regenerated BOPP film', 'de': '100 % regenerierte BOPP-Folie', 'it': 'Film BOPP rigenerato al 100%'}, 'Čisté odlepení': {'en': 'Clean removal', 'de': 'Sauberes Abziehen', 'it': 'Rimozione pulita'}, 'Nejčistější lepidlo': {'en': 'Cleanest adhesive', 'de': 'Sauberster Klebstoff', 'it': 'Adesivo più puro'}, 'Low noise odvíjení': {'en': 'Low-noise unwinding', 'de': 'Low-Noise-Abrollen', 'it': 'Svolgimento low noise'}, 'Vysoká odolnost proti UV': {'en': 'High UV resistance', 'de': 'Hohe UV-Beständigkeit', 'it': 'Elevata resistenza ai raggi UV'}, 'Snadné odvíjení': {'en': 'Easy unwinding', 'de': 'Leichtes Abrollen', 'it': 'Svolgimento facile'}, 'Partner pro recyklované kartony': {'en': 'Partner for recycled cartons', 'de': 'Partner für Recyclingkartons', 'it': 'Partner per cartoni riciclati'}, 'Vysoká přilnavost': {'en': 'High adhesion', 'de': 'Hohe Klebkraft', 'it': 'Elevata adesione'}, 'Stejná cena i kvalita': {'en': 'Same price and quality', 'de': 'Gleicher Preis und gleiche Qualität', 'it': 'Stesso prezzo e stessa qualità'}, 'Identické mechanické vlastnosti': {'en': 'Identical mechanical properties', 'de': 'Identische mechanische Eigenschaften', 'it': 'Proprietà meccaniche identiche'}, 'Fólie z vlastního výrobního odpadu': {'en': 'Film from our own production waste', 'de': 'Folie aus eigenem Produktionsabfall', 'it': 'Film dai nostri scarti di produzione'}, 'Fólie z vlastního odpadu z výroby': {'en': 'Film from our own production waste', 'de': 'Folie aus eigenem Produktionsabfall', 'it': 'Film dai nostri scarti di produzione'}, 'Podpora firemní reputace': {'en': 'Supporting corporate reputation', 'de': 'Stärkung der Unternehmensreputation', 'it': 'Supporto alla reputazione aziendale'}, 'Okamžitá detekce manipulace': {'en': 'Immediate tamper detection', 'de': 'Sofortige Manipulationserkennung', 'it': 'Rilevamento immediato delle manomissioni'}, 'Možnost vlastní personalizace': {'en': 'Custom personalization options', 'de': 'Individuelle Personalisierung möglich', 'it': 'Possibilità di personalizzazione'}, 'Inovativní recyklace (PIR)': {'en': 'Innovative recycling (PIR)', 'de': 'Innovatives Recycling (PIR)', 'it': 'Riciclo innovativo (PIR)'}, 'Mimořádný výkon v chladu a extrémech': {'en': 'Outstanding performance in cold and extreme conditions', 'de': 'Außergewöhnliche Leistung bei Kälte und Extrembedingungen', 'it': 'Prestazioni eccezionali al freddo e in condizioni estreme'}, 'Výkonné akrylátové lepidlo na vodní bázi': {'en': 'High-performance water-based acrylic adhesive', 'de': 'Hochleistungsfähiger wasserbasierter Acrylatkleber', 'it': 'Adesivo acrilico ad alte prestazioni a base d’acqua'}, 'Evropský patent & min. 85 % recyklovaného PET odpadu': {'en': 'European patent & min. 85% recycled PET waste', 'de': 'Europäisches Patent & min. 85 % recycelter PET-Abfall', 'it': 'Brevetto europeo e min. 85% di PET riciclato'}, 'Podpora cirkulární ekonomiky': {'en': 'Support for the circular economy', 'de': 'Unterstützung der Kreislaufwirtschaft', 'it': 'Supporto all’economia circolare'}, 'Extrémní mechanická odolnost': {'en': 'Extreme mechanical strength', 'de': 'Extreme mechanische Beständigkeit', 'it': 'Estrema resistenza meccanica'}, 'Vyšší efektivita díky polyesteru': {'en': 'Higher efficiency thanks to polyester', 'de': 'Höhere Effizienz dank Polyester', 'it': 'Maggiore efficienza grazie al poliestere'}, 'Inovativní tenká fólie': {'en': 'Innovative thin film', 'de': 'Innovativer dünner Film', 'it': 'Film sottile innovativo'}, 'Větší návin bez zvětšení role': {'en': 'More metres per roll without increasing diameter', 'de': 'Mehr Meter pro Rolle ohne größeren Durchmesser', 'it': 'Più metri per rotolo senza aumentare il diametro'}, 'Certifikovaný recyklovaný materiál': {'en': 'Certified recycled material', 'de': 'Zertifiziertes Recyclingmaterial', 'it': 'Materiale riciclato certificato'}, 'Identické vlastnosti jako standardní pásky': {'en': 'Identical properties to standard tapes', 'de': 'Identische Eigenschaften wie Standardbänder', 'it': 'Proprietà identiche ai nastri standard'}, 'Nižší spotřeba fosilních surovin': {'en': 'Lower consumption of fossil raw materials', 'de': 'Geringerer Verbrauch fossiler Rohstoffe', 'it': 'Minore consumo di materie prime fossili'}}

BENEFIT_TEXT_EXACT: dict[str, dict[str, str]] = {'Díky matné povrchové úpravě dodává páska balení antireflexní, prémiový charakter s perfektním kontrastem pro firemní potisk.': {'en': 'Thanks to the matte surface finish, the tape gives packaging a non-glare, premium character with perfect contrast for company printing.', 'de': 'Dank der matten Oberflächenveredelung verleiht das Band der Verpackung einen blendfreien Premium-Charakter mit perfektem Kontrast für den Firmendruck.', 'it': 'Grazie alla finitura opaca, il nastro conferisce all’imballaggio un carattere premium anti-riflesso con contrasto perfetto per la stampa aziendale.'}, 'Zesílená fólie o tloušťce 35 µm v kombinaci s výkonným akrylovým lepidlem zajišťuje vysokou mechanickou odolnost a spolehlivé uzavření i těžších kartonů.': {'en': 'Reinforced 35 µm film combined with high-performance acrylic adhesive ensures high mechanical resistance and secure sealing of even heavier cartons.', 'de': 'Verstärkte Folie mit 35 µm Dicke in Kombination mit leistungsstarkem Acrylklebstoff sorgt für hohe mechanische Beständigkeit und sicheren Verschluss auch schwererer Kartons.', 'it': 'Il film rinforzato da 35 µm combinato con adesivo acrilico ad alte prestazioni garantisce elevata resistenza meccanica e chiusura sicura anche di cartoni più pesanti.'}, 'Ideální řešení pro firmy, které chtějí nahradit ekologicky zatěžující PVC pásky. POLY+ nabízí srovnatelnou tloušťku, vysokou pevnost v tahu a prémiový vzhled.': {'en': 'Ideal solution for companies that want to replace environmentally burdensome PVC tapes. POLY+ offers comparable thickness, high tensile strength and a premium look.', 'de': 'Ideale Lösung für Unternehmen, die umweltbelastende PVC-Klebebänder ersetzen wollen. POLY+ bietet vergleichbare Dicke, hohe Zugfestigkeit und eine Premium-Optik.', 'it': 'Soluzione ideale per le aziende che vogliono sostituire i nastri in PVC impattanti sull’ambiente. POLY+ offre spessore comparabile, elevata resistenza alla trazione e un look premium.'}, 'Speciálně formulované akrylové lepidlo (Adhesive G1) přináší vyšší lepivost a okamžitou přilnavost. Páska spolehlivě drží i na drsnějších površích a recyklovaném kartonu.': {'en': 'Specially formulated acrylic adhesive (Adhesive G1) delivers higher tack and immediate adhesion. The tape holds reliably even on rougher surfaces and recycled cardboard.', 'de': 'Speziell formulierter Acrylklebstoff (Adhesive G1) sorgt für höhere Klebkraft und sofortige Haftung. Das Band hält zuverlässig auch auf raueren Oberflächen und Recyclingkarton.', 'it': 'L’adesivo acrilico formulato appositamente (Adhesive G1) offre maggiore tack e adesione immediata. Il nastro tiene in modo affidabile anche su superfici più ruvide e cartone riciclato.'}, 'NOPP+ posouvá udržitelnost na maximum. Certifikaci ISCC PLUS a obnovitelný původ z přírodních surovin má u této pásky jak nosná fólie, tak i akrylové lepidlo.': {'en': 'NOPP+ takes sustainability to the maximum. Both the carrier film and the acrylic adhesive have ISCC PLUS certification and a renewable origin from natural raw materials.', 'de': 'NOPP+ treibt Nachhaltigkeit aufs Maximum. Sowohl die Trägerfolie als auch der Acrylklebstoff verfügen über die ISCC-PLUS-Zertifizierung und einen erneuerbaren Ursprung aus natürlichen Rohstoffen.', 'it': 'NOPP+ porta la sostenibilità al massimo. Sia il film di supporto sia l’adesivo acrilico hanno certificazione ISCC PLUS e origine rinnovabile da materie prime naturali.'}, 'Redukuje závislost na primární ropě a pomáhá budovat skutečně cirkulární ekonomiku v obalovém průmyslu.': {'en': 'It reduces dependence on primary oil and helps build a truly circular economy in the packaging industry.', 'de': 'Es reduziert die Abhängigkeit von Primäröl und hilft, eine echte Kreislaufwirtschaft in der Verpackungsindustrie aufzubauen.', 'it': 'Riduce la dipendenza dal petrolio primario e aiuta a costruire una vera economia circolare nel settore dell’imballaggio.'}, 'Nosná BOPP fólie využívá obnovitelné suroviny z dřevního odpadu (vedlejší produkt výroby celulózy) s certifikací ISCC PLUS. Nahrazuje fosilní plasty bez jakýchkoliv kompromisů v pevnosti.': {'en': 'The BOPP carrier film uses renewable raw materials from wood waste (a by-product of pulp production) with ISCC PLUS certification. It replaces fossil plastics without any compromise on strength.', 'de': 'Die tragende BOPP-Folie nutzt erneuerbare Rohstoffe aus Holzabfällen (Nebenprodukt der Zellstoffherstellung) mit ISCC-PLUS-Zertifizierung. Sie ersetzt fossile Kunststoffe ohne Kompromisse bei der Festigkeit.', 'it': 'Il film di supporto BOPP utilizza materie prime rinnovabili da scarti del legno (sottoprodotto della produzione di cellulosa) con certificazione ISCC PLUS. Sostituisce le plastiche fossili senza alcun compromesso sulla resistenza.'}, 'Při sejmutí zanechá na krabici upozornění VOID / OPEN / FRAUD, které prakticky nelze odstranit.': {'en': 'When removed it leaves a VOID / OPEN / FRAUD warning on the box that is virtually impossible to eliminate.', 'de': 'Beim Abziehen hinterlässt es einen VOID-/OPEN-/FRAUD-Hinweis auf dem Karton, der praktisch nicht entfernt werden kann.', 'it': 'Una volta rimosso lascia sull’imballo un avviso VOID / OPEN / FRAUD praticamente impossibile da eliminare.'}, 'Tváří se jako běžná balicí páska, dokud ji někdo neoprávněně neodlepí.': {'en': 'It looks like ordinary packing tape until someone peels it off without authorization.', 'de': 'Es wirkt wie ein gewöhnliches Klebeband, bis es unbefugt abgezogen wird.', 'it': 'Sembra un nastro da imballaggio comune finché qualcuno non lo rimuove senza autorizzazione.'}, 'Vhodná pro všechny typy kartonů i stretch fólií, dostupná v různých barvách a s potiskem.': {'en': 'Suitable for all types of cardboard and stretch film, available in various colours and with custom printing.', 'de': 'Geeignet für alle Kartonarten und Stretchfolien, in verschiedenen Farben und mit Bedruckung erhältlich.', 'it': 'Adatto a tutti i tipi di cartone e film stretch, disponibile in vari colori e con stampa personalizzata.'}, 'Tiché odvíjení, dlouhodobá stabilita lepivosti a spolehlivý výkon ve skladových podmínkách.': {'en': 'Quiet unwinding, long-term adhesion stability and reliable performance in warehouse conditions.', 'de': 'Leises Abrollen, langfristig stabile Klebkraft und zuverlässige Leistung unter Lagerbedingungen.', 'it': 'Svolgimento silenzioso, adesione stabile nel tempo e prestazioni affidabili in magazzino.'}, 'Rychlé a pevné přilnutí i při nižších teplotách – vhodné pro ruční i strojové balení.': {'en': 'Fast, strong bonding even at lower temperatures, suitable for manual and machine packing.', 'de': 'Schnelle, feste Haftung auch bei niedrigen Temperaturen – für manuelles und maschinelles Verpacken.', 'it': 'Adesione rapida e resistente anche a basse temperature, adatta al confezionamento manuale e automatico.'}, 'Vysoká okamžitá přilnavost a pevné spojení i na recyklovaném kartonu.': {'en': 'High immediate adhesion and a firm bond even on recycled cardboard.', 'de': 'Hohe Soforthaftung und feste Verbindung auch auf Recyclingkarton.', 'it': 'Elevata adesione immediata e tenuta sicura anche sul cartone riciclato.'}, 'Stabilní výkon v extrémních teplotách a snadné odlepení bez zbytků lepidla.': {'en': 'Stable performance at extreme temperatures and clean removal without adhesive residue.', 'de': 'Stabile Leistung bei extremen Temperaturen und rückstandsfreies Ablösen.', 'it': 'Prestazioni stabili a temperature estreme e rimozione senza residui di adesivo.'}, 'Plně recyklovatelné balení – páska putuje spolu s kartonem bez oddělování.': {'en': 'Fully recyclable packaging, tape goes with the carton without separation.', 'de': 'Vollständig recycelbare Verpackung – das Band geht gemeinsam mit dem Karton ohne Trennung.', 'it': 'Imballaggio completamente riciclabile: il nastro va con il cartone senza separazione.'}, 'Páska i karton putují společně do recyklace – bez oddělování materiálů.': {'en': 'Tape and carton are recycled together, no need to separate materials.', 'de': 'Band und Karton werden gemeinsam recycelt – ohne Materialtrennung.', 'it': 'Nastro e cartone vengono riciclati insieme, senza separare i materiali.'}, 'Přírodní krepový papír z udržitelně obhospodařovaných lesů zaručuje pružnost, odolnost a čistý estetický ráz balení.': {'en': 'Natural crepe paper from sustainably managed forests ensures flexibility, durability and a clean aesthetic look for packaging.', 'de': 'Natürliches Krepppapier aus nachhaltig bewirtschafteten Wäldern garantiert Flexibilität, Widerstandsfähigkeit und eine saubere Ästhetik der Verpackung.', 'it': 'La carta crespa naturale da foreste gestite in modo sostenibile garantisce flessibilità, resistenza e un aspetto estetico pulito dell’imballaggio.'}, 'Mimořádně silný a hladký podklad z udržitelného lesního hospodářství (FSC).': {'en': 'Exceptionally strong and smooth backing from sustainable forestry (FSC).', 'de': 'Außergewöhnlich starker und glatter Träger aus nachhaltiger Forstwirtschaft (FSC).', 'it': 'Supporto eccezionalmente resistente e liscio da silvicoltura sostenibile (FSC).'}, 'Udržitelný a ekologický podklad ze 100% recyklovaného papíru s FSC certifikací.': {'en': 'Sustainable eco-friendly backing made from 100% recycled paper with FSC certification.', 'de': 'Nachhaltiger und ökologischer Träger aus 100 % Recyclingpapier mit FSC-Zertifizierung.', 'it': 'Supporto sostenibile ed ecologico in carta riciclata al 100% con certificazione FSC.'}, 'Hot Melt lepidlo (syntetický kaučuk) zajišťuje spolehlivé a okamžité uzavření obalů.': {'en': 'Hot Melt adhesive (synthetic rubber) ensures reliable and instant sealing of packs.', 'de': 'Hot-Melt-Klebstoff (Synthesekautschuk) sorgt für zuverlässiges und sofortiges Verschließen von Verpackungen.', 'it': 'L’adesivo Hot Melt (gomma sintetica) garantisce la chiusura affidabile e immediata degli imballaggi.'}, 'Certifikovaná papírová páska určená k třídění a recyklaci přímo s papírovým odpadem.': {'en': 'Certified paper tape designed to be sorted and recycled together with paper waste.', 'de': 'Zertifiziertes Papierklebeband zum Sortieren und Recyceln direkt mit dem Papierabfall.', 'it': 'Nastro di carta certificato pensato per la raccolta e il riciclo insieme ai rifiuti di carta.'}, 'Nahrazuje plastové či vázací pásky i u nadměrně těžkých kartonů a průmyslových zásilek.': {'en': 'Replaces plastic or strapping tapes even on oversized heavy cartons and industrial shipments.', 'de': 'Ersetzt Kunststoff- oder Umreifungsbänder auch bei übermäßig schweren Kartons und Industriesendungen.', 'it': 'Sostituisce nastri in plastica o reggia anche su cartoni sovradimensionati pesanti e spedizioni industriali.'}, 'Lepidlo ze syntetického kaučuku zajišťuje okamžité a spolehlivé uzavření obalů.': {'en': 'Synthetic rubber adhesive ensures instant and reliable sealing of packs.', 'de': 'Klebstoff aus Synthesekautschuk sorgt für sofortiges und zuverlässiges Verschließen von Verpackungen.', 'it': 'L’adesivo in gomma sintetica garantisce la chiusura immediata e affidabile degli imballaggi.'}, 'Nejvyšší lepivost ve své třídě okamžitě přilne i k prašným či recyklovaným kartonům.': {'en': 'Best-in-class tack that bonds instantly even to dusty or recycled cartons.', 'de': 'Beste Klebkraft ihrer Klasse – haftet sofort auch auf staubigen oder recycelten Kartons.', 'it': 'Massima adesività della categoria: aderisce subito anche a cartoni polverosi o riciclati.'}, 'Drží spolehlivě v širokém spektru teplot, nestárne a vytváří trvanlivý spoj i při delším skladování.': {'en': 'Holds reliably across a wide temperature range, does not age and forms a durable bond even during longer storage.', 'de': 'Hält zuverlässig über ein breites Temperaturspektrum, altert nicht und bildet auch bei längerer Lagerung eine dauerhafte Verbindung.', 'it': 'Mantiene l’adesione in un ampio intervallo di temperature, non invecchia e crea un legame duraturo anche con stoccaggio prolungato.'}, 'Robustnější papírový podklad pro vyšší otěruvzdornost a prémiový dojem z balíku.': {'en': 'A more robust paper backing for higher abrasion resistance and a premium look of the parcel.', 'de': 'Robusterer Papierträger für höhere Abriebfestigkeit und eine premiumhafte Paketoptik.', 'it': 'Supporto in carta più robusto per maggiore resistenza all’abrasione e un aspetto premium del pacco.'}, 'Umožňuje koncovým zákazníkům vyhodit celou krabici do papírového odpadu bez pracného odlepování pásky.': {'en': 'Lets end customers dispose of the whole box in paper waste without peeling the tape off.', 'de': 'Ermöglicht Endkunden, den gesamten Karton ohne mühsames Abziehen des Bandes in den Papierabfall zu geben.', 'it': 'Consente ai clienti finali di gettare l’intera scatola nei rifiuti di carta senza dover staccare il nastro.'}, 'I při nižší celkové tloušťce než C660 nabízí vyšší odolnost proti přetržení při balení.': {'en': 'Even with a lower total thickness than C660, it offers higher tear resistance during packing.', 'de': 'Auch bei geringerer Gesamtdicke als C660 bietet es höhere Reißfestigkeit beim Verpacken.', 'it': 'Anche con uno spessore totale inferiore rispetto al C660, offre una maggiore resistenza allo strappo in imballaggio.'}, 'Integrovaná vlákna zvyšují pevnost v tahu na 50 N/cm a brání prasknutí při těžších zásilkách.': {'en': 'Integrated fibres raise tensile strength to 50 N/cm and help prevent tearing on heavier shipments.', 'de': 'Integrierte Fasern erhöhen die Zugfestigkeit auf 50 N/cm und verhindern das Reißen bei schwereren Sendungen.', 'it': 'Le fibre integrate aumentano la resistenza alla trazione a 50 N/cm e aiutano a evitare rotture con spedizioni più pesanti.'}, 'Skelná vlákna tkaná v obou směrech dávají pásce špičkovou pevnost v tahu až 60 N/cm.': {'en': 'Glass fibres woven in both directions give the tape top tensile strength of up to 60 N/cm.', 'de': 'In beiden Richtungen gewebte Glasfasern verleihen dem Band eine Spitzen-Zugfestigkeit von bis zu 60 N/cm.', 'it': 'Le fibre di vetro intrecciate in entrambe le direzioni danno al nastro una resistenza alla trazione di punta fino a 60 N/cm.'}, 'Výkon při vysokých teplotách lakování i při mrazu – bez poškození povrchu.': {'en': 'Performance at high coating temperatures and in frost, without surface damage.', 'de': 'Leistung bei hohen Lackiertemperaturen und Frost – ohne Oberflächenschäden.', 'it': 'Prestazioni ad alte temperature di verniciatura e al freddo, senza danneggiare la superficie.'}, 'Vhodná pro lakování a náročné maskování v autoservisech.': {'en': 'Suitable for coating and demanding masking in body shops.', 'de': 'Geeignet für Lackierung und anspruchsvolles Abkleben in Werkstätten.', 'it': 'Adatta alla verniciatura e a mascherature impegnative nelle carrozzerie.'}, 'Recyklovaná PP fólie s nižší ekologickou stopou při zachování spolehlivého lepení.': {'en': 'Recycled PP film with a lower environmental footprint while maintaining reliable bonding.', 'de': 'Recycelte PP-Folie mit geringerem ökologischen Fußabdruck bei zuverlässiger Klebkraft.', 'it': 'Film PP riciclato con minore impatto ambientale mantenendo un incollaggio affidabile.'}, 'Vyrobeno výhradně z postindustriálního odpadu – plně recyklovatelná bez nového granulátu.': {'en': 'Made entirely from post-industrial waste, fully recyclable without virgin granulate.', 'de': 'Hergestellt ausschließlich aus postindustriellen Abfällen – vollständig recycelbar ohne Neumaterial.', 'it': 'Prodotto interamente da scarti post-industriali: completamente riciclabile senza granulato vergine.'}, 'Matná BOPP fólie 35 µm bez chloru a rozpouštědel – vhodná náhrada vinylových pásek.': {'en': 'Matte 35 µm BOPP film without chlorine or solvents, a suitable replacement for vinyl tapes.', 'de': 'Matte 35 µm BOPP-Folie ohne Chlor und Lösungsmittel – geeigneter Ersatz für Vinylbänder.', 'it': 'Film BOPP opaco da 35 µm senza cloro né solventi: sostituto adatto ai nastri in vinile.'}, 'Vysoká přilnavost s extrémní lepivostí oproti standard Akryl.': {'en': 'High adhesion with extreme tack compared to standard Akryl.', 'de': 'Hohe Haftung mit extremem Tack im Vergleich zu Standard-Akryl.', 'it': 'Elevata adesione con tack estremo rispetto all’Akryl standard.'}, 'Díky větší vrstvě lepidla vhodná pro obtížné aplikace jako prašné prostředí, opravdu velmi těžké balíky nebo recyklované kartony.': {'en': 'Thanks to the thicker adhesive layer, suitable for demanding applications such as dusty environments, truly very heavy parcels or recycled cardboard.', 'de': 'Dank der dickeren Klebstoffschicht geeignet für anspruchsvolle Anwendungen wie staubige Umgebungen, wirklich sehr schwere Pakete oder Recyclingkarton.', 'it': 'Grazie allo strato adesivo più spesso, adatto ad applicazioni impegnative come ambienti polverosi, pacchi davvero molto pesanti o cartone riciclato.'}, 'Akrylové lepidlo si drží lepivost i při dlouhodobém skladování i UV zatížení.': {'en': 'Acrylic adhesive keeps its tack even during long-term storage and UV exposure.', 'de': 'Acrylklebstoff behält seine Klebkraft auch bei langfristiger Lagerung und UV-Belastung.', 'it': 'L’adesivo acrilico mantiene il tack anche durante lo stoccaggio prolungato e l’esposizione ai raggi UV.'}, 'Okamžitá přilnavost s extrémní lepivostí oproti standard HOT MELT.': {'en': 'Instant adhesion with extreme tack compared to standard HOT MELT.', 'de': 'Sofortige Haftung mit extremem Tack im Vergleich zu Standard-HOT-MELT.', 'it': 'Adesione immediata con tack estremo rispetto allo HOT MELT standard.'}, 'Díky vylepšené formuli HOT MELT (tack+) vhodná pro obtížné aplikace jako prašné prostředí, velmi těžké balíky nebo recyklované kartony.': {'en': 'Thanks to the improved HOT MELT (tack+) formula, suitable for demanding applications such as dusty environments, very heavy parcels or recycled cardboard.', 'de': 'Dank der verbesserten HOT-MELT-(tack+)-Formel geeignet für anspruchsvolle Anwendungen wie staubige Umgebungen, sehr schwere Pakete oder Recyclingkarton.', 'it': 'Grazie alla formula HOT MELT (tack+) migliorata, adatta ad applicazioni impegnative come ambienti polverosi, pacchi molto pesanti o cartone riciclato.'}, 'Snižuje fyzickou námahu při ručním balení a je výborná pro automatické balicí stroje.': {'en': 'Reduces physical strain during manual packing and is excellent for automatic packing machines.', 'de': 'Reduziert die körperliche Belastung beim manuellen Verpacken und eignet sich hervorragend für automatische Verpackungsmaschinen.', 'it': 'Riduce lo sforzo fisico nel confezionamento manuale ed è ottima per macchine automatiche di imballaggio.'}, 'Okamžitá přilnavost a vyšší drživost než standardní hot melt – doporučeno pro balicí stroje.': {'en': 'Instant adhesion and higher hold than standard hot melt, recommended for packing machines.', 'de': 'Sofortige Klebkraft und höhere Haftung als Standard-Hot-Melt – empfohlen für Verpackungsmaschinen.', 'it': 'Adesione immediata e tenuta superiore al hot melt standard: consigliato per macchine da imballaggio.'}, 'Na bázi vodní disperze bez chemických rozpouštědel.': {'en': 'Water-based dispersion without chemical solvents.', 'de': 'Auf Basis einer wässrigen Dispersion ohne chemische Lösungsmittel.', 'it': 'A base di dispersione acquosa senza solventi chimici.'}, 'Možnost nehlučné úpravy – tiché odvíjení a provozní teplota až do −10 °C.': {'en': 'Optional low-noise finish, quiet unwinding and operating temperature down to −10 °C.', 'de': 'Optionale geräuscharme Ausstattung – leises Abrollen und Betriebstemperatur bis −10 °C.', 'it': 'Opzione low noise: svolgimento silenzioso e temperatura di esercizio fino a −10 °C.'}, 'Akrylové lepidlo si drží lepivost i při dlouhodobém skladování a UV zatížení.': {'en': 'Acrylic adhesive keeps its stickiness during long-term storage and UV exposure.', 'de': 'Acrylklebstoff behält die Klebkraft auch bei langer Lagerung und UV-Belastung.', 'it': "L'adesivo acrilico mantiene l'adesione anche con stoccaggio prolungato e esposizione UV."}, 'Snižuje fyzickou námahu při ručním balení a hodí se i pro automatické balicí stroje.': {'en': 'Reduces physical strain during manual packing and is also great for automatic packing machines.', 'de': 'Verringert die körperliche Belastung beim manuellen Verpacken und eignet sich auch für automatische Verpackungsmaschinen.', 'it': "Riduce lo sforzo fisico nell'imballaggio manuale ed è ideale anche per macchine automatiche."}, 'Díky vysoké lepivosti ideální na recyklované kartony a do prašného prostředí.': {'en': 'Thanks to high stickiness, ideal for recycled cartons and dusty environments.', 'de': 'Dank hoher Klebkraft ideal für Recyclingkartons und staubige Umgebungen.', 'it': "Grazie all'elevata adesività, ideale per cartoni riciclati e ambienti polverosi."}, 'Nelze snadno odlepit ze stretch fólií – zřetelný důkaz zabezpečení zásilky.': {'en': 'Hard to peel off stretch film, a clear sign of shipment security.', 'de': 'Lässt sich nicht leicht von Stretchfolie abziehen – klarer Nachweis der Sendungssicherung.', 'it': 'Difficile da staccare dal film stretch: prova evidente della sicurezza della spedizione.'}, 'Má stejné mechanické vlastnosti a spolehlivost jako standardní BOPP verze, ale bez „ekologické přirážky“.': {'en': 'It has the same mechanical properties and reliability as standard BOPP versions, but without an “eco surcharge”.', 'de': 'Gleiche mechanische Eigenschaften und Zuverlässigkeit wie Standard-BOPP-Varianten – ohne „Öko-Aufpreis“.', 'it': 'Stesse proprietà meccaniche e affidabilità delle versioni BOPP standard, ma senza “maggiorazione ecologica”.'}, 'Má stejnou pevnost v tahu a spolehlivost jako standardní BOPP verze i přes vysoký podíl recyklovaného materiálu.': {'en': 'It has the same tensile strength and reliability as standard BOPP versions despite the high recycled content.', 'de': 'Gleiche Zugfestigkeit und Zuverlässigkeit wie Standard-BOPP-Varianten – trotz hohem Recyclinganteil.', 'it': 'Stessa resistenza alla trazione e affidabilità delle versioni BOPP standard, nonostante l’alto contenuto di riciclato.'}, 'Páska vykazuje stejnou pevnost v tahu a spolehlivost jako standardní BOPP verze i přes 100% regenerovaný materiál.': {'en': 'The tape delivers the same tensile strength and reliability as standard BOPP versions despite 100% regenerated material.', 'de': 'Das Band bietet dieselbe Zugfestigkeit und Zuverlässigkeit wie Standard-BOPP-Varianten – trotz 100 % regeneriertem Material.', 'it': 'Il nastro offre la stessa resistenza alla trazione e affidabilità delle versioni BOPP standard, nonostante il materiale rigenerato al 100%.'}, 'Nosný materiál obsahuje 50 % postindustriálního odpadu, který vzniká přímo při naší výrobě fólií a je ihned efektivně vracen zpět do oběhu.': {'en': 'The carrier contains 50% post-industrial waste generated directly in our film production and immediately returned to the loop.', 'de': 'Der Träger enthält 50 % postindustriellen Abfall aus unserer Folienproduktion, der sofort effizient in den Kreislauf zurückgeführt wird.', 'it': 'Il supporto contiene il 50% di scarti post-industriali generati direttamente nella nostra produzione di film e subito reimmessi nel ciclo.'}, 'Nosný materiál obsahuje 80 % postindustriálního odpadu, který vzniká přímo při naší výrobě fólií a je ihned efektivně vracen zpět do oběhu.': {'en': 'The carrier contains 80% post-industrial waste generated directly in our film production and immediately returned to the loop.', 'de': 'Der Träger enthält 80 % postindustriellen Abfall aus unserer Folienproduktion, der sofort effizient in den Kreislauf zurückgeführt wird.', 'it': 'Il supporto contiene l’80% di scarti post-industriali generati direttamente nella nostra produzione di film e subito reimmessi nel ciclo.'}, 'Vyrobeno z čistého postindustriálního odpadu z naší vlastní výroby fólií – bez nového granulátu.': {'en': 'Made from clean post-industrial waste from our own film production, without virgin granulate.', 'de': 'Hergestellt aus sauberem postindustriellen Abfall aus unserer eigenen Folienproduktion – ohne Neumaterial.', 'it': 'Prodotto da scarti post-industriali puliti della nostra produzione di film, senza granulato vergine.'}, 'Pásky řady ECO+ spolehlivě chrání zboží a prokazují ekologickou odpovědnost – ať už v neutrálním provedení, nebo s firemním potiskem.': {'en': 'ECO+ tapes reliably protect goods and demonstrate environmental responsibility, in a plain finish or with company print.', 'de': 'ECO+-Bänder schützen Ware zuverlässig und zeigen ökologische Verantwortung – neutral oder mit Firmendruck.', 'it': 'I nastri ECO+ proteggono merce in modo affidabile e dimostrano responsabilità ambientale, in versione neutra o con stampa aziendale.'}, 'Při pokusu o odlepení zanechá viditelnou stopu VOID/FRAUD/OPEN – jakýkoliv neoprávněný vstup do zásilky je ihned odhalen.': {'en': 'Any attempt to peel it off leaves a visible VOID/FRAUD/OPEN mark – unauthorized access to the parcel is detected immediately.', 'de': 'Beim Abziehversuch hinterbleibt eine sichtbare VOID/FRAUD/OPEN-Spur – jeder unbefugte Zugriff auf die Sendung wird sofort erkannt.', 'it': 'Ogni tentativo di rimozione lascia un segno visibile VOID/FRAUD/OPEN: qualsiasi accesso non autorizzato al pacco viene rilevato subito.'}, 'Tváří se jako běžná balicí páska, dokud není neoprávněně odlepena.': {'en': 'It looks like ordinary packing tape until it is peeled off without authorization.', 'de': 'Es wirkt wie gewöhnliches Packband, bis es unbefugt abgezogen wird.', 'it': 'Sembra un nastro da imballaggio comune finché non viene rimosso senza autorizzazione.'}, 'Bezpečnostní text nebo motiv lze plně přizpůsobit (např. logo firmy, varování, vlastní text „VOID / OTEVŘENO“).': {'en': 'Security text or artwork can be fully customized (e.g. company logo, warning, custom “VOID / OPEN” text).', 'de': 'Sicherheitstext oder Motiv lassen sich vollständig anpassen (z. B. Firmenlogo, Warnhinweis, eigener Text „VOID / OFFEN“).', 'it': 'Il testo o il motivo di sicurezza sono completamente personalizzabili (es. logo aziendale, avviso, testo “VOID / APERTO”).'}, 'Páska je vyrobena z BOPP fólie s 50% podílem recyklovaného použitého kuchyňského oleje (U.C.O.) z potravinářského průmyslu. Jedná se o vysoce kvalitní postindustriální recyklát (PIR), díky kterému produkt obsahuje celkem 27 % recyklovaného materiálu.': {'en': 'The tape is made from BOPP film with 50% recycled used cooking oil (U.C.O.) from the food industry. This high-quality post-industrial recyclate (PIR) brings the product’s total recycled content to 27%.', 'de': 'Das Band besteht aus BOPP-Folie mit 50 % recyceltem gebrauchtem Speiseöl (U.C.O.) aus der Lebensmittelindustrie. Durch dieses hochwertige postindustrielle Rezyklat (PIR) enthält das Produkt insgesamt 27 % Recyclingmaterial.', 'it': 'Il nastro è realizzato in film BOPP con il 50% di olio da cucina usato riciclato (U.C.O.) dall’industria alimentare. Questo riciclato post-industriale di alta qualità (PIR) porta il contenuto totale di materiale riciclato al 27%.'}, 'Páska je vyrobena z BOPP fólie s 100% podílem recyklovaného použitého kuchyňského oleje (U.C.O.) z potravinářského průmyslu. Jedná se o vysoce kvalitní postindustriální recyklát (PIR), díky kterému produkt obsahuje celkem 54 % recyklovaného materiálu.': {'en': 'The tape is made from BOPP film with 100% recycled used cooking oil (U.C.O.) from the food industry. This high-quality post-industrial recyclate (PIR) brings the product’s total recycled content to 54%.', 'de': 'Das Band besteht aus BOPP-Folie mit 100 % recyceltem gebrauchtem Speiseöl (U.C.O.) aus der Lebensmittelindustrie. Durch dieses hochwertige postindustrielle Rezyklat (PIR) enthält das Produkt insgesamt 54 % Recyclingmaterial.', 'it': 'Il nastro è realizzato in film BOPP con il 100% di olio da cucina usato riciclato (U.C.O.) dall’industria alimentare. Questo riciclato post-industriale di alta qualità (PIR) porta il contenuto totale di materiale riciclato al 54%.'}, 'Vyvinuta pro aplikaci při teplotách blížících se 0 °C, skladování v chladném prostředí a lepení na náročné povrchy (např. méně kvalitní či recyklované kartony).': {'en': 'Designed for application near 0 °C, cold storage, and bonding to demanding surfaces (e.g. lower-grade or recycled cartons).', 'de': 'Entwickelt für die Anwendung nahe 0 °C, Kühllagerung und Verklebung auf anspruchsvollen Oberflächen (z. B. minderwertige oder recycelte Kartons).', 'it': 'Pensato per applicazione vicino a 0 °C, stoccaggio a freddo e adesione su superfici difficili (es. cartoni di qualità inferiore o riciclati).'}, 'Nabízí okamžitou přilnavost a spolehlivou lepivost, která v náročném prostředí plně nahradí i lepidla z přírodního kaučuku. Navíc neobsahuje rozpouštědla a skvěle odolává UV záření.': {'en': 'Delivers instant tack and reliable adhesion that can fully replace natural rubber adhesives in demanding environments. Solvent-free and highly UV resistant.', 'de': 'Bietet sofortige Haftung und zuverlässige Klebkraft, die in anspruchsvollen Umgebungen auch Naturkautschukkleber voll ersetzt. Lösungsmittelfrei und hervorragend UV-beständig.', 'it': 'Offre adesione immediata e affidabile, in grado di sostituire gli adesivi in gomma naturale anche in ambienti difficili. Senza solventi e molto resistente ai raggi UV.'}, 'Jediná lepicí páska v Evropě s chráněným patentem na použití recyklovaného PET z plastových lahví. Ideální volba pro e-shopy a firmy, které chtějí reálně plnit své udržitelné a ESG cíle.': {'en': 'The only adhesive tape in Europe with a protected patent for using recycled PET from plastic bottles. Ideal for e-shops and companies that want to genuinely meet sustainability and ESG goals.', 'de': 'Das einzige Klebeband in Europa mit geschütztem Patent für recyceltes PET aus Kunststoffflaschen. Ideal für E-Shops und Unternehmen, die Nachhaltigkeits- und ESG-Ziele ernsthaft erfüllen wollen.', 'it': 'L’unico nastro adesivo in Europa con brevetto protetto sull’uso di PET riciclato da bottiglie di plastica. Ideale per e-commerce e aziende che vogliono davvero raggiungere obiettivi di sostenibilità ed ESG.'}, 'Nosný materiál obsahuje 90 % PET odpadu z recyklovaných PET lahví a celkový podíl recyklovaného materiálu dosahuje 60 %. Ideální volba pro e-shopy a firmy, které chtějí plnit ESG cíle.': {'en': 'The carrier contains 90% PET waste from recycled PET bottles, with total recycled content reaching 60%. An ideal choice for e-shops and companies that want to meet ESG goals.', 'de': 'Der Träger enthält 90 % PET-Abfall aus recycelten PET-Flaschen; der gesamte Recyclinganteil erreicht 60 %. Ideal für E-Shops und Unternehmen, die ESG-Ziele erfüllen wollen.', 'it': 'Il supporto contiene il 90% di rifiuti PET da bottiglie riciclate e la quota totale di materiale riciclato arriva al 60%. Scelta ideale per e-shop e aziende che vogliono raggiungere obiettivi ESG.'}, 'Polyesterový základ dává pásce obrovskou odolnost proti přetržení – při odvíjení a aplikaci se nenatahuje ani nedeformuje.': {'en': 'The polyester backing gives the tape exceptional tear resistance – it neither stretches nor deforms during unwinding and application.', 'de': 'Der Polyesterträger verleiht dem Band enorme Reißfestigkeit – beim Abrollen und Applizieren dehnt oder verformt es sich nicht.', 'it': 'Il supporto in poliestere conferisce un’enorme resistenza allo strappo: non si allunga né si deforma durante svolgimento e applicazione.'}, 'Tenčí profil fólie pojme na standardním průměru role dvojnásobek metrů. To přináší méně častou výměnu rolí na balicích linkách, vyšší plynulost balení a úsporu skladovacího místa.': {'en': 'A thinner film profile fits twice the metres on a standard roll diameter. That means fewer roll changes on packing lines, smoother packing flow and less storage space.', 'de': 'Das dünnere Folienprofil fasst bei Standard-Rollendurchmesser die doppelte Meterzahl. Das bedeutet selteneren Rollenwechsel an Verpackungslinien, flüssigeren Betrieb und weniger Lagerplatz.', 'it': 'Il profilo più sottile del film consente il doppio dei metri su un diametro standard di rotolo. Meno cambi rotolo sulle linee, imballaggio più fluido e meno spazio a magazzino.'}, 'Mimořádně tenká, a přesto vysoce pevná fólie efektivně redukuje množství použitého plastového odpadu a snižuje váhu zásilek při zachování maximální spolehlivosti.': {'en': 'An exceptionally thin yet highly strong film that effectively reduces plastic waste and shipment weight while keeping maximum reliability.', 'de': 'Eine außergewöhnlich dünne und dennoch hochfeste Folie, die Plastikabfall und Sendungsgewicht wirksam reduziert – bei maximaler Zuverlässigkeit.', 'it': 'Un film estremamente sottile ma molto resistente che riduce efficacemente i rifiuti di plastica e il peso delle spedizioni, mantenendo la massima affidabilità.'}, 'Díky tenčí fólii se na jednu roli vejde podstatně více metrů pásky bez navýšení jejího průměru. To znamená méně častou výměnu rolí a úsporu místa při skladování.': {'en': 'Thanks to the thinner film, a single roll holds substantially more metres of tape without a larger diameter. That means fewer roll changes and less storage space.', 'de': 'Dank der dünneren Folie passen deutlich mehr Meter Band auf eine Rolle – ohne größeren Durchmesser. Das bedeutet selteneren Rollenwechsel und weniger Lagerplatz.', 'it': 'Grazie al film più sottile, un singolo rotolo contiene molti più metri di nastro senza aumentare il diametro. Meno cambi rotolo e meno spazio a magazzino.'}, 'Cirkulární BOPP fólie je vyrobená z polymerů z chemicky recyklovaného spotřebitelského plastového odpadu s mezinárodní certifikací ISCC PLUS (princip hmotnostní bilance).': {'en': 'Circular BOPP film made from polymers of chemically recycled post-consumer plastic waste with international ISCC PLUS certification (mass balance principle).', 'de': 'Zirkuläre BOPP-Folie aus Polymeren chemisch recycelten Post-Consumer-Kunststoffabfalls mit internationaler ISCC-PLUS-Zertifizierung (Massenbilanzprinzip).', 'it': 'Film BOPP circolare prodotto da polimeri di rifiuti plastici post-consumo riciclati chimicamente, con certificazione internazionale ISCC PLUS (principio del bilancio di massa).'}, 'Nabízí naprosto shodné mechanické a fyzikální parametry, pevnost v tahu i lepivost jako pásky vyráběné z prvotních fosilních surovin.': {'en': 'It offers exactly the same mechanical and physical parameters, tensile strength and tack as tapes made from virgin fossil raw materials.', 'de': 'Es bietet absolut gleiche mechanische und physikalische Parameter, Zugfestigkeit und Klebkraft wie Bänder aus fossilen Primärrohstoffen.', 'it': 'Offre parametri meccanici e fisici, resistenza alla trazione e tack assolutamente uguali ai nastri prodotti da materie prime fossili vergini.'}, 'Výrazně redukuje závislost na primární ropě a pomáhá budovat skutečně cirkulární ekonomiku v obalovém průmyslu.': {'en': 'It significantly reduces dependence on primary oil and helps build a truly circular economy in the packaging industry.', 'de': 'Es reduziert die Abhängigkeit von Primäröl deutlich und hilft, eine echte Kreislaufwirtschaft in der Verpackungsindustrie aufzubauen.', 'it': 'Riduce nettamente la dipendenza dal petrolio primario e aiuta a costruire una vera economia circolare nel settore dell’imballaggio.'}}


_NAME_PREFIX = {
    "en": {
        "Udržitelná páska ": "Sustainable tape ",
        "Papírová páska ": "Paper tape ",
        "BOPP páska ": "BOPP tape ",
        "BOPET páska ": "BOPET tape ",
        "Odstranitelná páska ": "Removable tape ",
        "Vyztužená páska ": "Reinforced tape ",
        "Textilní páska ": "Cloth tape ",
        "Malířská páska ": "Masking tape ",
        "MOPP páska ": "MOPP tape ",
    },
    "de": {
        "Udržitelná páska ": "Nachhaltiges Klebeband ",
        "Papírová páska ": "Papierklebeband ",
        "BOPP páska ": "BOPP-Klebeband ",
        "BOPET páska ": "BOPET-Klebeband ",
        "Odstranitelná páska ": "Abziehbares Klebeband ",
        "Vyztužená páska ": "Verstärktes Klebeband ",
        "Textilní páska ": "Gewebe-Klebeband ",
        "Malířská páska ": "Malerklebeband ",
        "MOPP páska ": "MOPP-Klebeband ",
    },
    "it": {
        "Udržitelná páska ": "Nastro sostenibile ",
        "Papírová páska ": "Nastro di carta ",
        "BOPP páska ": "Nastro BOPP ",
        "BOPET páska ": "Nastro BOPET ",
        "Odstranitelná páska ": "Nastro rimovibile ",
        "Vyztužená páska ": "Nastro rinforzato ",
        "Textilní páska ": "Nastro telato ",
        "Malířská páska ": "Nastro per mascheratura ",
        "MOPP páska ": "Nastro MOPP ",
    },
}


def _product_name(locale: str, name: str) -> str:
    out = name
    for source, target in _NAME_PREFIX[locale].items():
        if out.startswith(source):
            return target + out[len(source):]
    return out


def _benefit_title(locale: str, cs: str) -> str:
    if cs in BENEFIT_TITLE_MAP:
        return BENEFIT_TITLE_MAP[cs][locale]
    for pattern, tpl in (
        (r"^Pevnost v tahu (.+)$", {"en": "Tensile strength {}", "de": "Zugfestigkeit {}", "it": "Resistenza alla trazione {}"}),
        (r"^Pevnost (.+)$", {"en": "Strength {}", "de": "Festigkeit {}", "it": "Resistenza {}"}),
        (r"^Teplotní rozsah (.+)$", {"en": "Temperature range {}", "de": "Temperaturbereich {}", "it": "Intervallo di temperatura {}"}),
        (r"^Teplotní odolnost (.+)$", {"en": "Temperature resistance {}", "de": "Temperaturbeständigkeit {}", "it": "Resistenza alla temperatura {}"}),
        (r"^Extrémní pevnost (.+)$", {"en": "Extreme strength {}", "de": "Extreme Festigkeit {}", "it": "Resistenza estrema {}"}),
    ):
        m = re.match(pattern, cs)
        if m:
            parts = [_translate_param_value(locale, g) for g in m.groups()]
            return tpl[locale].format(*parts)
    raise KeyError(f"Missing benefit title translation: {cs!r}")


def _benefit_text(locale: str, cs: str) -> str:
    if cs in BENEFIT_TEXT_EXACT:
        return BENEFIT_TEXT_EXACT[cs][locale]
    patterns = (
        (r"^BOPP fólie o tloušťce (.+) vydrží napětí při balení i při dlouhodobém skladování\.$",
         {"en": "BOPP film {} thick withstands tension during packing and long-term storage.",
          "de": "BOPP-Folie mit {} Dicke hält Spannung beim Verpacken und bei langfristiger Lagerung stand.",
          "it": "Il film BOPP spesso {} resiste alla tensione durante l'imballaggio e lo stoccaggio a lungo termine."}),
        (r"^BOPP fólie \((.+)\) – po sejmutí nezanechává lepidlo ani poškození povrchu\.$",
         {"en": "BOPP film ({}), leaves no adhesive or surface damage after removal.",
          "de": "BOPP-Folie ({}) – hinterlässt nach dem Abziehen weder Klebstoff noch Oberflächenschäden.",
          "it": "Film BOPP ({}): non lascia adesivo né danni alla superficie dopo la rimozione."}),
        (r"^Kraftový papírový nosič \((.+)\) – ekologické balení s čistým matným vzhledem\.$",
         {"en": "Kraft paper carrier ({}), eco-friendly packaging with a clean matte look.",
          "de": "Kraftpapierträger ({}) – umweltfreundliche Verpackung mit sauberer matter Optik.",
          "it": "Supporto in carta kraft ({}): imballaggio ecologico con aspetto opaco e pulito."}),
        (r"^Krepový nosič \((.+)\) – barva nepronikne pod pásku při malování\.$",
         {"en": "Crepe carrier ({}), paint will not bleed under the tape.",
          "de": "Kreppträger ({}) – Farbe dringt beim Streichen nicht unter das Band.",
          "it": "Supporto in carta crespata ({}): il colore non penetra sotto il nastro durante la pittura."}),
        (r"^MOPP fólie \((.+)\) s prakticky nulovou tažností v podélném směru\.$",
         {"en": "MOPP film ({}) with virtually zero stretch in the longitudinal direction.",
          "de": "MOPP-Folie ({}) mit praktisch null Dehnung in Längsrichtung.",
          "it": "Film MOPP ({}) con allungamento praticamente nullo in direzione longitudinale."}),
        (r"^Odolnost proti UV a stárnutí v teplotním rozsahu (.+)\.$",
         {"en": "UV and ageing resistance in the temperature range {}.",
          "de": "UV- und Alterungsbeständigkeit im Temperaturbereich {}.",
          "it": "Resistenza ai raggi UV e all'invecchiamento nell'intervallo di temperatura {}."}),
        (r"^Pevnost (.+) – odolává rozpouštědlům, olejům a agresivnímu prostředí\.$",
         {"en": "Strength {}, resists solvents, oils and aggressive environments.",
          "de": "Festigkeit {} – beständig gegen Lösungsmittel, Öle und aggressive Umgebungen.",
          "it": "Resistenza {}: resiste a solventi, oli e ambienti aggressivi."}),
        (r"^Pevnost (.+) s nižší ekologickou stopou než běžná PET fólie\.$",
         {"en": "Strength {} with a lower environmental footprint than standard PET film.",
          "de": "Festigkeit {} mit geringerem ökologischen Fußabdruck als übliche PET-Folie.",
          "it": "Resistenza {} con minore impatto ambientale rispetto al film PET standard."}),
        (r"^Pevnost v tahu (.+) – maximální odolnost ve směru nátahu\.$",
         {"en": "Tensile strength {}, maximum resistance in the direction of pull.",
          "de": "Zugfestigkeit {} – maximale Beständigkeit in Zugrichtung.",
          "it": "Resistenza alla trazione {}: massima resistenza nella direzione di trazione."}),
        (r"^Pevnost v tahu (.+) – odolnost ve všech směrech zatížení\.$",
         {"en": "Tensile strength {}, resistance in all directions of load.",
          "de": "Zugfestigkeit {} – Beständigkeit in allen Belastungsrichtungen.",
          "it": "Resistenza alla trazione {}: resistenza in tutte le direzioni di carico."}),
        (r"^Pevnost v tahu (.+) pro každodenní provoz skladu i expedice\.$",
         {"en": "Tensile strength {} for everyday warehouse and dispatch operations.",
          "de": "Zugfestigkeit {} für den täglichen Lager- und Versandbetrieb.",
          "it": "Resistenza alla trazione {} per l'uso quotidiano in magazzino e spedizione."}),
        (r"^Pevnost v tahu (.+) pro náročnější udržitelné balení ve skladu i expedici\.$",
         {"en": "Tensile strength {} for more demanding sustainable packing in warehouse and dispatch.",
          "de": "Zugfestigkeit {} für anspruchsvollere nachhaltige Verpackung im Lager und Versand.",
          "it": "Resistenza alla trazione {} per imballaggi sostenibili più impegnativi in magazzino e spedizione."}),
        (r"^Přilnavost (.+), nehlučné akrylové lepidlo, snadné tržení a UV odolnost \((.+)\)\.$",
         {"en": "Adhesion {}, low-noise acrylic adhesive, easy tear and UV resistance ({}).",
          "de": "Klebkraft {}, leiser Acrylklebstoff, leichtes Abreißen und UV-Beständigkeit ({}).",
          "it": "Adesione {}, adesivo acrilico silenzioso, strappo facile e resistenza UV ({})."}),
        (r"^Přilnavost (.+), low-noise acrylic, easy tear a UV odolnost \((.+)\)\.$",
         {"en": "Adhesion {}, low-noise acrylic adhesive, easy tear and UV resistance ({}).",
          "de": "Klebkraft {}, leiser Acrylklebstoff, leichtes Abreißen und UV-Beständigkeit ({}).",
          "it": "Adesione {}, adesivo acrilico silenzioso, strappo facile e resistenza UV ({})."}),
        (r"^Přilnavost (.+) s nízkou hlučností – spolehlivý výkon ve skladu \((.+)\)\.$",
         {"en": "Adhesion {} with low noise, reliable performance in warehouse conditions ({}).",
          "de": "Klebkraft {} mit geringer Geräuschentwicklung – zuverlässige Leistung im Lager ({}).",
          "it": "Adesione {} con basso rumore: prestazioni affidabili in magazzino ({})."}),
        (r"^Přilnavost (.+) na všech typech kartonů včetně recyklovaných \((.+)\)\.$",
         {"en": "Adhesion {} on all carton types including recycled ({}).",
          "de": "Klebkraft {} auf allen Kartontypen einschließlich Recyclingkarton ({}).",
          "it": "Adesione {} su tutti i tipi di cartone, incluso il riciclato ({})."}),
        (r"^Po dokončení práce nezanechává lepidlo ani stopy \((.+)\)\.$",
         {"en": "Leaves no adhesive or marks after the job is done ({}).",
          "de": "Hinterlässt nach Abschluss der Arbeit weder Klebstoff noch Spuren ({}).",
          "it": "Non lascia adesivo né segni al termine del lavoro ({})."}),
        (r"^Polyesterový nosič \((.+)\) si drží vlastnosti v náročných provozech\.$",
         {"en": "Polyester carrier ({}) retains its properties in demanding operations.",
          "de": "Polyesterträger ({}) behält seine Eigenschaften in anspruchsvollen Betrieben.",
          "it": "Supporto in poliestere ({}) mantiene le proprie caratteristiche in condizioni impegnative."}),
        (r"^Přilnavost (.+) po celou dobu potřebné aplikace \((.+)\)\.$",
         {"en": "Adhesion {} for the entire required application period ({}).",
          "de": "Klebkraft {} für die gesamte benötigte Anwendungsdauer ({}).",
          "it": "Adesione {} per tutta la durata necessaria dell'applicazione ({})."}),
        (r"^Přilnavost (.+) – okamžitě drží i při nižších teplotách \((.+)\)\.$",
         {"en": "Adhesion {}, bonds instantly even at lower temperatures ({}).",
          "de": "Klebkraft {} – haftet sofort auch bei niedrigen Temperaturen ({}).",
          "it": "Adesione {}: aderisce immediatamente anche a basse temperature ({})."}),
        (r"^Přilnavost (.+) i na recyklovaný karton a členité povrchy \((.+)\)\.$",
         {"en": "Adhesion {} on recycled cardboard and uneven surfaces ({}).",
          "de": "Klebkraft {} auch auf Recyclingkarton und unebenen Oberflächen ({}).",
          "it": "Adesione {} anche su cartone riciclato e superfici irregolari ({})."}),
        (r"^Přilnavost (.+) – spolehlivá fixace palet a nadrozměrných zásilek\.$",
         {"en": "Adhesion {}, reliable securing of pallets and oversized shipments.",
          "de": "Klebkraft {} – zuverlässige Sicherung von Paletten und übergroßen Sendungen.",
          "it": "Adesione {}: fissaggio affidabile di pallet e spedizioni fuori sagoma."}),
        (r"^Přilnavost (.+) – drží na kovu, dřevě, betonu i plastu \((.+)\)\.$",
         {"en": "Adhesion {}, holds on metal, wood, concrete and plastic ({}).",
          "de": "Klebkraft {} – haftet auf Metall, Holz, Beton und Kunststoff ({}).",
          "it": "Adesione {}: aderisce a metallo, legno, cemento e plastica ({})."}),
        (r"^Recyklovaná PET fólie \((.+)\) – po sejmutí nezanechává lepidlo ani poškození povrchu\.$",
         {"en": "Recycled PET film ({}), leaves no adhesive or surface damage after removal.",
          "de": "Recycelte PET-Folie ({}) – hinterlässt nach dem Abziehen weder Klebstoff noch Oberflächenschäden.",
          "it": "Film PET riciclato ({}): non lascia adesivo né danni alla superficie dopo la rimozione."}),
        (r"^Textilní výztuž \((.+)\) – odolnost proti protržení při náročném použití\.$",
         {"en": "Textile reinforcement ({}), tear resistance for demanding use.",
          "de": "Gewebeverstärkung ({}) – Reißfestigkeit bei anspruchsvollem Einsatz.",
          "it": "Rinforzo tessile ({}): resistenza allo strappo in condizioni di uso impegnative."}),
        (r"^Vizuální značení balíků a skladová orientace v rozsahu (.+)\.$",
         {"en": "Visual parcel labelling and warehouse orientation in the range {}.",
          "de": "Visuelle Paketkennzeichnung und Lagerorientierung im Bereich {}.",
          "it": "Marcatura visiva dei colli e orientamento in magazzino nell'intervallo {}."}),
        (r"^Čistá fixace bez uvolňujících se vláken – teplotní rozsah (.+)\.$",
         {"en": "Clean fixing without loose fibres, temperature range {}.",
          "de": "Saubere Fixierung ohne sich lösende Fasern – Temperaturbereich {}.",
          "it": "Fissaggio pulito senza rilascio di fibre: intervallo di temperatura {}."}),
    )
    for pattern, tpl in patterns:
        m = re.match(pattern, cs)
        if m:
            return tpl[locale].format(*m.groups())
    raise KeyError(f"Missing benefit text translation: {cs!r}")


def _tailor_bullets(locale: str, category_slug: str) -> list[str]:
    page = SORTIMENT_PAGE[locale]
    if category_slug in SAMPLE_CATEGORIES:
        return [page["tailor_bullet_width"], page["tailor_bullet_print"], page["tailor_bullet_sample"]]
    return [page["tailor_bullet_width"], page["tailor_bullet_params"], page["tailor_bullet_consult"]]


def load_gp_namespace() -> dict:
    """Execute gen_products.py only through the product JSON construction."""
    source = GEN_PRODUCTS.read_text(encoding="utf-8")
    marker = "# Build product JSON"
    if marker not in source:
        raise RuntimeError(f"Missing marker in {GEN_PRODUCTS}")
    namespace = {"__name__": "scripts.gen_products_i18n_source", "__file__": str(GEN_PRODUCTS)}
    exec(compile(source.split(marker, 1)[0], str(GEN_PRODUCTS), "exec"), namespace)
    return namespace


def _params_from_product(p: dict) -> dict[str, str]:
    params = p["params"]
    if p.get("paper_spec"):
        keys = PAPER_SPEC_PARAM_FIELD_KEYS
    elif p.get("tech_spec"):
        keys = TECH_SPEC_PARAM_FIELD_KEYS
    else:
        keys = PARAM_FIELD_KEYS
    return {key: params[cs_key] for key, cs_key in keys if cs_key in params}


def _tech_variants_from_product(ns: dict, p: dict) -> dict[str, dict[str, str]]:
    variants = ns["product_tech_variant_tables"](p)
    if not variants:
        return {}
    out: dict[str, dict[str, str]] = {}
    for variant, params in variants.items():
        out[variant] = {
            key: params[cs_key]
            for key, cs_key in TECH_SPEC_PARAM_FIELD_KEYS
            if cs_key in params
        }
    return out


def _spec_pills(params_values: dict[str, str]) -> list[str]:
    return [params_values["carrier"], params_values["adhesive"], params_values["temperature"]]


def _translate_param_value(locale: str, value: str) -> str:
    if locale == "cs":
        return value
    if value in PARAM_VALUE_MAP:
        return PARAM_VALUE_MAP[value][locale]
    translated = value
    if translated.startswith("do "):
        prefix = {"en": "up to ", "de": "bis ", "it": "fino a "}[locale]
        translated = prefix + translated[3:]
    translated = translated.replace(" až ", {"en": " to ", "de": " bis ", "it": " a "}[locale])
    return translated


def _build_cs_product(cat: dict, p: dict, ns: dict) -> tuple[str, dict]:
    slugify = ns["slugify"]
    product_benefits = ns["product_benefits"]
    product_uses = ns["product_uses"]
    product_ctas = ns["product_ctas"]
    slug = p.get("slug") or slugify(p["name"])
    benefits = product_benefits(cat["cat"], p)
    uses = product_uses(cat, p)
    ctas = product_ctas(cat, p)
    page = SORTIMENT_PAGE["cs"]
    params_values = _params_from_product(p)
    tech_variants = _tech_variants_from_product(ns, p)
    if p.get("paper_spec"):
        labels = PAPER_SPEC_PARAM_LABELS["cs"]
    elif p.get("tech_spec"):
        labels = TECH_SPEC_PARAM_LABELS["cs"]
    else:
        labels = PARAM_LABELS["cs"]
    return slug, {
        "name": p["name"],
        "tagline": p["tagline"],
        "category_slug": cat["cat"],
        "category_title": cat["title"],
        "benefits": [{"title": title, "text": text} for title, text in benefits],
        "uses": uses,
        "params_values": params_values,
        "spec_pills": list(ns["product_spec_pills"](p)),
        "tech_variants": tech_variants,
        "tech_variant_labels": ns["product_tech_variant_labels"](p),
        "min_qty_note": ns["product_min_qty_note"](p),
        "params_labels": labels,
        "tech_spec": bool(p.get("tech_spec")),
        "paper_spec": bool(p.get("paper_spec")),
        "ctas": {
            "hero": ctas["hero"],
            "tailor_link": ctas["tailor_link"],
            "tailor_bullets": _tailor_bullets("cs", cat["cat"]),
            "bottom": ctas["bottom"],
            "back_category": page["back_to_category_short"].format(category=cat["title"]),
        },
    }


def build_products_cs(ns: dict) -> dict:
    """Return Czech product content keyed by slug, built from gen_products helpers."""
    products: dict = {}
    for cat in ns["CATS"]:
        for p in ns["PRODUCTS"][cat["cat"]]:
            slug, entry = _build_cs_product(cat, p, ns)
            products[slug] = entry
    return products


def build_products_locale(ns: dict, locale: str) -> dict:
    """Build a fully localised product dictionary for EN, DE or IT."""
    if locale == "cs":
        return build_products_cs(ns)
    if locale not in ("en", "de", "it"):
        raise ValueError(f"Unsupported locale: {locale}")
    products = copy.deepcopy(build_products_cs(ns))
    page = SORTIMENT_PAGE[locale]
    for slug, product in products.items():
        product["name"] = _product_name(locale, product["name"])
        product["tagline"] = TAGLINES[slug][locale]
        product["category_title"] = CATEGORY_TITLES[locale][product["category_slug"]]
        product["benefits"] = [
            {"title": _benefit_title(locale, b["title"]), "text": _benefit_text(locale, b["text"])}
            for b in product["benefits"]
        ]
        product["uses"] = [USE_MAP[u][locale] for u in product["uses"]]
        ctas = product["ctas"]
        product["ctas"] = {
            "hero": CTA_MAP[ctas["hero"]][locale],
            "tailor_link": CTA_MAP[ctas["tailor_link"]][locale],
            "tailor_bullets": _tailor_bullets(locale, product["category_slug"]),
            "bottom": CTA_MAP[ctas["bottom"]][locale],
            "back_category": page["back_to_category_short"].format(category=product["category_title"]),
        }
        product["params_labels"] = (
            PAPER_SPEC_PARAM_LABELS[locale]
            if product.get("paper_spec")
            else TECH_SPEC_PARAM_LABELS[locale]
            if product.get("tech_spec")
            else PARAM_LABELS[locale]
        )
        for key, value in product["params_values"].items():
            product["params_values"][key] = _translate_param_value(locale, value)
        for variant, params in product.get("tech_variants", {}).items():
            for key, value in params.items():
                params[key] = _translate_param_value(locale, value)
        product["spec_pills"] = [_translate_param_value(locale, pill) for pill in product["spec_pills"]]
        if product.get("min_qty_note"):
            product["min_qty_note"] = MIN_QTY_NOTE_MAP[product["min_qty_note"]][locale]
    return products


def _translate_cta(text: str, locale: str) -> str:
    if locale == "cs":
        return text
    mapped = CTA_MAP.get(text, {})
    return mapped.get(locale, text)


def build_category_ctas(ns: dict, locale: str) -> dict:
    result: dict = {}
    for cat in ns["CATS"]:
        slug = cat["cat"]
        hero, bottom = ns["category_ctas"](cat)
        result[slug] = {
            "hero": _translate_cta(hero, locale),
            "bottom": _translate_cta(bottom, locale),
        }
    return result


def merge_into_sortiment(sortiment_dict: dict, locale: str, ns: dict) -> dict:
    """Return a copy of sortiment i18n data augmented with product data."""
    out = copy.deepcopy(sortiment_dict)
    out.setdefault("products", {}).update(build_products_locale(ns, locale))
    out.setdefault("page", {}).update(SORTIMENT_PAGE[locale])
    out["category_ctas"] = build_category_ctas(ns, locale)
    return out


def merge_into_gallery(gallery_dict: dict, locale: str) -> dict:
    """Return a copy of gallery i18n data augmented with gallery item text."""
    out = copy.deepcopy(gallery_dict)
    out.setdefault("items", {}).update(copy.deepcopy(GALLERY_ITEMS[locale]))
    return out
