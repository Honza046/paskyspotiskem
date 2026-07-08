<?php
/**
 * Gallery items data.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Returns gallery items for the archive / static page.
 *
 * @return array<int, array<string, mixed>>
 */
function paskyonline_get_gallery_items() {
    return array(
        array(
            'id'          => 'alza',
            'image'       => 'gallery/gallery-alza.jpg',
            'title'       => 'Pásky s logem ALZA',
            'category'    => 'vicebarevny',
            'type'        => 'reference',
            'featured'    => true,
            'client'      => 'Alza',
            'industry'    => 'e-commerce',
            'width'       => '48 mm',
            'colors'      => 3,
            'adhesive'    => 'hot-melt',
            'description' => 'Vícejazyčný brand potisk pro e-commerce balení s opakovaným logem a sloganem na standardní BOPP pásku.',
            'graphic'     => false,
        ),
        array(
            'id'          => 'jednobarevny-firemni',
            'image'       => 'gallery/gallery-jednobarevny-firemni.jpg',
            'title'       => 'Jednobarevný firemní potisk',
            'category'    => 'jednobarevny',
            'type'        => 'reference',
            'featured'    => false,
            'client'      => '',
            'industry'    => 'vyroba',
            'width'       => '48 mm',
            'colors'      => 1,
            'adhesive'    => 'acryl',
            'description' => 'Klasický jednobarevný potisk loga na průhledné nebo bílé BOPP pásky — ideální pro firemní balení a skladovou logistiku.',
            'graphic'     => false,
        ),
        array(
            'id'          => 'flexotisk-8',
            'image'       => 'gallery/gallery-flexotisk-8.jpg',
            'title'       => 'Flexotisk – 8 barev',
            'category'    => 'vicebarevny',
            'type'        => 'reference',
            'featured'    => true,
            'client'      => '',
            'industry'    => 'potraviny',
            'width'       => '48 mm',
            'colors'      => 8,
            'adhesive'    => 'hot-melt',
            'description' => 'Plnobarevný flexotisk s vysokým rozlišením — vhodný pro atraktivní brand na balících páskách i potravinářských aplikacích.',
            'graphic'     => false,
        ),
        array(
            'id'          => 'rototisk-foto',
            'image'       => 'gallery/gallery-rototisk-foto.jpg',
            'title'       => 'Rototisk ve fotokvalitě',
            'category'    => 'vicebarevny',
            'type'        => 'reference',
            'featured'    => false,
            'client'      => '',
            'industry'    => 'potraviny',
            'width'       => '48 mm',
            'colors'      => 6,
            'adhesive'    => 'acryl',
            'description' => 'Rotogravurní tisk s fotografickou kvalitou pro náročné vizuály a dlouhodobou odolnost potisku.',
            'graphic'     => false,
        ),
        array(
            'id'            => 'tamper-void',
            'image'         => 'vykradani.jpg',
            'title'         => 'Tamper Evident VOID',
            'category'      => 'bezpecnostni',
            'type'          => 'demo',
            'featured'      => false,
            'client'        => '',
            'industry'      => 'bezpecnost',
            'width'         => '48 mm',
            'colors'        => 2,
            'adhesive'      => 'acryl',
            'description'   => 'Bezpečnostní páska s VOID efektem — při odlepení zanechá viditelné upozornění, které nelze bez stopy odstranit.',
            'graphic'       => false,
            'graphic_style' => 'security',
        ),
        array(
            'id'            => 'extra-glue',
            'image'         => 'Extra-glue.jpg',
            'title'         => 'EXTRA GLUE+ bezpečnostní série',
            'category'      => 'bezpecnostni',
            'type'          => 'demo',
            'featured'      => false,
            'client'        => '',
            'industry'      => 'bezpecnost',
            'width'         => '48 mm',
            'colors'        => 1,
            'adhesive'      => 'hot-melt',
            'description'   => 'Páska se zvýšenou vrstvou lepidla (+33 %) pro obtížné povrchy, těžké balíky a prašné skladové prostředí.',
            'graphic'       => false,
            'graphic_style' => 'glue',
        ),
        array(
            'id'          => 'pecetni',
            'image'       => 'gallery/gallery-pecetni.jpg',
            'title'       => 'Pečetní páska s potiskem',
            'category'    => 'bezpecnostni',
            'type'        => 'reference',
            'featured'    => false,
            'client'      => '',
            'industry'    => 'bezpecnost',
            'width'       => '48 mm',
            'colors'      => 2,
            'adhesive'    => 'hot-melt',
            'description' => 'Pečetní páska s vlastním potiskem pro zabezpečení zásilek a dokumentů proti neoprávněnému otevření.',
            'graphic'     => false,
        ),
        array(
            'id'          => 'logisticky-kontakty',
            'image'       => 'gallery/gallery-logisticky-kontakty.jpg',
            'title'       => 'Logistický potisk – kontakty',
            'category'    => 'logisticke',
            'type'        => 'reference',
            'featured'    => false,
            'client'      => '',
            'industry'    => 'logistika',
            'width'       => '48 mm',
            'colors'      => 2,
            'adhesive'    => 'hot-melt',
            'description' => 'Informační potisk s kontakty, QR kódem nebo instrukcemi pro příjemce zásilky.',
            'graphic'     => false,
        ),
        array(
            'id'          => 'neutralni-bopp',
            'image'       => 'gallery/gallery-neutralni-bopp.jpg',
            'title'       => 'Neutrální BOPP 25 mm',
            'category'    => 'jednobarevny',
            'type'        => 'reference',
            'featured'    => false,
            'client'      => '',
            'industry'    => 'vyroba',
            'width'       => '25 mm',
            'colors'      => 1,
            'adhesive'    => 'acryl',
            'description' => 'Úzká BOPP páska s jednoduchým potiskem pro ruční balení a lehčí zásilky.',
            'graphic'     => false,
        ),
        array(
            'id'            => 'prumyslova-serie',
            'image'         => 'kapacita.jpg',
            'title'         => 'Průmyslová série pro e-shop',
            'category'      => 'vicebarevny',
            'type'          => 'demo',
            'featured'      => false,
            'client'        => '',
            'industry'      => 'e-commerce',
            'width'         => '48 mm',
            'colors'        => 4,
            'adhesive'      => 'hot-melt',
            'description'   => 'Hromadná výroba potištěných pásek pro e-shopy a fulfillment — konzistentní kvalita v celé sérii.',
            'graphic'       => false,
            'graphic_style' => 'industrial',
        ),
        array(
            'id'          => 'vystrizny-krehke',
            'image'       => 'gallery/gallery-vystrizny-krehke.jpg',
            'title'       => 'Výstražný potisk – křehké',
            'category'    => 'logisticke',
            'type'        => 'demo',
            'featured'    => false,
            'client'      => '',
            'industry'    => 'logistika',
            'width'       => '48 mm',
            'colors'      => 3,
            'adhesive'    => 'acryl',
            'description' => 'Výstražné pásky s potiskem „Křehké“, „Neklopit“ nebo vlastním symbolem pro ochranu zboží při přepravě.',
            'graphic'     => false,
        ),
        array(
            'id'            => 'bezpecnostni-sklad',
            'image'         => 'kradez2-1.jpg',
            'title'         => 'Bezpečnostní páska sklad',
            'category'      => 'logisticke',
            'type'          => 'demo',
            'featured'      => false,
            'client'        => '',
            'industry'      => 'bezpecnost',
            'width'         => '48 mm',
            'colors'        => 1,
            'adhesive'      => 'hot-melt',
            'description'   => 'Kombinace logistického a bezpečnostního potisku pro sklady a distribuční centra.',
            'graphic'       => false,
            'graphic_style' => 'security',
        ),
    );
}

