<?php
/**
 * Sortiment page – product category directory (Magis-style) with tag filter.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

$categories = paskyonline_get_sortiment_categories();

// Flat product list for the client-side tag filter.
$js_products = array();
foreach ( $categories as $category ) {
    if ( empty( $category['products'] ) ) {
        continue;
    }
    $category_segment = basename( $category['slug'] );
    foreach ( $category['products'] as $product ) {
        $js_products[] = array(
            'name'     => $product['name'],
            'tagline'  => isset( $product['tagline'] ) ? $product['tagline'] : '',
            'image'    => paskyonline_product_image( $product['image'] ),
            'detail'   => esc_url( home_url( '/sortiment/' . $category_segment . '/' . $product['slug'] ) ),
            'category' => $category['title'],
            'tags'     => isset( $product['tags'] ) ? array_values( $product['tags'] ) : array(),
        );
    }
}

/**
 * Renders a single dropdown menu item (toggleable filter tag).
 *
 * @param string $tag   Tag slug.
 * @param string $label Human label.
 */
function paskyonline_filter_item( $tag, $label ) {
    printf(
        '<button type="button" data-tag="%1$s" data-label="%2$s" aria-pressed="false" class="flex items-center justify-between gap-3 rounded-xl px-3 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50"><span>%2$s</span><span data-check class="hidden text-orange-600"><svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg></span></button>',
        esc_attr( $tag ),
        esc_html( $label )
    );
}

/**
 * Renders a dropdown toggle button opener with chevron + count badge.
 *
 * @param string $label Dropdown label.
 */
function paskyonline_filter_dropdown_open( $label ) {
    printf(
        '<button type="button" data-dropdown-toggle class="relative flex cursor-pointer items-center gap-2 rounded-full border border-slate-200 bg-white px-5 py-2 text-sm font-medium text-slate-700 transition-colors hover:border-slate-300"><span>%s</span><span data-count class="hidden h-5 min-w-[20px] items-center justify-center rounded-full bg-orange-600 px-1.5 text-xs font-bold text-white"></span><svg data-chevron class="h-4 w-4 text-slate-400 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg></button>',
        esc_html( $label )
    );
}
?>

<!-- Hero -->
<section class="border-b border-slate-100 bg-gradient-to-b from-white to-slate-50">
    <div class="mx-auto max-w-7xl px-4 py-16 text-center sm:py-20">
        <p class="mb-3 text-sm font-bold uppercase tracking-widest text-orange-600"><?php esc_html_e( 'Sortiment', 'paskyonline' ); ?></p>
        <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl lg:text-5xl"><?php esc_html_e( 'Objevte naše lepicí pásky', 'paskyonline' ); ?></h1>
        <p class="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-slate-600 sm:text-lg"><?php esc_html_e( 'Vyberte typ produktu podle materiálu a určení. U každé kategorie najdete detailní přehled dostupných variant.', 'paskyonline' ); ?></p>
    </div>
</section>

