<?php
/**
 * Names of the contact tables; registers the meta table for the WordPress metadata API.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Repository;

final class Tables {

	/** Meta type for add_metadata() & co.: table {prefix}bw_perma_contactmeta, column bw_perma_contact_id. */
	public const META_TYPE = 'bw_perma_contact';

	public static function register(): void {
		global $wpdb;
		$wpdb->bw_perma_contactmeta = self::meta();
	}

	public static function contacts(): string {
		global $wpdb;
		return $wpdb->prefix . 'bw_perma_contacts';
	}

	public static function meta(): string {
		global $wpdb;
		return $wpdb->prefix . 'bw_perma_contactmeta';
	}

	public static function submissions(): string {
		global $wpdb;
		return $wpdb->prefix . 'bw_perma_submissions';
	}
}
