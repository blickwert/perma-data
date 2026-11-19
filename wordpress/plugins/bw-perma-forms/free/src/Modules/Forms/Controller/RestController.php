<?php
/**
 * REST routes for the form status and the manual sync with Contact Form 7.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Forms\Controller;

use BW\PermaForms\Core\Plugin;
use BW\PermaForms\Modules\Forms\Service\FormProvisioner;
use BW\PermaForms\Modules\Forms\Service\FormRegistry;

final class RestController {

	public function __construct(
		private readonly FormRegistry $registry,
		private readonly FormProvisioner $provisioner,
	) {}

	public function register(): void {
		add_action( 'rest_api_init', [ $this, 'routes' ] );
	}

	public function routes(): void {
		$perm = static fn(): bool => current_user_can( Plugin::CAPABILITY );
		register_rest_route( Plugin::REST_NS, '/forms', [ 'methods' => 'GET', 'callback' => [ $this, 'index' ], 'permission_callback' => $perm ] );
		register_rest_route( Plugin::REST_NS, '/forms/sync', [ 'methods' => 'POST', 'callback' => [ $this, 'sync' ], 'permission_callback' => $perm ] );
	}

	public function index(): \WP_REST_Response {
		$out    = [];
		$stored = $this->registry->stored();
		foreach ( $this->registry->definitions() as $key => $def ) {
			$id    = (int) ( $stored[ $key ]['id'] ?? 0 );
			$out[] = [
				'key'       => $key,
				'title'     => $def->title,
				'cf7_id'    => $id,
				'edit_url'  => $id ? admin_url( 'admin.php?page=wpcf7&post=' . $id . '&action=edit' ) : '',
				'in_sync'   => $id > 0 && ( $stored[ $key ]['hash'] ?? '' ) === $def->hash(),
			];
		}
		return new \WP_REST_Response( [ 'cf7_active' => Plugin::cf7_active(), 'forms' => $out ] );
	}

	public function sync(): \WP_REST_Response {
		return new \WP_REST_Response( [ 'result' => $this->provisioner->sync( true ) ] + $this->index()->get_data() );
	}
}
