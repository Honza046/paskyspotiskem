<?php
/**
 * Gallery lightbox overlay (render once, outside <main>).
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

$inquiry_url = paskyonline_gallery_inquiry_url();
?>

<div id="gallery-lightbox" class="gallery-lightbox" role="dialog" aria-modal="true" aria-labelledby="lightbox-title" hidden>
    <div id="lightbox-backdrop" class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm"></div>
    <button type="button" id="lightbox-prev" class="absolute left-2 top-[35%] z-20 flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full border border-white/20 bg-white/90 text-slate-700 shadow-lg transition hover:bg-white hover:text-orange-600 sm:left-4 lg:top-1/2 lg:left-6" aria-label="<?php esc_attr_e( 'Předchozí', 'paskyonline' ); ?>">
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
    </button>
    <button type="button" id="lightbox-next" class="absolute right-2 top-[35%] z-20 flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full border border-white/20 bg-white/90 text-slate-700 shadow-lg transition hover:bg-white hover:text-orange-600 sm:right-4 lg:top-1/2 lg:right-6" aria-label="<?php esc_attr_e( 'Další', 'paskyonline' ); ?>">
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
    </button>
    <div class="relative z-10 w-full max-w-5xl overflow-hidden rounded-2xl bg-white shadow-2xl">
        <button type="button" id="lightbox-close" class="absolute right-3 top-3 z-20 flex h-10 w-10 items-center justify-center rounded-full bg-white/90 text-slate-700 shadow-md transition hover:bg-white hover:text-orange-600" aria-label="<?php esc_attr_e( 'Zavřít', 'paskyonline' ); ?>">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
        <div class="flex flex-col lg:flex-row">
            <div id="lightbox-media" class="relative flex min-h-[220px] items-center justify-center bg-slate-100 lg:w-3/5">
                <img id="lightbox-image" src="" alt="" class="hidden max-h-[50vh] w-full object-contain lg:max-h-[65vh]">
                <div id="lightbox-graphic" class="hidden flex h-full min-h-[220px] w-full flex-col items-center justify-center bg-gradient-to-br from-rose-50 via-white to-orange-50 p-10 text-center lg:min-h-[320px]">
                    <div id="lightbox-graphic-icon" class="mb-4"></div>
                    <span class="text-xs font-bold uppercase tracking-widest text-slate-500"><?php esc_html_e( 'Ukázka technologie', 'paskyonline' ); ?></span>
                </div>
            </div>
            <div class="flex flex-col border-t border-slate-100 p-5 sm:p-6 lg:w-2/5 lg:border-l lg:border-t-0">
                <p id="lightbox-client" class="hidden text-xs font-semibold uppercase tracking-wide text-orange-600"></p>
                <h3 id="lightbox-title" class="text-lg font-bold text-slate-900 sm:text-xl"></h3>
                <dl id="lightbox-meta" class="mt-4 space-y-2 text-sm"></dl>
                <p id="lightbox-description" class="mt-4 flex-1 text-sm leading-relaxed text-slate-600"></p>
                <a id="lightbox-cta" href="<?php echo esc_url( $inquiry_url ); ?>" class="mt-6 inline-flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-orange-600/20 transition-all hover:scale-[1.02] hover:shadow-xl">
                    <?php esc_html_e( 'Chci podobný potisk', 'paskyonline' ); ?>
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
                </a>
            </div>
        </div>
    </div>
</div>
