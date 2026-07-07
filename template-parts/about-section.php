<?php
/**
 * "O nás" – two-column about section (front page).
 *
 * Self-contained styling so it renders correctly on the classic front page
 * (which does not load Tailwind).
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
?>

<section class="about-section" id="o-nas">
    <div class="about-inner">
        <div class="about-text">
            <span class="about-eyebrow"><?php esc_html_e( 'O nás', 'paskyonline' ); ?></span>
            <h2 class="about-title"><?php esc_html_e( 'Tradiční český výrobce lepicích pásek s potiskem', 'paskyonline' ); ?></h2>
            <p class="about-lead"><?php esc_html_e( 'Již více než 25 let pomáháme firmám bezpečně balit jejich zásilky a budovat silnou značku přímo na balicích materiálech. Jsme specialisté na zakázkový potisk lepicích pásek.', 'paskyonline' ); ?></p>
            <p class="about-para"><?php esc_html_e( 'Naše moderní výrobní zázemí nám umožňuje flexibilně reagovat na potřeby jak malých e-shopů, tak velkých průmyslových podniků. Zakládáme si na precizním tisku (až 8 barev), špičkové kvalitě použitých lepidel (Hot Melt, Akryl) a rychlém doručení po celé České republice.', 'paskyonline' ); ?></p>
            <p class="about-para"><?php esc_html_e( 'Díky certifikovaným procesům ISO 9001 a využívání ekologických, udržovatelných materiálů jsme stabilním partnerem pro více než 100 aktivních odběratelů.', 'paskyonline' ); ?></p>
        </div>
        <div class="about-media">
            <img src="<?php echo esc_url( paskyonline_image( 'kapacita.jpg' ) ); ?>" alt="<?php esc_attr_e( 'Výroba lepicích pásek ALFA IN', 'paskyonline' ); ?>" loading="lazy">
        </div>
    </div>
</section>

<style>
    .about-section { padding: 4rem 1rem; background: #ffffff; }
    .about-inner {
        max-width: 80rem;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1fr;
        gap: 3rem;
        align-items: center;
    }
    .about-eyebrow {
        display: inline-block;
        color: #ea580c;
        font-size: .75rem;
        font-weight: 700;
        letter-spacing: .15em;
        text-transform: uppercase;
    }
    .about-title {
        margin: .5rem 0 1.5rem;
        color: #0f172a;
        font-size: 1.875rem;
        line-height: 1.2;
        font-weight: 700;
    }
    .about-lead { margin: 0 0 1rem; color: #334155; font-size: 1.125rem; font-weight: 500; line-height: 1.6; }
    .about-para { margin: 0 0 1.5rem; color: #475569; font-size: 1rem; line-height: 1.75; }
    .about-para:last-child { margin-bottom: 0; }
    .about-media {
        position: relative;
        width: 100%;
        height: 400px;
        border-radius: 1.5rem;
        overflow: hidden;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,.1);
        border: 1px solid #f1f5f9;
    }
    .about-media img { width: 100%; height: 100%; object-fit: cover; display: block; }
    @media (min-width: 1024px) {
        .about-inner { grid-template-columns: 1fr 1fr; gap: 3rem; }
        .about-section { padding: 6rem 1rem; }
        .about-title { font-size: 2.25rem; }
    }
</style>
