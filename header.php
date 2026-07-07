<?php
/**
 * Theme header – Tailwind layout (matches index.html).
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

$home          = esc_url( home_url( '/' ) );
$gallery_url   = esc_url( home_url( '/galerie/' ) );
$sortiment_url = esc_url( home_url( '/sortiment/' ) );
$is_gallery    = is_page_template( 'page-galerie.php' ) || is_post_type_archive( 'galerie' );
$is_sortiment  = is_page_template( 'page-sortiment.php' )
    || is_page_template( 'page-sortiment-kategorie.php' )
    || is_page_template( 'page-sortiment-produkt.php' );
$nav_page      = $is_gallery ? 'gallery' : ( $is_sortiment ? 'sortiment' : ( is_front_page() ? 'home' : 'other' ) );
$nav_link      = 'px-2 py-1 text-sm font-semibold text-slate-700 transition-colors hover:text-orange-600';
$nav_active    = 'px-2 py-1 text-sm font-semibold text-orange-600';
$mobile_link   = 'block px-2 py-2 font-semibold text-slate-800 transition-colors hover:text-orange-600';
$mobile_active = 'block px-2 py-2 font-semibold text-orange-600';
$theme_uri     = get_template_directory_uri();
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script>
    (function () {
        if ('scrollRestoration' in history) {
            history.scrollRestoration = 'manual';
        }
        if (!window.location.hash) {
            var html = document.documentElement;
            html.classList.add('scroll-lock');
            html.style.scrollBehavior = 'auto';
            html.scrollTop = 0;
            window.scrollTo(0, 0);
        }
        function resetScroll() {
            if (window.location.hash) {
                return;
            }
            var html = document.documentElement;
            var prev = html.style.scrollBehavior;
            html.style.scrollBehavior = 'auto';
            html.scrollTop = 0;
            if (document.body) {
                document.body.scrollTop = 0;
            }
            window.scrollTo(0, 0);
            html.style.scrollBehavior = prev;
        }
        function unlockScroll() {
            resetScroll();
            document.documentElement.classList.remove('scroll-lock');
        }
        document.addEventListener('DOMContentLoaded', function () {
            resetScroll();
            requestAnimationFrame(resetScroll);
        });
        window.addEventListener('load', function () {
            requestAnimationFrame(function () {
                requestAnimationFrame(unlockScroll);
            });
        });
        window.addEventListener('pageshow', function () {
            if (!window.location.hash) {
                document.documentElement.classList.add('scroll-lock');
                resetScroll();
                requestAnimationFrame(function () {
                    requestAnimationFrame(unlockScroll);
                });
            }
        });
    })();
    </script>
    <meta name="theme-color" content="#ffffff">
    <meta name="msapplication-TileColor" content="#e67517">

    <link rel="apple-touch-icon" sizes="180x180" href="<?php echo esc_url( $theme_uri . '/icons/apple-touch-icon.png' ); ?>">
    <link rel="icon" type="image/png" sizes="32x32" href="<?php echo esc_url( $theme_uri . '/icons/favicon-32x32.png' ); ?>">
    <link rel="icon" type="image/png" sizes="16x16" href="<?php echo esc_url( $theme_uri . '/icons/favicon-16x16.png' ); ?>">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">

    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
                    },
                },
            },
        };
    </script>

    <?php wp_head(); ?>
</head>
<body <?php body_class( 'select-none bg-slate-50 font-sans text-slate-600 antialiased' ); ?> data-page="<?php echo esc_attr( $nav_page ); ?>">
<?php wp_body_open(); ?>

<header class="site-header sticky top-0 z-50 border-b border-slate-100 bg-white/90 backdrop-blur-md transition-transform duration-300 ease-in-out will-change-transform">
    <div class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4">
        <a href="<?php echo $home; ?>" class="flex shrink-0 items-center gap-1.5">
            <img src="<?php echo esc_url( paskyonline_image( 'logo.svg' ) ); ?>" width="160" height="74" alt="<?php echo esc_attr( get_bloginfo( 'name' ) ); ?>" data-i18n-attr="alt:meta.logo_alt" class="h-12 w-auto lg:h-14">
            <span class="hidden text-sm text-slate-500 sm:block" data-i18n="meta.site_name"><?php bloginfo( 'description' ); ?></span>
        </a>
        <div class="flex items-center gap-2 lg:gap-4">
            <nav id="main-nav" class="hidden lg:block" aria-label="<?php esc_attr_e( 'Hlavní navigace', 'paskyonline' ); ?>" data-i18n-attr="aria-label:nav.main_nav_label">
                <ul class="flex items-center gap-1">
                    <li><a href="<?php echo $home; ?>#uvod" class="<?php echo esc_attr( $nav_link ); ?>" data-i18n="nav.home"><?php esc_html_e( 'Úvod', 'paskyonline' ); ?></a></li>
                    <li><a href="<?php echo $gallery_url; ?>" class="<?php echo esc_attr( $is_gallery ? $nav_active : $nav_link ); ?>" data-i18n="nav.gallery"><?php esc_html_e( 'Galerie', 'paskyonline' ); ?></a></li>
                    <li><a href="<?php echo $sortiment_url; ?>" class="<?php echo esc_attr( $is_sortiment ? $nav_active : $nav_link ); ?>" data-i18n="nav.sortiment"><?php esc_html_e( 'Sortiment', 'paskyonline' ); ?></a></li>
                    <li><a href="<?php echo $home; ?>#reference" class="<?php echo esc_attr( $nav_link ); ?>" data-i18n="nav.references"><?php esc_html_e( 'Reference', 'paskyonline' ); ?></a></li>
                    <li><a href="<?php echo $home; ?>#kontakt1" class="<?php echo esc_attr( $nav_link ); ?>" data-i18n="nav.contacts"><?php esc_html_e( 'Kontakty', 'paskyonline' ); ?></a></li>
                </ul>
            </nav>
            <div data-lang-switcher class="relative shrink-0" aria-label="Language"></div>
            <button id="menu-toggle" type="button" class="inline-flex items-center rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50 lg:hidden" aria-expanded="false" aria-controls="main-nav" data-i18n="nav.menu"><?php esc_html_e( 'Menu', 'paskyonline' ); ?></button>
        </div>
    </div>
    <nav id="mobile-nav" class="hidden border-t border-slate-100 bg-white px-4 py-4 lg:hidden">
        <ul class="space-y-1">
            <li><a href="<?php echo $home; ?>#uvod" class="<?php echo esc_attr( $mobile_link ); ?>" data-i18n="nav.home"><?php esc_html_e( 'Úvod', 'paskyonline' ); ?></a></li>
            <li><a href="<?php echo $gallery_url; ?>" class="<?php echo esc_attr( $is_gallery ? $mobile_active : $mobile_link ); ?>" data-i18n="nav.gallery"><?php esc_html_e( 'Galerie', 'paskyonline' ); ?></a></li>
            <li><a href="<?php echo $sortiment_url; ?>" class="<?php echo esc_attr( $is_sortiment ? $mobile_active : $mobile_link ); ?>" data-i18n="nav.sortiment"><?php esc_html_e( 'Sortiment', 'paskyonline' ); ?></a></li>
            <li><a href="<?php echo $home; ?>#reference" class="<?php echo esc_attr( $mobile_link ); ?>" data-i18n="nav.references"><?php esc_html_e( 'Reference', 'paskyonline' ); ?></a></li>
            <li><a href="<?php echo $home; ?>#kontakt1" class="<?php echo esc_attr( $mobile_link ); ?>" data-i18n="nav.contacts"><?php esc_html_e( 'Kontakty', 'paskyonline' ); ?></a></li>
        </ul>
    </nav>
</header>
