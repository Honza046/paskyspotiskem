#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate sortiment product data (PHP) + static preview pages."""
import html, unicodedata, urllib.parse, glob, os

def esc(s): return html.escape(s, quote=True)
def url(p): return '/' + urllib.parse.quote(p)

def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode('ascii')
    s = s.lower()
    out=[]
    for ch in s:
        if ch.isalnum(): out.append(ch)
        elif ch in ' -_/+': out.append('-')
    slug='-'.join(x for x in ''.join(out).split('-') if x)
    return slug

# ---------------------------------------------------------------------------
# Category meta (cover, texts, properties, applications)
# ---------------------------------------------------------------------------
CATS = [
 {"title":"Udržitelné pásky","cat":"udrzitelne-pasky","cover":"Udržitelné Pásky/eco+50.jpg",
  "description":"Inovativní obalová řešení vyrobená z recyklovaných materiálů s ohledem na minimální ekologickou stopu a podporu cirkulární ekonomiky.",
  "intro":"Udržitelná řada pásek je vyrobena z recyklovaných materiálů a navržena tak, aby minimalizovala dopad na životní prostředí. Pomáhá firmám plnit ESG cíle a budovat obraz zodpovědné značky bez kompromisů ve výkonu.",
  "properties":[("Recyklovaný obsah","Materiály s vysokým podílem recyklátu."),("Nižší uhlíková stopa","Šetrnější výroba a cirkulární přístup."),("Bez kompromisů","Ekologie při zachování spolehlivého lepení.")],
  "apps":["Firmy s ESG a udržitelnými cíli","Zelené balení pro e-shopy","Cirkulární obalové procesy","Budování zodpovědné značky"]},
 {"title":"BOPP pásky","cat":"bopp-pasky","cover":"BOPP Tapes/BOPP_Cover.webp",
  "description":"Nejrozšířenější průmyslové balicí pásky z biaxiálně orientovaného polypropylenu. Vynikají skvělou pevností v tahu a dlouhou životností.",
  "intro":"BOPP pásky jsou standardem pro každodenní balení ve výrobě, logistice i e-commerce. Fólie z biaxiálně orientovaného polypropylenu nabízí vynikající poměr ceny a výkonu, dostupnost v akrylovém i hot melt provedení a širokou škálu šířek a barev.",
  "properties":[("Vysoká pevnost v tahu","Odolná fólie, která se při balení nepřetrhne ani pod napětím."),("ACRYL i HOT MELT","Volba lepidla podle prostředí, tiché odvíjení, nebo rychlé přilnutí za chladu."),("Dlouhá životnost","Odolnost proti UV a stárnutí pro dlouhodobé skladování.")],
  "apps":["Standardní uzavírání kartonů","Automatické balicí stroje","Expedice a skladová logistika","Potisk firemním logem a informacemi"]},
 {"title":"BOPET pásky","cat":"bopet-pasky","cover":"BOPET Tapes/BOPET_Cover.webp",
  "description":"Prémiové polyesterové pásky s extrémní odolností proti roztržení, chemikáliím a teplotním výkyvům. Navržené pro nejnáročnější průmyslové aplikace.",
  "intro":"BOPET pásky na bázi polyesterové fólie jsou určeny tam, kde běžné pásky nestačí. Zvládají vysoké teploty, agresivní chemické prostředí i mechanické namáhání a udrží si své vlastnosti i v extrémních podmínkách.",
  "properties":[("Teplotní odolnost","Stabilní výkon při vysokých i nízkých teplotách."),("Chemická odolnost","Odolává rozpouštědlům, olejům a agresivnímu prostředí."),("Odolnost proti roztržení","Pevná polyesterová fólie s minimální tažností.")],
  "apps":["Náročné průmyslové provozy","Maskování při práškovém lakování","Fixace v prostředí s vysokými teplotami","Elektrotechnika a specializovaná výroba"]},
 {"title":"Papírové pásky","cat":"papirove-pasky","cover":"Papírové Pásky/Papírovácover-nobg.png",
  "description":"Ekologické řešení pro bezpečné balení s vysokou lepivostí. Ideální pro plně recyklovatelné kartonové obaly a čistý korporátní design.",
  "intro":"Papírové lepicí pásky spojují spolehlivé lepení s maximální ekologickou šetrností. Díky papírovému nosiči jsou plně recyklovatelné společně s kartonem a představují elegantní, čistě vypadající řešení pro firmy, které dbají na udržitelnost i vizuální dojem zásilek.",
  "properties":[("Plná recyklovatelnost","Páska i karton putují do jednoho kontejneru – bez nutnosti oddělovat materiály."),("Vysoká lepivost","Spolehlivé přilnutí i na recyklovaný karton a členité povrchy."),("Čistý design","Matný papírový povrch působí prémiově a lze jej snadno potisknout logem.")],
  "apps":["E-shopy s důrazem na udržitelné balení","Uzavírání kartonových krabic a obalů","Firemní branding přímo na zásilce","Ruční i poloautomatické balení"]},
 {"title":"Odstranitelné pásky","cat":"odstranitelne-pasky","cover":"Odstranitelné Pásky/removable cover.webp",
  "description":"Pásky se speciálním složením lepidla, které nezanechává žádné stopy po odlepení. Ideální pro dočasné značení, ochranu citlivých povrchů nebo logistické procesy.",
  "intro":"Odstranitelné pásky používají speciální lepidlo, které pevně drží, ale po odlepení nezanechává žádné zbytky ani poškození povrchu. Jsou ideální pro dočasné aplikace a ochranu citlivých materiálů.",
  "properties":[("Beze stop","Po odlepení nezůstává lepidlo ani reziduum."),("Šetrné k povrchu","Nepoškodí lak, sklo ani citlivé materiály."),("Spolehlivá drživost","Drží po celou dobu potřebné aplikace.")],
  "apps":["Dočasné značení a etikety","Ochrana citlivých povrchů","Logistické a výrobní procesy","Fixace, která se musí opět odstranit"]},
 {"title":"Vyztužené pásky","cat":"vyztuzene-pasky","cover":"Vyztužené Pásky/Reinforcedcover.webp",
  "description":"Pásky zpevněné podélnými nebo křížovými skelnými vlákny. Nabízejí maximální pevnost při fixaci těžkých nákladů, palet a nadrozměrných balíků.",
  "intro":"Vyztužené (filament) pásky obsahují skelná vlákna vedená podélně nebo křížem, která zásadně zvyšují pevnost v tahu. Jsou určené pro fixaci těžkých a nadrozměrných zásilek, kde je potřeba absolutní jistota.",
  "properties":[("Skelná vlákna","Podélné nebo křížové vyztužení pro maximální pevnost."),("Nosnost","Spolehlivá fixace těžkých břemen a palet."),("Odolnost proti přetržení","Vydrží i vysoké tahové zatížení.")],
  "apps":["Fixace těžkých a nadrozměrných balíků","Zajištění zboží na paletách","Svazování trubek, profilů a tyčí","Náročná přeprava a export"]},
 {"title":"MOPP pásky","cat":"mopp-pasky","cover":"MOPP Pásky/moppcvoer.webp",
  "description":"Monoaxiálně orientované pásky s extrémní pevností v jednom směru a nulovou elasticitou. Speciálně určené pro fixaci elektrospotřebičů, komponentů nebo stahování palet.",
  "intro":"MOPP pásky mají monoaxiálně orientovanou fólii s extrémní pevností v podélném směru a prakticky nulovou tažností. Nahrazují vyztužené pásky tam, kde je potřeba pevná fixace bez skelných vláken.",
  "properties":[("Extrémní pevnost","Vysoká pevnost v tahu v jednom směru."),("Nulová elasticita","Fixace se nepovolí ani při zatížení."),("Bez skelných vláken","Čistá fixace bez uvolňujících se vláken.")],
  "apps":["Fixace dveří elektrospotřebičů","Zajištění komponentů během přepravy","Stahování a fixace palet","Svazování bez skelných vláken"]},
 {"title":"Textilní lepicí pásky","cat":"textilni-pasky","cover":"Textilní Lepící Pásky/Duct_Cover-2.webp",
  "description":"Vysoce pevné a univerzální pásky zpevněné textilní mřížkou. Perfektně drží na drsném povrchu, snadno se trhají rukou a jsou ideální pro rychlé opravy i svazování.",
  "intro":"Textilní (duct) pásky jsou nepostradatelným univerzálem. Textilní výztuž jim dodává vysokou pevnost a zároveň umožňuje snadné odtržení rukou bez nůžek. Skvěle drží i na hrubých a nerovných površích.",
  "properties":[("Textilní výztuž","Vysoká pevnost a odolnost proti protržení."),("Trhání rukou","Rychlá práce bez nutnosti nářadí."),("Přilnavost na drsný povrch","Drží na kovu, dřevě, betonu i plastu.")],
  "apps":["Rychlé opravy a provizorní spoje","Svazování a fixace předmětů","Zpevnění balíků a obalů","Údržba, montáže a řemeslo"]},
 {"title":"Malířské pásky","cat":"malirske-pasky","cover":"Malířské Pásky/malířskácover.webp",
  "description":"Krepové papírové pásky navržené pro přesné zakrývání při malování a lakování. Chrání hrany před protečením barvy a po dokončení práce se čistě odlepí.",
  "intro":"Malířské krepové pásky zajišťují ostré a čisté hrany při malování a lakování. Papírový krepový nosič se dobře přizpůsobí povrchu, snadno se trhá a po dokončení práce se odlepí bez zbytků lepidla.",
  "properties":[("Ostré hrany","Zabraňuje protečení barvy pod pásku."),("Čisté odlepení","Po práci nezanechává lepidlo ani stopy."),("Snadná aplikace","Krep se přizpůsobí tvaru a snadno se trhá.")],
  "apps":["Malování a lakování interiérů","Zakrývání hran a přechodů","Lakovny a autolakovny","Kutilské a řemeslné práce"]},
]

