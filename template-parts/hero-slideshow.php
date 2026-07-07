<?php
/**
 * Hero slideshow section.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

$slides = array(
    array(
        'image' => paskyonline_image( 'slide-pasky-1920x624.jpg' ),
        'title' => 'LEPICÍ PÁSKY SE SPODNÍM TISKEM',
        'text'  => 'Vysoce spolehlivé BOPP pásky s tiskem chráněným pod folií i ekologické varianty pro udržitelné balení.',
    ),
    array(
        'image' => paskyonline_image( 'slide22-1920x624.jpg' ),
        'title' => 'PROČ SI VYBRAT NÁS?',
        'text'  => 'Více než 30 let zkušeností a spolupráce s předními e-shopy i průmyslovými podniky. Spolehlivost, rychlé dodání a individuální přístup ke každé zakázce.',
    ),
    array(
        'image' => paskyonline_image( 'slide3-1920x624.jpg' ),
        'title' => 'OTESTUJTE NAŠI KVALITU VE SVÉM PROVOZU',
        'text'  => 'Nechte si zaslat bezplatný vzorek nebo nezávaznou kalkulaci na míru. Přesvědčte se o odolnosti a pevnosti lepidla ještě před objednávkou.',
    ),
);
?>

<section class="block slideshow" id="uvod" data-hero-slider>
    <div class="carousel">
        <?php foreach ( $slides as $index => $slide ) : ?>
            <div class="item<?php echo 0 === $index ? ' is-active' : ''; ?>" data-slide>
                <div class="inner" style="background-image: url('<?php echo esc_url( $slide['image'] ); ?>');">
                    <div class="picture-overlay" style="background-color: rgba(0,0,0,0.33);"></div>
                    <div class="container">
                        <div class="content">
                            <h1><?php echo esc_html( $slide['title'] ); ?></h1>
                            <h2><span><?php echo esc_html( $slide['text'] ); ?></span></h2>
                        </div>
                    </div>
                </div>
            </div>
        <?php endforeach; ?>
    </div>

    <div class="slideshow-dots" role="tablist" aria-label="<?php esc_attr_e( 'Výběr snímku', 'paskyonline' ); ?>">
        <?php foreach ( $slides as $index => $slide ) : ?>
            <button
                type="button"
                role="tab"
                aria-label="<?php echo esc_attr( sprintf( __( 'Snímek %d', 'paskyonline' ), $index + 1 ) ); ?>"
                aria-selected="<?php echo 0 === $index ? 'true' : 'false'; ?>"
                class="<?php echo 0 === $index ? 'is-active' : ''; ?>"
                data-slide-dot="<?php echo esc_attr( (string) $index ); ?>"
            ></button>
        <?php endforeach; ?>
    </div>
</section>
