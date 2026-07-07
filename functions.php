<?php
/**
 * ALFA IN – theme functions.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'PASKYONLINE_VERSION', '1.0' );

require_once get_template_directory() . '/inc/i18n.php';
require_once get_template_directory() . '/inc/gallery-data.php';
require_once get_template_directory() . '/inc/references-data.php';
require_once get_template_directory() . '/inc/sortiment-data.php';

/**
 * Theme setup.
 */
function paskyonline_setup() {
    load_theme_textdomain( 'paskyonline', get_template_directory() . '/languages' );

    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support(
        'html5',
        array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script' )
    );

    register_nav_menus(
        array(
            'primary' => __( 'Hlavní menu', 'paskyonline' ),
            'footer'  => __( 'Sociální sítě (patička)', 'paskyonline' ),
        )
    );
}
add_action( 'after_setup_theme', 'paskyonline_setup' );

/**
 * Whether the current request is a Tailwind gallery page.
 */
function paskyonline_is_gallery_page() {
    return is_page_template( 'page-galerie.php' ) || is_post_type_archive( 'galerie' );
}

/**
 * Whether the current request is a sortiment page.
 */
function paskyonline_is_sortiment_page() {
    return is_page_template( 'page-sortiment.php' )
        || is_page_template( 'page-sortiment-kategorie.php' )
        || is_page_template( 'page-sortiment-produkt.php' );
}

/**
 * Enqueue theme styles and scripts.
 */
function paskyonline_enqueue_assets() {
    wp_enqueue_style(
        'paskyonline-style',
        get_stylesheet_uri(),
        array(),
        PASKYONLINE_VERSION
    );

    wp_enqueue_style(
        'paskyonline-logo-carousel',
        get_template_directory_uri() . '/assets/css/logo-carousel.css',
        array( 'paskyonline-style' ),
        PASKYONLINE_VERSION
    );

    wp_enqueue_style(
        'paskyonline-footer-credit',
        get_template_directory_uri() . '/assets/css/footer-credit.css',
        array( 'paskyonline-style' ),
        PASKYONLINE_VERSION
    );

    wp_enqueue_script(
        'paskyonline-nav-active',
        get_template_directory_uri() . '/assets/js/nav-active.js',
        array(),
        PASKYONLINE_VERSION,
        true
    );

    wp_enqueue_script(
        'paskyonline-header-scroll',
        get_template_directory_uri() . '/assets/js/header-scroll.js',
        array(),
        PASKYONLINE_VERSION,
        true
    );

    wp_enqueue_script(
        'paskyonline-footer-credit',
        get_template_directory_uri() . '/assets/js/footer-credit.js',
        array(),
        PASKYONLINE_VERSION,
        true
    );

    wp_enqueue_script(
        'paskyonline-i18n',
        get_template_directory_uri() . '/assets/js/i18n.js',
        array(),
        PASKYONLINE_VERSION,
        true
    );

    wp_localize_script(
        'paskyonline-i18n',
        'paskyonlineI18n',
        array(
            'locale'       => paskyonline_get_locale(),
            'default'      => paskyonline_default_locale(),
            'baseUrl'      => get_template_directory_uri() . '/data/i18n/',
            'supported'    => paskyonline_supported_locales(),
            'homeUrl'      => home_url( '/' ),
            'galleryUrl'   => home_url( '/galerie/' ),
            'sortimentUrl' => home_url( '/sortiment/' ),
        )
    );

    if ( is_front_page() ) {
        wp_enqueue_script(
            'paskyonline-front-page',
            get_template_directory_uri() . '/assets/js/front-page.js',
            array(),
            PASKYONLINE_VERSION,
            true
        );

        wp_enqueue_script(
            'three-js',
            'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js',
            array(),
            '0.160.0',
            true
        );

        wp_enqueue_script(
            'paskyonline-tape-configurator',
            get_template_directory_uri() . '/assets/js/tape-configurator-3d.js',
            array( 'three-js' ),
            PASKYONLINE_VERSION,
            true
        );

        wp_add_inline_script(
            'paskyonline-tape-configurator',
            "document.addEventListener('DOMContentLoaded',function(){if(typeof initTapeConfigurator3D==='function'){initTapeConfigurator3D();}});"
        );
    }

    if ( paskyonline_is_gallery_page() || paskyonline_is_sortiment_page() ) {
        wp_enqueue_script(
            'paskyonline-gallery',
            get_template_directory_uri() . '/assets/js/gallery.js',
            array( 'paskyonline-i18n' ),
            PASKYONLINE_VERSION,
            true
        );
    }

    if ( is_page_template( 'page-sortiment.php' ) ) {
        wp_enqueue_script(
            'paskyonline-sortiment-filter',
            get_template_directory_uri() . '/assets/js/sortiment-filter.js',
            array( 'paskyonline-i18n' ),
            PASKYONLINE_VERSION,
            true
        );
    }
}
add_action( 'wp_enqueue_scripts', 'paskyonline_enqueue_assets' );

/**
 * Helper: theme image URL.
 *
 * @param string $filename Image filename inside /images/.
 */
function paskyonline_image( $filename ) {
    return esc_url( get_template_directory_uri() . '/images/' . ltrim( $filename, '/' ) );
}

/**
 * Helper: partner logo URL from /loga/.
 *
 * @param string $filename Logo filename inside /loga/.
 */
function paskyonline_logo( $filename ) {
    return esc_url( get_template_directory_uri() . '/loga/' . ltrim( $filename, '/' ) );
}

/**
 * Helper: illustrative tape image URL from /Pictures/.
 *
 * @param string $filename Image filename inside /Pictures/.
 */
function paskyonline_picture( $filename ) {
    return esc_url( get_template_directory_uri() . '/Pictures/' . ltrim( $filename, '/' ) );
}

/**
 * Helper: product image URL from a theme-root relative path.
 *
 * @param string $path Path relative to the theme root.
 */
function paskyonline_product_image( $path ) {
    return esc_url( get_template_directory_uri() . '/' . ltrim( $path, '/' ) );
}

/**
 * Fallback primary menu when no WP menu is assigned.
 */
function paskyonline_fallback_menu() {
    $home = esc_url( home_url( '/' ) );
    ?>
    <ul id="menu-hlavni-menu" class="menu">
        <li class="menu-item"><a href="<?php echo $home; ?>#uvod"><?php esc_html_e( 'Úvod', 'paskyonline' ); ?></a></li>
        <li class="menu-item"><a href="<?php echo esc_url( home_url( '/galerie/' ) ); ?>"><?php esc_html_e( 'Galerie', 'paskyonline' ); ?></a></li>
        <li class="menu-item"><a href="<?php echo esc_url( home_url( '/sortiment/' ) ); ?>"><?php esc_html_e( 'Sortiment', 'paskyonline' ); ?></a></li>
        <li class="menu-item"><a href="<?php echo $home; ?>#kontakt1"><?php esc_html_e( 'Kontakty', 'paskyonline' ); ?></a></li>
    </ul>
    <?php
}

/**
 * Fallback footer social menu.
 */
function paskyonline_fallback_footer_menu() {
    ?>
    <ul id="menu-socialni-site" class="menu">
        <li class="menu-item facebook"><a target="_blank" rel="noopener" href="https://www.facebook.com/AlfaIncz">Facebook</a></li>
        <li class="menu-item instagram"><a target="_blank" rel="noopener" href="https://www.instagram.com/AlfaIncz">Instagram</a></li>
        <li class="menu-item youtube"><a target="_blank" rel="noopener" href="https://www.youtube.com/AlfaInas">YouTube</a></li>
    </ul>
    <?php
}
