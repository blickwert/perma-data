<?php
/**
 * Removes all data of the plugin: tables, options, the Contact Form 7 forms it created.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

defined( 'WP_UNINSTALL_PLUGIN' ) || exit;

global $wpdb;

$bw_map = get_option( 'bw_perma_forms_cf7_forms', [] );
foreach ( is_array( $bw_map ) ? $bw_map : [] as $bw_entry ) {
	if ( ! empty( $bw_entry['id'] ) ) {
		wp_delete_post( (int) $bw_entry['id'], true );
	}
}
foreach ( [ 'bw_perma_contacts', 'bw_perma_contactmeta', 'bw_perma_submissions' ] as $bw_table ) {
	$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . $bw_table ); // phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared -- fixed table names.
}
foreach ( [ 'bw_perma_forms_settings', 'bw_perma_forms_db_version', 'bw_perma_forms_cf7_forms', 'bw_perma_forms_webhook_token' ] as $bw_option ) {
	delete_option( $bw_option );
}
$wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '\\_transient\\_bw\\_pf\\_rl\\_%' OR option_name LIKE '\\_transient\\_timeout\\_bw\\_pf\\_rl\\_%'" );