# ---------------------------------------------------------------------------
# Products: name, image, tagline, params (Nosič, Tloušťka, Lepidlo, Přilnavost, Teplota, Pevnost)
# ---------------------------------------------------------------------------
def P(name, image, tagline, nosic, tl, lep, pril, temp, pev):
    return {"name":name,"image":image,"tagline":tagline,
            "params":{"Nosič / materiál":nosic,"Tloušťka":tl,"Typ lepidla":lep,
                      "Přilnavost (ocel)":pril,"Teplotní odolnost":temp,"Pevnost v tahu":pev}}

PRODUCTS = {
 "papirove-pasky":[
   P("Papírová páska KH80","Papírové Pásky/KH80.jpg","Silná papírová páska s hot melt lepidlem pro spolehlivé uzavírání kartonů.","Papírový nosič (kraft)","120 µm","Hot melt (syntetický kaučuk)","4,5 N/25 mm","−10 až +60 °C","55 N/25 mm"),
   P("Papírová páska KS165","Papírové Pásky/KS165.jpg","Extra pevná papírová páska s kaučukovým lepidlem pro náročné balení.","Papírový nosič (kraft)","150 µm","Kaučukové (solvent)","5,5 N/25 mm","−20 až +70 °C","70 N/25 mm"),
   P("Papírová páska C660","Papírové Pásky/c660.jpg","Ekologická papírová páska s akrylovým lepidlem a čistým odvíjením.","Papírový nosič","100 µm","Akrylové (disperzní)","3,8 N/25 mm","−5 až +60 °C","45 N/25 mm"),
   P("Papírová páska C680","Papírové Pásky/c680.jpg","Univerzální papírová páska s vysokou lepivostí na recyklovaný karton.","Papírový nosič","115 µm","Kaučukové","4,2 N/25 mm","−10 až +60 °C","50 N/25 mm"),
   P("Papírová páska C680R","Papírové Pásky/c680r.jpeg","Papírová páska z recyklovaného papíru pro udržitelné balení.","Recyklovaný papír","115 µm","Kaučukové","4,0 N/25 mm","−10 až +60 °C","48 N/25 mm"),
   P("Papírová páska C680 RT","Papírové Pásky/c680RT.jpeg","Odolná papírová páska s vylepšenou přilnavostí pro těžší zásilky.","Papírový nosič","120 µm","Kaučukové","4,3 N/25 mm","−10 až +65 °C","52 N/25 mm"),
   P("Papírová páska C690","Papírové Pásky/c690.jpg","Prémiová kraftová páska s hot melt lepidlem a matným povrchem.","Papírový nosič (kraft)","130 µm","Hot melt","4,8 N/25 mm","−10 až +70 °C","60 N/25 mm"),
 ],
 "bopp-pasky":[
   P("BOPP páska Acrylic","BOPP Tapes/BOPPACRYLIC.jpeg","Spolehlivá BOPP páska s akrylovým lepidlem a dlouhou životností.","BOPP fólie","45 µm","Akrylové (vodní disperze)","2,8 N/25 mm","−5 až +60 °C","45 N/25 mm"),
   P("BOPP páska Hot Melt","BOPP Tapes/BOPPHOTMELT.jpeg","BOPP páska s hot melt lepidlem pro rychlé a pevné přilnutí.","BOPP fólie","40 µm","Hot melt (syntetický kaučuk)","3,5 N/25 mm","0 až +50 °C","42 N/25 mm"),
   P("BOPP páska Hot Melt II","BOPP Tapes/BOPPHOTMELT1.jpg","Silnější BOPP páska s hot melt lepidlem pro náročnější balení.","BOPP fólie","48 µm","Hot melt","3,8 N/25 mm","0 až +55 °C","48 N/25 mm"),
   P("BOPP páska Evergreen","BOPP Tapes/EVERGREEN.jpg","Barevná BOPP páska pro značení a vizuální odlišení zásilek.","BOPP fólie (barevná)","45 µm","Akrylové","3,0 N/25 mm","−5 až +60 °C","46 N/25 mm"),
 ],
 "bopet-pasky":[
   P("BOPET páska ATE23","BOPET Tapes/ATE23.jpg","Tenká polyesterová páska s vysokou teplotní odolností.","Polyesterová (PET) fólie","25 µm","Akrylové","3,5 N/25 mm","−40 až +150 °C","60 N/25 mm"),
   P("BOPET páska AIT","BOPET Tapes/BOPETAIT.jpg","Polyesterová páska se silikonovým lepidlem pro extrémní teploty.","Polyesterová (PET) fólie","30 µm","Silikonové","3,0 N/25 mm","−40 až +180 °C","65 N/25 mm"),
   P("BOPET páska HIT17","BOPET Tapes/BOPETHIT17.jpg","Ultratenká PET páska pro elektrotechniku a přesné aplikace.","Polyesterová (PET) fólie","17 µm","Akrylové","3,2 N/25 mm","−40 až +155 °C","55 N/25 mm"),
   P("BOPET páska ECO HIT19","BOPET Tapes/ECOHIT19.jpg","Polyesterová páska s recyklovaným obsahem a vysokou odolností.","Recyklovaná PET fólie","19 µm","Akrylové","3,3 N/25 mm","−40 až +150 °C","58 N/25 mm"),
 ],
 "textilni-pasky":[
   P("Textilní páska BC","Textilní Lepící Pásky/BC.jpg","Pevná textilní (duct) páska pro opravy a univerzální použití.","Textilní výztuž + PE laminát","250 µm","Kaučukové (syntetické)","6,0 N/25 mm","−10 až +70 °C","120 N/25 mm"),
   P("Textilní páska BC2","Textilní Lepící Pásky/BC2.jpg","Extra silná textilní páska s vysokou pevností v tahu.","Textilní výztuž + PE laminát","280 µm","Kaučukové (syntetické)","6,5 N/25 mm","−10 až +70 °C","130 N/25 mm"),
   P("Textilní páska NU","Textilní Lepící Pásky/NU.jpg","Univerzální textilní páska pro rychlé svazování a fixaci.","Textilní výztuž + PE laminát","220 µm","Kaučukové","5,5 N/25 mm","−10 až +65 °C","110 N/25 mm"),
 ],
 "vyztuzene-pasky":[
   P("Vyztužená páska RMPP32","Vyztužené Pásky/rmpp32.jpg","Vyztužená páska se skelnými vlákny pro fixaci těžkých břemen.","MOPP + podélná skelná vlákna","130 µm","Hot melt (syntetický kaučuk)","4,5 N/25 mm","−10 až +60 °C","300 N/25 mm"),
   P("Vyztužená páska RTPP32","Vyztužené Pásky/rtpp32.jpg","Křížově vyztužená páska pro maximální pevnost ve všech směrech.","MOPP + křížová skelná vlákna","140 µm","Hot melt","4,7 N/25 mm","−10 až +60 °C","320 N/25 mm"),
 ],
 "mopp-pasky":[
   P("MOPP páska S45-50","MOPP Pásky/s45-50.jpg","Monoaxiální MOPP páska s extrémní pevností a nulovou tažností.","MOPP fólie","100 µm","Hot melt","4,0 N/25 mm","−10 až +60 °C","250 N/25 mm"),
 ],
 "odstranitelne-pasky":[
   P("Odstranitelná páska R28-32","Odstranitelné Pásky/r28-32.jpg","Odstranitelná páska, která po odlepení nezanechá žádné stopy.","BOPP fólie","50 µm","Odstranitelné akrylové","1,5 N/25 mm","−5 až +50 °C","40 N/25 mm"),
   P("Odstranitelná páska ECO RIT19","Odstranitelné Pásky/ECORIT19.jpg","Šetrná odstranitelná páska s recyklovaným obsahem.","Recyklovaná PET fólie","19 µm","Odstranitelné akrylové","1,8 N/25 mm","−5 až +55 °C","45 N/25 mm"),
 ],
 "malirske-pasky":[
   P("Malířská páska C580","Malířské Pásky/c580.jpg","Krepová malířská páska pro ostré hrany při běžném malování.","Krepový papír","130 µm","Kaučukové","2,8 N/25 mm","do +80 °C","28 N/25 mm"),
   P("Malířská páska CS60-80","Malířské Pásky/cs60-80.jpg","Teplotně odolná malířská páska pro lakování a náročné maskování.","Krepový papír","150 µm","Kaučukové (odolné teplu)","3,0 N/25 mm","do +100 °C","32 N/25 mm"),
 ],
 "udrzitelne-pasky":[
   P("Udržitelná páska NOPP","Udržitelné Pásky/nopp.jpg","Udržitelná páska bez plastu pro plně recyklovatelné balení.","Papír (FSC)","110 µm","Akrylové (bez rozpouštědel)","4,0 N/25 mm","−5 až +60 °C","50 N/25 mm"),
   P("Udržitelná páska NOPP+","Udržitelné Pásky/nopp+.jpg","Vylepšená bezplastová páska s vyšší pevností a lepivostí.","Papír (FSC)","120 µm","Akrylové","4,4 N/25 mm","−5 až +65 °C","55 N/25 mm"),
   P("Udržitelná páska LOOPP","Udržitelné Pásky/loopp.jpg","Páska z recyklovaného polypropylenu pro cirkulární ekonomiku.","Recyklovaná PP fólie","45 µm","Akrylové","3,0 N/25 mm","−5 až +60 °C","46 N/25 mm"),
   P("Udržitelná páska Airtape","Udržitelné Pásky/airtape.jpg","Lehká udržitelná páska pro každodenní ekologické balení.","Recyklovaná PP fólie","40 µm","Akrylové","2,8 N/25 mm","−5 až +60 °C","42 N/25 mm"),
   P("Udržitelná páska ECO+ 50","Udržitelné Pásky/eco+50.jpg","Tenká recyklovaná páska pro standardní udržitelné balení.","Recyklovaná PP fólie","50 µm","Akrylové","3,0 N/25 mm","−5 až +60 °C","45 N/25 mm"),
   P("Udržitelná páska ECO+ 80","Udržitelné Pásky/eco+80.jpg","Silnější recyklovaná páska pro náročnější udržitelné balení.","Recyklovaná PP fólie","80 µm","Akrylové","3,4 N/25 mm","−5 až +60 °C","52 N/25 mm"),
 ],
}

