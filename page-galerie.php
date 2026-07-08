<?php
/**
 * Template Name: Galerie
 * Page template for gallery (Tailwind design).
 *
 * @package Paskyonline
 */

get_header();
?>

<main>
<?php get_template_part( 'template-parts/gallery', 'content' ); ?>
</main>

<?php get_template_part( 'template-parts/gallery', 'lightbox' ); ?>

<?php
get_footer();