/**
 * Gallery filter dropdown definitions for the compact filter bar.
 *
 * @return array<string, array{label: string, options: array<string, string>}>
 */
function paskyonline_get_gallery_filter_groups() {
    return array(
        'category' => array(
            'label'   => __( 'Typ tisku', 'paskyonline' ),
            'options' => array(
                'jednobarevny' => __( 'Jednobarevný tisk', 'paskyonline' ),
                'vicebarevny'  => __( 'Vícebarevný / Rototisk', 'paskyonline' ),
                'bezpecnostni' => __( 'Bezpečnostní pásky', 'paskyonline' ),
                'logisticke'   => __( 'Logistické / Výstražné', 'paskyonline' ),
            ),
        ),
        'adhesive' => array(
            'label'   => __( 'Lepidlo', 'paskyonline' ),
            'options' => array(
                'hot-melt' => 'Hot Melt',
                'acryl'    => 'Acryl',
            ),
        ),
        'industry' => array(
            'label'   => __( 'Odvětví', 'paskyonline' ),
            'options' => array(
                'e-commerce' => __( 'E-commerce', 'paskyonline' ),
                'vyroba'     => __( 'Výroba', 'paskyonline' ),
                'logistika'  => __( 'Logistika', 'paskyonline' ),
                'potraviny'  => __( 'Potraviny', 'paskyonline' ),
                'bezpecnost' => __( 'Bezpečnost', 'paskyonline' ),
            ),
        ),
        'type'     => array(
            'label'   => __( 'Typ ukázky', 'paskyonline' ),
            'options' => array(
                'reference' => __( 'Reálné reference', 'paskyonline' ),
                'demo'      => __( 'Možnosti tisku', 'paskyonline' ),
            ),
        ),
    );
}

/**
 * Human-readable adhesive label.
 *
 * @param string $slug Adhesive slug.
 */
function paskyonline_gallery_adhesive_label( $slug ) {
    $labels = array(
        'hot-melt' => 'Hot Melt',
        'acryl'    => 'Acryl',
    );

    return isset( $labels[ $slug ] ) ? $labels[ $slug ] : $slug;
}

/**
 * Human-readable industry label.
 *
 * @param string $slug Industry slug.
 */
function paskyonline_gallery_industry_label( $slug ) {
    $labels = array(
        'e-commerce' => __( 'E-commerce', 'paskyonline' ),
        'vyroba'     => __( 'Výroba', 'paskyonline' ),
        'logistika'  => __( 'Logistika', 'paskyonline' ),
        'potraviny'  => __( 'Potraviny', 'paskyonline' ),
        'bezpecnost' => __( 'Bezpečnost', 'paskyonline' ),
    );

    return isset( $labels[ $slug ] ) ? $labels[ $slug ] : $slug;
}

/**
 * Inquiry form URL for gallery CTA links.
 */
function paskyonline_gallery_inquiry_url() {
    if ( function_exists( 'home_url' ) ) {
        return home_url( '/#gf_1' );
    }

    return 'index.html#gf_1';
}

/**
 * Build inquiry URL with optional subject hint.
 *
 * @param array<string, mixed> $item Gallery item.
 */
function paskyonline_gallery_item_inquiry_url( $item ) {
    $base  = paskyonline_gallery_inquiry_url();
    $title = isset( $item['title'] ) ? $item['title'] : '';
    $hash  = '';

    if ( false !== strpos( $base, '#' ) ) {
        list( $base, $hash ) = explode( '#', $base, 2 );
        $hash = '#' . $hash;
    }

    $sep = ( false !== strpos( $base, '?' ) ) ? '&' : '?';

    return $base . $sep . 'poptavka=' . rawurlencode( $title ) . $hash;
}
