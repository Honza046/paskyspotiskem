<?php
/**
 * Homepage hero slideshow.
 *
 * @package Paskyonline
 */
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
?>
<section id="uvod" class="relative min-h-svh overflow-hidden">
    <div id="hero-slides" class="absolute inset-0">
        <div class="hero-slide is-active absolute inset-0 bg-cover bg-center" style="background-image:url('<?php echo esc_url( paskyonline_image( 'slide-pasky-1920x624.jpg' ) ); ?>')"></div>
        <div class="hero-slide absolute inset-0 bg-cover bg-center" style="background-image:url('<?php echo esc_url( paskyonline_image( 'slide22-1920x624.jpg' ) ); ?>')"></div>
        <div class="hero-slide absolute inset-0 bg-cover bg-center" style="background-image:url('<?php echo esc_url( paskyonline_image( 'slide3-1920x624.jpg' ) ); ?>')"></div>
    </div>
    <div class="absolute inset-0 bg-gradient-to-r from-slate-950 via-slate-900/80 to-transparent"></div>
    <div class="hero-inner absolute inset-0 flex items-center">
        <div class="mx-auto w-full max-w-7xl px-4">
        <div class="max-w-2xl">
            <div id="hero-content">
                <p class="mb-4 inline-flex items-center rounded-full border border-orange-500/30 bg-orange-500/10 px-4 py-1.5 text-sm font-semibold text-orange-300" data-i18n="home.hero.badge">ISO 9001 · Přímo od výrobce</p>
                <h1 id="hero-title" class="text-4xl font-extrabold leading-tight tracking-tight text-white sm:text-5xl lg:text-6xl">LEPICÍ PÁSKY SE SPODNÍM TISKEM</h1>
                <p id="hero-subtitle" class="mt-6 text-lg leading-relaxed text-slate-300 sm:text-xl">Vysoce spolehlivé BOPP pásky s tiskem chráněným pod folií i ekologické varianty pro udržitelné balení.</p>
            </div>
            <div class="mt-10 flex flex-wrap gap-4">
                <a id="hero-cta-primary" href="#nabidka" class="inline-flex items-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-7 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/25 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl hover:shadow-orange-600/30 active:scale-[0.98]">Prohlédnout nabídku</a>
                <a id="hero-cta-secondary" href="#gf_1" class="inline-flex items-center rounded-2xl border border-white/20 bg-white/10 px-7 py-3.5 text-sm font-bold text-white backdrop-blur-sm transition-all duration-300 hover:border-white/40 hover:bg-white/20">Nezávazná kalkulace</a>
            </div>
        </div>
        </div>
    </div>
    <div id="hero-dots" class="absolute bottom-8 left-1/2 flex -translate-x-1/2 gap-2"></div>
</section>
