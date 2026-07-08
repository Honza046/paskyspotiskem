<?php
/**
 * Homepage main content (Tailwind sections).
 *
 * @package Paskyonline
 */
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
?>

<!-- O NÁS -->
<section id="o-nas" class="bg-white">
    <div class="mx-auto grid max-w-7xl grid-cols-1 items-center gap-12 px-4 py-16 md:py-24 lg:grid-cols-2">
        <div>
            <span class="text-xs font-bold uppercase tracking-widest text-orange-600" data-i18n="home.about.label">O nás</span>
            <h2 class="mb-6 mt-2 text-3xl font-bold text-slate-900 md:text-4xl" data-i18n="home.about.title">Tradiční český výrobce lepicích pásek s potiskem</h2>
            <p class="mb-4 text-lg font-medium text-slate-700">Již více než 30 let pomáháme firmám bezpečně balit jejich zásilky a budovat silnou značku přímo na balicích materiálech. Jsme specialisté na zakázkový potisk lepicích pásek.</p>
            <p class="mb-6 text-base leading-relaxed text-slate-600">Naše moderní výrobní zázemí nám umožňuje flexibilně reagovat na potřeby jak malých e-shopů, tak velkých průmyslových podniků. Zakládáme si na precizním tisku (až 8 barev), špičkové kvalitě použitých lepidel (Hot Melt, Akryl) a rychlém doručení po celé České republice.</p>
            <p class="text-base leading-relaxed text-slate-600">Díky certifikovaným procesům ISO 9001 a využívání ekologických, udržovatelných materiálů jsme stabilním partnerem pro více než 100 aktivních odběratelů.</p>
        </div>
        <div class="relative overflow-hidden rounded-3xl shadow-xl">
            <img src="<?php echo esc_url( paskyonline_image( 'about-team.png' ) ); ?>" alt="Tým ALFA IN – zástupci společnosti" class="block aspect-[3/2] w-full object-cover">
            <div class="absolute bottom-4 left-4 right-4 rounded-2xl border border-white/60 bg-white/80 px-4 py-3 text-center shadow-sm backdrop-blur-sm">
                <p class="text-sm font-semibold text-slate-800">Tým ALFA IN</p>
                <p class="mt-0.5 text-xs text-slate-500">Tradice, zkušenosti a osobní přístup ke každé zakázce</p>
            </div>
        </div>
    </div>
</section>

<!-- REFERENCE -->
<section id="reference" class="border-t border-slate-100 bg-white">
    <div class="mx-auto max-w-7xl px-4 py-20">
        <div class="mb-14 text-center">
            <p class="mb-3 text-sm font-bold uppercase tracking-widest text-orange-600" data-i18n="home.references.label">Reference</p>
            <h2 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl" data-i18n="home.references.title">Spokojení zákazníci napříč obory</h2>
            <p class="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-slate-600">Firmy, které na našich páskách s potiskem spoléhají každý den — od e-commerce po výrobu a zdravotnictví.</p>
        </div>

        <div class="mb-14 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div class="rounded-2xl border border-slate-100 bg-slate-50 px-6 py-5 text-center">
                <p class="text-3xl font-extrabold text-orange-600">300+</p>
                <p class="mt-1 text-sm font-medium text-slate-600">aktivních odběratelů</p>
            </div>
            <div class="rounded-2xl border border-slate-100 bg-slate-50 px-6 py-5 text-center">
                <p class="text-3xl font-extrabold text-orange-600">30+ let</p>
                <p class="mt-1 text-sm font-medium text-slate-600">zkušeností s potiskem</p>
            </div>
            <div class="rounded-2xl border border-slate-100 bg-slate-50 px-6 py-5 text-center">
                <p class="text-3xl font-extrabold text-orange-600">ISO 9001</p>
                <p class="mt-1 text-sm font-medium text-slate-600">certifikovaná výroba</p>
            </div>
        </div>

        <?php get_template_part( 'template-parts/reference-logos', 'carousel' ); ?>
    </div>
</section>