# ---------------------------------------------------------------------------
# Filter tags per product (base set; more can be added manually later).
# Taxonomy:
#   Vlastnosti: ekologicke, tiche, odstranitelne, vyztuzene
#   Odolnost:   mrazuvzdorne, vysoke-teploty, chemicka-odolnost
#   Pouziti:    rucni, stroje
# ---------------------------------------------------------------------------
TAGMAP = {
 "Papírová páska KH80":["ekologicke","rucni"],
 "Papírová páska KS165":["ekologicke","rucni"],
 "Papírová páska C660":["ekologicke","tiche","rucni"],
 "Papírová páska C680":["ekologicke","rucni","stroje"],
 "Papírová páska C680R":["ekologicke","rucni"],
 "Papírová páska C680 RT":["ekologicke","rucni","stroje"],
 "Papírová páska C690":["ekologicke","rucni"],
 "BOPP páska Acrylic":["tiche","rucni","stroje"],
 "BOPP páska Hot Melt":["rucni","stroje"],
 "BOPP páska Hot Melt II":["rucni","stroje"],
 "BOPP páska Evergreen":["mrazuvzdorne","stroje"],
 "BOPET páska ATE23":["vysoke-teploty","chemicka-odolnost"],
 "BOPET páska AIT":["vysoke-teploty","mrazuvzdorne","chemicka-odolnost"],
 "BOPET páska HIT17":["vysoke-teploty","chemicka-odolnost"],
 "BOPET páska ECO HIT19":["ekologicke","vysoke-teploty","chemicka-odolnost"],
 "Textilní páska BC":["vyztuzene","rucni"],
 "Textilní páska BC2":["vyztuzene","rucni"],
 "Textilní páska NU":["vyztuzene","rucni"],
 "Vyztužená páska RMPP32":["vyztuzene","stroje"],
 "Vyztužená páska RTPP32":["vyztuzene","stroje"],
 "MOPP páska S45-50":["vyztuzene","stroje"],
 "Odstranitelná páska R28-32":["odstranitelne","rucni"],
 "Odstranitelná páska ECO RIT19":["odstranitelne","ekologicke","rucni"],
 "Malířská páska C580":["rucni"],
 "Malířská páska CS60-80":["vysoke-teploty","rucni"],
 "Udržitelná páska NOPP":["ekologicke","rucni"],
 "Udržitelná páska NOPP+":["ekologicke","rucni"],
 "Udržitelná páska LOOPP":["ekologicke","stroje"],
 "Udržitelná páska Airtape":["ekologicke","rucni"],
 "Udržitelná páska ECO+ 50":["ekologicke","stroje"],
 "Udržitelná páska ECO+ 80":["ekologicke","stroje"],
}

