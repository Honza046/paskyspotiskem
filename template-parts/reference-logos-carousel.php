<?php
/**
 * Infinite logo carousel for references section.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! function_exists( 'paskyonline_get_reference_logos' ) ) {
    require_once get_template_directory() . '/inc/references-data.php';
}

$logos = paskyonline_get_reference_logos();
if ( empty( $logos ) ) {
    return;
}
?>
<p class="mb-12 mt-16 text-center text-xs font-bold uppercase tracking-widest text-slate-500" data-i18n="home.references.carousel_label"><?php esc_html_e( 'Firmy, které s námi spolupracují', 'paskyonline' ); ?></p>
<div class="logo-carousel pb-4" data-logo-carousel>
    <div class="logo-carousel__viewport">
        <div class="logo-carousel__track" aria-hidden="false">
            <?php for ( $copy = 0; $copy < 2; $copy++ ) : ?>
                <div class="logo-carousel__group"<?php echo $copy === 1 ? ' aria-hidden="true"' : ''; ?>>
                    <?php foreach ( $logos as $logo ) : ?>
                        <?php if ( ! empty( $logo['wordmark'] ) ) : ?>
                            <?php
                            $item_mod = ! empty( $logo['wordmark_mod'] ) ? ' logo-carousel__item--' . sanitize_html_class( $logo['wordmark_mod'] ) : '';
                            $wm_class = 'logo-carousel__wordmark';
                            if ( ! empty( $logo['wordmark_mod'] ) ) {
                                $wm_class .= ' logo-carousel__wordmark--' . sanitize_html_class( $logo['wordmark_mod'] );
                            }
                            $lines = is_array( $logo['wordmark'] ) ? $logo['wordmark'] : array( $logo['wordmark'] );
                            ?>
                            <div class="logo-carousel__item logo-carousel__item--wordmark<?php echo esc_attr( $item_mod ); ?>">
                                <img src="<?php echo paskyonline_logo( $logo['file'] ); ?>" alt="<?php echo $copy === 0 ? esc_attr( $logo['name'] ) : ''; ?>" loading="lazy" decoding="async">
                                <span class="<?php echo esc_attr( $wm_class ); ?>">
                                    <?php foreach ( $lines as $line ) : ?>
                                        <span><?php echo esc_html( $line ); ?></span>
                                    <?php endforeach; ?>
                                </span>
                            </div>
                        <?php else : ?>
                            <?php
                            $item_class = 'logo-carousel__item';
                            if ( ! empty( $logo['mascot'] ) ) {
                                $item_class .= ' logo-carousel__item--alza';
                            }
                            ?>
                            <div class="<?php echo esc_attr( $item_class ); ?>">
                                <img src="<?php echo paskyonline_logo( $logo['file'] ); ?>" alt="<?php echo $copy === 0 ? esc_attr( $logo['name'] ) : ''; ?>" loading="lazy" decoding="async">
                                <?php if ( ! empty( $logo['mascot'] ) ) : ?>
                                    <img src="<?php echo paskyonline_logo( $logo['mascot'] ); ?>" alt="" aria-hidden="true" class="logo-carousel__mascot" loading="lazy" decoding="async">
                                <?php endif; ?>
                            </div>
                        <?php endif; ?>
                    <?php endforeach; ?>
                </div>
            <?php endfor; ?>
        </div>
    </div>
</div>
