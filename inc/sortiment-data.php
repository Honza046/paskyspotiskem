<?php
/**
 * Sortiment – product category directory, detail content, product lists and
 * per-product technical specifications.
 *
 * Product images live in category folders in the theme root (e.g. "BOPP Tapes/").
 * Paths are stored relative to the theme root and resolved via
 * paskyonline_product_image().
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Product categories with detail content and product lists.
 *
 * @return array
 */
function paskyonline_get_sortiment_categories() {
    return array(
        array(
            'title'        => 'Papírové pásky',
            'slug'         => '/sortiment/papirove-pasky',
            'image'        => 'Papírové Pásky/Papírovácover.png',
            'description'  => 'Ekologické řešení pro bezpečné balení s vysokou lepivostí. Ideální pro plně recyklovatelné kartonové obaly a čistý korporátní design.',
            'intro'        => 'Papírové lepicí pásky spojují spolehlivé lepení s maximální ekologickou šetrností. Díky papírovému nosiči jsou plně recyklovatelné společně s kartonem a představují elegantní, čistě vypadající řešení pro firmy, které dbají na udržitelnost i vizuální dojem zásilek.',
            'properties'   => array(
                array( 'title' => 'Plná recyklovatelnost', 'text' => 'Páska i karton putují do jednoho kontejneru – bez nutnosti oddělovat materiály.' ),
                array( 'title' => 'Vysoká lepivost', 'text' => 'Spolehlivé přilnutí i na recyklovaný karton a členité povrchy.' ),
                array( 'title' => 'Čistý design', 'text' => 'Matný papírový povrch působí prémiově a lze jej snadno potisknout logem.' ),
            ),
            'applications' => array(
                'E-shopy s důrazem na udržitelné balení',
                'Uzavírání kartonových krabic a obalů',
                'Firemní branding přímo na zásilce',
                'Ruční i poloautomatické balení',
            ),
            'products'     => array(
                array(
                    'name'    => 'Papírová páska KH80',
                    'slug'    => 'papirova-paska-kh80',
                    'image'   => 'Papírové Pásky/KH80.png',
                    'tagline' => 'Silná papírová páska s hot melt lepidlem pro spolehlivé uzavírání kartonů.',
                    'params'  => array(
                        'Nosič / materiál' => 'Papírový nosič (kraft)',
                        'Tloušťka' => '120 µm',
                        'Typ lepidla' => 'Hot melt (syntetický kaučuk)',
                        'Přilnavost (ocel)' => '4,5 N/25 mm',
                        'Teplotní odolnost' => '−10 až +60 °C',
                        'Pevnost v tahu' => '55 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'rucni'),
                ),
                array(
                    'name'    => 'Papírová páska KS165',
                    'slug'    => 'papirova-paska-ks165',
                    'image'   => 'Papírové Pásky/KS165.png',
                    'tagline' => 'Extra pevná papírová páska s kaučukovým lepidlem pro náročné balení.',
                    'params'  => array(
                        'Nosič / materiál' => 'Papírový nosič (kraft)',
                        'Tloušťka' => '150 µm',
                        'Typ lepidla' => 'Kaučukové (solvent)',
                        'Přilnavost (ocel)' => '5,5 N/25 mm',
                        'Teplotní odolnost' => '−20 až +70 °C',
                        'Pevnost v tahu' => '70 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'rucni'),
                ),
                array(
                    'name'    => 'Papírová páska C660',
                    'slug'    => 'papirova-paska-c660',
                    'image'   => 'Papírové Pásky/c660.png',
                    'tagline' => 'Ekologická papírová páska s akrylovým lepidlem a čistým odvíjením.',
                    'params'  => array(
                        'Nosič / materiál' => 'Papírový nosič',
                        'Tloušťka' => '100 µm',
                        'Typ lepidla' => 'Akrylové (disperzní)',
                        'Přilnavost (ocel)' => '3,8 N/25 mm',
                        'Teplotní odolnost' => '−5 až +60 °C',
                        'Pevnost v tahu' => '45 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'tiche', 'rucni'),
                ),
                array(
                    'name'    => 'Papírová páska C680',
                    'slug'    => 'papirova-paska-c680',
                    'image'   => 'Papírové Pásky/c680.png',
                    'tagline' => 'Univerzální papírová páska s vysokou lepivostí na recyklovaný karton.',
                    'params'  => array(
                        'Nosič / materiál' => 'Papírový nosič',
                        'Tloušťka' => '115 µm',
                        'Typ lepidla' => 'Kaučukové',
                        'Přilnavost (ocel)' => '4,2 N/25 mm',
                        'Teplotní odolnost' => '−10 až +60 °C',
                        'Pevnost v tahu' => '50 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'rucni', 'stroje'),
                ),
                array(
                    'name'    => 'Papírová páska C680R',
                    'slug'    => 'papirova-paska-c680r',
                    'image'   => 'Papírové Pásky/c680r.jpeg',
                    'tagline' => 'Papírová páska z recyklovaného papíru pro udržitelné balení.',
                    'params'  => array(
                        'Nosič / materiál' => 'Recyklovaný papír',
                        'Tloušťka' => '115 µm',
                        'Typ lepidla' => 'Kaučukové',
                        'Přilnavost (ocel)' => '4,0 N/25 mm',
                        'Teplotní odolnost' => '−10 až +60 °C',
                        'Pevnost v tahu' => '48 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'rucni'),
                ),
                array(
                    'name'    => 'Papírová páska C680 RT',
                    'slug'    => 'papirova-paska-c680-rt',
                    'image'   => 'Papírové Pásky/c680RT.jpeg',
                    'tagline' => 'Odolná papírová páska s vylepšenou přilnavostí pro těžší zásilky.',
                    'params'  => array(
                        'Nosič / materiál' => 'Papírový nosič',
                        'Tloušťka' => '120 µm',
                        'Typ lepidla' => 'Kaučukové',
                        'Přilnavost (ocel)' => '4,3 N/25 mm',
                        'Teplotní odolnost' => '−10 až +65 °C',
                        'Pevnost v tahu' => '52 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'rucni', 'stroje'),
                ),
                array(
                    'name'    => 'Papírová páska C690',
                    'slug'    => 'papirova-paska-c690',
                    'image'   => 'Papírové Pásky/c690.png',
                    'tagline' => 'Prémiová kraftová páska s hot melt lepidlem a matným povrchem.',
                    'params'  => array(
                        'Nosič / materiál' => 'Papírový nosič (kraft)',
                        'Tloušťka' => '130 µm',
                        'Typ lepidla' => 'Hot melt',
                        'Přilnavost (ocel)' => '4,8 N/25 mm',
                        'Teplotní odolnost' => '−10 až +70 °C',
                        'Pevnost v tahu' => '60 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'rucni'),
                ),
            ),
        ),
        array(
            'title'        => 'BOPP pásky',
            'slug'         => '/sortiment/bopp-pasky',
            'image'        => 'BOPP Tapes/BOPP_Cover.png',
            'description'  => 'Nejrozšířenější průmyslové balicí pásky z biaxiálně orientovaného polypropylenu. Vynikají skvělou pevností v tahu a dlouhou životností.',
            'intro'        => 'BOPP pásky jsou standardem pro každodenní balení ve výrobě, logistice i e-commerce. Fólie z biaxiálně orientovaného polypropylenu nabízí vynikající poměr ceny a výkonu, dostupnost v akrylovém i hot melt provedení a širokou škálu šířek a barev.',
            'properties'   => array(
                array( 'title' => 'Vysoká pevnost v tahu', 'text' => 'Odolná fólie, která se při balení nepřetrhne ani pod napětím.' ),
                array( 'title' => 'ACRYL i HOT MELT', 'text' => 'Volba lepidla podle prostředí – tiché odvíjení, nebo rychlé přilnutí za chladu.' ),
                array( 'title' => 'Dlouhá životnost', 'text' => 'Odolnost proti UV a stárnutí pro dlouhodobé skladování.' ),
            ),
            'applications' => array(
                'Standardní uzavírání kartonů',
                'Automatické balicí stroje',
                'Expedice a skladová logistika',
                'Potisk firemním logem a informacemi',
            ),
            'products'     => array(
                array(
                    'name'    => 'BOPP páska Acrylic',
                    'slug'    => 'bopp-paska-acrylic',
                    'image'   => 'BOPP Tapes/BOPPACRYLIC.jpeg',
                    'tagline' => 'Spolehlivá BOPP páska s akrylovým lepidlem a dlouhou životností.',
                    'params'  => array(
                        'Nosič / materiál' => 'BOPP fólie',
                        'Tloušťka' => '45 µm',
                        'Typ lepidla' => 'Akrylové (vodní disperze)',
                        'Přilnavost (ocel)' => '2,8 N/25 mm',
                        'Teplotní odolnost' => '−5 až +60 °C',
                        'Pevnost v tahu' => '45 N/25 mm',
                    ),
                    'tags'    => array('tiche', 'rucni', 'stroje'),
                ),
                array(
                    'name'    => 'BOPP páska Hot Melt',
                    'slug'    => 'bopp-paska-hot-melt',
                    'image'   => 'BOPP Tapes/BOPPHOTMELT.jpeg',
                    'tagline' => 'BOPP páska s hot melt lepidlem pro rychlé a pevné přilnutí.',
                    'params'  => array(
                        'Nosič / materiál' => 'BOPP fólie',
                        'Tloušťka' => '40 µm',
                        'Typ lepidla' => 'Hot melt (syntetický kaučuk)',
                        'Přilnavost (ocel)' => '3,5 N/25 mm',
                        'Teplotní odolnost' => '0 až +50 °C',
                        'Pevnost v tahu' => '42 N/25 mm',
                    ),
                    'tags'    => array('rucni', 'stroje'),
                ),
                array(
                    'name'    => 'BOPP páska Hot Melt II',
                    'slug'    => 'bopp-paska-hot-melt-ii',
                    'image'   => 'BOPP Tapes/BOPPHOTMELT1.png',
                    'tagline' => 'Silnější BOPP páska s hot melt lepidlem pro náročnější balení.',
                    'params'  => array(
                        'Nosič / materiál' => 'BOPP fólie',
                        'Tloušťka' => '48 µm',
                        'Typ lepidla' => 'Hot melt',
                        'Přilnavost (ocel)' => '3,8 N/25 mm',
                        'Teplotní odolnost' => '0 až +55 °C',
                        'Pevnost v tahu' => '48 N/25 mm',
                    ),
                    'tags'    => array('rucni', 'stroje'),
                ),
                array(
                    'name'    => 'BOPP páska Evergreen',
                    'slug'    => 'bopp-paska-evergreen',
                    'image'   => 'BOPP Tapes/EVERGREEN.png',
                    'tagline' => 'Barevná BOPP páska pro značení a vizuální odlišení zásilek.',
                    'params'  => array(
                        'Nosič / materiál' => 'BOPP fólie (barevná)',
                        'Tloušťka' => '45 µm',
                        'Typ lepidla' => 'Akrylové',
                        'Přilnavost (ocel)' => '3,0 N/25 mm',
                        'Teplotní odolnost' => '−5 až +60 °C',
                        'Pevnost v tahu' => '46 N/25 mm',
                    ),
                    'tags'    => array('mrazuvzdorne', 'stroje'),
                ),
            ),
        ),
        array(
            'title'        => 'BOPET pásky',
            'slug'         => '/sortiment/bopet-pasky',
            'image'        => 'BOPET Tapes/BOPET_Cover.png',
            'description'  => 'Prémiové polyesterové pásky s extrémní odolností proti roztržení, chemikáliím a teplotním výkyvům. Navržené pro nejnáročnější průmyslové aplikace.',
            'intro'        => 'BOPET pásky na bázi polyesterové fólie jsou určeny tam, kde běžné pásky nestačí. Zvládají vysoké teploty, agresivní chemické prostředí i mechanické namáhání a udrží si své vlastnosti i v extrémních podmínkách.',
            'properties'   => array(
                array( 'title' => 'Teplotní odolnost', 'text' => 'Stabilní výkon při vysokých i nízkých teplotách.' ),
                array( 'title' => 'Chemická odolnost', 'text' => 'Odolává rozpouštědlům, olejům a agresivnímu prostředí.' ),
                array( 'title' => 'Odolnost proti roztržení', 'text' => 'Pevná polyesterová fólie s minimální tažností.' ),
            ),
            'applications' => array(
                'Náročné průmyslové provozy',
                'Maskování při práškovém lakování',
                'Fixace v prostředí s vysokými teplotami',
                'Elektrotechnika a specializovaná výroba',
            ),
            'products'     => array(
                array(
                    'name'    => 'BOPET páska ATE23',
                    'slug'    => 'bopet-paska-ate23',
                    'image'   => 'BOPET Tapes/ATE23.png',
                    'tagline' => 'Tenká polyesterová páska s vysokou teplotní odolností.',
                    'params'  => array(
                        'Nosič / materiál' => 'Polyesterová (PET) fólie',
                        'Tloušťka' => '25 µm',
                        'Typ lepidla' => 'Akrylové',
                        'Přilnavost (ocel)' => '3,5 N/25 mm',
                        'Teplotní odolnost' => '−40 až +150 °C',
                        'Pevnost v tahu' => '60 N/25 mm',
                    ),
                    'tags'    => array('vysoke-teploty', 'chemicka-odolnost'),
                ),
                array(
                    'name'    => 'BOPET páska AIT',
                    'slug'    => 'bopet-paska-ait',
                    'image'   => 'BOPET Tapes/BOPETAIT.png',
                    'tagline' => 'Polyesterová páska se silikonovým lepidlem pro extrémní teploty.',
                    'params'  => array(
                        'Nosič / materiál' => 'Polyesterová (PET) fólie',
                        'Tloušťka' => '30 µm',
                        'Typ lepidla' => 'Silikonové',
                        'Přilnavost (ocel)' => '3,0 N/25 mm',
                        'Teplotní odolnost' => '−40 až +180 °C',
                        'Pevnost v tahu' => '65 N/25 mm',
                    ),
                    'tags'    => array('vysoke-teploty', 'mrazuvzdorne', 'chemicka-odolnost'),
                ),
                array(
                    'name'    => 'BOPET páska HIT17',
                    'slug'    => 'bopet-paska-hit17',
                    'image'   => 'BOPET Tapes/BOPETHIT17.png',
                    'tagline' => 'Ultratenká PET páska pro elektrotechniku a přesné aplikace.',
                    'params'  => array(
                        'Nosič / materiál' => 'Polyesterová (PET) fólie',
                        'Tloušťka' => '17 µm',
                        'Typ lepidla' => 'Akrylové',
                        'Přilnavost (ocel)' => '3,2 N/25 mm',
                        'Teplotní odolnost' => '−40 až +155 °C',
                        'Pevnost v tahu' => '55 N/25 mm',
                    ),
                    'tags'    => array('vysoke-teploty', 'chemicka-odolnost'),
                ),
                array(
                    'name'    => 'BOPET páska ECO HIT19',
                    'slug'    => 'bopet-paska-eco-hit19',
                    'image'   => 'BOPET Tapes/ECOHIT19.png',
                    'tagline' => 'Polyesterová páska s recyklovaným obsahem a vysokou odolností.',
                    'params'  => array(
                        'Nosič / materiál' => 'Recyklovaná PET fólie',
                        'Tloušťka' => '19 µm',
                        'Typ lepidla' => 'Akrylové',
                        'Přilnavost (ocel)' => '3,3 N/25 mm',
                        'Teplotní odolnost' => '−40 až +150 °C',
                        'Pevnost v tahu' => '58 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'vysoke-teploty', 'chemicka-odolnost'),
                ),
            ),
        ),
        array(
            'title'        => 'Textilní lepicí pásky',
            'slug'         => '/sortiment/textilni-pasky',
            'image'        => 'Textilní Lepící Pásky/Duct_Cover-2.png',
            'description'  => 'Vysoce pevné a univerzální pásky zpevněné textilní mřížkou. Perfektně drží na drsném povrchu, snadno se trhají rukou a jsou ideální pro rychlé opravy i svazování.',
            'intro'        => 'Textilní (duct) pásky jsou nepostradatelným univerzálem. Textilní výztuž jim dodává vysokou pevnost a zároveň umožňuje snadné odtržení rukou bez nůžek. Skvěle drží i na hrubých a nerovných površích.',
            'properties'   => array(
                array( 'title' => 'Textilní výztuž', 'text' => 'Vysoká pevnost a odolnost proti protržení.' ),
                array( 'title' => 'Trhání rukou', 'text' => 'Rychlá práce bez nutnosti nářadí.' ),
                array( 'title' => 'Přilnavost na drsný povrch', 'text' => 'Drží na kovu, dřevě, betonu i plastu.' ),
            ),
            'applications' => array(
                'Rychlé opravy a provizorní spoje',
                'Svazování a fixace předmětů',
                'Zpevnění balíků a obalů',
                'Údržba, montáže a řemeslo',
            ),
            'products'     => array(
                array(
                    'name'    => 'Textilní páska BC',
                    'slug'    => 'textilni-paska-bc',
                    'image'   => 'Textilní Lepící Pásky/BC.png',
                    'tagline' => 'Pevná textilní (duct) páska pro opravy a univerzální použití.',
                    'params'  => array(
                        'Nosič / materiál' => 'Textilní výztuž + PE laminát',
                        'Tloušťka' => '250 µm',
                        'Typ lepidla' => 'Kaučukové (syntetické)',
                        'Přilnavost (ocel)' => '6,0 N/25 mm',
                        'Teplotní odolnost' => '−10 až +70 °C',
                        'Pevnost v tahu' => '120 N/25 mm',
                    ),
                    'tags'    => array('vyztuzene', 'rucni'),
                ),
                array(
                    'name'    => 'Textilní páska BC2',
                    'slug'    => 'textilni-paska-bc2',
                    'image'   => 'Textilní Lepící Pásky/BC2.png',
                    'tagline' => 'Extra silná textilní páska s vysokou pevností v tahu.',
                    'params'  => array(
                        'Nosič / materiál' => 'Textilní výztuž + PE laminát',
                        'Tloušťka' => '280 µm',
                        'Typ lepidla' => 'Kaučukové (syntetické)',
                        'Přilnavost (ocel)' => '6,5 N/25 mm',
                        'Teplotní odolnost' => '−10 až +70 °C',
                        'Pevnost v tahu' => '130 N/25 mm',
                    ),
                    'tags'    => array('vyztuzene', 'rucni'),
                ),
                array(
                    'name'    => 'Textilní páska NU',
                    'slug'    => 'textilni-paska-nu',
                    'image'   => 'Textilní Lepící Pásky/NU.png',
                    'tagline' => 'Univerzální textilní páska pro rychlé svazování a fixaci.',
                    'params'  => array(
                        'Nosič / materiál' => 'Textilní výztuž + PE laminát',
                        'Tloušťka' => '220 µm',
                        'Typ lepidla' => 'Kaučukové',
                        'Přilnavost (ocel)' => '5,5 N/25 mm',
                        'Teplotní odolnost' => '−10 až +65 °C',
                        'Pevnost v tahu' => '110 N/25 mm',
                    ),
                    'tags'    => array('vyztuzene', 'rucni'),
                ),
            ),
        ),
        array(
            'title'        => 'Vyztužené pásky',
            'slug'         => '/sortiment/vyztuzene-pasky',
            'image'        => 'Vyztužené Pásky/Reinforcedcover.png',
            'description'  => 'Pásky zpevněné podélnými nebo křížovými skelnými vlákny. Nabízejí maximální pevnost při fixaci těžkých nákladů, palet a nadrozměrných balíků.',
            'intro'        => 'Vyztužené (filament) pásky obsahují skelná vlákna vedená podélně nebo křížem, která zásadně zvyšují pevnost v tahu. Jsou určené pro fixaci těžkých a nadrozměrných zásilek, kde je potřeba absolutní jistota.',
            'properties'   => array(
                array( 'title' => 'Skelná vlákna', 'text' => 'Podélné nebo křížové vyztužení pro maximální pevnost.' ),
                array( 'title' => 'Nosnost', 'text' => 'Spolehlivá fixace těžkých břemen a palet.' ),
                array( 'title' => 'Odolnost proti přetržení', 'text' => 'Vydrží i vysoké tahové zatížení.' ),
            ),
            'applications' => array(
                'Fixace těžkých a nadrozměrných balíků',
                'Zajištění zboží na paletách',
                'Svazování trubek, profilů a tyčí',
                'Náročná přeprava a export',
            ),
            'products'     => array(
                array(
                    'name'    => 'Vyztužená páska RMPP32',
                    'slug'    => 'vyztuzena-paska-rmpp32',
                    'image'   => 'Vyztužené Pásky/rmpp32.png',
                    'tagline' => 'Vyztužená páska se skelnými vlákny pro fixaci těžkých břemen.',
                    'params'  => array(
                        'Nosič / materiál' => 'MOPP + podélná skelná vlákna',
                        'Tloušťka' => '130 µm',
                        'Typ lepidla' => 'Hot melt (syntetický kaučuk)',
                        'Přilnavost (ocel)' => '4,5 N/25 mm',
                        'Teplotní odolnost' => '−10 až +60 °C',
                        'Pevnost v tahu' => '300 N/25 mm',
                    ),
                    'tags'    => array('vyztuzene', 'stroje'),
                ),
                array(
                    'name'    => 'Vyztužená páska RTPP32',
                    'slug'    => 'vyztuzena-paska-rtpp32',
                    'image'   => 'Vyztužené Pásky/rtpp32.png',
                    'tagline' => 'Křížově vyztužená páska pro maximální pevnost ve všech směrech.',
                    'params'  => array(
                        'Nosič / materiál' => 'MOPP + křížová skelná vlákna',
                        'Tloušťka' => '140 µm',
                        'Typ lepidla' => 'Hot melt',
                        'Přilnavost (ocel)' => '4,7 N/25 mm',
                        'Teplotní odolnost' => '−10 až +60 °C',
                        'Pevnost v tahu' => '320 N/25 mm',
                    ),
                    'tags'    => array('vyztuzene', 'stroje'),
                ),
            ),
        ),
        array(
            'title'        => 'MOPP pásky',
            'slug'         => '/sortiment/mopp-pasky',
            'image'        => 'MOPP Pásky/moppcvoer.png',
            'description'  => 'Monoaxiálně orientované pásky s extrémní pevností v jednom směru a nulovou elasticitou. Speciálně určené pro fixaci elektrospotřebičů, komponentů nebo stahování palet.',
            'intro'        => 'MOPP pásky mají monoaxiálně orientovanou fólii s extrémní pevností v podélném směru a prakticky nulovou tažností. Nahrazují vyztužené pásky tam, kde je potřeba pevná fixace bez skelných vláken.',
            'properties'   => array(
                array( 'title' => 'Extrémní pevnost', 'text' => 'Vysoká pevnost v tahu v jednom směru.' ),
                array( 'title' => 'Nulová elasticita', 'text' => 'Fixace se nepovolí ani při zatížení.' ),
                array( 'title' => 'Bez skelných vláken', 'text' => 'Čistá fixace bez uvolňujících se vláken.' ),
            ),
            'applications' => array(
                'Fixace dveří elektrospotřebičů',
                'Zajištění komponentů během přepravy',
                'Stahování a fixace palet',
                'Svazování bez skelných vláken',
            ),
            'products'     => array(
                array(
                    'name'    => 'MOPP páska S45-50',
                    'slug'    => 'mopp-paska-s45-50',
                    'image'   => 'MOPP Pásky/s45-50.png',
                    'tagline' => 'Monoaxiální MOPP páska s extrémní pevností a nulovou tažností.',
                    'params'  => array(
                        'Nosič / materiál' => 'MOPP fólie',
                        'Tloušťka' => '100 µm',
                        'Typ lepidla' => 'Hot melt',
                        'Přilnavost (ocel)' => '4,0 N/25 mm',
                        'Teplotní odolnost' => '−10 až +60 °C',
                        'Pevnost v tahu' => '250 N/25 mm',
                    ),
                    'tags'    => array('vyztuzene', 'stroje'),
                ),
            ),
        ),
        array(
            'title'        => 'Odstranitelné pásky',
            'slug'         => '/sortiment/odstranitelne-pasky',
            'image'        => 'Odstranitelné Pásky/removable cover.png',
            'description'  => 'Pásky se speciálním složením lepidla, které nezanechává žádné stopy po odlepení. Ideální pro dočasné značení, ochranu citlivých povrchů nebo logistické procesy.',
            'intro'        => 'Odstranitelné pásky používají speciální lepidlo, které pevně drží, ale po odlepení nezanechává žádné zbytky ani poškození povrchu. Jsou ideální pro dočasné aplikace a ochranu citlivých materiálů.',
            'properties'   => array(
                array( 'title' => 'Beze stop', 'text' => 'Po odlepení nezůstává lepidlo ani reziduum.' ),
                array( 'title' => 'Šetrné k povrchu', 'text' => 'Nepoškodí lak, sklo ani citlivé materiály.' ),
                array( 'title' => 'Spolehlivá drživost', 'text' => 'Drží po celou dobu potřebné aplikace.' ),
            ),
            'applications' => array(
                'Dočasné značení a etikety',
                'Ochrana citlivých povrchů',
                'Logistické a výrobní procesy',
                'Fixace, která se musí opět odstranit',
            ),
            'products'     => array(
                array(
                    'name'    => 'Odstranitelná páska R28-32',
                    'slug'    => 'odstranitelna-paska-r28-32',
                    'image'   => 'Odstranitelné Pásky/r28-32.png',
                    'tagline' => 'Odstranitelná páska, která po odlepení nezanechá žádné stopy.',
                    'params'  => array(
                        'Nosič / materiál' => 'BOPP fólie',
                        'Tloušťka' => '50 µm',
                        'Typ lepidla' => 'Odstranitelné akrylové',
                        'Přilnavost (ocel)' => '1,5 N/25 mm',
                        'Teplotní odolnost' => '−5 až +50 °C',
                        'Pevnost v tahu' => '40 N/25 mm',
                    ),
                    'tags'    => array('odstranitelne', 'rucni'),
                ),
                array(
                    'name'    => 'Odstranitelná páska ECO RIT19',
                    'slug'    => 'odstranitelna-paska-eco-rit19',
                    'image'   => 'Odstranitelné Pásky/ECORIT19.png',
                    'tagline' => 'Šetrná odstranitelná páska s recyklovaným obsahem.',
                    'params'  => array(
                        'Nosič / materiál' => 'Recyklovaná PET fólie',
                        'Tloušťka' => '19 µm',
                        'Typ lepidla' => 'Odstranitelné akrylové',
                        'Přilnavost (ocel)' => '1,8 N/25 mm',
                        'Teplotní odolnost' => '−5 až +55 °C',
                        'Pevnost v tahu' => '45 N/25 mm',
                    ),
                    'tags'    => array('odstranitelne', 'ekologicke', 'rucni'),
                ),
            ),
        ),
        array(
            'title'        => 'Malířské pásky',
            'slug'         => '/sortiment/malirske-pasky',
            'image'        => 'Malířské Pásky/malířskácover.png',
            'description'  => 'Krepové papírové pásky navržené pro přesné zakrývání při malování a lakování. Chrání hrany před protečením barvy a po dokončení práce se čistě odlepí.',
            'intro'        => 'Malířské krepové pásky zajišťují ostré a čisté hrany při malování a lakování. Papírový krepový nosič se dobře přizpůsobí povrchu, snadno se trhá a po dokončení práce se odlepí bez zbytků lepidla.',
            'properties'   => array(
                array( 'title' => 'Ostré hrany', 'text' => 'Zabraňuje protečení barvy pod pásku.' ),
                array( 'title' => 'Čisté odlepení', 'text' => 'Po práci nezanechává lepidlo ani stopy.' ),
                array( 'title' => 'Snadná aplikace', 'text' => 'Krep se přizpůsobí tvaru a snadno se trhá.' ),
            ),
            'applications' => array(
                'Malování a lakování interiérů',
                'Zakrývání hran a přechodů',
                'Lakovny a autolakovny',
                'Kutilské a řemeslné práce',
            ),
            'products'     => array(
                array(
                    'name'    => 'Malířská páska C580',
                    'slug'    => 'malirska-paska-c580',
                    'image'   => 'Malířské Pásky/c580.png',
                    'tagline' => 'Krepová malířská páska pro ostré hrany při běžném malování.',
                    'params'  => array(
                        'Nosič / materiál' => 'Krepový papír',
                        'Tloušťka' => '130 µm',
                        'Typ lepidla' => 'Kaučukové',
                        'Přilnavost (ocel)' => '2,8 N/25 mm',
                        'Teplotní odolnost' => 'do +80 °C',
                        'Pevnost v tahu' => '28 N/25 mm',
                    ),
                    'tags'    => array('rucni'),
                ),
                array(
                    'name'    => 'Malířská páska CS60-80',
                    'slug'    => 'malirska-paska-cs60-80',
                    'image'   => 'Malířské Pásky/cs60-80.png',
                    'tagline' => 'Teplotně odolná malířská páska pro lakování a náročné maskování.',
                    'params'  => array(
                        'Nosič / materiál' => 'Krepový papír',
                        'Tloušťka' => '150 µm',
                        'Typ lepidla' => 'Kaučukové (odolné teplu)',
                        'Přilnavost (ocel)' => '3,0 N/25 mm',
                        'Teplotní odolnost' => 'do +100 °C',
                        'Pevnost v tahu' => '32 N/25 mm',
                    ),
                    'tags'    => array('vysoke-teploty', 'rucni'),
                ),
            ),
        ),
        array(
            'title'        => 'Udržitelné pásky',
            'slug'         => '/sortiment/udrzitelne-pasky',
            'image'        => 'Udržitelné Pásky/eco+100cover.png',
            'description'  => 'Inovativní obalová řešení vyrobená z recyklovaných materiálů s ohledem na minimální ekologickou stopu a podporu cirkulární ekonomiky.',
            'intro'        => 'Udržitelná řada pásek je vyrobena z recyklovaných materiálů a navržena tak, aby minimalizovala dopad na životní prostředí. Pomáhá firmám plnit ESG cíle a budovat obraz zodpovědné značky bez kompromisů ve výkonu.',
            'properties'   => array(
                array( 'title' => 'Recyklovaný obsah', 'text' => 'Materiály s vysokým podílem recyklátu.' ),
                array( 'title' => 'Nižší uhlíková stopa', 'text' => 'Šetrnější výroba a cirkulární přístup.' ),
                array( 'title' => 'Bez kompromisů', 'text' => 'Ekologie při zachování spolehlivého lepení.' ),
            ),
            'applications' => array(
                'Firmy s ESG a udržitelnými cíli',
                'Zelené balení pro e-shopy',
                'Cirkulární obalové procesy',
                'Budování zodpovědné značky',
            ),
            'products'     => array(
                array(
                    'name'    => 'Udržitelná páska NOPP',
                    'slug'    => 'udrzitelna-paska-nopp',
                    'image'   => 'Udržitelné Pásky/nopp.png',
                    'tagline' => 'Udržitelná páska bez plastu pro plně recyklovatelné balení.',
                    'params'  => array(
                        'Nosič / materiál' => 'Papír (FSC)',
                        'Tloušťka' => '110 µm',
                        'Typ lepidla' => 'Akrylové (bez rozpouštědel)',
                        'Přilnavost (ocel)' => '4,0 N/25 mm',
                        'Teplotní odolnost' => '−5 až +60 °C',
                        'Pevnost v tahu' => '50 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'rucni'),
                ),
                array(
                    'name'    => 'Udržitelná páska NOPP+',
                    'slug'    => 'udrzitelna-paska-nopp',
                    'image'   => 'Udržitelné Pásky/nopp+.png',
                    'tagline' => 'Vylepšená bezplastová páska s vyšší pevností a lepivostí.',
                    'params'  => array(
                        'Nosič / materiál' => 'Papír (FSC)',
                        'Tloušťka' => '120 µm',
                        'Typ lepidla' => 'Akrylové',
                        'Přilnavost (ocel)' => '4,4 N/25 mm',
                        'Teplotní odolnost' => '−5 až +65 °C',
                        'Pevnost v tahu' => '55 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'rucni'),
                ),
                array(
                    'name'    => 'Udržitelná páska LOOPP',
                    'slug'    => 'udrzitelna-paska-loopp',
                    'image'   => 'Udržitelné Pásky/loopp.png',
                    'tagline' => 'Páska z recyklovaného polypropylenu pro cirkulární ekonomiku.',
                    'params'  => array(
                        'Nosič / materiál' => 'Recyklovaná PP fólie',
                        'Tloušťka' => '45 µm',
                        'Typ lepidla' => 'Akrylové',
                        'Přilnavost (ocel)' => '3,0 N/25 mm',
                        'Teplotní odolnost' => '−5 až +60 °C',
                        'Pevnost v tahu' => '46 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'stroje'),
                ),
                array(
                    'name'    => 'Udržitelná páska Airtape',
                    'slug'    => 'udrzitelna-paska-airtape',
                    'image'   => 'Udržitelné Pásky/airtape.png',
                    'tagline' => 'Lehká udržitelná páska pro každodenní ekologické balení.',
                    'params'  => array(
                        'Nosič / materiál' => 'Recyklovaná PP fólie',
                        'Tloušťka' => '40 µm',
                        'Typ lepidla' => 'Akrylové',
                        'Přilnavost (ocel)' => '2,8 N/25 mm',
                        'Teplotní odolnost' => '−5 až +60 °C',
                        'Pevnost v tahu' => '42 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'rucni'),
                ),
                array(
                    'name'    => 'Udržitelná páska ECO+ 50',
                    'slug'    => 'udrzitelna-paska-eco-50',
                    'image'   => 'Udržitelné Pásky/eco+50.png',
                    'tagline' => 'Tenká recyklovaná páska pro standardní udržitelné balení.',
                    'params'  => array(
                        'Nosič / materiál' => 'Recyklovaná PP fólie',
                        'Tloušťka' => '50 µm',
                        'Typ lepidla' => 'Akrylové',
                        'Přilnavost (ocel)' => '3,0 N/25 mm',
                        'Teplotní odolnost' => '−5 až +60 °C',
                        'Pevnost v tahu' => '45 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'stroje'),
                ),
                array(
                    'name'    => 'Udržitelná páska ECO+ 80',
                    'slug'    => 'udrzitelna-paska-eco-80',
                    'image'   => 'Udržitelné Pásky/eco+80.png',
                    'tagline' => 'Silnější recyklovaná páska pro náročnější udržitelné balení.',
                    'params'  => array(
                        'Nosič / materiál' => 'Recyklovaná PP fólie',
                        'Tloušťka' => '80 µm',
                        'Typ lepidla' => 'Akrylové',
                        'Přilnavost (ocel)' => '3,4 N/25 mm',
                        'Teplotní odolnost' => '−5 až +60 °C',
                        'Pevnost v tahu' => '52 N/25 mm',
                    ),
                    'tags'    => array('ekologicke', 'stroje'),
                ),
            ),
        ),
    );
}

/**
 * Look up a single category by its slug segment (last URL part).
 *
 * @param string $slug_segment e.g. "papirove-pasky".
 * @return array|null
 */
function paskyonline_get_sortiment_category( $slug_segment ) {
    $slug_segment = trim( (string) $slug_segment, '/' );

    foreach ( paskyonline_get_sortiment_categories() as $category ) {
        if ( basename( $category['slug'] ) === $slug_segment ) {
            return $category;
        }
    }

    return null;
}

/**
 * Look up a single product (and its parent category) by the product slug.
 *
 * @param string $product_slug e.g. "papirova-paska-c690".
 * @return array{product: array, category: array}|null
 */
function paskyonline_get_sortiment_product( $product_slug ) {
    $product_slug = trim( (string) $product_slug, '/' );

    foreach ( paskyonline_get_sortiment_categories() as $category ) {
        if ( empty( $category['products'] ) ) {
            continue;
        }
        foreach ( $category['products'] as $product ) {
            if ( isset( $product['slug'] ) && $product['slug'] === $product_slug ) {
                return array( 'product' => $product, 'category' => $category );
            }
        }
    }

    return null;
}