<!-- SROVNÁVAČ LEPIDEL -->
<section id="lepidla" class="mx-auto max-w-7xl border-t border-slate-100 px-4 pb-20 pt-16 md:pt-24">
    <div class="mb-12 text-center">
        <p class="mb-3 text-sm font-bold uppercase tracking-widest text-orange-600">Průvodce výběrem</p>
        <h2 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">Jaké lepidlo zvolit?</h2>
    </div>

    <div class="grid grid-cols-1 gap-8 md:grid-cols-2">
        <article class="group rounded-2xl border border-slate-100 bg-white p-8 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-slate-200 hover:shadow-xl">
            <div class="mb-6 flex items-start justify-between gap-4">
                <div>
                    <span class="mb-2 inline-flex rounded-full border border-sky-200 bg-sky-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-sky-700">Chlad &amp; rychlost</span>
                    <h3 class="text-2xl font-extrabold text-slate-900">HOT MELT</h3>
                    <p class="mt-1 text-sm font-medium text-slate-500">Syntetický kaučuk</p>
                </div>
                <div class="flex shrink-0 gap-2">
                    <span class="flex h-12 w-12 items-center justify-center rounded-2xl bg-sky-50 text-2xl transition-transform duration-300 group-hover:scale-110" aria-hidden="true">❄️</span>
                    <span class="flex h-12 w-12 items-center justify-center rounded-2xl bg-orange-50 text-2xl transition-transform duration-300 group-hover:scale-110" aria-hidden="true">📦</span>
                </div>
            </div>
            <p class="leading-relaxed text-slate-600">Ideální volba do chladnějšího prostředí a nevytápěných skladů. Vyznačuje se extrémně rychlým a silným přilnutím k podkladu ihned po zalepení. Nelze snadno odlepit z fixační stretch fólie.</p>
        </article>

        <article class="group rounded-2xl border border-slate-100 bg-white p-8 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-slate-200 hover:shadow-xl">
            <div class="mb-6 flex items-start justify-between gap-4">
                <div>
                    <span class="mb-2 inline-flex rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-amber-700">Ticho &amp; UV odolnost</span>
                    <h3 class="text-2xl font-extrabold text-slate-900">ACRYL</h3>
                    <p class="mt-1 text-sm font-medium text-slate-500">S nehlučnou úpravou</p>
                </div>
                <div class="flex shrink-0 gap-2">
                    <span class="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-2xl transition-transform duration-300 group-hover:scale-110" aria-hidden="true">🔇</span>
                    <span class="flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-50 text-2xl transition-transform duration-300 group-hover:scale-110" aria-hidden="true">☀️</span>
                </div>
            </div>
            <p class="leading-relaxed text-slate-600">Zajišťuje tiché a komfortní odvíjení, které oceníte ve velkých balicích halách. Je vysoce odolné proti UV záření a stárnutí, což z něj dělá perfektní volbu pro dlouhodobé skladování zboží.</p>
        </article>
    </div>
</section>

<!-- UDRŽITELNOST -->
<section id="udrzitelnost" class="mx-auto max-w-7xl px-4 pb-20">
    <div class="mb-12 text-center">
        <p class="mb-3 text-sm font-bold uppercase tracking-widest text-emerald-600">Ekologie &amp; udržitelnost</p>
        <h2 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">Udržitelné balení pro Váš e-shop i výrobu</h2>
        <p class="mx-auto mt-4 max-w-3xl text-base leading-relaxed text-slate-600 sm:text-lg">Ekologická stopa obalových materiálů je pro nás prioritou. Naše lepicí pásky vyvíjíme s ohledem na snadnou recyklovatelnost a minimální dopad na životní prostředí.</p>
    </div>

    <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
        <article class="group flex h-full flex-col rounded-2xl border border-slate-100 bg-white p-8 shadow-sm transition-all duration-300 hover:border-emerald-100 hover:shadow-md">
            <div class="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-50 text-2xl transition-transform duration-300 group-hover:scale-105" aria-hidden="true">♻️</div>
            <h3 class="mb-3 text-lg font-bold text-slate-900">100% Recyklovatelná fólie</h3>
            <p class="text-sm leading-relaxed text-slate-600">Naše pásky jsou vyrobeny z moderní BOPP fólie, která je plně recyklovatelná. Na rozdíl od starších PVC materiálů při jejím zpracování nevznikají žádné toxické látky a je šetrná k přírodě.</p>
        </article>

        <article class="group flex h-full flex-col rounded-2xl border border-slate-100 bg-white p-8 shadow-sm transition-all duration-300 hover:border-emerald-100 hover:shadow-md">
            <div class="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-50 text-2xl transition-transform duration-300 group-hover:scale-105" aria-hidden="true">🍃</div>
            <h3 class="mb-3 text-lg font-bold text-slate-900">Ekologická lepidla bez rozpouštědel</h3>
            <p class="text-sm leading-relaxed text-slate-600">Používáme výhradně lepidla šetrná k životnímu prostředí. Akrylová lepidla jsou vyrobena na vodní bázi a Hot Melt technologie funguje bez použití jakýchkoliv chemických rozpouštědel či syntetických příměsí.</p>
        </article>

        <article class="group flex h-full flex-col rounded-2xl border border-slate-100 bg-white p-8 shadow-sm transition-all duration-300 hover:border-emerald-100 hover:shadow-md">
            <div class="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-50 text-2xl transition-transform duration-300 group-hover:scale-105" aria-hidden="true">📦</div>
            <h3 class="mb-3 text-lg font-bold text-slate-900">Bezproblémová recyklace kartonů</h3>
            <p class="text-sm leading-relaxed text-slate-600">Díky pokročilé technologii dokážou moderní recyklační linky naše pásky z papírových krabic snadno oddělit. Vaši zákazníci tak mohou použité krabice bez obav vyhodit přímo do modrého kontejneru.</p>
        </article>
    </div>
