<?php
/**
 * Dev only: creates the pages from wordpress/content/ in a local WordPress Playground.
 * Mount wordpress/content at /perma-content and this file in the web root, then open /seed-pages.php.
 *
 * @package PermaMind
 */

declare(strict_types=1);

require '/wordpress/wp-load.php';
header( 'Content-Type: text/plain; charset=utf-8' );

$bw_dir  = '/perma-content/';
$bw_data = json_decode( (string) file_get_contents( $bw_dir . 'pages.json' ), true );
foreach ( $bw_data['pages'] as $bw_page ) {
	$bw_markup = (string) file_get_contents( $bw_dir . $bw_page['file'] );
	$bw_markup = (string) preg_replace_callback( '/\{\{home:([^}]*)\}\}/', static fn( array $m ): string => esc_url( home_url( $m[1] ) ), $bw_markup );
	$bw_markup = (string) preg_replace_callback( '/\{\{asset:([^}]*)\}\}/', static fn( array $m ): string => esc_url( get_theme_file_uri( $m[1] ) ), $bw_markup );
	$bw_old    = get_page_by_path( $bw_page['slug'] );
	$bw_id     = wp_insert_post(
		[
			'ID'            => $bw_old ? $bw_old->ID : 0,
			'post_type'     => 'page',
			'post_status'   => 'publish',
			'post_title'    => $bw_page['title'],
			'post_name'     => $bw_page['slug'],
			'post_content'  => wp_slash( $bw_markup ),
			'page_template' => $bw_page['template'],
		]
	);
	if ( $bw_page['front_page'] ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $bw_id );
	}
	echo esc_html( $bw_page['slug'] . ' => ' . $bw_id ) . "\n";
}
flush_rewrite_rules();
