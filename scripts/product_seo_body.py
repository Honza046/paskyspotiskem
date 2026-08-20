#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Long-form SEO copy for product detail pages (Czech, B2B)."""

from __future__ import annotations

# Explicit paragraphs per product: (p1, p2). Verbatim copy from "Texty pásek.docx".
PRODUCT_SEO: dict[str, tuple[str, str]] = {
    "Udržitelná páska ECO+ 100": (
        "Maximální ekologický standard a čistá cirkulární ekonomika v praxi. Páska je vyrobena ze 100% regenerované "
        "BOPP fólie z čistého postindustriálního odpadu bez použití nového primárního granulátu. Vzhledem i "
        "pevností v tahu plnohodnotně nahrazuje konvenční pásky a poskytuje nekompromisní ochranu zásilek při "
        "přepravě.",
        "Dostupná s lepidlem Akryl i HOT MELT pro okamžitou přilnavost. Pásky dodáváme v neutrálním provedení "
        "pro každodenní expedici i s firemním potiskem na míru. Minimální odběr začíná již od 360 ks.",
    ),
    "Udržitelná páska ECO+ 80": (
        "Výrazné snížení spotřeby primárního granulátu při zachování stoprocentního balicího výkonu. Nosič je "
        "tvořen z 80 % postindustriálním regenerátem, díky čemuž představuje ideální volbu pro firmy, které "
        "aktivně naplňují své ESG cíle a chtějí výrazně omezit dopad na životní prostředí bez kompromisů v "
        "pevnosti spoje na kartonu.",
        "Dostupná s lepidlem Akryl i HOT MELT pro okamžitou přilnavost. Pásky dodáváme v neutrálním provedení "
        "pro každodenní expedici i s firemním potiskem na míru. Minimální odběr začíná již od 360 ks.",
    ),
    "Udržitelná páska ECO+ 50": (
        "Optimální rovnováha mezi udržitelným balením a efektivními náklady bez jakékoliv „ekologické přirážky“. "
        "Nosič obsahuje 50 % postindustriálního regenerátu z vlastní výroby fólií, který je okamžitě vracen zpět "
        "do oběhu. Páska si zachovává identické mechanické vlastnosti, pevnost v tahu i spolehlivost jako "
        "standardní BOPP pásky z primárních plastů.",
        "Dostupná s lepidlem Akryl i HOT MELT pro okamžitou přilnavost. Pásky dodáváme v neutrálním provedení "
        "pro každodenní expedici i s firemním potiskem na míru. Minimální odběr začíná již od 360 ks.",
    ),
    "Udržitelná páska POLY+": (
        "Plnohodnotná a stoprocentně recyklovatelná alternativa k ekologicky zatěžujícím PVC páskám, která "
        "vyniká reprezentativním matným vzhledem. Robustní 35µm matná BOPP fólie v kombinaci se zesíleným "
        "akrylovým lepidlem zajišťuje mimořádnou odolnost proti přetržení a garantuje pevné uzavření i těžkých "
        "kartonových zásilek. Představuje ideální cestu pro firmy, které chtějí opustit PVC materiály bez "
        "kompromisů v estetice a mechanické pevnosti.",
        "Díky matné antireflexní úpravě nabízí páska špičkový kontrast pro čitelnost grafiky a dodává každému "
        "balíku prémiový charakter. K dispozici je ve standardním provedení i v tiché úpravě Low Noise pro "
        "klidný expediční provoz. Pásky dodáváme v neutrálním provedení i s vysokorychlostním firemním potiskem "
        "na míru, který perfektně zviditelní vaši značku na každé zásilce.",
    ),
    "Udržitelná páska Airtape+": (
        "Maximální efektivita skladování i expedice v ultratenkém provedení s ohledem na redukci plastového "
        "odpadu. Inovativní polypropylenový nosič s tloušťkou pouhých 19 µm výrazně snižuje celkovou spotřebu "
        "plastů i váhu balených zásilek, přičemž si zachovává mimořádnou odolnost proti roztržení. Díky tenčímu "
        "profilu fólie pojme role se standardním průměrem podstatně více metrů, což šetří skladovací plochu a "
        "omezuje prostoje způsobené častou výměnou rolí na pracovišti.",
        "Páska je osazena vysoce kvalitním lepidlem Akryl Low Noise, které zajišťuje tiché odvíjení pro klidný "
        "provoz skladu a vynikající odolnost vůči UV záření i stárnutí. Dodáváme ji v neutrálním provedení pro "
        "rychlé a ekologicky optimalizované balení i s firemním potiskem na míru, který propojí vaši značku s "
        "tématem materiálové úspory.",
    ),
    "Udržitelná páska LOOPP": (
        "Prémiové ekologické řešení uzavírající koloběh plastových obalů na spotřebitelském trhu. Nosič je "
        "vyroben z polymerů chemicky recyklovaného spotřebitelského plastu s mezinárodní certifikací ISCC PLUS "
        "(na bázi hmotnostní bilance). Páska vykazuje naprosto identické mechanické vlastnosti, tahovou pevnost "
        "i špičkovou přilnavost jako pásky z primárních surovin, ale s výrazně nižší fosilní stopou.",
        "Kvalitní akrylové lepidlo na vodní bázi poskytuje stabilní lepivost, UV odolnost a možnost tiché "
        "varianty Low Noise. Pásky dodáváme v neutrálním provedení pro univerzální expediční potřeby i s "
        "reprezentativním firemním potiskem na míru, který transparentně demonstruje podporu cirkulární "
        "ekonomiky na každé odeslané zásilce.",
    ),
    "Udržitelná páska NOPP": (
        "Průlomová bio-cirkulární balicí páska s mezinárodní certifikací ISCC PLUS, která nahrazuje fosilní "
        "plasty obnovitelnými surovinami. Nosič je vyroben z vedlejšího produktu při výrobě celulózy (dřevní "
        "odpad / borovicový olej), aniž by ztratil cokoliv ze špičkové mechanické pevnosti standardní BOPP "
        "pásky. Výkonné akrylové lepidlo na vodní bázi nevysychá, poskytuje vysokou UV odolnost a zajišťuje "
        "spolehlivé uzavření zásilek při dlouhodobém skladování.",
        "Ideální řešení pro firmy, které aktivně snižují svou závislost na primární ropě a chtějí reálně plnit "
        "své ESG cíle. K dispozici je ve standardním provedení i v tiché úpravě Low Noise pro klidnější provoz "
        "na balicích pracovištích. Pásky dodáváme v neutrálním provedení i s individuálním firemním potiskem na "
        "míru, který transparentně demonstruje váš udržitelný přístup přímo na obalu.",
    ),
    "Udržitelná páska NOPP+": (
        "Nejvyšší úroveň bio-cirkulární udržitelnosti na trhu. Varianta NOPP+ disponuje certifikací ISCC PLUS "
        "pro nosnou fólii i pro samotné lepidlo, čímž dosahuje maximálního možného snížení uhlíkové stopy. "
        "Speciálně formulované akrylové lepidlo Adhesive G1 navíc poskytuje zesílenou okamžitou přilnavost "
        "(tack) a spolehlivě drží i na drsnějších površích, prašných materiálech či savých recyklovaných "
        "kartonech.",
        "Špičková volba pro prémiový branding a transparentní ESG reporting bez jakýchkoliv kompromisů v "
        "balicí rychlosti či pevnosti spoje. Páska je dostupná také v tiché variantě Low Noise. Dodáváme ji v "
        "neutrálním provedení i s reprezentativním firemním potiskem na míru, který udělá z každé zásilky "
        "vlajkovou loď vaší ekologické odpovědnosti.",
    ),
    "BOPP páska Akryl": (
        "Ideální volba pro spolehlivé uzavírání kartonových zásilek a dlouhodobé skladování bez rizika "
        "odlepování. Akrylové lepidlo na bázi vodní disperze vyniká mimořádnou UV stabilitou a stálostí – v "
        "čase nevysychá, nežloutne a udržuje si plnou lepivost i po měsících ve skladu. Navíc neobsahuje "
        "agresivní chemická rozpouštědla, takže je zcela bez zápachu a maximálně šetrné k pracovnímu prostředí.",
        "Podle typu vašeho provozu můžete volit mezi standardním provedením a tichou úpravou Low Noise, která "
        "výrazně snižuje hlukovou zátěž na balicích linkách a zvyšuje komfort zaměstnanců. Pásky dodáváme v "
        "neutrálním provedení pro univerzální použití i s individuálním firemním potiskem na míru (logo, claim, "
        "bezpečnostní prvky) již od minimálního odběru 360 ks.",
    ),
    "BOPP páska HOT MELT": (
        "Průmyslový standard a nejčastější volba pro dynamické provozy, e-commerce expedice i automatizované "
        "balicí linky. Syntetické kaučukové lepidlo vyniká okamžitou počáteční přilnavostí a vytváří pevný spoj "
        "ihned po aplikaci.",
        "Díky snadnému a plynulému odvíjení výrazně zrychluje proces balení a snižuje fyzickou námahu personálu "
        "při ruční aplikaci. Pásky dodáváme v neutrálním provedení pro každodenní expediční potřeby i s vysoce "
        "kvalitním firemním potiskem na míru. Minimální odběr začíná již od 504 ks.",
    ),
    "BOPP páska TACK+": (
        "Prémiová volba pro náročné expediční podmínky, kde standardní pásky selhávají. Vylepšená formule "
        "lepidla na bázi syntetického kaučuku nabízí o +20 % vyšší počáteční lepivost (tack) a extrémní sílu "
        "spoje ihned po přitlačení. Páska bezpečně uzavře těžké balíky a spolehlivě drží i na problematických "
        "podkladech, jako jsou vysoce porézní recyklované krabice, hrubé povrchy nebo prašnější skladové "
        "prostředí.",
        "I přes maximální lepicí sílu si páska zachovává plynulé a snadné odvíjení, takže nebrzdí personál při "
        "ručním balení a skvěle funguje i na automatických balicích linkách. Dodáváme ji v neutrálním provedení "
        "pro univerzální použití i s individuálním firemním potiskem na míru (flexotisk / rototisk), který "
        "promění každou těžkou zásilku v bezpečný a reprezentativní balík. Minimální odběr je od 504 ks.",
    ),
    "BOPP páska EXTRA GLUE+": (
        "Maximální lepicí síla spojená s dlouhou životností akrylu. Díky zesílené vrstvě lepidla (+33 %) nabízí "
        "páska výrazně vyšší okamžitou přilnavost než běžný akryl a bezpečně fixuje i těžké zásilky na "
        "problematických površích – jako jsou hrubé, nekvalitní či recyklované kartony a prašnější prostředí. "
        "Ekologická vodní disperze nevysychá, nežloutne a skvěle odolává stárnutí i UV záření.",
        "Ideální volba pro provozy, které vyžadují nekompromisní pevnost spoje, ale zároveň chtějí zachovat "
        "výhody akrylové technologie, včetně šetrnosti k pracovnímu prostředí a možnosti tichého odvíjení. "
        "Pásky dodáváme v neutrálním provedení pro univerzální expediční použití i s reprezentativním firemním "
        "potiskem na míru (logo, bezpečnostní páska) již od minimálního odběru 360 ks.",
    ),
    "BOPP páska Evergreen": (
        "Špičkové řešení navržené pro extrémní teplotní podmínky, chladné provozy a náročné povrchy. Speciálně "
        "vyvinuté vysoce výkonné akrylové lepidlo na vodní bázi plnohodnotně nahrazuje přírodní kaučuk (Solvent) "
        "a umožňuje bezproblémovou aplikaci už od 0 °C. Po nalepení spoj spolehlivě odolává mrazu až do -20 °C, "
        "nevysychá a perfektně drží i na hrubších, méně kvalitních nebo recyklovaných kartonech.",
        "Páska nabízí okamžitou přilnavost, vysokou UV stabilitu při dlouhodobém skladování a neobsahuje žádná "
        "chemická rozpouštědla. Dodáváme ji v neutrálním provedení pro každodenní expediční i chladírenské "
        "provozy a s individuálním firemním potiskem na míru (např. bezpečnostní motivy či logo). Minimální "
        "odběr činí 1 paletu (2 376 ks).",
    ),
    "BOPP páska ecoEVERGREEN 50%": (
        "Ideální rovnováha mezi udržitelným balením a špičkovým výkonem v náročných teplotních podmínkách. "
        "Nosič obsahuje 50 % PIR recyklátu z použitého kuchyňského oleje (27 % celkového recyklovaného obsahu). "
        "Páska vyniká mimořádnou odolností v chladu – bez problémů ji aplikujete již od 0 °C a po nalepení "
        "garantuje stoprocentní pevnost spoje v mrazu až do -20 °C, a to i na prašných či méně kvalitních "
        "kartonech.",
        "Cenově efektivní krok k ekologičtější expedici a spolehlivému balení pro celoroční i chladírenský "
        "provoz. Pásky nabízíme v neutrálním provedení i s reprezentativním firemním potiskem na míru, který "
        "podtrhne zodpovědný přístup vaší značky. Minimální odběr začíná na 1 paletě (2 376 ks).",
    ),
    "BOPP páska ecoEVERGREEN 100%": (
        "Maximálně udržitelná volba pro provozy, které nechtějí dělat kompromisy mezi ekologií a extrémní "
        "funkčností. Nosič je vyroben ze 100% PIR recyklátu na bázi použitého kuchyňského oleje (celkově 54 % "
        "recyklovaného podílu). Speciální vysoce výkonné akrylové lepidlo spolehlivě aplikujete i v chladných "
        "skladech při teplotách blížících se 0 °C, přičemž po nalepení páska bezpečně drží v mrazu až do -20 °C. "
        "Perfektně přilne i k náročnějším recyklovaným kartonům.",
        "Představuje plnohodnotnou, zelenou náhradu lepidel z přírodního kaučuku bez nutnosti měnit balicí "
        "procesy. Pásky dodáváme v neutrálním provedení i s individuálním firemním potiskem na míru, který "
        "transparentně komunikuje vaše ESG cíle zákazníkům přímo na zásilce. Minimální odběr je 1 paleta "
        "(2 376 ks).",
    ),
    "BOPET páska ECO HIT19": (
        "Inovativní ekologické řešení s evropským patentem, které posouvá udržitelnost i efektivitu expedice na "
        "novou úroveň. Polyesterový nosič (BOPET) s tloušťkou pouhých 19 µm obsahuje minimálně 85 % "
        "recyklovaného PET odpadu z plastových lahví, přičemž nabízí výrazně vyšší pevnost v tahu a odolnost "
        "proti přetržení než běžné BOPP fólie. Díky tenčímu profilu pojme standardní role dvojnásobný návin (až "
        "132 m), což znamená méně častou výměnu rolí na balicích pracovištích a výraznou úsporu skladovacího "
        "místa.",
        "Výkonné lepidlo Hot Melt zaručuje okamžitou přilnavost a spolehlivou fixaci na kartonu bez deformace či "
        "natahování pásky. Dodáváme ji v neutrálním provedení i s prémiovým firemním potiskem na míru, který "
        "transparentně komunikuje vaše ESG cíle zákazníkům přímo na zásilce. Minimální odběr je od 1 080 ks.",
    ),
    "BOPET páska ECO HIT23": (
        "Zesílená polyesterová páska pro náročné expediční úkoly, těžké balíky a maximální zabezpečení zásilek. "
        "Nosič o síle 23 µm obsahuje minimálně 85 % recyklovaného PET odpadu z plastových lahví a poskytuje "
        "mimořádnou mechanickou odolnost – páska se při odvíjení ani tahu nenatahuje a prakticky ji nelze "
        "roztrhnout. Spojuje tak nekompromisní pevnost s reálnou podporou cirkulární ekonomiky a plněním ESG "
        "cílů.",
        "Díky vysoké pevnosti polyesteru a okamžitému nástupu lepivosti Hot Melt lepidla je ideální volbou pro "
        "automatické linky i těžké kartonové obaly. Pásky nabízíme v neutrálním provedení pro každodenní "
        "průmyslové použití i s reprezentativním firemním potiskem na míru, který podtrhne kvalitu a "
        "udržitelnost vaší značky. Minimální odběr je od 1 080 ks.",
    ),
    "BOPET páska AIT23": (
        "Kombinace extrémní mechanické odolnosti polyesteru a dlouhé životnosti akrylového lepidla. Nosič BOPET "
        "o síle 23 µm vyniká mimořádnou pevností v tahu a odolností proti roztržení – při aplikaci se "
        "nenatahuje, nedeformuje a poskytuje zásilkám maximální fixaci. Vysoce stabilní akrylové lepidlo na "
        "vodní bázi skvěle snáší UV zatížení, nežloutne a udržuje si spolehlivou lepivost i při dlouhodobém "
        "skladování.",
        "Díky tenkému profilu polyesterového nosiče nabízí role vyšší návin metrů na standardním průměru, což "
        "šetří skladovací místo a snižuje frekvenci výměny rolí v provozu. Pásky dodáváme v neutrálním provedení "
        "i s prémiovým firemním potiskem na míru.",
    ),
    "BOPET páska HIT17": (
        "Maximální efektivita expedice v ultratenkém, ale vysoce pevném provedení. Polyesterový nosič (BOPET) o "
        "tloušťce pouhých 17 µm překonává běžné BOPP pásky v pevnosti v tahu i odolnosti proti roztržení – při "
        "odvíjení se nenatahuje a nedeformuje. Spolu s lepidlem Hot Melt vytváří okamžitý, silný spoj, který "
        "spolehlivě drží i na náročnějších podkladech, recyklovaných kartonech nebo v mírně prašném prostředí "
        "skladu.",
        "Díky tenkému profilu pojme role se standardním průměrem dvojnásobný návin metrů, což přináší méně "
        "častou výměnu rolí na balicích linkách, vyšší plynulost práce a výraznou úsporu skladovacího místa. "
        "Pásky dodáváme v neutrálním provedení pro rychlé průmyslové balení i s kvalitním firemním potiskem na "
        "míru, který promění každou zásilku v profesionální vizitku vaší firmy.",
    ),
    "BOPET páska ATE23": (
        "Špičkové bezpečnostní řešení pro ochranu hodnotného zboží a okamžitou detekci neoprávněného vniknutí "
        "do zásilky. Polyesterový nosič (BOPET) se speciálně vrstveným akrylovým lepidlem – při jakémkoliv "
        "pokusu o odlepení zanechá na povrchu kartonu nesmazatelnou stopu (VOID / FRAUD / OPEN), kterou nelze "
        "vrátit zpět ani zamaskovat. Na pohled přitom působí jako standardní balicí páska.",
        "Kromě ochrany proti krádežím nabízí extrémní mechanickou pevnost polyesteru – páska se netrhá, "
        "nevytahuje a drží tvar i při hrubé manipulaci během přepravy. Dodáváme ji v neutrálním provedení i s "
        "individuálním firemním potiskem na míru, který ještě více posílí bezpečnost a unikátní identifikaci "
        "vašich prémiových zásilek.",
    ),
    "Papírová páska KH80": (
        "Exkluzivní a stoprocentně ekologické řešení s hladkým kraftovým vzhledem pro náročné e-shopy i B2B "
        "expedice. Robustní nosič ze 100% recyklovaného papíru s FSC certifikací o gramáži 80 g/m² vyniká "
        "vysokou pevností v tahu a tvarovou stálostí bez průtahu. Umožňuje plně udržitelné balení s certifikací "
        "recyklace PAP 22, kdy zákazník odkládá celou zásilku přímo do tříděného papírového odpadu bez nutnosti "
        "odstraňování pásky.",
        "Hot melt se špičkovou lepicí silou zaručuje okamžité a trvalé uzavření kartonů ihned po aplikaci. "
        "Pásky dodáváme v neutrálním provedení pro čistý přírodní vizuál i s reprezentativním firemním potiskem "
        "na míru, který promění každý balík v dokonalý unboxing zážitek bez použití plastových materiálů.",
    ),
    "Papírová páska C660": (
        "Ekologické a stoprocentně recyklovatelné řešení pro moderní e-shopy a značky s důrazem na udržitelnost "
        "i prémiový unboxing. Nosič z krepového papíru s certifikací FSC dodává zásilkám čistý přírodní vzhled "
        "a díky své pružnosti se skvěle přizpůsobí hranám kartonu. Zásadní výhodou je plná recyklovatelnost – "
        "koncový zákazník může celou krabici vyhodit přímo do tříděného papíru bez nutnosti pracného strhávání "
        "pásky.",
        "Hot melt zaručuje okamžitou a silnou přilnavost ke kartonu, což zrychluje proces balení při ruční i "
        "strojové aplikaci. Pásky dodáváme v hnědém provedení i s individuálním firemním potiskem na míru (až 4 "
        "barvy), který podtrhne ekologickou image vaší značky ihned při převzetí balíku.",
    ),
    "Papírová páska C680": (
        "Ideální volba pro plně recyklovatelné a vysoce estetické balení s důrazem na pevnost a spolehlivost. "
        "Vyniká optimalizovaným tenkým profilem (110 µm) a vysokou pevností v tahu (35 N/cm), což zaručuje "
        "bezpečné uzavření zásilek bez rizika přetržení při ruční i strojové aplikaci. Pružný nosič z krepového "
        "papíru s certifikací FSC umožňuje koncovým zákazníkům vyhodit celou krabici rovnou do tříděného papíru "
        "bez nutnosti pracného strhávání pásky.",
        "Hot melt zajišťuje okamžitou a silnou přilnavost ke kartonu ihned po přitlačení. Pásky dodáváme v "
        "hnědé i bílé barvě, v neutrálním provedení pro každodenní expediční provoz i s individuálním firemním "
        "potiskem na míru (až 4 barvy), který promění každý odeslaný balík v prémiový a stoprocentně ekologický "
        "unboxing zážitek.",
    ),
    "Papírová páska C680 RT": (
        "Nejvyšší úroveň mechanické pevnosti mezi ekologickými obaly pro ty nejnáročnější a nejtěžší zásilky. "
        "Nosič z krepového papíru s certifikací FSC je zpevněn křížovou mřížkovou výztuží ze skelných vláken, "
        "která zaručuje extrémní pevnost v tahu až 60 N/cm a zabraňuje prasknutí či roztržení pásky v podélném i "
        "příčném směru. Páska poskytuje maximální zabezpečení nákladu při přepravě a zároveň umožňuje snadnou "
        "recyklaci celého kartonu.",
        "Hot melt zaručuje okamžitou a silnou přilnavost ke kartonu, což zrychluje proces balení při ruční i "
        "strojové aplikaci. Pásky dodáváme v hnědém provedení i s individuálním firemním potiskem na míru (až 4 "
        "barvy), který plní funkci spolehlivé bezpečnostní plomby i prémiového brandingu.",
    ),
    "Papírová páska C680R": (
        "Vysoce spolehlivé řešení pro bezpečné balení těžších kartonů a objemných balíků. Nosič z krepového "
        "papíru s certifikací FSC je vyztužen podélnými skelnými vlákny, která zvyšují pevnost v tahu a "
        "efektivně brání přetržení pásky při aplikaci i manipulaci během přepravy. Umožňuje plně ekologické "
        "balení, kdy zásilka putuje do tříděného papírového odpadu jako jeden celek bez nutnosti odstraňování "
        "pásky.",
        "Hot melt zajišťuje okamžitou a silnou přilnavost ke kartonu ihned po přitlačení. Pásky dodáváme v "
        "hnědé i bílé barvě, v neutrálním provedení pro každodenní expediční provoz i s individuálním firemním "
        "potiskem na míru (až 4 barvy), který promění každý odeslaný balík v prémiový a stoprocentně ekologický "
        "unboxing zážitek.",
    ),
    "Papírová páska C690": (
        "Robustní řešení s vysokou gramáží pro nejnáročnější aplikace a těžké kartonové zásilky. Zesílený "
        "nosič z krepového papíru s certifikací FSC vyniká vysokou odolností proti prodření i mechanickému "
        "poškození a poskytuje špičkovou pevnost v tahu. Páska zajišťuje stoprocentně ekologické balení, které "
        "umožňuje koncovým příjemcům recyklovat bez odstraňování lepicí pásky.",
        "Vysokovýkonné lepidlo Hot melt se pyšní extrémní přilnavostí k oceli 7,0 N/cm – nejvyšší ve své třídě "
        "– a okamžitě přilne i k prašným či porézním recyklovaným kartonům. Pásky dodáváme v neutrálním "
        "provedení pro zátěžové průmyslové provozy i s individuálním firemním potiskem na míru (až 4 barvy), "
        "který propůjčí každému balíku reprezentativní a udržitelný vzhled.",
    ),
    "Papírová páska C780": (
        "Prémiové ekologické řešení spojující přírodní krepový papír s certifikací FSC a vysoce výkonné lepidlo "
        "z přírodního kaučuku (Solvent). Tato kombinace vyniká špičkovou mechanickou odolností s pevností v "
        "tahu a bezproblémovým fungováním v širokém spektru teplot i náročnějších podmínkách. Páska umožňuje "
        "plně udržitelný oběh obalů – celou krabici lze po doručení vyhodit rovnou do tříděného papírového "
        "odpadu bez nutnosti odlepování.",
        "Lepidlo Solvent vytváří trvanlivý a nestárnoucí spoj, který si zachovává stálou lepicí sílu i při "
        "dlouhodobém skladování zásilek. Pásky nabízíme v neutrálním provedení pro každodenní expediční provoz "
        "i s individuálním firemním potiskem na míru (až 4 barvy), který promění každý balík v reprezentativní "
        "a stoprocentně recyklovatelnou vizitku vaší značky.",
    ),
    "Papírová páska KS165": (
        "Nekompromisní zátěžové řešení pro nejtěžší průmyslové balení, fixaci na paletách a svazkování, které "
        "plnohodnotně nahrazuje plastové či vázací pásky. Extrémně silný nosič z hladkého kraftového papíru s "
        "FSC certifikací o bezkonkurenční gramáži 165 g/m² poskytuje enormní pevnost v tahu až 150 N/cm. Páska "
        "spolehlivě odolává vysokému mechanickému namáhání i protržení a umožňuje stoprocentně udržitelnou "
        "likvidaci obalu spolu s kartonem.",
        "Hot melt s vysokou přilnavostí k oceli zajišťuje bleskový a trvalý spoj ihned po kontaktu s povrchem "
        "krabice. Pásky dodáváme v neutrálním provedení pro zátěžové expediční aplikace i s reprezentativním "
        "firemním potiskem na míru, který promění i robustní průmyslové balení v bezpečný a ekologicky čistý "
        "obal vaší značky.",
    ),
    "BOPP páska Tamper Evident": (
        "Bezpečnostní Tamper Evident páska s potiskem chrání zásilku před neoprávněným otevřením. "
        "Při odlepení zanechá na kartonu upozornění (VOID / OPEN), které prakticky nelze odstranit. "
        "Hodí se pro e-shopy, farmaceutiku, elektroniku a logistiku s vyšším rizikem manipulace.",
        "Na rozdíl od běžné BOPP pásky není cílem jen uzavření kartonu, ale viditelný důkaz porušení. "
        "Dodáváme ji s firemním potiskem a v barevných variantách podle potřeby identifikace zásilek.",
    ),
}