</section>

<!-- VÝHODY – BEZPEČNOST & LEPIVOST -->
<section class="mx-auto max-w-7xl px-4 pb-20">
    <div class="grid grid-cols-1 gap-8 md:grid-cols-2">

        <article class="group relative flex flex-col overflow-hidden rounded-3xl border border-slate-100 bg-white shadow-sm transition-all duration-300 hover:border-red-100 hover:shadow-lg">
            <div class="relative h-52 overflow-hidden bg-white sm:h-56">
                <img src="<?php echo esc_url( paskyonline_image( 'benefit-tamper-evident.jpg' ) ); ?>" alt="Lepicí páska TAMPER EVIDENT s VOID efektem" class="h-full w-full object-cover object-center transition-transform duration-500 group-hover:scale-105" loading="lazy">
                <div class="pointer-events-none absolute inset-0 bg-gradient-to-t from-white/30 via-transparent to-transparent"></div>
            </div>
            <div class="flex flex-1 flex-col px-8 pb-10 pt-6">
                <span class="inline-flex w-fit rounded-full border border-red-200 bg-red-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-red-700" data-i18n="home.benefits.security.badge">Bezpečnost</span>
                <h3 class="mt-4 text-2xl font-extrabold text-slate-900">Lepicí páska TAMPER EVIDENT – porušení zřejmé!</h3>
                <p class="mt-4 leading-relaxed text-slate-600">Tato bezpečnostní lepicí páska se „tváří“ jako neutrální, nicméně při odlepení na krabici zanechává upozornění, které prakticky nelze odstranit. Páska je vhodná pro všechny typy kartonů i stretch folií, lze dodat v různých barvách či i s potiskem.</p>
                <div class="mt-6 flex flex-wrap gap-2">
                    <span class="rounded-lg border border-red-200 bg-red-50 px-3 py-1.5 text-sm font-bold text-red-700">VOID</span>
                    <span class="rounded-lg border border-red-200 bg-red-50 px-3 py-1.5 text-sm font-bold text-red-700">OPEN</span>
                    <span class="rounded-lg border border-red-200 bg-red-50 px-3 py-1.5 text-sm font-bold text-red-700">FRAUD</span>
                </div>
            </div>
        </article>

        <article class="group relative flex flex-col overflow-hidden rounded-3xl border border-slate-100 bg-white shadow-sm transition-all duration-300 hover:border-orange-100 hover:shadow-lg">
            <div class="relative h-52 overflow-hidden bg-orange-50 sm:h-56">
                <img src="<?php echo esc_url( paskyonline_image( 'Extra-glue.jpg' ) ); ?>" alt="EXTRA GLUE+ a TACK+ pásky s extrémní lepivostí" class="h-full w-full object-cover object-center transition-transform duration-500 group-hover:scale-105" loading="lazy">
                <div class="pointer-events-none absolute inset-0 bg-gradient-to-t from-white/20 via-transparent to-transparent"></div>
            </div>
            <div class="flex flex-1 flex-col px-8 pb-10 pt-6">
                <span class="inline-flex w-fit rounded-full border border-orange-200 bg-orange-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-orange-700" data-i18n="home.benefits.glue.badge">Extrémní lepivost</span>
                <h3 class="mt-4 text-2xl font-extrabold text-slate-900">EXTRA GLUE+ (ACRYL) a TACK+ (HOT MELT)</h3>
                <p class="mt-4 leading-relaxed text-slate-600">Pásky se <strong class="font-semibold text-slate-800">zvýšenou vrstvou lepidla</strong> (33 % resp. 20 %) i s možností <strong class="font-semibold text-slate-800">pevnější folie</strong> oproti standardu, určené i pro velmi obtížné aplikace jako např. velmi těžké balíky, nekvalitní kartony nebo prašné prostředí. Na kartonu drží velmi pevně — <strong class="font-semibold text-orange-600">zjevný důkaz vykradení!</strong></p>
                <div class="mt-6 flex flex-wrap gap-2">
                    <span class="rounded-lg border border-orange-200 bg-orange-50 px-3 py-1.5 text-sm font-bold text-orange-700">EXTRA GLUE+</span>
                    <span class="rounded-lg border border-orange-200 bg-orange-50 px-3 py-1.5 text-sm font-bold text-orange-700">TACK+</span>
                    <span class="rounded-lg border border-orange-200 bg-orange-50 px-3 py-1.5 text-sm font-bold text-orange-700">+33 % lepidla</span>
                </div>
            </div>
        </article>

    </div>
