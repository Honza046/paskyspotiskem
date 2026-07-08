<?php
/**
 * Gallery page content: hero, filters, sections, grid, CTA.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

$gallery_items  = paskyonline_get_gallery_items();
$filter_groups  = paskyonline_get_gallery_filter_groups();
$inquiry_url    = paskyonline_gallery_inquiry_url();
$references     = array_values( array_filter( $gallery_items, static function ( $item ) {
    return 'reference' === $item['type'];
} ) );
$demos          = array_values( array_filter( $gallery_items, static function ( $item ) {
    return 'demo' === $item['type'];
} ) );
$featured_items = array_values( array_filter( $gallery_items, static function ( $item ) {
    return ! empty( $item['featured'] );
} ) );
?>

<!-- Hero -->
<section class="border-b border-slate-100 bg-white">
    <div class="mx-auto max-w-7xl px-4 py-10 sm:py-12">
        <p class="mb-2 text-sm font-bold uppercase tracking-widest text-orange-600"><?php esc_html_e( 'Galerie', 'paskyonline' ); ?></p>
        <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div class="max-w-2xl">
                <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl"><?php esc_html_e( 'Ukázky naší práce', 'paskyonline' ); ?></h1>
                <p class="mt-3 text-base leading-relaxed text-slate-600"><?php esc_html_e( 'Reálné reference z výroby i ukázky technologií tisku — filtrujte podle typu potisku, lepidla nebo odvětví.', 'paskyonline' ); ?></p>
            </div>
            <a href="<?php echo esc_url( $inquiry_url ); ?>" class="inline-flex shrink-0 items-center justify-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-orange-600/20 transition-all hover:scale-[1.02] hover:shadow-xl">
                <?php esc_html_e( 'Chci vlastní potisk', 'paskyonline' ); ?>
            </a>
        </div>
    </div>
</section>

<!-- Filter bar -->
<section class="border-b border-slate-100 bg-slate-50">
    <div class="mx-auto max-w-7xl px-4">
        <div id="gallery-filter" class="flex flex-wrap items-center gap-3 py-4 sm:gap-4" data-inquiry="<?php echo esc_url( $inquiry_url ); ?>">
            <div class="flex items-center gap-2 font-medium text-slate-800">
                <svg class="h-5 w-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M3 4h18M6 8h12M9 12h6M11 16h2"/></svg>
                <?php esc_html_e( 'Filtr', 'paskyonline' ); ?>
            </div>

            <?php foreach ( $filter_groups as $group_key => $group ) : ?>
                <div class="relative" data-dropdown>
                    <button type="button" data-dropdown-toggle class="relative flex cursor-pointer items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition-colors hover:border-slate-300 sm:px-5">
                        <span><?php echo esc_html( $group['label'] ); ?></span>
                        <span data-count class="hidden h-5 min-w-[20px] items-center justify-center rounded-full bg-orange-600 px-1.5 text-xs font-bold text-white"></span>
                        <svg data-chevron class="h-4 w-4 text-slate-400 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
                    </button>
                    <div data-dropdown-menu class="absolute left-0 top-full z-50 mt-2 hidden min-w-[220px] flex-col gap-1 rounded-2xl border border-slate-100 bg-white p-3 shadow-xl">
                        <?php foreach ( $group['options'] as $tag => $label ) : ?>
                            <button
                                type="button"
                                data-filter-group="<?php echo esc_attr( $group_key ); ?>"
                                data-tag="<?php echo esc_attr( $tag ); ?>"
                                data-label="<?php echo esc_attr( $label ); ?>"
                                aria-pressed="false"
                                class="flex items-center justify-between gap-3 rounded-xl px-3 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50"
                            >
                                <span><?php echo esc_html( $label ); ?></span>
                                <span data-check class="hidden text-orange-600">
                                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
                                </span>
                            </button>
                        <?php endforeach; ?>
                    </div>
                </div>
            <?php endforeach; ?>

            <div id="gallery-active" class="flex flex-wrap items-center gap-2"></div>
            <button type="button" id="gallery-clear" class="hidden text-sm font-semibold text-slate-500 transition-colors hover:text-orange-600"><?php esc_html_e( 'Vymazat vše', 'paskyonline' ); ?></button>
            <span id="gallery-count" class="ml-auto text-sm font-semibold text-slate-500"></span>
        </div>
    </div>
</section>

<!-- Featured -->
<section id="gallery-featured-section" class="mx-auto max-w-7xl px-4 pt-8 sm:pt-10">
    <div class="mb-5 flex items-center justify-between gap-3">
        <h2 class="text-xl font-extrabold tracking-tight text-slate-900 sm:text-2xl"><?php esc_html_e( 'Vybrané ukázky', 'paskyonline' ); ?></h2>
    </div>
    <div id="gallery-featured" class="grid grid-cols-1 gap-6 lg:grid-cols-4">
        <?php foreach ( $featured_items as $item ) : ?>
            <?php
            $featured_layout = true;
            include locate_template( 'template-parts/gallery-card.php' );
            ?>
        <?php endforeach; ?>
    </div>
</section>

<!-- References -->
<section id="gallery-references-section" class="mx-auto max-w-7xl px-4 pb-4 pt-12 sm:pt-16">
    <div class="mb-6 border-b border-slate-100 pb-4">
        <h2 class="text-xl font-extrabold tracking-tight text-slate-900 sm:text-2xl"><?php esc_html_e( 'Reálné reference', 'paskyonline' ); ?></h2>
        <p class="mt-1 text-sm text-slate-500"><?php esc_html_e( 'Fotografie skutečných potisků z naší výroby. Po novém focení doplníme další reference.', 'paskyonline' ); ?></p>
    </div>
    <div id="gallery-references" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <?php foreach ( $references as $item ) : ?>
            <?php if ( ! empty( $item['featured'] ) ) : ?>
                <?php continue; ?>
            <?php endif; ?>
            <?php
            $featured_layout = false;
            include locate_template( 'template-parts/gallery-card.php' );
            ?>
        <?php endforeach; ?>
    </div>
</section>

<!-- Demos -->
<section id="gallery-demos-section" class="mx-auto max-w-7xl px-4 pb-12 pt-8 sm:pb-16 sm:pt-12">
    <div class="mb-6 border-b border-slate-100 pb-4">
        <h2 class="text-xl font-extrabold tracking-tight text-slate-900 sm:text-2xl"><?php esc_html_e( 'Možnosti tisku a technologie', 'paskyonline' ); ?></h2>
        <p class="mt-1 text-sm text-slate-500"><?php esc_html_e( 'Ukázky bezpečnostních, logistických a speciálních řešení — ilustrace technologií, které nabízíme.', 'paskyonline' ); ?></p>
    </div>
    <div id="gallery-demos" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <?php foreach ( $demos as $item ) : ?>
            <?php
            $featured_layout = false;
            include locate_template( 'template-parts/gallery-card.php' );
            ?>
        <?php endforeach; ?>
    </div>
</section>

<!-- Filtered results -->
<section id="gallery-results-section" class="mx-auto hidden max-w-7xl px-4 py-8 sm:py-10">
    <div id="gallery-empty" class="mb-8 hidden rounded-2xl border border-dashed border-slate-200 bg-white p-12 text-center">
        <p class="text-slate-500"><?php esc_html_e( 'Žádná ukázka neodpovídá vybraným filtrům. Zkuste ubrat některý z filtrů.', 'paskyonline' ); ?></p>
    </div>
    <div id="gallery-results" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"></div>
</section>

<!-- CTA -->
<section class="border-t border-slate-100 bg-white">
    <div class="mx-auto max-w-7xl px-4 py-12 sm:py-16">
        <div class="rounded-3xl bg-gradient-to-br from-orange-600 to-amber-500 px-6 py-10 text-center text-white shadow-xl shadow-orange-600/20 sm:px-12 sm:py-14">
            <h2 class="text-2xl font-extrabold tracking-tight sm:text-3xl"><?php esc_html_e( 'Máte vlastní logo?', 'paskyonline' ); ?></h2>
            <p class="mx-auto mt-3 max-w-xl text-base text-orange-50"><?php esc_html_e( 'Připravíme vám nezávaznou kalkulaci a vzorek potisku. Stačí nám poslat logo a požadované parametry pásky.', 'paskyonline' ); ?></p>
            <a href="<?php echo esc_url( $inquiry_url ); ?>" class="mt-6 inline-flex items-center gap-2 rounded-2xl bg-white px-8 py-3.5 text-sm font-bold text-orange-600 shadow-lg transition-all hover:scale-[1.02] hover:shadow-xl">
                <?php esc_html_e( 'Nezávazně poptat', 'paskyonline' ); ?>
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
            </a>
        </div>
    </div>
</section>
