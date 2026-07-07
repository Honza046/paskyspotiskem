<?php
/**
 * Sortiment – single product detail content.
 *
 * The product is resolved from the current page slug (e.g.
 * "papirova-paska-c690"), so the same template can be assigned to every
 * product subpage. Its parent category is resolved automatically.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

$resolved = isset( $paskyonline_product ) ? $paskyonline_product : null;

if ( null === $resolved ) {
    $slug     = get_post_field( 'post_name', get_queried_object_id() );
    $resolved = paskyonline_get_sortiment_product( $slug );
}

if ( null === $resolved ) {
    ?>
    <section class="mx-auto max-w-3xl px-4 py-24 text-center">
        <h1 class="text-2xl font-extrabold text-slate-900"><?php esc_html_e( 'Produkt nenalezen', 'paskyonline' ); ?></h1>
        <p class="mt-4 text-slate-600"><?php esc_html_e( 'Požadovaná páska neexistuje.', 'paskyonline' ); ?></p>
        <a href="<?php echo esc_url( home_url( '/sortiment/' ) ); ?>" class="mt-8 inline-flex items-center rounded-2xl bg-orange-600 px-6 py-3 text-sm font-bold text-white"><?php esc_html_e( 'Zpět na sortiment', 'paskyonline' ); ?></a>
    </section>
    <?php
    return;
}

$product      = $resolved['product'];
$category     = $resolved['category'];
$category_url = esc_url( home_url( $category['slug'] ) );
$inquiry_url  = esc_url( home_url( '/#gf_1' ) );
$contact_url  = esc_url( home_url( '/#kontakt1' ) );
$params       = isset( $product['params'] ) ? $product['params'] : array();
?>

<!-- Breadcrumb + product header -->
<section class="mx-auto max-w-7xl px-4 py-10 sm:py-14">
    <nav class="mb-8 text-sm text-slate-500" aria-label="Drobečková navigace">
        <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="hover:text-orange-600"><?php esc_html_e( 'Domů', 'paskyonline' ); ?></a>
        <span class="mx-2 text-slate-300">/</span>
        <a href="<?php echo esc_url( home_url( '/sortiment/' ) ); ?>" class="hover:text-orange-600"><?php esc_html_e( 'Sortiment', 'paskyonline' ); ?></a>
        <span class="mx-2 text-slate-300">/</span>
        <a href="<?php echo $category_url; ?>" class="hover:text-orange-600"><?php echo esc_html( $category['title'] ); ?></a>
        <span class="mx-2 text-slate-300">/</span>
        <span class="text-slate-600"><?php echo esc_html( $product['name'] ); ?></span>
    </nav>

    <div class="grid grid-cols-1 gap-10 lg:grid-cols-2 lg:gap-14">
        <div class="flex items-center justify-center rounded-3xl border border-slate-100 bg-white p-8 shadow-sm sm:p-12">
            <img src="<?php echo esc_url( paskyonline_product_image( $product['image'] ) ); ?>" alt="<?php echo esc_attr( $product['name'] ); ?>" class="h-[360px] w-full object-contain mix-blend-multiply contrast-[1.1] brightness-[1.05] sm:h-[440px]">
        </div>
        <div class="flex flex-col justify-center">
            <span class="text-sm font-semibold uppercase tracking-wide text-orange-600"><?php echo esc_html( $category['title'] ); ?></span>
            <h1 class="mt-2 text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl"><?php echo esc_html( $product['name'] ); ?></h1>
            <?php if ( ! empty( $product['tagline'] ) ) : ?>
                <p class="mt-4 text-base leading-relaxed text-slate-600 sm:text-lg"><?php echo esc_html( $product['tagline'] ); ?></p>
            <?php endif; ?>
            <?php if ( ! empty( $params ) ) : ?>
                <div class="mt-6 flex flex-wrap gap-2">
                    <?php
                    $badges = array();
                    foreach ( array( 'Nosič / materiál', 'Typ lepidla', 'Teplotní odolnost' ) as $badge_key ) {
                        if ( isset( $params[ $badge_key ] ) ) {
                            $badges[] = $params[ $badge_key ];
                        }
                    }
                    foreach ( $badges as $badge ) :
                        ?>
                        <span class="rounded-full bg-slate-100 px-4 py-1.5 text-xs font-semibold text-slate-700"><?php echo esc_html( $badge ); ?></span>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>
            <div class="mt-8 flex flex-wrap gap-4">
                <a href="<?php echo $inquiry_url; ?>" class="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/25 transition-all hover:scale-[1.02] hover:shadow-xl">
                    <?php esc_html_e( 'Nezávazně poptat / Kalkulace', 'paskyonline' ); ?>
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
                </a>
                <a href="<?php echo $category_url; ?>" class="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-6 py-3.5 text-sm font-bold text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50">
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M11 17l-5-5m0 0l5-5m-5 5h12"/></svg>
                    <?php esc_html_e( 'Zpět na kategorii', 'paskyonline' ); ?>
                </a>
            </div>
        </div>
    </div>
</section>

<!-- Technical params + benefits -->
<section class="border-t border-slate-100 bg-slate-50">
    <div class="mx-auto max-w-7xl px-4 py-14 sm:py-16">
        <div class="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-16">
            <div>
                <h2 class="mb-6 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl"><?php esc_html_e( 'Technické parametry', 'paskyonline' ); ?></h2>
                <div class="overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm">
                    <table class="w-full">
                        <tbody>
                            <?php foreach ( $params as $key => $value ) : ?>
                                <tr class="border-b border-slate-100 last:border-0">
                                    <th scope="row" class="w-1/2 px-6 py-4 pr-4 text-left align-top text-sm font-semibold text-slate-500"><?php echo esc_html( $key ); ?></th>
                                    <td class="px-6 py-4 text-sm font-semibold text-slate-900"><?php echo esc_html( $value ); ?></td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
                <p class="mt-4 text-xs leading-relaxed text-slate-400"><?php esc_html_e( 'Uvedené hodnoty jsou orientační a mohou se lišit podle konkrétní šířky, návinu a provedení. Rádi vám připravíme přesnou specifikaci na míru.', 'paskyonline' ); ?></p>

                <div class="mt-8">
                    <div class="rounded-2xl border border-orange-100 bg-gradient-to-br from-orange-50/80 to-white p-6 shadow-sm">
                        <h3 class="text-base font-bold text-slate-900"><?php esc_html_e( 'Na míru vašemu provozu', 'paskyonline' ); ?></h3>
                        <ul class="mt-3 space-y-2.5 text-sm leading-relaxed text-slate-600">
                            <li class="flex gap-2"><span class="font-bold text-orange-600" aria-hidden="true">•</span><?php esc_html_e( 'Volitelná šířka a délka návinu', 'paskyonline' ); ?></li>
                            <li class="flex gap-2"><span class="font-bold text-orange-600" aria-hidden="true">•</span><?php esc_html_e( 'Barva podkladu a počet barev potisku', 'paskyonline' ); ?></li>
                            <li class="flex gap-2"><span class="font-bold text-orange-600" aria-hidden="true">•</span><?php esc_html_e( 'Nezávazná kalkulace a vzorek před objednávkou', 'paskyonline' ); ?></li>
                        </ul>
                        <a href="<?php echo $inquiry_url; ?>" class="mt-4 inline-flex items-center gap-1 text-sm font-bold text-orange-600 transition-colors hover:text-orange-700">
                            <?php esc_html_e( 'Nezávazně poptat', 'paskyonline' ); ?>
                            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
                        </a>
                    </div>
                </div>
            </div>
            <div>
                <h2 class="mb-6 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl"><?php esc_html_e( 'Hlavní výhody a použití', 'paskyonline' ); ?></h2>
                <div class="grid grid-cols-1 gap-4">
                    <?php foreach ( $category['properties'] as $property ) : ?>
                        <div class="flex gap-4 rounded-2xl border border-slate-100 bg-white p-6 shadow-sm">
                            <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-orange-50 text-orange-600" aria-hidden="true">
                                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
                            </span>
                            <div>
                                <h3 class="text-base font-bold text-slate-900"><?php echo esc_html( $property['title'] ); ?></h3>
                                <p class="mt-1 text-sm leading-relaxed text-slate-600"><?php echo esc_html( $property['text'] ); ?></p>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>
                <h3 class="mb-4 mt-8 text-lg font-bold text-slate-900"><?php esc_html_e( 'Typické použití', 'paskyonline' ); ?></h3>
                <ul class="grid grid-cols-1 gap-3 sm:grid-cols-2">
                    <?php foreach ( $category['applications'] as $application ) : ?>
                        <li class="flex items-center gap-3 rounded-xl border border-slate-100 bg-white px-5 py-4">
                            <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-orange-50 text-orange-600" aria-hidden="true">
                                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                            </span>
                            <span class="text-sm font-medium text-slate-700"><?php echo esc_html( $application ); ?></span>
                        </li>
                    <?php endforeach; ?>
                </ul>
            </div>
        </div>

        <div class="mx-auto mt-14 max-w-3xl rounded-2xl border border-slate-200 bg-white px-6 py-5 text-center shadow-sm sm:px-8">
            <p class="text-sm leading-relaxed text-slate-600">
                <span class="font-bold text-slate-900"><?php esc_html_e( 'Pásku lze objednat i bez potisku.', 'paskyonline' ); ?></span>
                <?php esc_html_e( 'Pokud nepotřebujete logo na pásku, stejný materiál vám dodáme v nepotištěném provedení, ideální pro okamžité balení nebo skladové zásoby.', 'paskyonline' ); ?>
                <a href="<?php echo $contact_url; ?>" class="font-semibold text-orange-600 transition-colors hover:text-orange-700"><?php esc_html_e( 'Zeptejte se na dostupnost', 'paskyonline' ); ?></a>
            </p>
        </div>

        <div class="mt-8 flex flex-wrap items-center justify-center gap-4">
            <a href="<?php echo $category_url; ?>" class="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-6 py-3 text-sm font-bold text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50">
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M11 17l-5-5m0 0l5-5m-5 5h12"/></svg>
                <?php echo esc_html( sprintf( /* translators: %s: category name */ __( 'Zpět na %s', 'paskyonline' ), $category['title'] ) ); ?>
            </a>
            <a href="<?php echo $contact_url; ?>" class="inline-flex items-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/25 transition-all hover:scale-[1.02] hover:shadow-xl"><?php esc_html_e( 'Mám zájem o tuto pásku', 'paskyonline' ); ?></a>
        </div>
    </div>
</section>