</section>

<!-- FORMULÁŘ – MULTI-STEP -->
<section id="gf_1" class="mx-auto max-w-7xl border-t border-slate-100 px-4 pt-20 pb-20">
    <div id="form-outer-head" class="mb-8 text-center">
        <p class="mb-2 text-sm font-bold uppercase tracking-widest text-orange-600">Poptávka</p>
        <h2 class="text-2xl font-extrabold text-slate-900 sm:text-3xl">Mám zájem o kalkulaci pásek s potiskem</h2>
    </div>

    <div id="gform_wrapper_1" class="gform_wrapper gform-theme--no-framework mx-auto w-full max-w-2xl" data-step="0">
        <form id="gform_1" action="#" method="post" class="select-text overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-lg shadow-slate-200/50" novalidate>

            <!-- Progress -->
            <div class="gform_progress_wrap border-b border-slate-100 px-6 py-5">
                <div class="mb-3 flex items-center justify-between text-xs font-semibold uppercase tracking-wide text-slate-500">
                    <span id="form-step-label">Krok 1 ze 3</span>
                    <span id="form-step-name">Specifikace produktu</span>
                </div>
                <div class="h-1.5 overflow-hidden rounded-full bg-slate-100">
                    <div id="form-progress-bar" class="h-full rounded-full bg-gradient-to-r from-orange-600 to-amber-500 transition-all duration-500 ease-out" style="width:33.33%"></div>
                </div>
                <div class="mt-4 flex justify-center gap-2" id="form-progress-dots" aria-hidden="true">
                    <span class="h-2 w-8 rounded-full bg-orange-500 transition-all" data-dot="0"></span>
                    <span class="h-2 w-2 rounded-full bg-slate-200 transition-all" data-dot="1"></span>
                    <span class="h-2 w-2 rounded-full bg-slate-200 transition-all" data-dot="2"></span>
                </div>
            </div>

            <div class="gform_body px-6 py-6 sm:px-8 sm:py-8">

                <!-- KROK 1 — Specifikace produktu -->
                <div class="gform_page" id="gform_page_1_1" data-step="0">
                    <h3 class="mb-1 text-lg font-bold text-slate-900">Specifikace produktu</h3>
                    <p class="mb-6 text-sm text-slate-500">Vyberte typ pásky, podkladovou barvu a počet barev k tisku.</p>

                    <fieldset class="mb-6">
                        <legend class="mb-3 block text-sm font-semibold text-slate-800">Typ pásky (materiál) <span class="text-orange-600">*</span></legend>
                        <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
                            <label class="cursor-pointer">
                                <input type="radio" name="input_8" value="HOT MELT" checked class="peer sr-only" required>
                                <span class="flex flex-col rounded-xl border-2 border-slate-200 px-4 py-4 text-center transition-all duration-200 hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700 peer-checked:shadow-sm">
                                    <span class="text-sm font-bold">HOT MELT</span>
                                    <span class="mt-1 text-xs text-slate-500 peer-checked:text-orange-600/80">Syntetický kaučuk</span>
                                </span>
                            </label>
                            <label class="cursor-pointer">
                                <input type="radio" name="input_8" value="ACRYL" class="peer sr-only">
                                <span class="flex flex-col rounded-xl border-2 border-slate-200 px-4 py-4 text-center transition-all duration-200 hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700 peer-checked:shadow-sm">
                                    <span class="text-sm font-bold">ACRYL</span>
                                    <span class="mt-1 text-xs text-slate-500 peer-checked:text-orange-600/80">Nehlučná úprava</span>
                                </span>
                            </label>
                        </div>
                    </fieldset>

                    <div id="acryl-noise-option" class="mb-6 hidden">
                        <label class="flex cursor-pointer items-start gap-3 rounded-xl border-2 border-slate-200 p-4 transition-all hover:border-slate-300 has-[:checked]:border-orange-500 has-[:checked]:bg-orange-50">
                            <input type="checkbox" name="input_acryl_no_silent" id="input_acryl_no_silent" value="bez nehlučného činidla" class="mt-0.5 h-4 w-4 rounded border-slate-300 accent-orange-600 focus:ring-orange-500/20">
                            <span class="text-sm leading-relaxed text-slate-700">
                                <span class="font-semibold text-slate-900">Bez nehlučného činidla</span>
                                <span class="mt-0.5 block text-xs text-slate-500">Standardně je u ACRYL pásek tiché odvíjení. Zaškrtněte, pokud preferujete variantu bez této úpravy.</span>
                            </span>
                        </label>
                    </div>

                    <fieldset class="mb-6">
                        <legend class="mb-3 block text-sm font-semibold text-slate-800">Podkladová barva <span class="text-orange-600">*</span></legend>
                        <div class="grid grid-cols-2 gap-2 sm:grid-cols-4">
                            <label class="cursor-pointer"><input type="radio" name="input_9" value="bílá" checked class="peer sr-only"><span class="block rounded-xl border-2 border-slate-200 px-3 py-3 text-center text-sm font-semibold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">bílá</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_9" value="hnědá" class="peer sr-only"><span class="block rounded-xl border-2 border-slate-200 px-3 py-3 text-center text-sm font-semibold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">hnědá</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_9" value="transparentní" class="peer sr-only"><span class="block rounded-xl border-2 border-slate-200 px-3 py-3 text-center text-sm font-semibold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">transp.</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_9" value="jiná" class="peer sr-only"><span class="block rounded-xl border-2 border-slate-200 px-3 py-3 text-center text-sm font-semibold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">jiná</span></label>
                        </div>
                    </fieldset>

                    <fieldset class="mb-6">
                        <legend class="mb-3 block text-sm font-semibold text-slate-800">Počet barev k tisku</legend>
                        <div class="grid grid-cols-4 gap-2 sm:grid-cols-8">
                            <label class="cursor-pointer"><input type="radio" name="input_10" value="1" checked class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">1</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_10" value="2" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">2</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_10" value="3" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">3</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_10" value="4" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">4</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_10" value="5" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">5</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_10" value="6" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">6</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_10" value="7" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">7</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_10" value="8" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">8</span></label>
                        </div>
                    </fieldset>

                    <div class="gform_page_footer mt-8 flex justify-end">
                        <button type="button" class="gform_next_button btn-next rounded-xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3 text-sm font-bold text-white shadow-md shadow-orange-600/20 transition-all hover:scale-[1.02] hover:shadow-lg active:scale-[0.98]">Pokračovat</button>
                    </div>
                </div>

                <!-- KROK 2 — Rozměry a množství -->
                <div class="gform_page hidden" id="gform_page_1_2" data-step="1">
                    <h3 class="mb-1 text-lg font-bold text-slate-900">Rozměry a množství</h3>
                    <p class="mb-6 text-sm text-slate-500">Upřesněte rozměry pásky a plánované objednávky.</p>

                    <fieldset class="mb-6">
                        <legend class="mb-3 block text-sm font-semibold text-slate-800">Šíře pásky v mm</legend>
                        <div class="grid grid-cols-3 gap-2 sm:grid-cols-5">
                            <label class="cursor-pointer"><input type="radio" name="input_12" value="19" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">19</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_12" value="25" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">25</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_12" value="38" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">38</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_12" value="50" checked class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">50</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_12" value="75" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">75</span></label>
                        </div>
                    </fieldset>

                    <fieldset class="mb-6">
                        <legend class="mb-3 block text-sm font-semibold text-slate-800">Délka pásky v metrech</legend>
                        <div class="grid grid-cols-4 gap-2 sm:grid-cols-4 lg:grid-cols-8">
                            <label class="cursor-pointer"><input type="radio" name="input_11" value="66" checked class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">66</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_11" value="100" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">100</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_11" value="132" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">132</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_11" value="180" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">180</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_11" value="330" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">330</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_11" value="495" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">495</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_11" value="660" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">660</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_11" value="990" class="peer sr-only"><span class="flex h-11 items-center justify-center rounded-xl border-2 border-slate-200 text-sm font-bold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">990</span></label>
                        </div>
                    </fieldset>

                    <div class="mb-6">
                        <label for="qty" class="mb-2 block text-sm font-semibold text-slate-800">Poptávané množství v kusech <span class="text-orange-600">*</span></label>
                        <input type="number" id="qty" name="input_19" min="360" max="9999" placeholder="360" required class="w-full rounded-xl border border-slate-200 px-4 py-3 text-slate-900 transition-all focus:border-orange-500 focus:outline-none focus:ring-4 focus:ring-orange-500/20">
                        <p class="mt-1 text-xs text-slate-400">Minimální množství je 360 ks.</p>
                        <div id="qty-discount-badge" class="mt-2 overflow-hidden rounded-lg border px-3 py-1.5 text-xs leading-snug transition-all duration-300 ease-out opacity-100 max-h-24 border-slate-200 bg-slate-50 font-medium text-slate-500" role="status" aria-live="polite" aria-atomic="true">
                            <span id="qty-discount-text">Od 360 ks získáváte dopravu zdarma. Doprava trvá přibližně 3–4 týdny.</span>
                        </div>
                    </div>

                    <fieldset>
                        <legend class="mb-3 block text-sm font-semibold text-slate-800">Předpokládaná perioda objednávky</legend>
                        <div class="grid grid-cols-1 gap-2 sm:grid-cols-2">
                            <label class="cursor-pointer"><input type="radio" name="input_18" value="Každý měsíc" checked class="peer sr-only"><span class="block rounded-xl border-2 border-slate-200 px-4 py-3 text-sm font-semibold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">Každý měsíc</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_18" value="Každé 3 měsíce" class="peer sr-only"><span class="block rounded-xl border-2 border-slate-200 px-4 py-3 text-sm font-semibold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">Každé 3 měsíce</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_18" value="Jednou za 6 měsíců" class="peer sr-only"><span class="block rounded-xl border-2 border-slate-200 px-4 py-3 text-sm font-semibold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">Jednou za 6 měsíců</span></label>
                            <label class="cursor-pointer"><input type="radio" name="input_18" value="Jednou za 1 rok" class="peer sr-only"><span class="block rounded-xl border-2 border-slate-200 px-4 py-3 text-sm font-semibold transition-all hover:border-slate-300 peer-checked:border-orange-500 peer-checked:bg-orange-50 peer-checked:text-orange-700">Jednou za 1 rok</span></label>
                        </div>
                    </fieldset>

                    <div class="gform_page_footer mt-8 flex justify-between gap-3">
                        <button type="button" class="gform_previous_button btn-prev rounded-xl border border-slate-200 px-6 py-3 text-sm font-semibold text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50">Zpět</button>
                        <button type="button" class="gform_next_button btn-next rounded-xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3 text-sm font-bold text-white shadow-md shadow-orange-600/20 transition-all hover:scale-[1.02] hover:shadow-lg active:scale-[0.98]">Pokračovat</button>
                    </div>
                </div>

                <!-- KROK 3 -->
                <div class="gform_page hidden" id="gform_page_1_3" data-step="2">
                    <h3 class="mb-1 text-lg font-bold text-slate-900">Firemní a kontaktní údaje</h3>
                    <p class="mb-6 text-sm text-slate-500">Doplňte údaje pro zpracování nezávazné kalkulace.</p>

                    <div class="space-y-4">
                        <div>
                            <label for="company" class="mb-2 block text-sm font-semibold text-slate-800">Název společnosti <span class="text-orange-600">*</span></label>
                            <input type="text" id="company" name="input_20" required class="w-full rounded-xl border border-slate-200 px-4 py-3 text-slate-900 transition-all focus:border-orange-500 focus:outline-none focus:ring-4 focus:ring-orange-500/20">
                        </div>
                        <div>
                            <label for="ico" class="mb-2 block text-sm font-semibold text-slate-800">Vložte IČ Vaší společnosti <span class="text-orange-600">*</span></label>
                            <input type="text" id="ico" name="input_21" required class="w-full rounded-xl border border-slate-200 px-4 py-3 text-slate-900 transition-all focus:border-orange-500 focus:outline-none focus:ring-4 focus:ring-orange-500/20">
                        </div>
                        <div>
                            <label for="name" class="mb-2 block text-sm font-semibold text-slate-800">Jméno a příjmení (Kontaktní osoba) <span class="text-orange-600">*</span></label>
                            <input type="text" id="name" name="input_1" required class="w-full rounded-xl border border-slate-200 px-4 py-3 text-slate-900 transition-all focus:border-orange-500 focus:outline-none focus:ring-4 focus:ring-orange-500/20">
                        </div>
                        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                            <div>
                                <label for="email" class="mb-2 block text-sm font-semibold text-slate-800">E-mail <span class="text-orange-600">*</span></label>
                                <input type="email" id="email" name="input_2" required class="w-full rounded-xl border border-slate-200 px-4 py-3 text-slate-900 transition-all focus:border-orange-500 focus:outline-none focus:ring-4 focus:ring-orange-500/20">
                            </div>
                            <div>
                                <label for="phone" class="mb-2 block text-sm font-semibold text-slate-800">Telefon <span class="text-orange-600">*</span></label>
                                <input type="tel" id="phone" name="input_3" required class="w-full rounded-xl border border-slate-200 px-4 py-3 text-slate-900 transition-all focus:border-orange-500 focus:outline-none focus:ring-4 focus:ring-orange-500/20">
                            </div>
                        </div>
                        <div>
                            <div class="mb-2 flex flex-wrap items-center justify-between gap-2">
                                <label for="note" class="block text-sm font-semibold text-slate-800">Poznámka</label>
                                <button type="button" id="note-sample-btn" class="rounded-lg border border-orange-200 bg-orange-50 px-3 py-1 text-xs font-semibold text-orange-700 transition-colors hover:border-orange-300 hover:bg-orange-100">Mám zájem o vzorek</button>
                            </div>
                            <textarea id="note" name="input_13" rows="3" class="w-full resize-none rounded-xl border border-slate-200 px-4 py-3 text-slate-900 transition-all focus:border-orange-500 focus:outline-none focus:ring-4 focus:ring-orange-500/20"></textarea>
                        </div>
                        <label class="flex cursor-pointer items-start gap-3 rounded-xl border-2 border-slate-200 p-4 transition-all has-[:checked]:border-orange-500 has-[:checked]:bg-orange-50">
                            <input type="checkbox" name="input_14.1" required class="mt-0.5 h-4 w-4 rounded border-slate-300 accent-orange-600 focus:ring-orange-500/20">
                            <span class="text-sm leading-relaxed">Odesláním souhlasíte se <a href="#" class="font-semibold text-orange-600 hover:underline">zpracováním osobních údajů</a> <span class="text-orange-600">*</span></span>
                        </label>
                    </div>

                    <div class="gform_page_footer mt-8 flex flex-col-reverse gap-3 sm:flex-row sm:justify-between">
                        <button type="button" class="gform_previous_button btn-prev rounded-xl border border-slate-200 px-6 py-3 text-sm font-semibold text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50">Zpět</button>
                        <button type="submit" id="gform_submit_button_1" class="gform_button rounded-xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3 text-sm font-bold text-white shadow-md shadow-orange-600/20 transition-all hover:scale-[1.02] hover:shadow-lg active:scale-[0.98]">Odeslat poptávku</button>
                    </div>
                </div>

            </div>
        </form>
    </div>
