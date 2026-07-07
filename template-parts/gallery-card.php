<?php
/**
 * Single gallery card.
 *
 * Expects $item (gallery item array) and optional $featured_layout (bool).
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) || empty( $item ) ) {
    exit;
}

$img_url          = paskyonline_image( $item['image'] );
$is_featured      = ! empty( $featured_layout );
$is_graphic       = ! empty( $item['graphic'] );
$graphic_style    = isset( $item['graphic_style'] ) ? $item['graphic_style'] : 'security';
$adhesive_label   = paskyonline_gallery_adhesive_label( $item['adhesive'] );
$industry_label   = ! empty( $item['industry'] ) ? paskyonline_gallery_industry_label( $item['industry'] ) : '';
$colors_label     = sprintf(
    /* translators: %d: number of print colors */
    _n( '%d barva', '%d barvy', (int) $item['colors'], 'paskyonline' ),
    (int) $item['colors']
);

$graphic_gradients = array(
    'security'   => 'from-rose-50 via-white to-orange-50',
    'glue'       => 'from-amber-50 via-white to-orange-50',
    'industrial' => 'from-slate-50 via-white to-sky-50',
    'warning'    => 'from-yellow-50 via-white to-orange-50',
);
$graphic_gradient = isset( $graphic_gradients[ $graphic_style ] ) ? $graphic_gradients[ $graphic_style ] : $graphic_gradients['security'];

$article_classes = 'group overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm transition-all duration-300 hover:border-slate-200 hover:shadow-lg';
if ( $is_featured ) {
    $article_classes .= ' lg:col-span-2';
}

$data_attrs = array(
    'data-gallery-item'     => '',
    'data-id'               => $item['id'],
    'data-category'         => $item['category'],
    'data-adhesive'         => $item['adhesive'],
    'data-industry'         => $item['industry'],
    'data-type'             => $item['type'],
    'data-featured'         => ! empty( $item['featured'] ) ? 'true' : 'false',
    'data-image'            => $img_url,
    'data-title'            => $item['title'],
    'data-client'           => $item['client'],
    'data-width'            => $item['width'],
    'data-colors'           => (string) $item['colors'],
    'data-adhesive-label'   => $adhesive_label,
    'data-industry-label'   => $industry_label,
    'data-description'      => $item['description'],
    'data-graphic'          => $is_graphic ? 'true' : 'false',
    'data-graphic-style'    => $graphic_style,
);
?>

<article class="<?php echo esc_attr( $article_classes ); ?>"
<?php foreach ( $data_attrs as $key => $value ) : ?>
    <?php echo esc_attr( $key ); ?>="<?php echo esc_attr( $value ); ?>"
<?php endforeach; ?>>
    <button
        type="button"
        data-lightbox-trigger
        class="relative block w-full overflow-hidden text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-orange-500 focus-visible:ring-offset-2 <?php echo $is_featured ? 'aspect-[16/10] lg:aspect-auto lg:min-h-[280px]' : 'aspect-[4/3]'; ?>"
        aria-label="<?php echo esc_attr( sprintf( __( 'Zobrazit detail: %s', 'paskyonline' ), $item['title'] ) ); ?>"
    >
        <?php if ( $is_graphic ) : ?>
            <div class="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br <?php echo esc_attr( $graphic_gradient ); ?> p-8 text-center">
                <?php if ( 'security' === $graphic_style ) : ?>
                    <svg class="mb-4 h-14 w-14 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"/></svg>
                <?php elseif ( 'glue' === $graphic_style ) : ?>
                    <svg class="mb-4 h-14 w-14 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"/></svg>
                <?php else : ?>
                    <svg class="mb-4 h-14 w-14 text-sky-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z"/></svg>
                <?php endif; ?>
                <span class="text-xs font-bold uppercase tracking-widest text-slate-500"><?php esc_html_e( 'Ukázka technologie', 'paskyonline' ); ?></span>
            </div>
        <?php else : ?>
            <img
                src="<?php echo esc_url( $img_url ); ?>"
                alt="<?php echo esc_attr( $item['title'] ); ?>"
                class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                loading="lazy"
            >
        <?php endif; ?>
        <span class="pointer-events-none absolute inset-0 flex items-center justify-center bg-slate-950/0 transition-all duration-300 group-hover:bg-slate-950/40">
            <span class="flex translate-y-2 items-center gap-2 rounded-full bg-white/95 px-4 py-2 text-sm font-semibold text-slate-900 opacity-0 shadow-lg transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100">
                <svg class="h-4 w-4 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35M11 18a7 7 0 100-14 7 7 0 000 14z"/></svg>
                <?php esc_html_e( 'Zobrazit detail', 'paskyonline' ); ?>
            </span>
        </span>
        <?php if ( ! empty( $item['featured'] ) ) : ?>
            <span class="absolute left-3 top-3 rounded-full bg-orange-600 px-3 py-1 text-xs font-bold uppercase tracking-wide text-white shadow-md"><?php esc_html_e( 'Vybraná ukázka', 'paskyonline' ); ?></span>
        <?php endif; ?>
        <?php if ( 'demo' === $item['type'] ) : ?>
            <span class="absolute right-3 top-3 rounded-full border border-slate-200 bg-white/90 px-2.5 py-1 text-xs font-semibold text-slate-600 backdrop-blur-sm"><?php esc_html_e( 'Technologie', 'paskyonline' ); ?></span>
        <?php endif; ?>
    </button>
    <div class="p-4 <?php echo $is_featured ? 'sm:p-5' : ''; ?>">
        <?php if ( ! empty( $item['client'] ) ) : ?>
            <p class="text-xs font-semibold uppercase tracking-wide text-orange-600"><?php echo esc_html( $item['client'] ); ?></p>
        <?php endif; ?>
        <h2 class="<?php echo $is_featured ? 'text-base sm:text-lg' : 'text-sm'; ?> font-bold text-slate-900"><?php echo esc_html( $item['title'] ); ?></h2>
        <div class="mt-2 flex flex-wrap gap-1.5">
            <?php if ( $industry_label ) : ?>
                <span class="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600"><?php echo esc_html( $industry_label ); ?></span>
            <?php endif; ?>
            <span class="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600"><?php echo esc_html( $item['width'] ); ?></span>
            <span class="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600"><?php echo esc_html( $colors_label ); ?></span>
            <span class="rounded-md bg-orange-50 px-2 py-0.5 text-xs font-semibold text-orange-700"><?php echo esc_html( $adhesive_label ); ?></span>
        </div>
    </div>
</article>
