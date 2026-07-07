<?php
/**
 * Render gallery main content for static galerie.html (stdout).
 *
 * Usage: php scripts/render_gallery_static.php
 */

define( 'ABSPATH', true );

function esc_html( $text ) {
    return htmlspecialchars( (string) $text, ENT_QUOTES, 'UTF-8' );
}

function esc_attr( $text ) {
    return htmlspecialchars( (string) $text, ENT_QUOTES, 'UTF-8' );
}

function esc_url( $url ) {
    return htmlspecialchars( (string) $url, ENT_QUOTES, 'UTF-8' );
}

function esc_html_e( $text ) {
    echo esc_html( $text );
}

function esc_attr_e( $text ) {
    echo esc_attr( $text );
}

function __( $text ) {
    return $text;
}

function _e( $text ) {
    echo $text;
}

function _n( $single, $plural, $number ) {
    return 1 === (int) $number ? $single : $plural;
}

function home_url( $path = '' ) {
    return ltrim( (string) $path, '/' );
}

function locate_template( $path ) {
    return dirname( __DIR__ ) . '/' . ltrim( $path, '/' );
}

function paskyonline_image( $filename ) {
    return 'images/' . ltrim( $filename, '/' );
}

require dirname( __DIR__ ) . '/inc/gallery-data.php';

include dirname( __DIR__ ) . '/template-parts/gallery-content.php';