# sort products alphabetically within each category
for k in PRODUCTS:
    PRODUCTS[k] = sorted(PRODUCTS[k], key=lambda p: p["name"])

# assign slugs + tags
for cat in CATS:
    for p in PRODUCTS[cat["cat"]]:
        p["slug"]=slugify(p["name"])
        p["tags"]=TAGMAP.get(p["name"],[])

# ---------------------------------------------------------------------------
# Static page generation: shared header/footer from sortiment.html
# ---------------------------------------------------------------------------
base=open("sortiment.html").read()
if "<!-- SITE-TOP -->" in base and "<!-- /SITE-TOP -->" in base:
    start = base.index("<!-- SITE-TOP -->")
    end = base.index("<!-- /SITE-TOP -->") + len("<!-- /SITE-TOP -->")
    header = base[:base.index("</head>")+len("</head>")] + base[base.index("<body"):start] + base[start:end]
else:
    header = base[:base.index("</header>")+len("</header>")]
footer=base[base.index('<footer id="kontakt1"'):]

def absolutize(b):
    for a,x in [('src="images/','src="/images/'),('src="icons/','src="/icons/'),('href="icons/','href="/icons/'),
                ('src="assets/','src="/assets/'),('href="assets/','href="/assets/'),
                ('href="index.html','href="/index.html'),('href="galerie.html','href="/galerie.html'),
                ('href="sortiment.html','href="/sortiment.html')]:
        b=b.replace(a,x)
    return b
