<?php
/**
 * Front page template – Tailwind homepage (matches index.html).
 *
 * @package Paskyonline
 */

get_header();

get_template_part( 'template-parts/home', 'hero' );
?>

<main>
<?php get_template_part( 'template-parts/front-page', 'content' ); ?>
</main>

<?php
get_footer();