</section>

<!-- KONTAKTY -->
<section id="kontakt1" class="mx-auto max-w-7xl px-4 pb-20">
    <div class="mb-12 text-center">
        <p class="mb-3 text-sm font-bold uppercase tracking-widest text-orange-600">Tým</p>
        <h2 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl" data-i18n="home.contacts.title">KONTAKTY NA ODDĚLENÍ</h2>
    </div>

    <div class="mx-auto grid max-w-4xl grid-cols-1 gap-8 md:grid-cols-2">
        <article class="flex h-full flex-col rounded-3xl border border-slate-100 bg-white p-8 text-center shadow-sm">
            <img src="<?php echo esc_url( paskyonline_image( 'karel-petrak1.png' ) ); ?>" alt="Ing. Karel Petrák" width="131" height="130" class="mx-auto mb-5 h-28 w-28 rounded-full border-4 border-white object-cover shadow-md ring-2 ring-orange-100">
            <h3 class="text-xl font-bold text-slate-900">Ing. Karel Petrák</h3>
            <p class="mt-1 text-sm text-slate-500">Zastoupení pro prodej balicích pásek</p>
            <div class="mt-6 flex flex-1 flex-col justify-start space-y-3">
                <a href="tel:+420602746017" class="flex items-center justify-center gap-3 rounded-xl border border-slate-100 bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-800 transition-all hover:border-orange-200 hover:bg-orange-50 hover:text-orange-700">
                    <svg class="h-5 w-5 shrink-0 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                    +420 602 746 017
                </a>
                <a href="mailto:karel.petrak@alfain.eu" class="flex items-center justify-center gap-3 rounded-xl border border-slate-100 bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-800 transition-all hover:border-orange-200 hover:bg-orange-50 hover:text-orange-700">
                    <svg class="h-5 w-5 shrink-0 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                    karel.petrak@alfain.eu
                </a>
            </div>
        </article>

        <article class="flex h-full flex-col rounded-3xl border border-slate-100 bg-white p-8 text-center shadow-sm">
            <div class="mx-auto mb-5 flex h-28 w-28 items-center justify-center rounded-full border-4 border-white bg-orange-50 shadow-md ring-2 ring-orange-100" aria-hidden="true">
                <span class="text-2xl font-bold tracking-wide text-orange-600">VP</span>
            </div>
            <h3 class="text-xl font-bold text-slate-900">Vojtěch Petrák</h3>
            <p class="mt-1 text-sm text-slate-500">Asistent prodeje</p>
            <div class="mt-6 flex flex-1 flex-col justify-start space-y-3">
                <a href="tel:+420773216266" class="flex items-center justify-center gap-3 rounded-xl border border-slate-100 bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-800 transition-all hover:border-orange-200 hover:bg-orange-50 hover:text-orange-700">
                    <svg class="h-5 w-5 shrink-0 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                    +420 773 216 266
                </a>
                <a href="mailto:vojtech.petrak@alfain.eu" class="flex items-center justify-center gap-3 rounded-xl border border-slate-100 bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-800 transition-all hover:border-orange-200 hover:bg-orange-50 hover:text-orange-700">
                    <svg class="h-5 w-5 shrink-0 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                    vojtech.petrak@alfain.eu
                </a>
            </div>
        </article>
    </div>

    <div class="mt-12 flex justify-center">
        <a href="https://www.alfain.eu/s99-kontakt" target="_blank" rel="noopener" class="inline-flex items-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-6 py-3 text-sm font-bold text-white shadow-md transition-all hover:scale-[1.02] hover:shadow-lg" data-i18n="footer.more_contacts">Další kontakty</a>
    </div>