header=absolutize(header); footer=absolutize(footer)
header=header.replace('<a href="/sortiment.html" class="rounded-lg px-4 py-2 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-100 hover:text-orange-600">Sortiment</a>','<a href="/sortiment.html" class="rounded-lg bg-orange-50 px-4 py-2 text-sm font-semibold text-orange-600">Sortiment</a>')
header=header.replace('<a href="/sortiment.html" class="block rounded-xl px-4 py-3 font-semibold text-slate-800 hover:bg-slate-50">Sortiment</a>','<a href="/sortiment.html" class="block rounded-xl bg-orange-50 px-4 py-3 font-semibold text-orange-600">Sortiment</a>')

CHK='<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>'
ARR='<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>'
BACK='<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M11 17l-5-5m0 0l5-5m-5 5h12"/></svg>'
FWD='<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>'
PRODUCT_LEFT_EXTRA='''                <div class="mt-8">
                    <div class="product-tailor-box rounded-2xl bg-slate-50 p-6">
                        <h3 class="text-base font-bold text-slate-900">Na míru vašemu provozu</h3>
                        <ul class="product-tailor-list mt-3 space-y-2.5 text-sm leading-relaxed text-slate-600">
                            <li class="flex gap-2"><span class="font-bold text-orange-600" aria-hidden="true">•</span>Volitelná šířka a délka návinu</li>
                            <li class="flex gap-2"><span class="font-bold text-orange-600" aria-hidden="true">•</span>Barva podkladu a počet barev potisku</li>
                            <li class="flex gap-2"><span class="font-bold text-orange-600" aria-hidden="true">•</span>Nezávazná kalkulace a vzorek před objednávkou</li>
                        </ul>
                        <a href="/index.html#gf_1" class="mt-4 inline-flex items-center gap-1 text-sm font-bold text-orange-600 transition-colors hover:text-orange-700">Nezávazně poptat %s</a>
                    </div>
                </div>''' % FWD