<!-- Filter bar -->
<section class="mx-auto max-w-7xl px-4 pt-4 sm:pt-6">
    <div id="sortiment-filter" class="mb-0 flex flex-wrap items-center gap-4 border-b border-slate-100 py-4">
        <div class="flex items-center gap-2 font-medium text-slate-800">
            <svg class="h-5 w-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M3 4h18M6 8h12M9 12h6M11 16h2"/></svg>
            <?php esc_html_e( 'Filtr', 'paskyonline' ); ?>
        </div>

        <div class="relative" data-dropdown>
            <?php paskyonline_filter_dropdown_open( __( 'Vlastnosti', 'paskyonline' ) ); ?>
            <div data-dropdown-menu class="absolute left-0 top-full z-50 mt-2 hidden min-w-[220px] flex-col gap-2 rounded-2xl border border-slate-100 bg-white p-4 shadow-xl flex">
                <?php
                paskyonline_filter_item( 'ekologicke', __( 'Ekologické', 'paskyonline' ) );
                paskyonline_filter_item( 'tiche', __( 'Tiché (Low Noise)', 'paskyonline' ) );
                paskyonline_filter_item( 'odstranitelne', __( 'Odstranitelné bez stop', 'paskyonline' ) );
                paskyonline_filter_item( 'vyztuzene', __( 'Vyztužené', 'paskyonline' ) );
                ?>
            </div>
        </div>

        <div class="relative" data-dropdown>
            <?php paskyonline_filter_dropdown_open( __( 'Odolnost', 'paskyonline' ) ); ?>
            <div data-dropdown-menu class="absolute left-0 top-full z-50 mt-2 hidden min-w-[220px] flex-col gap-2 rounded-2xl border border-slate-100 bg-white p-4 shadow-xl flex">
                <?php
                paskyonline_filter_item( 'mrazuvzdorne', __( 'Mrazuvzdorné (do −70 °C)', 'paskyonline' ) );
                paskyonline_filter_item( 'vysoke-teploty', __( 'Vysoké teploty', 'paskyonline' ) );
                paskyonline_filter_item( 'chemicka-odolnost', __( 'Chemická odolnost', 'paskyonline' ) );
                ?>
            </div>
        </div>

        <div class="relative" data-dropdown>
            <?php paskyonline_filter_dropdown_open( __( 'Použití', 'paskyonline' ) ); ?>
            <div data-dropdown-menu class="absolute left-0 top-full z-50 mt-2 hidden min-w-[220px] flex-col gap-2 rounded-2xl border border-slate-100 bg-white p-4 shadow-xl flex">
                <?php
                paskyonline_filter_item( 'rucni', __( 'Ruční aplikace', 'paskyonline' ) );
                paskyonline_filter_item( 'stroje', __( 'Stroje a baličky', 'paskyonline' ) );
                ?>
            </div>
        </div>

        <div id="sortiment-active" class="flex flex-wrap items-center gap-2"></div>
        <button type="button" id="sortiment-clear" class="hidden text-sm font-semibold text-slate-500 transition-colors hover:text-orange-600"><?php esc_html_e( 'Vymazat vše', 'paskyonline' ); ?></button>
    </div>
</section>

<!-- Filtered product results -->
<section id="sortiment-results" class="mx-auto hidden max-w-7xl px-4 py-12 sm:py-16">
    <div class="flex flex-wrap items-center justify-between gap-3">
        <h2 class="text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl"><?php esc_html_e( 'Nalezené produkty podle filtrů', 'paskyonline' ); ?></h2>
        <span id="sortiment-results-count" class="text-sm font-semibold text-slate-500"></span>
    </div>
    <div id="sortiment-results-grid" data-inquiry="<?php echo esc_url( home_url( '/#gf_1' ) ); ?>" class="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3"></div>
    <div id="sortiment-empty" class="mt-8 hidden rounded-2xl border border-dashed border-slate-200 bg-white p-12 text-center">
        <p class="text-slate-500"><?php esc_html_e( 'Žádná páska neodpovídá vybrané kombinaci filtrů. Zkuste ubrat některý z filtrů.', 'paskyonline' ); ?></p>
    </div>
</section>

<!-- Category directory -->
<section id="sortiment-categories" class="mx-auto max-w-7xl px-4 pb-12 pt-4 sm:pt-6">
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <?php foreach ( $categories as $category ) : ?>
            <a
                href="<?php echo esc_url( home_url( $category['slug'] ) ); ?>"
                class="group relative flex h-full cursor-pointer flex-col overflow-hidden rounded-2xl border border-slate-100 bg-white p-8 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-orange-100 hover:shadow-lg"
            >
                <img src="<?php echo esc_url( paskyonline_product_image( $category['image'] ) ); ?>" alt="" aria-hidden="true" class="absolute right-[-15%] bottom-[-10%] w-80 h-80 object-contain opacity-20 pointer-events-none transform rotate-12 transition-all duration-500 ease-out group-hover:scale-[1.15] group-hover:-rotate-3">
                <div class="relative z-10 flex h-full flex-col">
                    <h3 class="text-xl font-bold text-slate-900"><?php echo esc_html( $category['title'] ); ?></h3>
                    <p class="mt-3 flex-1 text-sm leading-relaxed text-slate-600"><?php echo esc_html( $category['description'] ); ?></p>
                    <span class="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-orange-600">
                        <?php esc_html_e( 'Zobrazit produkty', 'paskyonline' ); ?>
                        <svg class="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
                    </span>
                </div>
            </a>
        <?php endforeach; ?>
    </div>

    <div class="mt-14 text-center">
        <a href="<?php echo esc_url( home_url( '/#gf_1' ) ); ?>" class="inline-flex items-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/25 transition-all hover:scale-[1.02] hover:shadow-xl"><?php esc_html_e( 'Nezávazná kalkulace', 'paskyonline' ); ?></a>
    </div>
</section>

<script id="sortiment-products" type="application/json"><?php echo wp_json_encode( $js_products ); ?></script>
