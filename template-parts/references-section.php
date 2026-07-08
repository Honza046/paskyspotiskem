<?php
/**
 * Customer references section.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
?>
<section id="reference" class="border-t border-slate-100 bg-white">
    <div class="mx-auto max-w-7xl px-4 py-20">
        <div class="mb-14 text-center">
            <p class="mb-3 text-sm font-bold uppercase tracking-widest text-orange-600"><?php esc_html_e( 'Reference', 'paskyonline' ); ?></p>
            <h2 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl"><?php esc_html_e( 'Spokojení zákazníci napříč obory', 'paskyonline' ); ?></h2>
            <p class="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-slate-600"><?php esc_html_e( 'Firmy, které na našich páskách s potiskem spoléhají každý den, od e-commerce po výrobu a zdravotnictví.', 'paskyonline' ); ?></p>
        </div>

        <div class="mb-14 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div class="rounded-2xl border border-slate-100 bg-slate-50 px-6 py-5 text-center">
                <p class="text-3xl font-extrabold text-orange-600">300+</p>
                <p class="mt-1 text-sm font-medium text-slate-600"><?php esc_html_e( 'aktivních odběratelů', 'paskyonline' ); ?></p>
            </div>
            <div class="rounded-2xl border border-slate-100 bg-slate-50 px-6 py-5 text-center">
                <p class="text-3xl font-extrabold text-orange-600">30+ let</p>
                <p class="mt-1 text-sm font-medium text-slate-600"><?php esc_html_e( 'zkušeností s potiskem', 'paskyonline' ); ?></p>
            </div>
            <div class="rounded-2xl border border-slate-100 bg-slate-50 px-6 py-5 text-center">
                <p class="text-3xl font-extrabold text-orange-600">ISO 9001</p>
                <p class="mt-1 text-sm font-medium text-slate-600"><?php esc_html_e( 'certifikovaná výroba', 'paskyonline' ); ?></p>
            </div>
        </div>

        <?php get_template_part( 'template-parts/reference-logos', 'carousel' ); ?>
    </div>
</section>
