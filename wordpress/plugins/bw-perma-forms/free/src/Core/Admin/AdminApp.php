<?php
/**
 * Admin menu "PERMA Kontakte": one page, drawn by the admin app (build/admin.js), plus the settings REST route.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Core\Admin;

use BW\PermaForms\Core\ModuleManager;
use BW\PermaForms\Core\Plugin;
use BW\PermaForms\Core\Settings;

final class AdminApp {

	public const PAGE   = 'bw-perma-forms';
	public const HANDLE = 'bw-perma-forms-admin';

	public function __construct(
		private readonly Settings $settings,
		private readonly ModuleManager $modules,
	) {}

	public function register(): void {
		add_action( 'admin_menu', [ $this, 'menu' ] );
		add_action( 'admin_enqueue_scripts', [ $this, 'enqueue' ] );
		add_action( 'rest_api_init', [ $this, 'routes' ] );
	}

	public function menu(): void {
		add_menu_page( __( 'PERMA contacts', 'bw-perma-forms' ), __( 'PERMA contacts', 'bw-perma-forms' ), Plugin::CAPABILITY, self::PAGE, [ $this, 'render' ], 'dashicons-groups', 26 );
		add_submenu_page( self::PAGE, __( 'Contacts', 'bw-perma-forms' ), __( 'Contacts', 'bw-perma-forms' ), Plugin::CAPABILITY, self::PAGE, [ $this, 'render' ] );
		add_submenu_page( self::PAGE, __( 'Settings', 'bw-perma-forms' ), __( 'Settings', 'bw-perma-forms' ), Plugin::CAPABILITY, self::PAGE . '&path=/settings', '__return_null' );
	}

	public function render(): void {
		echo '<div class="wrap"><div id="bw-perma-forms-app" class="bwo-app"></div></div>';
	}

	public function enqueue( string $hook ): void {
		if ( 'toplevel_page_' . self::PAGE !== $hook ) {
			return;
		}
		$asset_file = BW_PERMA_FORMS_DIR . 'build/admin.asset.php';
		if ( ! is_readable( $asset_file ) ) {
			return;
		}
		$asset = require $asset_file;
		$url   = plugins_url( 'build/', BW_PERMA_FORMS_FILE );
		wp_enqueue_script( self::HANDLE, $url . 'admin.js', $asset['dependencies'], $asset['version'], true );
		wp_enqueue_style( self::HANDLE, $url . 'admin.css', [ 'wp-components' ], $asset['version'] );
		wp_set_script_translations( self::HANDLE, Plugin::SLUG, BW_PERMA_FORMS_DIR . 'languages' );
		wp_add_inline_script(
			self::HANDLE,
			'window.bwPermaFormsAdmin = ' . wp_json_encode(
				/**
				 * Data for the admin app; modules add their part (e.g. export URL, status lists).
				 *
				 * @param array<string, mixed> $data
				 */
				apply_filters(
					'bw_perma_forms_admin_data',
					[
						'restNs'   => Plugin::REST_NS,
						'adminUrl' => admin_url( 'admin.php?page=' . self::PAGE ),
						'modules'  => array_keys( $this->modules->active() ),
					]
				)
			) . ';',
			'before'
		);
	}

	public function routes(): void {
		register_rest_route(
			Plugin::REST_NS,
			'/settings',
			[
				[ 'methods' => 'GET', 'callback' => [ $this, 'get_settings' ], 'permission_callback' => static fn(): bool => current_user_can( Plugin::CAPABILITY ) ],
				[ 'methods' => 'POST', 'callback' => [ $this, 'save_settings' ], 'permission_callback' => static fn(): bool => current_user_can( Plugin::CAPABILITY ) ],
			]
		);
	}

	public function get_settings(): \WP_REST_Response {
		$values = $this->settings->all();
		// Never send the API key back to the browser.
		$values['brevo_api_key'] = '';
		$modules                 = [];
		foreach ( $this->modules->all() as $id => $module ) {
			$modules[] = [ 'id' => $id, 'name' => $module->name(), 'active' => isset( $this->modules->active()[ $id ] ), 'requires' => $module->requires() ];
		}
		/**
		 * Settings response for the admin app; modules add read-only information (e.g. webhook URL).
		 *
		 * @param array<string, mixed> $response
		 */
		return new \WP_REST_Response(
			apply_filters(
				'bw_perma_forms_settings_response',
				[
					'values'          => $values,
					'has_own_api_key' => '' !== $this->settings->string( 'brevo_api_key' ),
					'turnstile_url'   => admin_url( 'admin.php?page=wpcf7-integration' ),
					'modules'         => $modules,
				]
			)
		);
	}

	public function save_settings( \WP_REST_Request $request ): \WP_REST_Response {
		$input = (array) $request->get_json_params();
		// An empty key field keeps the stored key; "-" removes it.
		if ( isset( $input['brevo_api_key'] ) ) {
			if ( '' === $input['brevo_api_key'] ) {
				unset( $input['brevo_api_key'] );
			} elseif ( '-' === $input['brevo_api_key'] ) {
				$input['brevo_api_key'] = '';
			}
		}
		$this->settings->update( $input );
		/**
		 * Fires after the settings were saved (forms are synced with the new recipient etc.).
		 */
		do_action( 'bw_perma_forms_settings_updated' );
		return $this->get_settings();
	}
}