PRODUCT_BOTTOM_NOTE='''        <div class="mx-auto mt-14 max-w-3xl rounded-2xl border border-slate-200 bg-white px-6 py-5 text-center shadow-sm sm:px-8">
            <p class="text-sm leading-relaxed text-slate-600">
                <span class="font-bold text-slate-900">Pásku lze objednat i bez potisku.</span>
                Pokud nepotřebujete logo na pásku, stejný materiál vám dodáme v nepotištěném provedení, ideální pro okamžité balení nebo skladové zásoby.
                <a href="/index.html#kontakt1" class="font-semibold text-orange-600 transition-colors hover:text-orange-700">Zeptejte se na dostupnost</a>
            </p>
        </div>

        <div class="mt-8 flex flex-wrap items-center justify-center gap-4">'''
IMG_CLS='w-full h-full object-contain max-h-56 mix-blend-multiply contrast-[1.1] brightness-[1.05] transform transition-transform duration-300 group-hover:scale-105'
PORTRAIT_CATEGORIES = {'udrzitelne-pasky'}

def product_card_image_box(cat_slug):
    base = 'product-image-frame w-full h-64 flex items-center justify-center overflow-hidden'
    if cat_slug in PORTRAIT_CATEGORIES:
        return base
    return base + ' p-6'

def product_card_image_cls(cat_slug):
    base = 'object-contain mix-blend-multiply contrast-[1.1] brightness-[1.05] transform transition-transform duration-300'
    if cat_slug in PORTRAIT_CATEGORIES:
        return 'h-56 w-auto max-w-none scale-[1.75] ' + base + ' group-hover:scale-[1.85]'
    return 'w-full h-full max-h-56 ' + base + ' group-hover:scale-105'

def product_detail_image_box(cat_slug):
    if cat_slug in PORTRAIT_CATEGORIES:
        return 'product-image-frame flex items-center justify-center overflow-hidden rounded-3xl border border-slate-100 p-4 shadow-sm sm:p-6'
    return 'product-image-frame flex items-center justify-center rounded-3xl border border-slate-100 p-8 shadow-sm sm:p-12'

def product_detail_image_cls(cat_slug):
    base = 'object-contain mix-blend-multiply contrast-[1.1] brightness-[1.05]'
    if cat_slug in PORTRAIT_CATEGORIES:
        return 'h-[360px] w-auto max-w-none scale-[1.35] ' + base + ' sm:h-[440px] sm:scale-[1.4]'
    return 'h-[360px] w-full ' + base + ' sm:h-[440px]'

def page(title, main):
    p=header+main+footer
    return p.replace('<title>Sortiment | Pásky s potiskem</title>', '<title>%s | Pásky s potiskem</title>'%esc(title))

