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
        "description": "Una soluzione ecologica per imballaggi sicuri con elevata adesione. Ideale per scatole in cartone completamente riciclabili e un'immagine aziendale pulita.",
        "intro": "I nastri adesivi in carta combinano un incollaggio affidabile con la massima attenzione all'ambiente. Grazie al supporto in carta, sono completamente riciclabili insieme al cartone e rappresentano una soluzione elegante e ordinata per le aziende attente alla sostenibilità e all'immagine delle proprie spedizioni.",
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
        "tailor_bullet_sample": "Vzorek s vaším logem před objednávkou",
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
        "tailor_bullet_sample": "Sample with your logo before ordering",
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
        "tailor_bullet_sample": "Muster mit Ihrem Logo vor der Bestellung",
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
        "tailor_bullet_sample": "Campione con il vostro logo prima dell'ordine",
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
]

TECH_SPEC_PARAM_LABELS = {
    "cs": {
        "carrier": "Nosič",
        "thickness": "Tloušťka fólie",
        "adhesive": "Typ lepidla",
        "adhesion": "Tloušťka lepidla",
        "strength": "Skladovací a aplikační teplota",
        "temperature": "Provozní teplota po nalepení",
    },
    "en": {
        "carrier": "Carrier",
        "thickness": "Film thickness",
        "adhesive": "Adhesive type",
        "adhesion": "Adhesive thickness",
        "strength": "Storage and application temperature",
        "temperature": "Operating temperature after application",
    },
    "de": {
        "carrier": "Träger",
        "thickness": "Foliendicke",
        "adhesive": "Klebstofftyp",
        "adhesion": "Klebstoffdicke",
        "strength": "Lager- und Verarbeitungstemperatur",
        "temperature": "Betriebstemperatur nach dem Aufkleben",
    },
    "it": {
        "carrier": "Supporto",
        "thickness": "Spessore del film",
        "adhesive": "Tipo di adesivo",
        "adhesion": "Spessore dell'adesivo",
        "strength": "Temperatura di stoccaggio e applicazione",
        "temperature": "Temperatura di esercizio dopo l'applicazione",
    },
}

PARAM_VALUE_MAP: dict[str, dict[str, str]] = {
    "Akrylové": {"en": "Acrylic", "de": "Acryl", "it": "Acrilico"},
    "Akrylové (bez rozpouštědel)": {"en": "Acrylic (solvent-free)", "de": "Acryl (lösungsmittelfrei)", "it": "Acrilico (senza solventi)"},
    "Akrylové (disperzní)": {"en": "Acrylic (dispersion)", "de": "Acryl (Dispersion)", "it": "Acrilico (dispersione)"},
    "Akrylové (vodní disperze)": {"en": "Acrylic (water-based dispersion)", "de": "Acryl (wässrige Dispersion)", "it": "Acrilico (dispersione acquosa)"},
    "BOPP fólie": {"en": "BOPP film", "de": "BOPP-Folie", "it": "Film BOPP"},
    "BOPP fólie (barevná)": {"en": "BOPP film (coloured)", "de": "BOPP-Folie (farbig)", "it": "Film BOPP (colorato)"},
    "Hot melt": {"en": "Hot melt", "de": "Hot Melt", "it": "Hot melt"},
    "HOT MELT": {"en": "Hot melt", "de": "Hot Melt", "it": "Hot melt"},
    "Hot melt (syntetický kaučuk)": {"en": "Hot melt (synthetic rubber)", "de": "Hot Melt (Synthesekautschuk)", "it": "Hot melt (gomma sintetica)"},
    "HOT MELT (syntetický kaučuk)": {"en": "Hot melt (synthetic rubber)", "de": "Hot Melt (Synthesekautschuk)", "it": "Hot melt (gomma sintetica)"},
    "Kaučukové": {"en": "Rubber-based", "de": "Kautschuk", "it": "Gomma"},
    "Kaučukové (odolné teplu)": {"en": "Rubber-based (heat-resistant)", "de": "Kautschuk (hitzebeständig)", "it": "Gomma (resistente al calore)"},
    "Kaučukové (solvent)": {"en": "Rubber-based (solvent)", "de": "Kautschuk (Lösungsmittel)", "it": "Gomma (solvente)"},
    "Kaučukové (syntetické)": {"en": "Rubber-based (synthetic)", "de": "Kautschuk (synthetisch)", "it": "Gomma (sintetica)"},
    "Krepový papír": {"en": "Crepe paper", "de": "Krepppapier", "it": "Carta crespa"},
    "MOPP + křížová skelná vlákna": {"en": "MOPP + cross-laid glass fibres", "de": "MOPP + kreuzweise Glasfasern", "it": "MOPP + fibre di vetro incrociate"},
    "MOPP + podélná skelná vlákna": {"en": "MOPP + longitudinal glass fibres", "de": "MOPP + längs verlaufende Glasfasern", "it": "MOPP + fibre di vetro longitudinali"},
    "MOPP fólie": {"en": "MOPP film", "de": "MOPP-Folie", "it": "Film MOPP"},
    "Odstranitelné akrylové": {"en": "Removable acrylic", "de": "Abziehbares Acryl", "it": "Acrilico rimovibile"},
    "Papír (FSC)": {"en": "Paper (FSC)", "de": "Papier (FSC)", "it": "Carta (FSC)"},
    "Papírový nosič": {"en": "Paper carrier", "de": "Papierträger", "it": "Supporto in carta"},
    "Papírový nosič (kraft)": {"en": "Paper carrier (kraft)", "de": "Papierträger (Kraft)", "it": "Supporto in carta kraft"},
    "Polyesterová (PET) fólie": {"en": "Polyester (PET) film", "de": "Polyester- (PET-) Folie", "it": "Film in poliestere (PET)"},
    "Recyklovaná PET fólie": {"en": "Recycled PET film", "de": "Recycelte PET-Folie", "it": "Film PET riciclato"},
    "Recyklovaná PP fólie": {"en": "Recycled PP film", "de": "Recycelte PP-Folie", "it": "Film PP riciclato"},
    "100% regenerovaná BOPP fólie": {"en": "100% regenerated BOPP film", "de": "100 % regenerierte BOPP-Folie", "it": "Film BOPP rigenerato al 100%"},
    "BOPP fólie (matná, 35 µm)": {"en": "BOPP film (matte, 35 µm)", "de": "BOPP-Folie (matt, 35 µm)", "it": "Film BOPP (opaco, 35 µm)"},
    "Akrylové (tiché, bez rozpouštědel)": {"en": "Acrylic (quiet, solvent-free)", "de": "Acryl (leise, lösungsmittelfrei)", "it": "Acrilico (silenzioso, senza solventi)"},
    "Akrylové (zvýšená vrstva +33 %)": {"en": "Acrylic (increased adhesive layer +33%)", "de": "Acryl (erhöhte Klebstoffschicht +33 %)", "it": "Acrilico (strato adesivo aumentato +33%)"},
    "Hot melt (super tack, +20 %)": {"en": "Hot melt (super tack, +20%)", "de": "Hot Melt (Super-Tack, +20 %)", "it": "Hot melt (super tack, +20%)"},
    "HOT MELT (super tack, +20 %)": {"en": "Hot melt (super tack, +20%)", "de": "Hot Melt (Super-Tack, +20 %)", "it": "Hot melt (super tack, +20%)"},
    "Recyklovaný papír": {"en": "Recycled paper", "de": "Recyclingpapier", "it": "Carta riciclata"},
    "Silikonové": {"en": "Silicone", "de": "Silikon", "it": "Silicone"},
    "BOPP": {"en": "BOPP", "de": "BOPP", "it": "BOPP"},
    "Akryl (Low noise / Noisy)": {"en": "Akryl (Low noise / Noisy)", "de": "Akryl (Low noise / Noisy)", "it": "Akryl (Low noise / Noisy)"},
    "Akryl (Low noise / Noisy) / HOT MELT": {
        "en": "Akryl (Low noise / Noisy) / HOT MELT",
        "de": "Akryl (Low noise / Noisy) / HOT MELT",
        "it": "Akryl (Low noise / Noisy) / HOT MELT",
    },
    "25 / 28 / 32 µm": {"en": "25 / 28 / 32 µm", "de": "25 / 28 / 32 µm", "it": "25 / 28 / 32 µm"},
    "21 µm": {"en": "21 µm", "de": "21 µm", "it": "21 µm"},
    "18 µm": {"en": "18 µm", "de": "18 µm", "it": "18 µm"},
    "21 µm (Akryl) / 18 µm (HOT MELT)": {
        "en": "21 µm (Akryl) / 18 µm (HOT MELT)",
        "de": "21 µm (Akryl) / 18 µm (HOT MELT)",
        "it": "21 µm (Akryl) / 18 µm (HOT MELT)",
    },
    "50 % regenerát": {
        "en": "50% regenerated",
        "de": "50 % regeneriert",
        "it": "50% rigenerato",
    },
    "80 % regenerát": {
        "en": "80% regenerated",
        "de": "80 % regeneriert",
        "it": "80% rigenerato",
    },
    "100 % regenerát": {
        "en": "100% regenerated",
        "de": "100 % regeneriert",
        "it": "100% rigenerato",
    },
    "Akryl / HOT MELT": {
        "en": "Akryl / HOT MELT",
        "de": "Akryl / HOT MELT",
        "it": "Akryl / HOT MELT",
    },
    "14–28 °C": {"en": "14–28 °C", "de": "14–28 °C", "it": "14–28 °C"},
    "Textilní výztuž + PE laminát": {"en": "Textile reinforcement + PE laminate", "de": "Textilverstärkung + PE-Laminat", "it": "Rinforzo tessile + laminato PE"},
}

