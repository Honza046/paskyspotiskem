<?php
/**
 * Partner logo filenames for the references carousel.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * @return array<int, array{name: string, file: string}>
 */
function paskyonline_get_reference_logos() {
    return array(
        array( 'name' => 'Alza', 'file' => 'Alza_logo.png', 'mascot' => 'alza-alzak.png' ),
        array( 'name' => 'Tescoma', 'file' => 'tescoma-seeklogo.png' ),
        array( 'name' => 'Pierburg', 'file' => 'RMA_PIERBURG_BAREVNE-pro-dokumenty-a-excel-na-bile-pozadi_KVALITNI.jpg' ),
        array( 'name' => 'Black Tag', 'file' => 'wordmark-blacktag_v=1779091514.png' ),
        array( 'name' => 'Just nahrin', 'file' => 'idCmboYVuN_logos.png' ),
        array( 'name' => 'FIXED', 'file' => 'idOlugJR_G_logos.png' ),
        array( 'name' => 'Dr. Max', 'file' => 'idTeLF6frI_1781781563665.png' ),
        array( 'name' => 'KOH-I-NOOR HARDTMUTH', 'file' => 'idatQHbzbo_1781781887303.png' ),
        array( 'name' => 'CURAPROX', 'file' => 'iddXgbhi7m_logos.png' ),
        array( 'name' => 'Pilulka', 'file' => 'ideXl3nCqb_logos.png' ),
        array( 'name' => 'Mobil Pohotovost', 'file' => 'idgFDwSpdE_logos.png', 'wordmark' => 'Mobil Pohotovost' ),
        array( 'name' => 'Yoggies', 'file' => 'idrXT87fep_logos.png' ),
        array(
            'name'         => 'Global Wines & Spirits',
            'file'         => 'global-wines-spirits-icon.png',
            'wordmark'     => array( 'GLOBAL WINES', '& SPIRITS' ),
            'wordmark_mod' => 'gws',
        ),
    );
}
