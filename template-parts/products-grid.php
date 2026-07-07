<?php
/**
 * Products / benefits grid – Bezpečnost & Lepivost.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
?>

<section class="products-section products-section--benefits">
    <div class="products-grid products-grid--2 products-grid--benefits">
        <article class="product-card product-card--benefit product-card--security">
            <figure class="product-card__benefit-image">
                <img src="<?php echo esc_url( paskyonline_image( 'benefit-tamper-evident.jpg' ) ); ?>" alt="<?php esc_attr_e( 'Lepicí páska TAMPER EVIDENT s VOID efektem', 'paskyonline' ); ?>" loading="lazy">
            </figure>
            <div class="product-card__body">
                <span class="product-card__badge product-card__badge--red"><?php esc_html_e( 'Bezpečnost', 'paskyonline' ); ?></span>
                <h3 class="product-card__title"><?php esc_html_e( 'Lepicí páska TAMPER EVIDENT – porušení zřejmé!', 'paskyonline' ); ?></h3>
                <p class="product-card__text"><?php esc_html_e( 'Tato bezpečnostní lepicí páska se „tváří“ jako neutrální, nicméně při odlepení na krabici zanechává upozornění, které prakticky nelze odstranit. Páska je vhodná pro všechny typy kartonů i stretch folií, lze dodat v různých barvách či i s potiskem.', 'paskyonline' ); ?></p>
                <div class="product-card__tags">
                    <span>VOID</span>
                    <span>OPEN</span>
                    <span>FRAUD</span>
                </div>
            </div>
        </article>

        <article class="product-card product-card--benefit product-card--glue">
            <figure class="product-card__benefit-image">
                <img src="<?php echo esc_url( paskyonline_image( 'Extra-glue.jpg' ) ); ?>" alt="<?php esc_attr_e( 'EXTRA GLUE+ a TACK+ pásky s extrémní lepivostí', 'paskyonline' ); ?>" loading="lazy">
            </figure>
            <div class="product-card__body">
                <span class="product-card__badge product-card__badge--orange"><?php esc_html_e( 'Extrémní lepivost', 'paskyonline' ); ?></span>
                <h3 class="product-card__title"><?php esc_html_e( 'EXTRA GLUE+ (ACRYL) a TACK+ (HOT MELT)', 'paskyonline' ); ?></h3>
                <p class="product-card__text"><?php esc_html_e( 'Pásky se zvýšenou vrstvou lepidla (33 % resp. 20 %) i s možností pevnější folie oproti standardu, určené i pro velmi obtížné aplikace jako např. velmi těžké balíky, nekvalitní kartony nebo prašné prostředí. Na kartonu drží velmi pevně — zjevný důkaz vykradení!', 'paskyonline' ); ?></p>
                <div class="product-card__tags product-card__tags--orange">
                    <span>EXTRA GLUE+</span>
                    <span>TACK+</span>
                    <span>+33 % lepidla</span>
                </div>
            </div>
        </article>
    </div>
</section>

<style>
    .products-section--benefits { padding: 0 1rem 4rem; max-width: 80rem; margin: 0 auto; }
    .products-grid--benefits { display: grid; grid-template-columns: 1fr; gap: 2rem; }
    @media (min-width: 768px) { .products-grid--benefits { grid-template-columns: 1fr 1fr; } }
    .product-card--benefit {
        border: 1px solid #f1f5f9; border-radius: 1.5rem; overflow: hidden;
        background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,.06);
        transition: box-shadow .3s, border-color .3s;
    }
    .product-card--benefit:hover { box-shadow: 0 10px 25px -5px rgba(0,0,0,.1); }
    .product-card--security:hover { border-color: #fecaca; }
    .product-card--glue:hover { border-color: #fed7aa; }
    .product-card__benefit-image {
        margin: 0; height: 14rem; overflow: hidden; background: #fff;
    }
    @media (min-width: 640px) { .product-card__benefit-image { height: 15rem; } }
    .product-card__benefit-image img {
        width: 100%; height: 100%; object-fit: cover; object-position: center;
        transition: transform .5s ease;
    }
    .product-card--benefit:hover .product-card__benefit-image img { transform: scale(1.05); }
    .product-card--glue .product-card__benefit-image {
        display: flex; align-items: center; justify-content: center; padding: 1rem;
    }
    .product-card--glue .product-card__benefit-image img { object-fit: contain; }
    .product-card__badge {
        display: inline-block; padding: .25rem .75rem; border-radius: 9999px;
        font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em;
        margin-bottom: 1rem;
    }
    .product-card__badge--red { color: #b91c1c; border: 1px solid #fecaca; background: #fef2f2; }
    .product-card__badge--orange { color: #c2410c; border: 1px solid #fed7aa; background: #fff7ed; }
    .product-card--benefit .product-card__title { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0 0 1rem; line-height: 1.3; }
    .product-card--benefit .product-card__body { padding: 1.5rem 2rem 2.5rem; }
    .product-card--benefit .product-card__text { color: #475569; line-height: 1.75; margin: 0 0 1.5rem; }
    .product-card__tags { display: flex; flex-wrap: wrap; gap: .5rem; }
    .product-card__tags span {
        padding: .375rem .75rem; border-radius: .5rem; font-size: .875rem; font-weight: 700;
        color: #b91c1c; background: #fef2f2; border: 1px solid #fecaca;
    }
    .product-card__tags--orange span { color: #c2410c; background: #fff7ed; border-color: #fed7aa; }
</style>