PARAM_LABELS = {
    "cs": {"carrier": "Nosič / materiál", "thickness": "Tloušťka", "adhesive": "Typ lepidla", "adhesion": "Přilnavost (ocel)", "temperature": "Teplotní odolnost", "strength": "Pevnost v tahu"},
    "en": {"carrier": "Carrier / material", "thickness": "Thickness", "adhesive": "Adhesive type", "adhesion": "Adhesion (steel)", "temperature": "Temperature resistance", "strength": "Tensile strength"},
    "de": {"carrier": "Träger / Material", "thickness": "Dicke", "adhesive": "Klebstofftyp", "adhesion": "Haftung (Stahl)", "temperature": "Temperaturbeständigkeit", "strength": "Zugfestigkeit"},
    "it": {"carrier": "Supporto / materiale", "thickness": "Spessore", "adhesive": "Tipo di adesivo", "adhesion": "Adesione (acciaio)", "temperature": "Resistenza alla temperatura", "strength": "Resistenza alla trazione"},
}

GALLERY_ITEMS = {
    "cs": {
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

TAGLINES: dict[str, dict[str, str]] = {'udrzitelna-paska-airtape': {'en': 'Lightweight sustainable tape for everyday eco-friendly packaging.', 'de': 'Leichtes nachhaltiges Klebeband für den täglichen, umweltfreundlichen Einsatz.', 'it': 'Nastro sostenibile leggero per imballaggi ecologici quotidiani.'}, 'udrzitelna-paska-eco-50': {'en': 'Efficient packaging with 50% regenerated material. The optimal balance of ecology and best price.', 'de': 'Effizientes Verpacken mit 50 % regeneriertem Material. Optimale Balance aus Ökologie und bestem Preis.', 'it': 'Imballaggio efficiente con il 50% di materiale rigenerato. Il giusto equilibrio tra ecologia e miglior prezzo.'}, 'udrzitelna-paska-eco-80': {'en': 'BOPP film with 80% regenerated material. Combines a high ecological standard with full strength.', 'de': 'BOPP-Folie mit 80 % regeneriertem Material. Verbindet hohen ökologischen Standard mit voller Festigkeit.', 'it': 'Film BOPP con l’80% di materiale rigenerato. Unisce un elevato standard ecologico e piena resistenza.'}, 'udrzitelna-paska-eco-100': {'en': '100% regenerated BOPP film from post-industrial waste. Maximum ecological standard without compromising performance.', 'de': '100 % regenerierte BOPP-Folie aus postindustriellen Abfällen. Maximaler ökologischer Standard ohne Kompromisse bei der Leistung.', 'it': 'Film BOPP rigenerato al 100% da scarti post-industriali. Massimo standard ecologico senza compromessi sulle prestazioni.'}, 'udrzitelna-paska-poly-plus': {'en': 'Eco-friendly PVC alternative, matte non-reflective BOPP tape with quiet acrylic adhesive.', 'de': 'Ökologische PVC-Alternative – mattes, nicht reflektierendes BOPP-Klebeband mit leisem Acrylklebstoff.', 'it': 'Alternativa ecologica al PVC: nastro BOPP opaco non riflettente con adesivo acrilico silenzioso.'}, 'udrzitelna-paska-loopp': {'en': 'Tape made from recycled polypropylene for the circular economy.', 'de': 'Klebeband aus recyceltem Polypropylen für die Kreislaufwirtschaft.', 'it': "Nastro in polipropilene riciclato per l'economia circolare."}, 'udrzitelna-paska-nopp': {'en': 'Plastic-free sustainable tape for fully recyclable packaging.', 'de': 'Plastikfreies nachhaltiges Klebeband für vollständig recycelbare Verpackungen.', 'it': 'Nastro sostenibile senza plastica per imballaggi completamente riciclabili.'}, 'udrzitelna-paska-nopp-plus': {'en': 'Enhanced plastic-free tape with higher strength and adhesion.', 'de': 'Verbessertes plastikfreies Klebeband mit höherer Festigkeit und Klebkraft.', 'it': 'Nastro senza plastica migliorato con maggiore resistenza e adesione.'}, 'bopp-paska-acrylic': {'en': 'Reliable BOPP tape with long service life.', 'de': 'Zuverlässiges BOPP-Klebeband mit langer Lebensdauer.', 'it': 'Nastro BOPP affidabile con lunga durata.'}, 'bopp-paska-evergreen': {'en': 'Coloured BOPP tape for labelling and visual shipment identification.', 'de': 'Farbiges BOPP-Klebeband zur Kennzeichnung und visuellen Unterscheidung von Sendungen.', 'it': 'Nastro BOPP colorato per etichettatura e identificazione visiva delle spedizioni.'}, 'bopp-paska-hot-melt': {'en': 'BOPP tape with hot melt adhesive for fast, strong bonding.', 'de': 'BOPP-Klebeband mit Hot-Melt-Klebstoff für schnelle, feste Haftung.', 'it': "Nastro BOPP con adesivo hot melt per un'adesione rapida e resistente."}, 'bopp-paska-extra-glue-plus': {'en': 'Acrylic BOPP tape with an increased adhesive layer (+33%) for demanding surfaces and recycled cardboard.', 'de': 'Acryl-BOPP-Klebeband mit erhöhter Klebstoffschicht (+33 %) für anspruchsvolle Oberflächen und Recyclingkarton.', 'it': 'Nastro BOPP acrilico con strato adesivo aumentato (+33%) per superfici difficili e cartone riciclato.'}, 'bopp-paska-tack-plus': {'en': 'Hot melt BOPP tape with higher adhesion (+20%) and super tack for packing machines and recycled cardboard.', 'de': 'Hot-Melt-BOPP-Klebeband mit höherer Klebkraft (+20 %) und Super-Tack für Verpackungsmaschinen und Recyclingkarton.', 'it': 'Nastro BOPP hot melt con adesione superiore (+20%) e super tack per macchine da imballaggio e cartone riciclato.'}, 'bopet-paska-ait': {'en': 'Polyester tape with silicone adhesive for extreme temperatures.', 'de': 'Polyesterband mit Silikonklebstoff für extreme Temperaturen.', 'it': 'Nastro in poliestere con adesivo siliconico per temperature estreme.'}, 'bopet-paska-ate23': {'en': 'Thin polyester tape with high temperature resistance.', 'de': 'Dünnes Polyesterband mit hoher Temperaturbeständigkeit.', 'it': 'Nastro sottile in poliestere con elevata resistenza alla temperatura.'}, 'bopet-paska-eco-hit19': {'en': 'Polyester tape with recycled content and high durability.', 'de': 'Polyesterband mit recyceltem Anteil und hoher Beständigkeit.', 'it': 'Nastro in poliestere con contenuto riciclato e alta resistenza.'}, 'bopet-paska-hit17': {'en': 'Ultra-thin PET tape for electronics and precision applications.', 'de': 'Ultradünnes PET-Band für Elektrotechnik und präzise Anwendungen.', 'it': 'Nastro PET ultrasottile per elettrotecnica e applicazioni di precisione.'}, 'papirova-paska-c660': {'en': 'Eco-friendly paper tape with acrylic adhesive and quiet unwinding.', 'de': 'Umweltfreundliches Papierklebeband mit Acrylklebstoff und leisem Abrollen.', 'it': 'Nastro di carta ecologico con adesivo acrilico e svolgimento silenzioso.'}, 'papirova-paska-c680': {'en': 'Universal paper tape with high adhesion on recycled cardboard.', 'de': 'Universelles Papierklebeband mit hoher Haftung auf Recyclingkarton.', 'it': 'Nastro di carta universale con elevata adesione sul cartone riciclato.'}, 'papirova-paska-c680-rt': {'en': 'Durable paper tape with improved adhesion for heavier shipments.', 'de': 'Robustes Papierklebeband mit verbesserter Haftung für schwerere Sendungen.', 'it': 'Nastro di carta resistente con adesione migliorata per spedizioni più pesanti.'}, 'papirova-paska-c680r': {'en': 'Paper tape made from recycled paper for sustainable packaging.', 'de': 'Papierklebeband aus Recyclingpapier für nachhaltige Verpackung.', 'it': 'Nastro di carta realizzato con carta riciclata per imballaggi sostenibili.'}, 'papirova-paska-c690': {'en': 'Premium kraft paper tape with hot melt adhesive and matte finish.', 'de': 'Premium-Kraftpapierklebeband mit Hot-Melt-Klebstoff und matter Oberfläche.', 'it': 'Nastro kraft premium con adesivo hot melt e finitura opaca.'}, 'papirova-paska-kh80': {'en': 'Strong paper tape with hot melt adhesive for reliable carton sealing.', 'de': 'Starkes Papierklebeband mit Hot-Melt-Klebstoff für zuverlässigen Kartonverschluss.', 'it': 'Nastro di carta resistente con adesivo hot melt per una chiusura affidabile dei cartoni.'}, 'papirova-paska-ks165': {'en': 'Extra-strong paper tape with rubber adhesive for demanding packaging.', 'de': 'Extra starkes Papierklebeband mit Kautschukklebstoff für anspruchsvolles Verpacken.', 'it': 'Nastro di carta extra resistente con adesivo in gomma per imballaggi impegnativi.'}, 'odstranitelna-paska-eco-rit19': {'en': 'Gentle removable tape with recycled content.', 'de': 'Schonendes abziehbares Klebeband mit recyceltem Anteil.', 'it': 'Nastro rimovibile delicato con contenuto riciclato.'}, 'odstranitelna-paska-r28-32': {'en': 'Removable tape that leaves no trace after peeling.', 'de': 'Abziehbares Klebeband, das nach dem Entfernen keine Spuren hinterlässt.', 'it': 'Nastro rimovibile che non lascia tracce dopo la rimozione.'}, 'vyztuzena-paska-rmpp32': {'en': 'Reinforced tape with glass fibres for securing heavy loads.', 'de': 'Verstärktes Klebeband mit Glasfasern zur Sicherung schwerer Lasten.', 'it': 'Nastro rinforzato con fibre di vetro per fissare carichi pesanti.'}, 'vyztuzena-paska-rtpp32': {'en': 'Cross-reinforced tape for maximum strength in all directions.', 'de': 'Kreuzverstärktes Klebeband für maximale Festigkeit in alle Richtungen.', 'it': 'Nastro rinforzato incrociato per la massima resistenza in ogni direzione.'}, 'mopp-paska-s45-50': {'en': 'Monoaxial MOPP tape with extreme strength and zero stretch.', 'de': 'Monoaxiales MOPP-Band mit extremer Festigkeit und null Dehnung.', 'it': 'Nastro MOPP monoassiale con resistenza estrema e allungamento nullo.'}, 'textilni-paska-bc': {'en': 'Strong cloth (duct) tape for repairs and universal use.', 'de': 'Starkes Gewebeband (Duct Tape) für Reparaturen und universellen Einsatz.', 'it': 'Nastro telato resistente (duct tape) per riparazioni e uso universale.'}, 'textilni-paska-bc2': {'en': 'Extra-strong cloth tape with high tensile strength.', 'de': 'Extra starkes Gewebeband mit hoher Zugfestigkeit.', 'it': 'Nastro telato extra resistente con elevata resistenza alla trazione.'}, 'textilni-paska-nu': {'en': 'Universal cloth tape for quick bundling and fixing.', 'de': 'Universelles Gewebeband für schnelles Bündeln und Fixieren.', 'it': 'Nastro telato universale per fascettatura e fissaggio rapidi.'}, 'malirska-paska-c580': {'en': 'Crepe masking tape for sharp edges in everyday painting.', 'de': 'Krepp-Malerklebeband für saubere Kanten beim regulären Streichen.', 'it': 'Nastro per mascheratura in carta crespata per bordi netti nella pittura quotidiana.'}, 'malirska-paska-cs60-80': {'en': 'Heat-resistant masking tape for painting and demanding masking.', 'de': 'Hitzebeständiges Malerklebeband für Lackierung und anspruchsvolles Abkleben.', 'it': 'Nastro per mascheratura resistente al calore per verniciatura e mascherature impegnative.'}}

USE_MAP: dict[str, dict[str, str]] = {'Aplikace s důrazem na udržitelnější materiál': {'en': 'Applications with a focus on more sustainable materials', 'de': 'Anwendungen mit Fokus auf nachhaltigere Materialien', 'it': 'Applicazioni con attenzione a materiali più sostenibili'}, 'Automatické balicí linky s ESG cíli': {'en': 'Automatic packing lines with ESG goals', 'de': 'Automatische Verpackungslinien mit ESG-Zielen', 'it': 'Linee di imballaggio automatiche con obiettivi ESG'}, 'Automatické balicí stroje': {'en': 'Automatic packing machines', 'de': 'Automatische Verpackungsmaschinen', 'it': 'Macchine automatiche per imballaggio'}, 'Budování zodpovědné značky': {'en': 'Building a responsible brand', 'de': 'Aufbau einer verantwortungsvollen Marke', 'it': 'Costruzione di un marchio responsabile'}, 'Cirkulární obalové procesy': {'en': 'Circular packaging processes', 'de': 'Zirkuläre Verpackungsprozesse', 'it': 'Processi di imballaggio circolari'}, 'Dočasné značení a etikety': {'en': 'Temporary marking and labels', 'de': 'Temporäre Kennzeichnung und Etiketten', 'it': 'Marcature ed etichette temporanee'}, 'E-shopy s důrazem na udržitelné balení': {'en': 'E-shops focused on sustainable packaging', 'de': 'E-Shops mit Fokus auf nachhaltige Verpackung', 'it': 'E-shop orientati al packaging sostenibile'}, 'Elektrotechnika a specializovaná výroba': {'en': 'Electronics and specialised manufacturing', 'de': 'Elektrotechnik und spezialisierte Fertigung', 'it': 'Elettrotecnica e produzione specializzata'}, 'Expedice a skladová logistika': {'en': 'Dispatch and warehouse logistics', 'de': 'Versand und Lagerlogistik', 'it': 'Spedizione e logistica di magazzino'}, 'Firemní branding přímo na zásilce': {'en': 'Corporate branding directly on shipments', 'de': 'Firmen-Branding direkt auf der Sendung', 'it': 'Branding aziendale direttamente sulle spedizioni'}, 'Firmy s ESG a udržitelnými cíli': {'en': 'Companies with ESG and sustainability goals', 'de': 'Unternehmen mit ESG- und Nachhaltigkeitszielen', 'it': 'Aziende con obiettivi ESG e di sostenibilità'}, 'Fixace dveří elektrospotřebičů': {'en': 'Securing appliance doors', 'de': 'Fixierung von Gerätetüren', 'it': 'Fissaggio delle porte degli elettrodomestici'}, 'Fixace těžkých a nadrozměrných balíků': {'en': 'Securing heavy and oversized parcels', 'de': 'Sicherung schwerer und übergroßer Pakete', 'it': 'Fissaggio di colli pesanti e fuori sagoma'}, 'Fixace v prostředí s vysokými teplotami': {'en': 'Fixing in high-temperature environments', 'de': 'Fixierung in Umgebungen mit hohen Temperaturen', 'it': 'Fissaggio in ambienti ad alta temperatura'}, 'Fixace, která se musí opět odstranit': {'en': 'Fixing that must be removed again', 'de': 'Fixierungen, die wieder entfernt werden müssen', 'it': 'Fissaggi che devono essere rimossi'}, 'Kutilské a řemeslné práce': {'en': 'DIY and craft work', 'de': 'Heimwerker- und Handwerksarbeiten', 'it': 'Lavori fai da te e artigianali'}, 'Lakovny a autolakovny': {'en': 'Paint shops and body shops', 'de': 'Lackierereien und Autolackierereien', 'it': 'Verniciature industriali e carrozzerie'}, 'Logistické a výrobní procesy': {'en': 'Logistics and production processes', 'de': 'Logistische und Produktionsprozesse', 'it': 'Processi logistici e produttivi'}, 'Malování a lakování interiérů': {'en': 'Interior painting and coating', 'de': 'Innenanstrich und Lackierung', 'it': 'Pittura e verniciatura di interni'}, 'Maskování při práškovém lakování': {'en': 'Masking during powder coating', 'de': 'Abkleben bei der Pulverbeschichtung', 'it': 'Mascheratura nella verniciatura a polvere'}, 'Náročné průmyslové provozy': {'en': 'Demanding industrial operations', 'de': 'Anspruchsvolle Industriebetriebe', 'it': 'Impianti industriali impegnativi'}, 'Ochrana citlivých povrchů': {'en': 'Protection of sensitive surfaces', 'de': 'Schutz empfindlicher Oberflächen', 'it': 'Protezione di superfici sensibili'}, 'Potisk až 10 barev (reverse printing)': {'en': 'Printing up to 10 colours (reverse printing)', 'de': 'Bedruckung bis zu 10 Farben (Reverse-Druck)', 'it': 'Stampa fino a 10 colori (reverse printing)'}, 'Potisk firemním logem a informacemi': {'en': 'Printing with company logos and information', 'de': 'Bedruckung mit Firmenlogo und Informationen', 'it': 'Stampa con logo e informazioni aziendali'}, 'Recyklovaný karton a náročné povrchy': {'en': 'Recycled cardboard and demanding surfaces', 'de': 'Recyclingkarton und anspruchsvolle Oberflächen', 'it': 'Cartone riciclato e superfici difficili'}, 'Provoz v chladírenských a mrazicích skladech': {'en': 'Use in chilled and frozen warehouses', 'de': 'Einsatz in Kühl- und Tiefkühllagern', 'it': 'Utilizzo in magazzini refrigerati e congelati'}, 'Práškové lakování a vysokoteplotní procesy': {'en': 'Powder coating and high-temperature processes', 'de': 'Pulverbeschichtung und hochtemperaturfähige Prozesse', 'it': 'Verniciatura a polvere e processi ad alta temperatura'}, 'Ruční balení a uzavírání e-commerce zásilek': {'en': 'Manual packing and sealing of e-commerce shipments', 'de': 'Manuelles Verpacken und Verschließen von E-Commerce-Sendungen', 'it': 'Imballaggio manuale e chiusura di spedizioni e-commerce'}, 'Ruční i poloautomatické balení': {'en': 'Manual and semi-automatic packing', 'de': 'Manuelles und halbautomatisches Verpacken', 'it': 'Imballaggio manuale e semiautomatico'}, 'Rychlé opravy a provizorní spoje': {'en': 'Quick repairs and temporary joints', 'de': 'Schnelle Reparaturen und provisorische Verbindungen', 'it': 'Riparazioni rapide e giunzioni provvisorie'}, 'Stahování a fixace palet': {'en': 'Strapping and securing pallets', 'de': 'Umreifung und Fixierung von Paletten', 'it': 'Reggiatura e fissaggio dei pallet'}, 'Standardní uzavírání kartonů': {'en': 'Standard carton sealing', 'de': 'Standard-Kartonverschluss', 'it': 'Chiusura standard dei cartoni'}, 'Strojové balení těžkých zásilek': {'en': 'Machine packing of heavy shipments', 'de': 'Maschinelles Verpacken schwerer Sendungen', 'it': 'Imballaggio automatico di spedizioni pesanti'}, 'Svazování a fixace předmětů': {'en': 'Bundling and securing items', 'de': 'Bündeln und Fixieren von Gegenständen', 'it': 'Fascettatura e fissaggio di oggetti'}, 'Svazování bez skelných vláken': {'en': 'Bundling without glass fibres', 'de': 'Bündeln ohne Glasfasern', 'it': 'Fascettatura senza fibre di vetro'}, 'Svazování trubek, profilů a tyčí': {'en': 'Bundling pipes, profiles and rods', 'de': 'Bündeln von Rohren, Profilen und Stäben', 'it': 'Fascettatura di tubi, profili e barre'}, 'Tiché ruční odvíjení ve skladech a expedici': {'en': 'Quiet manual unwinding in warehouses and dispatch', 'de': 'Leises manuelles Abrollen in Lagern und im Versand', 'it': 'Svolgimento manuale silenzioso in magazzino e spedizione'}, 'Uzavírání kartonových krabic a obalů': {'en': 'Sealing cardboard boxes and packaging', 'de': 'Verschließen von Kartonschachteln und Verpackungen', 'it': 'Chiusura di scatole e imballaggi in cartone'}, 'Uzavírání kartonů všech typů povrchů': {'en': 'Sealing cartons of all surface types', 'de': 'Verschließen von Kartons aller Oberflächentypen', 'it': 'Chiusura di cartoni su tutti i tipi di superficie'}, 'Zajištění komponentů během přepravy': {'en': 'Securing components during transport', 'de': 'Sicherung von Komponenten während des Transports', 'it': 'Messa in sicurezza dei componenti durante il trasporto'}, 'Zajištění zboží na paletách': {'en': 'Securing goods on pallets', 'de': 'Sicherung von Waren auf Paletten', 'it': 'Messa in sicurezza delle merci sui pallet'}, 'Zakrývání hran a přechodů': {'en': 'Masking edges and transitions', 'de': 'Abkleben von Kanten und Übergängen', 'it': 'Mascheratura di bordi e passaggi'}, 'Zelené balení pro e-shopy': {'en': 'Green packaging for e-shops', 'de': 'Grüne Verpackung für E-Shops', 'it': 'Imballaggi verdi per e-shop'}, 'Zpevnění balíků a obalů': {'en': 'Reinforcing parcels and packaging', 'de': 'Verstärkung von Paketen und Verpackungen', 'it': 'Rinforzo di colli e imballaggi'}, 'Údržba, montáže a řemeslo': {'en': 'Maintenance, assembly and craft work', 'de': 'Wartung, Montage und Handwerk', 'it': 'Manutenzione, montaggio e lavori artigianali'}, 'Ruční balení s tichým (low noise) odvíjením': {'en': 'Manual packing with quiet (low noise) unwinding', 'de': 'Manuelles Verpacken mit leisem (Low-Noise) Abrollen', 'it': 'Imballaggio manuale con svolgimento silenzioso (low noise)'}, 'Automatické balicí stroje – hlučná (noisy) verze': {'en': 'Automatic packing machines – noisy version', 'de': 'Automatische Verpackungsmaschinen – laute (Noisy) Version', 'it': 'Macchine automatiche per imballaggio – versione noisy'}, 'Recyklované kartony a prašné prostředí': {'en': 'Recycled cartons and dusty environments', 'de': 'Recyclingkartons und staubige Umgebungen', 'it': 'Cartoni riciclati e ambienti polverosi'}, 'Zabezpečení zásilek na stretch fólii': {'en': 'Securing shipments on stretch film', 'de': 'Sicherung von Sendungen auf Stretchfolie', 'it': 'Sicurezza delle spedizioni su film stretch'}}

CTA_MAP: dict[str, dict[str, str]] = {
    'Chci vzorek zdarma': {'en': 'I want a free sample', 'de': 'Ich möchte ein kostenloses Muster', 'it': 'Voglio un campione gratuito'},
    'Kalkulace s potiskem': {'en': 'Quote with printing', 'de': 'Kalkulation mit Bedruckung', 'it': 'Preventivo con stampa'},
    'Kalkulace balicí pásky': {'en': 'Packaging tape quote', 'de': 'Kalkulation Verpackungsband', 'it': 'Preventivo nastro da imballaggio'},
    'Kalkulace technické pásky': {'en': 'Technical tape quote', 'de': 'Kalkulation technisches Band', 'it': 'Preventivo nastro tecnico'},
    'Kalkulace papírové pásky': {'en': 'Paper tape quote', 'de': 'Kalkulation Papierband', 'it': 'Preventivo nastro di carta'},
    'Spočítat eko pásku': {'en': 'Calculate eco tape quote', 'de': 'Öko-Band kalkulieren', 'it': 'Calcola preventivo nastro ecologico'},
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
    'Vzorek s vaším logem před objednávkou': {'en': 'Sample with your logo before ordering', 'de': 'Muster mit Ihrem Logo vor der Bestellung', 'it': "Campione con il vostro logo prima dell'ordine"},
}

BENEFIT_TITLE_MAP: dict[str, dict[str, str]] = {'Akrylové lepidlo': {'en': 'Acrylic adhesive', 'de': 'Acrylklebstoff', 'it': 'Adesivo acrilico'}, 'Barevné odlišení zásilek': {'en': 'Colour-coded shipment identification', 'de': 'Farbliche Kennzeichnung von Sendungen', 'it': 'Identificazione visiva delle spedizioni'}, 'Bez skelných vláken': {'en': 'No glass fibres', 'de': 'Ohne Glasfasern', 'it': 'Senza fibre di vetro'}, 'Beze stop po odlepení': {'en': 'No residue after removal', 'de': 'Keine Rückstände nach dem Abziehen', 'it': 'Senza residui dopo la rimozione'}, 'Bezplastový papírový nosič': {'en': 'Plastic-free paper carrier', 'de': 'Plastikfreier Papierträger', 'it': 'Supporto in carta senza plastica'}, 'Chemická odolnost': {'en': 'Chemical resistance', 'de': 'Chemische Beständigkeit', 'it': 'Resistenza chimica'}, 'Dlouhá životnost': {'en': 'Long service life', 'de': 'Lange Lebensdauer', 'it': 'Lunga durata'}, 'Ekologická alternativa k PVC': {'en': 'Eco-friendly PVC alternative', 'de': 'Ökologische PVC-Alternative', 'it': 'Alternativa ecologica al PVC'}, 'Extrémní teploty': {'en': 'Extreme temperatures', 'de': 'Extreme Temperaturen', 'it': 'Temperature estreme'}, 'Fixace těžkých břemen': {'en': 'Securing heavy loads', 'de': 'Sicherung schwerer Lasten', 'it': 'Fissaggio di carichi pesanti'}, 'HOT MELT lepidlo': {'en': 'Hot melt adhesive', 'de': 'Hot-Melt-Klebstoff', 'it': 'Adesivo hot melt'}, 'Hot melt lepidlo': {'en': 'Hot melt adhesive', 'de': 'Hot-Melt-Klebstoff', 'it': 'Adesivo hot melt'}, 'Kaučukové lepidlo': {'en': 'Rubber adhesive', 'de': 'Kautschukklebstoff', 'it': 'Adesivo in gomma'}, 'Křížová skelná vlákna': {'en': 'Cross-laid glass fibres', 'de': 'Kreuzweise Glasfasern', 'it': 'Fibre di vetro incrociate'}, 'Ostré hrany bez protečení': {'en': 'Sharp edges without bleed-through', 'de': 'Saubere Kanten ohne Auslaufen', 'it': 'Bordi netti senza sbavature'}, 'Plná recyklovatelnost': {'en': 'Fully recyclable', 'de': 'Vollständig recycelbar', 'it': 'Completamente riciclabile'}, 'Podélná skelná vlákna': {'en': 'Longitudinal glass fibres', 'de': 'Längs verlaufende Glasfasern', 'it': 'Fibre di vetro longitudinali'}, 'Přilnavost na drsný povrch': {'en': 'Adhesion on rough surfaces', 'de': 'Haftung auf rauen Oberflächen', 'it': 'Adesione su superfici ruvide'}, 'Recyklovaný papírový nosič': {'en': 'Recycled paper carrier', 'de': 'Recycelter Papierträger', 'it': 'Supporto in carta riciclato'}, 'Recyklovaný polyester': {'en': 'Recycled polyester', 'de': 'Recyceltes Polyester', 'it': 'Poliestere riciclato'}, 'Recyklovaný polypropylen': {'en': 'Recycled polypropylene', 'de': 'Recyceltes Polypropylen', 'it': 'Polipropilene riciclato'}, 'Rychlé přilnutí': {'en': 'Fast bonding', 'de': 'Schnelle Haftung', 'it': 'Adesione rapida'}, 'Silikonové lepidlo': {'en': 'Silicone adhesive', 'de': 'Silikonklebstoff', 'it': 'Adesivo siliconico'}, 'Snadné odvíjení pro stroje': {'en': 'Easy unwinding for machines', 'de': 'Leichtes Abrollen für Maschinen', 'it': 'Svolgimento facile per macchine'}, 'Spolehlivá drživost': {'en': 'Reliable hold', 'de': 'Zuverlässige Haftung', 'it': 'Tenuta affidabile'}, 'Super tack (+20 % přilnavosti)': {'en': 'Super tack (+20% adhesion)', 'de': 'Super-Tack (+20 % Klebkraft)', 'it': 'Super tack (+20% adesione)'}, 'Tiché odvíjení a snadné trhání': {'en': 'Quiet unwinding and easy tear', 'de': 'Leises Abrollen und leichtes Abreißen', 'it': 'Svolgimento silenzioso e strappo facile'}, 'Tiché odvíjení a UV odolnost': {'en': 'Quiet unwinding and UV resistance', 'de': 'Leises Abrollen und UV-Beständigkeit', 'it': 'Svolgimento silenzioso e resistenza UV'}, 'Zvýšená vrstva lepidla (+33 %)': {'en': 'Increased adhesive layer (+33%)', 'de': 'Erhöhte Klebstoffschicht (+33 %)', 'it': 'Strato adesivo aumentato (+33%)'}, '100% regenerovaná BOPP fólie': {'en': '100% regenerated BOPP film', 'de': '100 % regenerierte BOPP-Folie', 'it': 'Film BOPP rigenerato al 100%'}, 'Čisté odlepení': {'en': 'Clean removal', 'de': 'Sauberes Abziehen', 'it': 'Rimozione pulita'}, 'Nejčistější lepidlo': {'en': 'Cleanest adhesive', 'de': 'Sauberster Klebstoff', 'it': 'Adesivo più puro'}, 'Low noise odvíjení': {'en': 'Low-noise unwinding', 'de': 'Low-Noise-Abrollen', 'it': 'Svolgimento low noise'}, 'Vysoká odolnost proti UV': {'en': 'High UV resistance', 'de': 'Hohe UV-Beständigkeit', 'it': 'Elevata resistenza ai raggi UV'}, 'Snadné odvíjení': {'en': 'Easy unwinding', 'de': 'Leichtes Abrollen', 'it': 'Svolgimento facile'}, 'Partner pro recyklované kartony': {'en': 'Partner for recycled cartons', 'de': 'Partner für Recyclingkartons', 'it': 'Partner per cartoni riciclati'}, 'Vysoká přilnavost': {'en': 'High adhesion', 'de': 'Hohe Klebkraft', 'it': 'Elevata adesione'}, 'Stejná cena i kvalita': {'en': 'Same price and quality', 'de': 'Gleicher Preis und gleiche Qualität', 'it': 'Stesso prezzo e stessa qualità'}, 'Identické mechanické vlastnosti': {'en': 'Identical mechanical properties', 'de': 'Identische mechanische Eigenschaften', 'it': 'Proprietà meccaniche identiche'}, 'Fólie z vlastního výrobního odpadu': {'en': 'Film from our own production waste', 'de': 'Folie aus eigenem Produktionsabfall', 'it': 'Film dai nostri scarti di produzione'}, 'Fólie z vlastního odpadu z výroby': {'en': 'Film from our own production waste', 'de': 'Folie aus eigenem Produktionsabfall', 'it': 'Film dai nostri scarti di produzione'}, 'Podpora firemní reputace': {'en': 'Supporting corporate reputation', 'de': 'Stärkung der Unternehmensreputation', 'it': 'Supporto alla reputazione aziendale'}}

BENEFIT_TEXT_EXACT: dict[str, dict[str, str]] = {'Tiché odvíjení, dlouhodobá stabilita lepivosti a spolehlivý výkon ve skladových podmínkách.': {'en': 'Quiet unwinding, long-term adhesion stability and reliable performance in warehouse conditions.', 'de': 'Leises Abrollen, langfristig stabile Klebkraft und zuverlässige Leistung unter Lagerbedingungen.', 'it': 'Svolgimento silenzioso, adesione stabile nel tempo e prestazioni affidabili in magazzino.'}, 'Rychlé a pevné přilnutí i při nižších teplotách – vhodné pro ruční i strojové balení.': {'en': 'Fast, strong bonding even at lower temperatures, suitable for manual and machine packing.', 'de': 'Schnelle, feste Haftung auch bei niedrigen Temperaturen – für manuelles und maschinelles Verpacken.', 'it': 'Adesione rapida e resistente anche a basse temperature, adatta al confezionamento manuale e automatico.'}, 'Vysoká okamžitá přilnavost a pevné spojení i na recyklovaném kartonu.': {'en': 'High immediate adhesion and a firm bond even on recycled cardboard.', 'de': 'Hohe Soforthaftung und feste Verbindung auch auf Recyclingkarton.', 'it': 'Elevata adesione immediata e tenuta sicura anche sul cartone riciclato.'}, 'Stabilní výkon v extrémních teplotách a snadné odlepení bez zbytků lepidla.': {'en': 'Stable performance at extreme temperatures and clean removal without adhesive residue.', 'de': 'Stabile Leistung bei extremen Temperaturen und rückstandsfreies Ablösen.', 'it': 'Prestazioni stabili a temperature estreme e rimozione senza residui di adesivo.'}, 'Plně recyklovatelné balení – páska putuje spolu s kartonem bez oddělování.': {'en': 'Fully recyclable packaging, tape goes with the carton without separation.', 'de': 'Vollständig recycelbare Verpackung – das Band geht gemeinsam mit dem Karton ohne Trennung.', 'it': 'Imballaggio completamente riciclabile: il nastro va con il cartone senza separazione.'}, 'Páska i karton putují společně do recyklace – bez oddělování materiálů.': {'en': 'Tape and carton are recycled together, no need to separate materials.', 'de': 'Band und Karton werden gemeinsam recycelt – ohne Materialtrennung.', 'it': 'Nastro e cartone vengono riciclati insieme, senza separare i materiali.'}, 'Výkon při vysokých teplotách lakování i při mrazu – bez poškození povrchu.': {'en': 'Performance at high coating temperatures and in frost, without surface damage.', 'de': 'Leistung bei hohen Lackiertemperaturen und Frost – ohne Oberflächenschäden.', 'it': 'Prestazioni ad alte temperature di verniciatura e al freddo, senza danneggiare la superficie.'}, 'Vhodná pro lakování a náročné maskování v autoservisech.': {'en': 'Suitable for coating and demanding masking in body shops.', 'de': 'Geeignet für Lackierung und anspruchsvolles Abkleben in Werkstätten.', 'it': 'Adatta alla verniciatura e a mascherature impegnative nelle carrozzerie.'}, 'Recyklovaná PP fólie s nižší ekologickou stopou při zachování spolehlivého lepení.': {'en': 'Recycled PP film with a lower environmental footprint while maintaining reliable bonding.', 'de': 'Recycelte PP-Folie mit geringerem ökologischen Fußabdruck bei zuverlässiger Klebkraft.', 'it': 'Film PP riciclato con minore impatto ambientale mantenendo un incollaggio affidabile.'}, 'Vyrobeno výhradně z postindustriálního odpadu – plně recyklovatelná bez nového granulátu.': {'en': 'Made entirely from post-industrial waste, fully recyclable without virgin granulate.', 'de': 'Hergestellt ausschließlich aus postindustriellen Abfällen – vollständig recycelbar ohne Neumaterial.', 'it': 'Prodotto interamente da scarti post-industriali: completamente riciclabile senza granulato vergine.'}, 'Matná BOPP fólie 35 µm bez chloru a rozpouštědel – vhodná náhrada vinylových pásek.': {'en': 'Matte 35 µm BOPP film without chlorine or solvents, a suitable replacement for vinyl tapes.', 'de': 'Matte 35 µm BOPP-Folie ohne Chlor und Lösungsmittel – geeigneter Ersatz für Vinylbänder.', 'it': 'Film BOPP opaco da 35 µm senza cloro né solventi: sostituto adatto ai nastri in vinile.'}, 'Vysoká přilnavost i na recyklovaném kartonu, prašných a nerovných površích.': {'en': 'High adhesion even on recycled cardboard, dusty and uneven surfaces.', 'de': 'Hohe Klebkraft auch auf Recyclingkarton, staubigen und unebenen Oberflächen.', 'it': 'Elevata adesione anche su cartone riciclato, superfici polverose e irregolari.'}, 'Okamžitá přilnavost a vyšší drživost než standardní HOT MELT – doporučeno pro balicí stroje.': {'en': 'Instant adhesion and higher hold than standard HOT MELT, recommended for packing machines.', 'de': 'Sofortige Haftung und höhere Klebkraft als Standard-HOT MELT – empfohlen für Verpackungsmaschinen.', 'it': 'Adesione immediata e tenuta superiore allo HOT MELT standard: consigliato per macchine da imballaggio.'}, 'Okamžitá přilnavost a vyšší drživost než standardní hot melt – doporučeno pro balicí stroje.': {'en': 'Instant adhesion and higher hold than standard hot melt, recommended for packing machines.', 'de': 'Sofortige Klebkraft und höhere Haftung als Standard-Hot-Melt – empfohlen für Verpackungsmaschinen.', 'it': 'Adesione immediata e tenuta superiore al hot melt standard: consigliato per macchine da imballaggio.'}, 'Na bázi vodní disperze bez chemických rozpouštědel.': {'en': 'Water-based dispersion without chemical solvents.', 'de': 'Auf Basis einer wässrigen Dispersion ohne chemische Lösungsmittel.', 'it': 'A base di dispersione acquosa senza solventi chimici.'}, 'Možnost nehlučné úpravy – tiché odvíjení a provozní teplota až do −10 °C.': {'en': 'Optional low-noise finish, quiet unwinding and operating temperature down to −10 °C.', 'de': 'Optionale geräuscharme Ausstattung – leises Abrollen und Betriebstemperatur bis −10 °C.', 'it': 'Opzione low noise: svolgimento silenzioso e temperatura di esercizio fino a −10 °C.'}, 'Akrylové lepidlo si drží lepivost i při dlouhodobém skladování a UV zatížení.': {'en': 'Acrylic adhesive keeps its stickiness during long-term storage and UV exposure.', 'de': 'Acrylklebstoff behält die Klebkraft auch bei langer Lagerung und UV-Belastung.', 'it': "L'adesivo acrilico mantiene l'adesione anche con stoccaggio prolungato e esposizione UV."}, 'Snižuje fyzickou námahu při ručním balení a hodí se i pro automatické balicí stroje.': {'en': 'Reduces physical strain during manual packing and is also great for automatic packing machines.', 'de': 'Verringert die körperliche Belastung beim manuellen Verpacken und eignet sich auch für automatische Verpackungsmaschinen.', 'it': "Riduce lo sforzo fisico nell'imballaggio manuale ed è ideale anche per macchine automatiche."}, 'Díky vysoké lepivosti ideální na recyklované kartony a do prašného prostředí.': {'en': 'Thanks to high stickiness, ideal for recycled cartons and dusty environments.', 'de': 'Dank hoher Klebkraft ideal für Recyclingkartons und staubige Umgebungen.', 'it': "Grazie all'elevata adesività, ideale per cartoni riciclati e ambienti polverosi."}, 'Nelze snadno odlepit ze stretch fólií – zřetelný důkaz zabezpečení zásilky.': {'en': 'Hard to peel off stretch film, a clear sign of shipment security.', 'de': 'Lässt sich nicht leicht von Stretchfolie abziehen – klarer Nachweis der Sendungssicherung.', 'it': 'Difficile da staccare dal film stretch: prova evidente della sicurezza della spedizione.'}, 'Má stejné mechanické vlastnosti a spolehlivost jako standardní BOPP verze, ale bez „ekologické přirážky“.': {'en': 'It has the same mechanical properties and reliability as standard BOPP versions, but without an “eco surcharge”.', 'de': 'Gleiche mechanische Eigenschaften und Zuverlässigkeit wie Standard-BOPP-Varianten – ohne „Öko-Aufpreis“.', 'it': 'Stesse proprietà meccaniche e affidabilità delle versioni BOPP standard, ma senza “maggiorazione ecologica”.'}, 'Má stejnou pevnost v tahu a spolehlivost jako standardní BOPP verze i přes vysoký podíl recyklovaného materiálu.': {'en': 'It has the same tensile strength and reliability as standard BOPP versions despite the high recycled content.', 'de': 'Gleiche Zugfestigkeit und Zuverlässigkeit wie Standard-BOPP-Varianten – trotz hohem Recyclinganteil.', 'it': 'Stessa resistenza alla trazione e affidabilità delle versioni BOPP standard, nonostante l’alto contenuto di riciclato.'}, 'Páska vykazuje stejnou pevnost v tahu a spolehlivost jako standardní BOPP verze i přes 100% regenerovaný materiál.': {'en': 'The tape delivers the same tensile strength and reliability as standard BOPP versions despite 100% regenerated material.', 'de': 'Das Band bietet dieselbe Zugfestigkeit und Zuverlässigkeit wie Standard-BOPP-Varianten – trotz 100 % regeneriertem Material.', 'it': 'Il nastro offre la stessa resistenza alla trazione e affidabilità delle versioni BOPP standard, nonostante il materiale rigenerato al 100%.'}, 'Nosný materiál obsahuje 50 % postindustriálního odpadu, který vzniká přímo při naší výrobě fólií a je ihned efektivně vracen zpět do oběhu.': {'en': 'The carrier contains 50% post-industrial waste generated directly in our film production and immediately returned to the loop.', 'de': 'Der Träger enthält 50 % postindustriellen Abfall aus unserer Folienproduktion, der sofort effizient in den Kreislauf zurückgeführt wird.', 'it': 'Il supporto contiene il 50% di scarti post-industriali generati direttamente nella nostra produzione di film e subito reimmessi nel ciclo.'}, 'Nosný materiál obsahuje 80 % postindustriálního odpadu, který vzniká přímo při naší výrobě fólií a je ihned efektivně vracen zpět do oběhu.': {'en': 'The carrier contains 80% post-industrial waste generated directly in our film production and immediately returned to the loop.', 'de': 'Der Träger enthält 80 % postindustriellen Abfall aus unserer Folienproduktion, der sofort effizient in den Kreislauf zurückgeführt wird.', 'it': 'Il supporto contiene l’80% di scarti post-industriali generati direttamente nella nostra produzione di film e subito reimmessi nel ciclo.'}, 'Vyrobeno z čistého postindustriálního odpadu z naší vlastní výroby fólií – bez nového granulátu.': {'en': 'Made from clean post-industrial waste from our own film production, without virgin granulate.', 'de': 'Hergestellt aus sauberem postindustriellen Abfall aus unserer eigenen Folienproduktion – ohne Neumaterial.', 'it': 'Prodotto da scarti post-industriali puliti della nostra produzione di film, senza granulato vergine.'}, 'Pásky řady ECO+ spolehlivě chrání zboží a prokazují ekologickou odpovědnost – ať už v neutrálním provedení, nebo s firemním potiskem.': {'en': 'ECO+ tapes reliably protect goods and demonstrate environmental responsibility, in a plain finish or with company print.', 'de': 'ECO+-Bänder schützen Ware zuverlässig und zeigen ökologische Verantwortung – neutral oder mit Firmendruck.', 'it': 'I nastri ECO+ proteggono merce in modo affidabile e dimostrano responsabilità ambientale, in versione neutra o con stampa aziendale.'}}


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
    keys = TECH_SPEC_PARAM_FIELD_KEYS if p.get("tech_spec") else PARAM_FIELD_KEYS
    return {key: params[cs_key] for key, cs_key in keys}


def _tech_variants_from_product(ns: dict, p: dict) -> dict[str, dict[str, str]]:
    variants = ns["product_tech_variant_tables"](p)
    if not variants:
        return {}
    out: dict[str, dict[str, str]] = {}
    for variant, params in variants.items():
        out[variant] = {
            key: params[cs_key]
            for key, cs_key in TECH_SPEC_PARAM_FIELD_KEYS
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
    labels = TECH_SPEC_PARAM_LABELS["cs"] if p.get("tech_spec") else PARAM_LABELS["cs"]
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
        "tech_variant_labels": {"akryl": "Akryl", "hot_melt": "HOT MELT"} if tech_variants else {},
        "min_qty_note": ns["product_min_qty_note"](p),
        "params_labels": labels,
        "tech_spec": bool(p.get("tech_spec")),
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
            TECH_SPEC_PARAM_LABELS[locale] if product.get("tech_spec") else PARAM_LABELS[locale]
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