CATEGORY_SEO_FALLBACK: dict[str, tuple[str, str]] = {
    "bopp-pasky": (
        "BOPP pásky s potiskem jsou průmyslový standard pro uzavírání kartonů ve výrobě, skladech a e-shopech. "
        "Biaxiálně orientovaný polypropylen nabízí výborný poměr pevnosti a ceny a skvěle se potiskuje logem.",
        "Vyberte HOT MELT pro rychlou lepivost v chladu, Akryl pro tiché odvíjení a UV stabilitu, "
        "nebo speciální varianty TACK+ / EXTRA GLUE+ / Tamper Evident podle aplikace. Minimální odběry a potisk "
        "konzultujeme individuálně: typicky stovky kusů podle typu lepidla.",
    ),
    "udrzitelne-pasky": (
        "Udržitelné pásky s potiskem od ALFA IN pokrývají regenerovaný BOPP (ECO+), bio-cirkulární NOPP/NOPP+, "
        "cirkulární LOOPP i matnou náhradu PVC (POLY+). Cílem je snížit ekologickou stopu balení bez ztráty výkonu.",
        "Porovnejte podíly regenerátu, certifikace ISCC PLUS a typ lepidla (Akryl / Low noise / HOT MELT). "
        "Rádi připravíme potisk loga a vzorek zdarma pro ověření v reálném provozu.",
    ),
    "papirove-pasky": (
        "Papírové pásky s potiskem umožňují plně recyklovatelné balení: páska putuje do sběru spolu s kartonem. "
        "Kraftový vzhled působí přírodně a prémiově a hodí se pro e-shopy i značky s důrazem na udržitelnost.",
        "Volte gramáž a pevnost podle hmotnosti zásilek (např. C680 vs KS165). Potisk firemním logem "
        "a FSC nosič patří k nejčastějším požadavkům B2B zákazníků.",
    ),
    "bopet-pasky": (
        "BOPET pásky s potiskem nabízejí polyesterovou pevnost a odolnost pro náročné průmyslové aplikace. "
        "Oproti BOPP lépe vzdorují roztržení a teplotním výkyvům.",
        "Řada ECO HIT přidává regenerovaný obsah z PET lahví. Technické varianty AIT/ATE/HIT volíte podle "
        "tloušťky fólie a lepidla: rádi doporučíme podle vaší linky.",
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