# ---------------------------------------------------------------------------
# 2) Category pages (product cards link to product detail)
# ---------------------------------------------------------------------------
for cat in CATS:
    props="\n".join('''            <article class="flex h-full flex-col rounded-2xl border border-slate-100 bg-white p-7 shadow-sm">
                <div class="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-orange-50 text-orange-600" aria-hidden="true">%s</div>
                <h3 class="text-lg font-bold text-slate-900">%s</h3>
                <p class="mt-2 flex-1 text-sm leading-relaxed text-slate-600">%s</p>
            </article>'''%(CHK,esc(t),esc(x)) for t,x in cat["properties"])
    apps="\n".join('''                <div class="flex items-center gap-3 rounded-xl border border-slate-100 bg-white px-5 py-4">
                    <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-orange-50 text-orange-600" aria-hidden="true">%s</span>
                    <span class="text-sm font-medium text-slate-700">%s</span>
                </div>'''%(ARR,esc(a)) for a in cat["apps"])
    cards="\n".join('''            <a href="/sortiment/%s/%s" class="group flex h-full flex-col overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-orange-100 hover:shadow-lg">
                <div class="%s">
                    <img src="%s" alt="%s" loading="lazy" class="%s">
                </div>
                <div class="flex flex-1 flex-col p-6">
                    <h3 class="text-lg font-bold text-slate-900">%s</h3>
                    <p class="mt-2 flex-1 text-sm leading-relaxed text-slate-600">%s</p>
                    <span class="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-orange-600 to-amber-500 px-5 py-3 text-sm font-bold text-white shadow-sm transition-all group-hover:scale-[1.02] group-hover:shadow-md">Zobrazit detail %s</span>
                </div>
            </a>'''%(cat["cat"],p["slug"],product_card_image_box(cat["cat"]),url(p["image"]),esc(p["name"]),product_card_image_cls(cat["cat"]),esc(p["name"]),esc(p["tagline"]),FWD) for p in PRODUCTS[cat["cat"]])

    main='''

<main>

<section class="border-b border-slate-100 bg-gradient-to-b from-white to-slate-50">
    <div class="mx-auto max-w-7xl px-4 py-14 sm:py-16">
        <nav class="mb-6 text-sm text-slate-500" aria-label="Drobečková navigace">
            <a href="/index.html" class="hover:text-orange-600">Domů</a>
            <span class="mx-2 text-slate-300">/</span>
            <a href="/sortiment.html" class="font-semibold text-orange-600 hover:text-orange-700">Sortiment</a>
            <span class="mx-2 text-slate-300">/</span>
            <span class="text-slate-600">%s</span>
        </nav>
        <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div class="max-w-3xl">
                <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl lg:text-5xl">%s</h1>
                <p class="mt-4 text-base leading-relaxed text-slate-600 sm:text-lg">%s</p>
            </div>
            <div class="shrink-0">
                <a href="/index.html#gf_1" class="inline-flex items-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-7 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/25 transition-all hover:scale-[1.02] hover:shadow-xl">Nezávazná kalkulace</a>
            </div>
        </div>
    </div>
</section>

<section class="mx-auto max-w-7xl px-4 py-14 sm:py-16">
    <h2 class="mb-8 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Klíčové vlastnosti</h2>
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
%s
    </div>
</section>

<section class="border-t border-slate-100 bg-white">
    <div class="mx-auto max-w-7xl px-4 py-14 sm:py-16">
        <h2 class="mb-8 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Produkty v této kategorii</h2>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
%s
        </div>
    </div>
</section>

<section class="border-t border-slate-100 bg-slate-50">
    <div class="mx-auto max-w-7xl px-4 py-14 sm:py-16">
        <h2 class="mb-8 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Typické použití</h2>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
%s
        </div>
        <div class="mt-12 flex flex-wrap items-center justify-center gap-4">
            <a href="/sortiment.html" class="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-6 py-3 text-sm font-bold text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50">%s Zpět na sortiment</a>
            <a href="/index.html#gf_1" class="inline-flex items-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/25 transition-all hover:scale-[1.02] hover:shadow-xl">Mám zájem o tuto kategorii</a>
        </div>
    </div>
</section>

</main>

'''%(esc(cat["title"]),esc(cat["title"]),esc(cat["intro"]),props,cards,apps,BACK)
    os.makedirs("sortiment/%s"%cat["cat"],exist_ok=True)
    open("sortiment/%s/index.html"%cat["cat"],"w").write(page(cat["title"],main))
print("rebuilt %d category pages"%len(CATS))

