<?php
/**
 * Hooks the newsletter into the forms and receives Brevo webhooks (confirmed, unsubscribed).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Newsletter\Controller;

use BW\PermaForms\Core\Plugin;
use BW\PermaForms\Modules\Newsletter\Service\NewsletterService;

final class NewsletterController {

	public const TOKEN_OPTION = 'bw_perma_forms_webhook_token';

	public function __construct(
		private readonly NewsletterService $service,
		private readonly \BW\PermaForms\Modules\Newsletter\Service\BrevoClient $client,
		private readonly \BW\PermaForms\Core\Settings $settings,
	) {}

	public function register(): void {
		add_filter( 'bw_perma_forms_before_submit', [ $this, 'before_submit' ], 10, 3 );
		add_action( 'bw_perma_forms_submitted', [ $this, 'after_interest' ], 20, 2 );
		add_action( 'rest_api_init', [ $this, 'routes' ] );
	}

	/**
	 * Newsletter form: the signup must reach Brevo, otherwise the visitor sees an error.
	 *
	 * @param array<string, mixed> $data
	 */
	public function before_submit( ?\WP_Error $error, string $key, array $data ): ?\WP_Error {
		if ( $error || 'newsletter' !== $key ) {
			return $error;
		}
		$result = $this->service->subscribe( (string) $data['email'], (string) ( $data['first_name'] ?? '' ) );
		if ( true === $result ) {
			return null;
		}
		error_log( 'bw-perma-forms: newsletter signup failed: ' . $result->get_error_code() ); // phpcs:ignore WordPress.PHP.DevelopmentFunctions -- no personal data in the log.
		return new \WP_Error( 'bw_perma_forms_newsletter', 'Die Anmeldung zum Newsletter hat gerade nicht geklappt. Bitte versuche es später noch einmal.' );
	}

	/**
	 * Interest list with the newsletter box ticked: signup in addition, a failure does not block the entry.
	 *
	 * @param array<string, mixed> $data
	 */
	public function after_interest( string $key, array $data ): void {
		if ( 'interest' === $key && ! empty( $data['newsletter_optin'] ) ) {
			$this->service->subscribe( (string) $data['email'], (string) ( $data['first_name'] ?? '' ) );
		}
	}

	public function routes(): void {
		register_rest_route(
			Plugin::REST_NS,
			'/brevo/options',
			[
				'methods'             => 'GET',
				'callback'            => [ $this, 'brevo_options' ],
				'permission_callback' => static fn(): bool => current_user_can( Plugin::CAPABILITY ),
			]
		);
		register_rest_route(
			Plugin::REST_NS,
			'/brevo/setup',
			[
				'methods'             => 'POST',
				'callback'            => [ $this, 'brevo_setup' ],
				'permission_callback' => static fn(): bool => current_user_can( Plugin::CAPABILITY ),
				'args'                => [
					'create_list'     => [ 'type' => 'boolean', 'default' => true ],
					'create_template' => [ 'type' => 'boolean', 'default' => true ],
				],
			]
		);
		register_rest_route(
			Plugin::REST_NS,
			'/brevo/webhook',
			[
				'methods'             => 'POST',
				'callback'            => [ $this, 'webhook' ],
				// Brevo cannot log in; the secret token in the URL protects the route.
				'permission_callback' => static fn( \WP_REST_Request $r ): bool => hash_equals( self::token(), (string) $r->get_param( 'token' ) ),
			]
		);
	}

	/** Lists and templates from Brevo for the settings page. */
	public function brevo_options(): \WP_REST_Response|\WP_Error {
		if ( ! $this->client->configured() ) {
			return new \WP_Error( 'bw_perma_forms_brevo_key', __( 'No Brevo API key.', 'bw-perma-forms' ), [ 'status' => 400 ] );
		}
		$options = $this->client->options();
		return is_wp_error( $options ) ? new \WP_Error( $options->get_error_code(), $options->get_error_message(), [ 'status' => 502 ] ) : new \WP_REST_Response( $options );
	}

	/** Creates list and double opt-in template in Brevo and stores their ids in the settings. */
	public function brevo_setup( \WP_REST_Request $request ): \WP_REST_Response|\WP_Error {
		if ( ! $this->client->configured() ) {
			return new \WP_Error( 'bw_perma_forms_brevo_key', __( 'No Brevo API key.', 'bw-perma-forms' ), [ 'status' => 400 ] );
		}
		$result = ( new \BW\PermaForms\Modules\Newsletter\Service\BrevoSetup( $this->client ) )->run(
			(bool) $request->get_param( 'create_list' ),
			(bool) $request->get_param( 'create_template' ),
			wp_specialchars_decode( get_bloginfo( 'name' ), ENT_QUOTES ),
			self::webhook_url()
		);
		if ( is_wp_error( $result ) ) {
			return new \WP_Error( $result->get_error_code(), $result->get_error_message(), [ 'status' => 502 ] );
		}
		$values = [];
		if ( $result['list_id'] ) {
			$values['brevo_list_ids'] = (string) $result['list_id'];
		}
		if ( $result['template_id'] ) {
			$values['brevo_doi_template_id'] = $result['template_id'];
		}
		$this->settings->update( $values );
		return new \WP_REST_Response( $result );
	}

	public function webhook( \WP_REST_Request $request ): \WP_REST_Response {
		$events = $request->get_json_params();
		$events = isset( $events['event'] ) ? [ $events ] : (array) $events;
		$count  = 0;
		foreach ( $events as $event ) {
			$state = NewsletterService::state_for_event( (string) ( $event['event'] ?? '' ) );
			$email = sanitize_email( (string) ( $event['email'] ?? '' ) );
			if ( '' !== $state && '' !== $email ) {
				/** This action is documented in NewsletterService::subscribe(). */
				do_action( 'bw_perma_forms_newsletter_state', $email, $state, '' );
				++$count;
			}
		}
		return new \WP_REST_Response( [ 'processed' => $count ] );
	}

	/** Secret token for the webhook URL (created on first use). */
	public static function token(): string {
		$token = (string) get_option( self::TOKEN_OPTION, '' );
		if ( '' === $token ) {
			$token = wp_generate_password( 32, false );
			update_option( self::TOKEN_OPTION, $token, false );
		}
		return $token;
	}

	public static function webhook_url(): string {
		return add_query_arg( 'token', self::token(), rest_url( Plugin::REST_NS . '/brevo/webhook' ) );
	}
}
