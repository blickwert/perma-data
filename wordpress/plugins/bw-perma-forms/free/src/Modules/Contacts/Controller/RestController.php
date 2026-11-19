<?php
/**
 * REST routes of the contact database for the admin app.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Controller;

use BW\PermaForms\Core\Plugin;
use BW\PermaForms\Modules\Contacts\Model\Contact;
use BW\PermaForms\Modules\Contacts\Repository\ContactRepository;
use BW\PermaForms\Modules\Contacts\Service\ContactService;

final class RestController {

	public function __construct(
		private readonly ContactRepository $contacts,
		private readonly ContactService $service,
	) {}

	public function register(): void {
		add_action( 'rest_api_init', [ $this, 'routes' ] );
	}

	public function routes(): void {
		$perm = static fn(): bool => current_user_can( Plugin::CAPABILITY );
		register_rest_route(
			Plugin::REST_NS,
			'/contacts',
			[
				'methods'             => 'GET',
				'callback'            => [ $this, 'index' ],
				'permission_callback' => $perm,
				'args'                => [
					'search'     => [ 'type' => 'string', 'default' => '' ],
					'status'     => [ 'type' => 'string', 'default' => '', 'enum' => array_merge( [ '' ], Contact::STATUSES ) ],
					'interest'   => [ 'type' => 'string', 'default' => '', 'enum' => array_merge( [ '' ], Contact::INTERESTS ) ],
					'newsletter' => [ 'type' => 'string', 'default' => '', 'enum' => array_merge( [ '' ], Contact::NEWSLETTER ) ],
					'page'       => [ 'type' => 'integer', 'default' => 1, 'minimum' => 1 ],
					'per_page'   => [ 'type' => 'integer', 'default' => 50, 'minimum' => 1, 'maximum' => 200 ],
				],
			]
		);
		register_rest_route(
			Plugin::REST_NS,
			'/contacts/(?P<id>\d+)',
			[
				[ 'methods' => 'GET', 'callback' => [ $this, 'show' ], 'permission_callback' => $perm ],
				[ 'methods' => 'POST', 'callback' => [ $this, 'update' ], 'permission_callback' => $perm ],
				[ 'methods' => 'DELETE', 'callback' => [ $this, 'destroy' ], 'permission_callback' => $perm ],
			]
		);
	}

	public function index( \WP_REST_Request $request ): \WP_REST_Response {
		$result = $this->contacts->search(
			self::filters( $request ),
			(int) $request->get_param( 'page' ),
			(int) $request->get_param( 'per_page' )
		);
		return new \WP_REST_Response(
			[
				'items' => array_map( static fn( Contact $c ): array => $c->to_array(), $result['items'] ),
				'total' => $result['total'],
			]
		);
	}

	public function show( \WP_REST_Request $request ): \WP_REST_Response|\WP_Error {
		$detail = $this->service->detail( (int) $request['id'] );
		return $detail ? new \WP_REST_Response( $detail ) : new \WP_Error( 'bw_perma_forms_not_found', __( 'Contact not found.', 'bw-perma-forms' ), [ 'status' => 404 ] );
	}

	public function update( \WP_REST_Request $request ): \WP_REST_Response|\WP_Error {
		$result = $this->service->update( (int) $request['id'], (array) $request->get_json_params() );
		return is_wp_error( $result ) ? $result : $this->show( $request );
	}

	public function destroy( \WP_REST_Request $request ): \WP_REST_Response|\WP_Error {
		return $this->service->delete( (int) $request['id'] )
			? new \WP_REST_Response( [ 'deleted' => true ] )
			: new \WP_Error( 'bw_perma_forms_not_found', __( 'Contact not found.', 'bw-perma-forms' ), [ 'status' => 404 ] );
	}

	/**
	 * Filters from a request (shared with the CSV export).
	 *
	 * @param \WP_REST_Request|array<string, mixed> $source
	 * @return array{search: string, status: string, interest: string, newsletter: string}
	 */
	public static function filters( \WP_REST_Request|array $source ): array {
		$get = static fn( string $k ): string => sanitize_text_field( (string) ( is_array( $source ) ? ( $source[ $k ] ?? '' ) : $source->get_param( $k ) ) );
		return [
			'search'     => $get( 'search' ),
			'status'     => in_array( $get( 'status' ), Contact::STATUSES, true ) ? $get( 'status' ) : '',
			'interest'   => in_array( $get( 'interest' ), Contact::INTERESTS, true ) ? $get( 'interest' ) : '',
			'newsletter' => in_array( $get( 'newsletter' ), Contact::NEWSLETTER, true ) ? $get( 'newsletter' ) : '',
		];
	}
}
