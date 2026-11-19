<?php
/**
 * Creates and upgrades the database tables.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Core;

use BW\PermaForms\Modules\Contacts\Repository\Tables;

final class Installer {

	public const DB_VERSION        = '1';
	public const DB_VERSION_OPTION = 'bw_perma_forms_db_version';

	/** Runs on plugin activation. */
	public static function activate(): void {
		self::install();
	}

	/** Runs the schema update after a plugin update. */
	public static function maybe_upgrade(): void {
		if ( get_option( self::DB_VERSION_OPTION ) !== self::DB_VERSION ) {
			self::install();
		}
	}

	private static function install(): void {
		global $wpdb;
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		Tables::register();
		$charset = $wpdb->get_charset_collate();
		$c       = Tables::contacts();
		$m       = Tables::meta();
		$s       = Tables::submissions();
		// dbDelta needs two spaces before PRIMARY KEY and one field per line.
		dbDelta(
			"CREATE TABLE {$c} (
				id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
				email varchar(190) NOT NULL,
				first_name varchar(100) NOT NULL DEFAULT '',
				last_name varchar(100) NOT NULL DEFAULT '',
				phone varchar(50) NOT NULL DEFAULT '',
				profession varchar(255) NOT NULL DEFAULT '',
				status varchar(20) NOT NULL DEFAULT 'prospect',
				interests varchar(255) NOT NULL DEFAULT '',
				newsletter varchar(20) NOT NULL DEFAULT 'none',
				source varchar(40) NOT NULL DEFAULT '',
				notes text NOT NULL,
				created_at datetime NOT NULL,
				updated_at datetime NOT NULL,
				PRIMARY KEY  (id),
				UNIQUE KEY email (email),
				KEY status (status)
			) {$charset};
			CREATE TABLE {$m} (
				meta_id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
				bw_perma_contact_id bigint(20) unsigned NOT NULL DEFAULT 0,
				meta_key varchar(255) DEFAULT NULL,
				meta_value longtext,
				PRIMARY KEY  (meta_id),
				KEY bw_perma_contact_id (bw_perma_contact_id),
				KEY meta_key (meta_key(191))
			) {$charset};
			CREATE TABLE {$s} (
				id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
				contact_id bigint(20) unsigned NOT NULL DEFAULT 0,
				form varchar(40) NOT NULL DEFAULT '',
				interests varchar(255) NOT NULL DEFAULT '',
				message text NOT NULL,
				data longtext NOT NULL,
				created_at datetime NOT NULL,
				PRIMARY KEY  (id),
				KEY contact_id (contact_id)
			) {$charset};"
		);
		update_option( self::DB_VERSION_OPTION, self::DB_VERSION, false );
	}
}
