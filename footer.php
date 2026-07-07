<?php
/**
 * Theme footer – Tailwind layout (matches index.html).
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
?>
<footer id="kontakt1" class="bg-slate-900 text-slate-400">
    <div class="mx-auto grid max-w-7xl gap-10 px-4 py-16 sm:grid-cols-2 lg:grid-cols-4">
        <div>
            <h4 class="mb-4 text-sm font-bold uppercase tracking-wider text-white" data-i18n="footer.address_heading"><?php esc_html_e( 'Najdete nás na adrese', 'paskyonline' ); ?></h4>
            <address class="not-italic leading-relaxed">
                <strong class="text-slate-200">ALFA IN a.s.</strong><br>
                č.p. 74<br>
                675 21 Nová Ves u Třebíče<br>
                <?php esc_html_e( 'Česká republika', 'paskyonline' ); ?>
            </address>
            <a href="https://goo.gl/maps/EYBAoYVGWfB2nPVVA" target="_blank" rel="noopener" class="mt-3 inline-block text-sm font-semibold text-orange-400 hover:text-orange-300" data-i18n="footer.show_on_map"><?php esc_html_e( 'Ukaž na mapě', 'paskyonline' ); ?></a>
        </div>
        <div>
            <h4 class="mb-4 text-sm font-bold uppercase tracking-wider text-white" data-i18n="footer.email_heading"><?php esc_html_e( 'Napište na e-mail', 'paskyonline' ); ?></h4>
            <div class="space-y-2">
                <a href="mailto:karel.petrak@alfain.eu" class="block font-semibold text-slate-300 hover:text-orange-400">karel.petrak@alfain.eu</a>
                <a href="mailto:vojtech.petrak@alfain.eu" class="block font-semibold text-slate-300 hover:text-orange-400">vojtech.petrak@alfain.eu</a>
            </div>
        </div>
        <div>
            <h4 class="mb-4 text-sm font-bold uppercase tracking-wider text-white" data-i18n="footer.phone_heading"><?php esc_html_e( 'Volejte na číslo', 'paskyonline' ); ?></h4>
            <div class="space-y-2">
                <a href="tel:+420602746017" class="block font-semibold text-slate-300 hover:text-orange-400">+420 602 746 017</a>
                <a href="tel:+420773216266" class="block font-semibold text-slate-300 hover:text-orange-400">+420 773 216 266</a>
            </div>
            <p class="mt-2 text-sm"><?php esc_html_e( 'od 7:00 do 15:30 h', 'paskyonline' ); ?></p>
        </div>
        <div>
            <h4 class="mb-4 text-sm font-bold uppercase tracking-wider text-white" data-i18n="footer.social_heading"><?php esc_html_e( 'Sociální sítě', 'paskyonline' ); ?></h4>
            <div class="flex flex-wrap gap-3">
                <a href="https://www.facebook.com/AlfaIncz" target="_blank" rel="noopener" class="inline-flex h-11 w-11 items-center justify-center rounded-xl bg-slate-800 text-slate-300 transition-all hover:bg-[#1877F2] hover:text-white" data-i18n-attr="aria-label:nav.facebook" aria-label="Facebook">
                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                </a>
                <a href="https://www.instagram.com/AlfaIncz" target="_blank" rel="noopener" class="inline-flex h-11 w-11 items-center justify-center rounded-xl bg-slate-800 text-slate-300 transition-all hover:bg-gradient-to-br hover:from-[#f9ce34] hover:via-[#ee2a7b] hover:to-[#6228d7] hover:text-white" data-i18n-attr="aria-label:nav.instagram" aria-label="Instagram">
                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
                </a>
                <a href="https://www.youtube.com/AlfaInas" target="_blank" rel="noopener" class="inline-flex h-11 w-11 items-center justify-center rounded-xl bg-slate-800 text-slate-300 transition-all hover:bg-[#FF0000] hover:text-white" data-i18n-attr="aria-label:nav.youtube" aria-label="YouTube">
                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                </a>
            </div>
        </div>
    </div>
    <div class="border-t border-slate-800">
        <div class="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-4 py-6 text-sm sm:flex-row">
            <div class="flex flex-wrap items-center gap-3">
                <a href="https://www.alfain.eu/" target="_blank" rel="noopener" class="footer-logo shrink-0" aria-label="ALFA IN">
                    <img src="<?php echo esc_url( paskyonline_image( 'logo-footer.svg' ) ); ?>" width="80" height="38" alt="<?php echo esc_attr( get_bloginfo( 'name' ) ); ?>" data-i18n-attr="alt:meta.logo_alt" class="footer-logo__img footer-logo__img--mono">
                    <img src="<?php echo esc_url( paskyonline_image( 'logo.svg' ) ); ?>" width="80" height="38" alt="" aria-hidden="true" class="footer-logo__img footer-logo__img--brand">
                </a>
                <?php echo esc_html( gmdate( 'Y' ) ); ?> ©
                <a href="https://www.alfain.eu" target="_blank" rel="noopener" class="text-slate-300 hover:text-orange-400">ALFA IN a.s.</a>
                | <?php esc_html_e( 'Všechna práva vyhrazena', 'paskyonline' ); ?>
            </div>
            <span class="footer-made-by"><?php esc_html_e( 'vytvořil', 'paskyonline' ); ?> <button type="button" class="footer-credit" aria-label="Jan Sedlář"><span class="footer-credit__text"><?php esc_html_e( 'Jan Sedlář', 'paskyonline' ); ?></span></button></span>
        </div>
    </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