# ---------------------------------------------------------------------------
# 3) Product detail pages
# ---------------------------------------------------------------------------
n=0
for cat in CATS:
    for p in PRODUCTS[cat["cat"]]:
        rows="\n".join('''                    <tr class="border-b border-slate-100 last:border-0">
                        <th scope="row" class="w-1/2 px-6 py-4 pr-4 text-left align-top text-sm font-semibold text-slate-500">%s</th>
                        <td class="px-6 py-4 text-sm font-semibold text-slate-900">%s</td>
                    </tr>'''%(esc(k),esc(v)) for k,v in p["params"].items())
        advs="\n".join('''                <div class="flex gap-4 rounded-2xl border border-slate-100 bg-white p-6 shadow-sm">
                    <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-orange-50 text-orange-600" aria-hidden="true">%s</span>
                    <div>
                        <h3 class="text-base font-bold text-slate-900">%s</h3>
                        <p class="mt-1 text-sm leading-relaxed text-slate-600">%s</p>
                    </div>
                </div>'''%(CHK,esc(t),esc(x)) for t,x in cat["properties"])
        uses="\n".join('''                <li class="flex items-center gap-3 rounded-xl border border-slate-100 bg-white px-5 py-4">
                    <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-orange-50 text-orange-600" aria-hidden="true">%s</span>
                    <span class="text-sm font-medium text-slate-700">%s</span>
                </li>'''%(ARR,esc(a)) for a in cat["apps"])

        main='''

<main>

<section class="mx-auto max-w-7xl px-4 py-10 sm:py-14">
    <nav class="mb-8 text-sm text-slate-500" aria-label="Drobečková navigace">
        <a href="/index.html" class="hover:text-orange-600">Domů</a>
        <span class="mx-2 text-slate-300">/</span>
        <a href="/sortiment.html" class="hover:text-orange-600">Sortiment</a>
        <span class="mx-2 text-slate-300">/</span>
        <a href="/sortiment/%s" class="hover:text-orange-600">%s</a>
        <span class="mx-2 text-slate-300">/</span>
        <span class="text-slate-600">%s</span>
    </nav>

    <div class="grid grid-cols-1 gap-10 lg:grid-cols-2 lg:gap-14">
        <div class="%s">
            <img src="%s" alt="%s" class="%s">
        </div>
        <div class="flex flex-col justify-center">
            <span class="text-sm font-semibold uppercase tracking-wide text-orange-600">%s</span>
            <h1 class="mt-2 text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">%s</h1>
            <p class="mt-4 text-base leading-relaxed text-slate-600 sm:text-lg">%s</p>
            <div class="mt-6 flex flex-wrap gap-2">
                <span class="rounded-full bg-slate-100 px-4 py-1.5 text-xs font-semibold text-slate-700">%s</span>
                <span class="rounded-full bg-slate-100 px-4 py-1.5 text-xs font-semibold text-slate-700">%s</span>
                <span class="rounded-full bg-slate-100 px-4 py-1.5 text-xs font-semibold text-slate-700">%s</span>
            </div>
            <div class="mt-8 flex flex-wrap gap-4">
                <a href="/index.html#gf_1" class="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/25 transition-all hover:scale-[1.02] hover:shadow-xl">Nezávazně poptat / Kalkulace %s</a>
                <a href="/sortiment/%s" class="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-6 py-3.5 text-sm font-bold text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50">%s Zpět na kategorii</a>
            </div>
        </div>
    </div>
</section>

<section class="border-t border-slate-100 bg-slate-50">
    <div class="mx-auto max-w-7xl px-4 py-14 sm:py-16">
        <div class="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-16">
            <div>
                <h2 class="mb-6 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Technické parametry</h2>
                <div class="overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm">
                    <table class="w-full">
                        <tbody>
%s
                        </tbody>
                    </table>
                </div>
                <p class="mt-4 text-xs leading-relaxed text-slate-400">Uvedené hodnoty jsou orientační a mohou se lišit podle konkrétní šířky, návinu a provedení. Rádi vám připravíme přesnou specifikaci na míru.</p>
%s
            </div>
            <div>
                <h2 class="mb-6 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Hlavní výhody a použití</h2>
                <div class="grid grid-cols-1 gap-4">
%s
                </div>
                <h3 class="mb-4 mt-8 text-lg font-bold text-slate-900">Typické použití</h3>
                <ul class="grid grid-cols-1 gap-3 sm:grid-cols-2">
%s
                </ul>
            </div>
        </div>

%s
            <a href="/sortiment/%s" class="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-6 py-3 text-sm font-bold text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50">%s Zpět na %s</a>
            <a href="/index.html#kontakt1" class="inline-flex items-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/25 transition-all hover:scale-[1.02] hover:shadow-xl">Mám zájem o tuto pásku</a>
        </div>
    </div>
</section>

</main>

'''%(cat["cat"],esc(cat["title"]),esc(p["name"]),
     product_detail_image_box(cat["cat"]),url(p["image"]),esc(p["name"]),product_detail_image_cls(cat["cat"]),
     esc(cat["title"]),esc(p["name"]),esc(p["tagline"]),
     esc(p["params"]["Nosič / materiál"]),esc(p["params"]["Typ lepidla"]),esc(p["params"]["Teplotní odolnost"]),
     FWD,cat["cat"],BACK,
     rows,PRODUCT_LEFT_EXTRA,advs,uses,
     PRODUCT_BOTTOM_NOTE,
     cat["cat"],BACK,esc(cat["title"]))
        os.makedirs("sortiment/%s/%s"%(cat["cat"],p["slug"]),exist_ok=True)
        open("sortiment/%s/%s/index.html"%(cat["cat"],p["slug"]),"w").write(page(p["name"],main))
        n+=1
print("generated %d product detail pages"%n)

# ---------------------------------------------------------------------------
# 4) Inject product JSON (for tag filter) into sortiment.html
# ---------------------------------------------------------------------------
import json
items=[]
for cat in CATS:
    for p in PRODUCTS[cat["cat"]]:
        items.append({
            "name":p["name"],
            "tagline":p["tagline"],
            "image":url(p["image"]),
            "detail":"/sortiment/%s/%s"%(cat["cat"],p["slug"]),
            "category":cat["title"],
            "tags":p["tags"],
            "portrait":cat["cat"] in PORTRAIT_CATEGORIES,
        })
blob=json.dumps(items, ensure_ascii=False, indent=2)
s=open("sortiment.html").read()
start_m='<script id="sortiment-products" type="application/json">'
end_m='</script>'
if start_m in s:
    i=s.index(start_m)+len(start_m)
    j=s.index(end_m,i)
    s=s[:i]+"\n"+blob+"\n"+s[j:]
    open("sortiment.html","w").write(s)
    print("injected product JSON into sortiment.html (%d items)"%len(items))
else:
    print("WARN: JSON marker not found in sortiment.html – add the filter block first")
