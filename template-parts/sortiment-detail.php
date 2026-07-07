<?php
/**
 * Sortiment – single category detail content.
 *
 * Expects $paskyonline_category to be set before including, otherwise it is
 * resolved from the current page slug.
 *
 * @package Paskyonline
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

$category = isset( $paskyonline_category ) ? $paskyonline_category : null;

if ( null === $category ) {
    $slug     = get_post_field( 'post_name', get_queried_object_id() );
    $category = paskyonline_get_sortiment_category( $slug );
}

if ( null === $category ) {
    ?>
    <section class="mx-auto max-w-3xl px-4 py-24 text-center">
        <h1 class="text-2xl font-extrabold text-slate-900"><?php esc_html_e( 'Kategorie nenalezena', 'paskyonline' ); ?></h1>
        <p class="mt-4 text-slate-600"><?php esc_html_e( 'Požadovaná kategorie pásek neexistuje.', 'paskyonline' ); ?></p>
        <a href="<?php echo esc_url( home_url( '/sortiment/' ) ); ?>" class="mt-8 inline-flex items-center rounded-2xl bg-orange-600 px-6 py-3 text-sm font-bold text-white"><?php esc_html_e( 'Zpět na sortiment', 'paskyonline' ); ?></a>
    </section>
    <?php
    return;
}

$sortiment_url = esc_url( home_url( '/sortiment/' ) );
?>

<!-- Breadcrumb + hero -->
<section class="border-b border-slate-100 bg-gradient-to-b from-white to-slate-50">
    <div class="mx-auto max-w-7xl px-4 py-14 sm:py-16">
        <nav class="mb-6 text-sm text-slate-500" aria-label="Drobečková navigace">
            <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="hover:text-orange-600"><?php esc_html_e( 'Domů', 'paskyonline' ); ?></a>
            <span class="mx-2 text-slate-300">/</span>
            <a href="<?php echo $sortiment_url; ?>" class="font-semibold text-orange-600 hover:text-orange-700"><?php esc_html_e( 'Sortiment', 'paskyonline' ); ?></a>
            <span class="mx-2 text-slate-300">/</span>
            <span class="text-slate-600"><?php echo esc_html( $category['title'] ); ?></span>
        </nav>

        <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div class="max-w-3xl">
                <div class="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-orange-50 text-orange-600" aria-hidden="true">
                    <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>
                </div>
                <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl lg:text-5xl"><?php echo esc_html( $category['title'] ); ?></h1>
                <p class="mt-4 text-base leading-relaxed text-slate-600 sm:text-lg"><?php echo esc_html( $category['intro'] ); ?></p>
            </div>
            <div class="shrink-0">
                <a href="<?php echo esc_url( home_url( '/#gf_1' ) ); ?>" class="inline-flex items-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-7 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/25 transition-all hover:scale-[1.02] hover:shadow-xl"><?php esc_html_e( 'Nezávazná kalkulace', 'paskyonline' ); ?></a>
            </div>
        </div>
    </div>
</section>

<!-- Properties -->
<section class="mx-auto max-w-7xl px-4 py-14 sm:py-16">
    <h2 class="mb-8 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl"><?php esc_html_e( 'Klíčové vlastnosti', 'paskyonline' ); ?></h2>
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <?php foreach ( $category['properties'] as $property ) : ?>
            <article class="flex h-full flex-col rounded-2xl border border-slate-100 bg-white p-7 shadow-sm">
                <div class="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-orange-50 text-orange-600" aria-hidden="true">
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
                </div>
                <h3 class="text-lg font-bold text-slate-900"><?php echo esc_html( $property['title'] ); ?></h3>
                <p class="mt-2 flex-1 text-sm leading-relaxed text-slate-600"><?php echo esc_html( $property['text'] ); ?></p>
            </article>
        <?php endforeach; ?>
    </div>
</section>

<?php if ( ! empty( $category['products'] ) ) : ?>
<!-- Products -->
<section class="border-t border-slate-100 bg-white">
    <div class="mx-auto max-w-7xl px-4 py-14 sm:py-16">
        <h2 class="mb-8 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl"><?php esc_html_e( 'Produkty v této kategorii', 'paskyonline' ); ?></h2>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            <?php
            $category_segment = basename( $category['slug'] );
            foreach ( $category['products'] as $product ) :
                $product_url = esc_url( home_url( '/sortiment/' . $category_segment . '/' . $product['slug'] ) );
                ?>
                <a href="<?php echo $product_url; ?>" class="group flex h-full flex-col overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-orange-100 hover:shadow-lg">
                    <div class="w-full h-64 flex items-center justify-center overflow-hidden p-6 bg-white">
                        <img src="<?php echo esc_url( paskyonline_product_image( $product['image'] ) ); ?>" alt="<?php echo esc_attr( $product['name'] ); ?>" loading="lazy" class="w-full h-full object-contain max-h-56 mix-blend-multiply contrast-[1.1] brightness-[1.05] transform transition-transform duration-300 hover:scale-105">
                    </div>
                    <div class="flex flex-1 flex-col p-6">
                        <h3 class="text-lg font-bold text-slate-900"><?php echo esc_html( $product['name'] ); ?></h3>
                        <?php if ( ! empty( $product['tagline'] ) ) : ?>
                            <p class="mt-2 flex-1 text-sm leading-relaxed text-slate-600"><?php echo esc_html( $product['tagline'] ); ?></p>
                        <?php else : ?>
                            <div class="mt-5 flex-1"></div>
                        <?php endif; ?>
                        <span class="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-orange-600 to-amber-500 px-5 py-3 text-sm font-bold text-white shadow-sm transition-all group-hover:scale-[1.02] group-hover:shadow-md">
                            <?php esc_html_e( 'Zobrazit detail', 'paskyonline' ); ?>
                            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
                        </span>
                    </div>
                </a>
            <?php endforeach; ?>
        </div>
    </div>
</section>
<?php endif; ?>

<!-- Applications -->
<section class="border-t border-slate-100 bg-slate-50">
    <div class="mx-auto max-w-7xl px-4 py-14 sm:py-16">
        <h2 class="mb-8 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl"><?php esc_html_e( 'Typické použití', 'paskyonline' ); ?></h2>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <?php foreach ( $category['applications'] as $application ) : ?>
                <div class="flex items-center gap-3 rounded-xl border border-slate-100 bg-white px-5 py-4">
                    <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-orange-50 text-orange-600" aria-hidden="true">
                        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                    </span>
                    <span class="text-sm font-medium text-slate-700"><?php echo esc_html( $application ); ?></span>
                </div>
            <?php endforeach; ?>
        </div>

        <div class="mt-12 flex flex-wrap items-center justify-center gap-4">
            <a href="<?php echo $sortiment_url; ?>" class="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-6 py-3 text-sm font-bold text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50">
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M11 17l-5-5m0 0l5-5m-5 5h12"/></svg>
                <?php esc_html_e( 'Zpět na sortiment', 'paskyonline' ); ?>
            </a>
            <a href="<?php echo esc_url( home_url( '/#kontakt1' ) ); ?>" class="inline-flex items-center rounded-2xl bg-gradient-to-r from-orange-600 to-amber-500 px-8 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-600/25 transition-all hover:scale-[1.02] hover:shadow-xl"><?php esc_html_e( 'Mám zájem o tuto pásku', 'paskyonline' ); ?></a>
        </div>
    </div>
</section>
