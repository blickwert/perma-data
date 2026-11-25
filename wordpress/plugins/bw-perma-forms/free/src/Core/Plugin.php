<?php
/**
 * Plugin entry point (the only singleton).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Core;

use BW\PermaForms\Core\Admin\AdminApp;

final class Plugin {

	public const SLUG      = 'bw-perma-forms';
	public const REST_NS   = 'bw-perma-forms/v1';
	public const CAPABILITY = 'manage_options';

	/** Contact list and CSV export; granted to administrators and editors (filter bw_perma_forms_contacts_roles). */
	public const CONTACTS_CAPABILITY = 'bw_perma_forms_contacts';

	private static ?Plugin $instance = null;

	private Settings $settings;

	private ModuleManager $modules;

	public static function instance(): Plugin {
		return self::$instance ??= new self();
	}

	public function boot(): void {
		$this->settings = new Settings();
		$this->modules  = new ModuleManager( $this->settings );
		add_action( 'plugins_loaded', [ $this, 'start' ], 20 );
	}

	/** Starts modules once all plugins (Contact Form 7) are loaded. */
	public function start(): void {
		load_plugin_textdomain( self::SLUG, false, dirname( plugin_basename( BW_PERMA_FORMS_FILE ) ) . '/languages' );
		Installer::maybe_upgrade();
		$this->modules->discover();
		$this->modules->register();
		( new AdminApp( $this->settings, $this->modules ) )->register();
		add_action( 'admin_notices', [ $this, 'notice_missing_cf7' ] );
	}

	/** Shows a notice when Contact Form 7 is missing; nothing else breaks. */
	public function notice_missing_cf7(): void {
		if ( self::cf7_active() || ! current_user_can( 'activate_plugins' ) ) {
			return;
		}
		printf(
			'<div class="notice notice-warning"><p>%s</p></div>',
			esc_html__( 'BW PERMA Forms needs Contact Form 7. The forms stay empty until it is active.', 'bw-perma-forms' )
		);
	}

	public static function cf7_active(): bool {
		return class_exists( '\WPCF7_ContactForm' );
	}

	public function settings(): Settings {
		return $this->settings;
	}

	public function modules(): ModuleManager {
		return $this->modules;
	}
}
