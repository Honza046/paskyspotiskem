<?php
/**
 * Internationalization helpers (CS / EN / DE).
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Supported locales.
 *
 * @return string[]
 */
function paskyonline_supported_locales() {
    return array( 'cs', 'en', 'de' );
}

/**
 * Default locale.
 */
function paskyonline_default_locale() {
    return 'cs';
}

/**
 * Detect active locale.
 */
function paskyonline_get_locale() {
    static $locale = null;

    if ( null !== $locale ) {
        return $locale;
    }

    $supported = paskyonline_supported_locales();
    $default   = paskyonline_default_locale();

    if ( isset( $_GET['lang'] ) ) {
        $candidate = sanitize_key( wp_unslash( $_GET['lang'] ) );
        if ( in_array( $candidate, $supported, true ) ) {
            $locale = $candidate;
            return $locale;
        }
    }

    if ( isset( $_COOKIE['paskyonline_lang'] ) ) {
        $candidate = sanitize_key( wp_unslash( $_COOKIE['paskyonline_lang'] ) );
        if ( in_array( $candidate, $supported, true ) ) {
            $locale = $candidate;
            return $locale;
        }
    }

    $wp_locale = get_locale();
    if ( 0 === strpos( $wp_locale, 'de' ) ) {
        $locale = 'de';
        return $locale;
    }
    if ( 0 === strpos( $wp_locale, 'en' ) ) {
        $locale = 'en';
        return $locale;
    }

    $locale = $default;
    return $locale;
}

/**
 * Load translation tree for a locale.
 *
 * @param string|null $locale Locale code.
 * @return array<string, mixed>
 */
function paskyonline_load_translations( $locale = null ) {
    static $cache = array();

    if ( null === $locale ) {
        $locale = paskyonline_get_locale();
    }

    if ( isset( $cache[ $locale ] ) ) {
        return $cache[ $locale ];
    }

    $path = get_template_directory() . '/data/i18n/' . $locale . '.json';
    if ( ! file_exists( $path ) ) {
        $path = get_template_directory() . '/data/i18n/' . paskyonline_default_locale() . '.json';
    }

    $data = array();
    if ( file_exists( $path ) ) {
        $decoded = json_decode( file_get_contents( $path ), true );
        if ( is_array( $decoded ) ) {
            $data = $decoded;
        }
    }

    $cache[ $locale ] = $data;
    return $data;
}

/**
 * Get nested translation by dot path.
 *
 * @param string               $key   Dot path, e.g. nav.home.
 * @param string               $fallback Fallback if missing.
 * @param array<string, mixed> $tree  Optional translation tree.
 */
function paskyonline_translate( $key, $fallback = '', $tree = null ) {
    if ( null === $tree ) {
        $tree = paskyonline_load_translations();
    }

    $parts = explode( '.', $key );
    $value = $tree;

    foreach ( $parts as $part ) {
        if ( ! is_array( $value ) || ! array_key_exists( $part, $value ) ) {
            return $fallback;
        }
        $value = $value[ $part ];
    }

    if ( is_string( $value ) || is_numeric( $value ) ) {
        return (string) $value;
    }

    return $fallback;
}

/**
 * Echo translated string.
 *
 * @param string $key Dot path.
 */
function paskyonline_te( $key, $fallback = '' ) {
    echo esc_html( paskyonline_translate( $key, $fallback ) );
}

/**
 * Build URL with lang query arg.
 *
 * @param string $locale Locale code.
 * @param string $url    Optional base URL.
 */
function paskyonline_locale_url( $locale, $url = '' ) {
    if ( ! $url ) {
        $url = home_url( add_query_arg( array() ) );
    }

    return add_query_arg( 'lang', $locale, $url );
}

/**
 * Enqueue i18n script + pass bootstrap data.
 */
function paskyonline_enqueue_i18n_assets() {
    // Handled in paskyonline_enqueue_gallery_assets for tailwind + front page.
}
add_action( 'wp_enqueue_scripts', 'paskyonline_enqueue_i18n_assets', 25 );

/**
 * Persist lang cookie when switching.
 */
function paskyonline_set_lang_cookie() {
    if ( empty( $_GET['lang'] ) ) {
        return;
    }

    $locale = sanitize_key( wp_unslash( $_GET['lang'] ) );
    if ( ! in_array( $locale, paskyonline_supported_locales(), true ) ) {
        return;
    }

    if ( ! headers_sent() ) {
        setcookie( 'paskyonline_lang', $locale, time() + YEAR_IN_SECONDS, COOKIEPATH, COOKIE_DOMAIN, is_ssl(), false );
    }
}
add_action( 'init', 'paskyonline_set_lang_cookie' );