</section>

<!-- BANNER VZOREK ZDARMA -->
<section id="vzorek-zdarma" class="px-4 pb-20">
    <div class="mx-auto max-w-7xl">
        <div class="overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8 text-center text-white shadow-xl sm:p-12">
            <p class="mb-3 text-sm font-bold uppercase tracking-widest text-orange-400" data-i18n="home.sample.label">Testovací vzorek</p>
            <h2 class="mx-auto max-w-3xl text-2xl font-extrabold leading-tight tracking-tight sm:text-3xl lg:text-4xl">Nejste si jistí výběrem? Pošleme Vám vzorek zdarma.</h2>
            <p class="mx-auto mt-5 max-w-2xl text-base leading-relaxed text-slate-300 sm:text-lg" data-i18n="home.sample.text">Chápeme, že kvalita lepicí pásky je pro hladký chod Vaší logistiky klíčová. Vyplňte poptávku — poznámku o testovací vzorek doplníme za vás.</p>
            <div class="mt-8 flex justify-center">
                <a href="#gf_1" id="sample-inquiry-cta" class="js-inquiry-sample inline-flex items-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/30 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl hover:shadow-orange-600/40 active:scale-[0.98]" data-i18n="home.sample.cta">Mám zájem o vzorek</a>
            </div>
        </div>
    </div>
</section>
