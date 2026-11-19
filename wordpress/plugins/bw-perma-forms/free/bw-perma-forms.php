<?php
/**
 * Plugin Name: BW PERMA Forms
 * Description: Forms of the PERMA Mind Academy (interest list, newsletter, contact) on top of Contact Form 7, with spam protection, Brevo double opt-in and a contact database with CSV export.
 * Version: 0.1.0
 * Requires at least: 6.8
 * Requires PHP: 8.3
 * Requires Plugins: contact-form-7
 * Author: blickwert
 * License: GPL-2.0-or-later
 * Text Domain: bw-perma-forms
 * Domain Path: /languages
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

defined( 'ABSPATH' ) || exit;

define( 'BW_PERMA_FORMS_VERSION', '0.1.0' );
define( 'BW_PERMA_FORMS_FILE', __FILE__ );
define( 'BW_PERMA_FORMS_DIR', __DIR__ . '/' );

spl_autoload_register(
	static function ( string $class ): void {
		$prefix = 'BW\\PermaForms\\';
		if ( ! str_starts_with( $class, $prefix ) ) {
			return;
		}
		$file = BW_PERMA_FORMS_DIR . 'src/' . str_replace( '\\', '/', substr( $class, strlen( $prefix ) ) ) . '.php';
		if ( is_readable( $file ) ) {
			require_once $file;
		}
	}
);

register_activation_hook( __FILE__, [ BW\PermaForms\Core\Installer::class, 'activate' ] );

BW\PermaForms\Core\Plugin::instance()->boot();
