<?php
/**
 * Minimal Brevo API v3 client: double opt-in signup.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Newsletter\Service;

class BrevoClient {

	public const ENDPOINT = 'https://api.brevo.com/v3/contacts/doubleOptinConfirmation';

	public function __construct( private readonly string $api_key ) {}

	public function configured(): bool {
		return '' !== $this->api_key;
	}

	/**
	 * Request body for the double opt-in call.
	 *
	 * @param int[]                 $list_ids
	 * @param array<string, string> $attributes
	 * @return array<string, mixed>
	 */
	public static function payload( string $email, array $list_ids, int $template_id, string $redirect_url, array $attributes = [] ): array {
		$body       = [
			'email'          => $email,
			'includeListIds' => array_values( array_map( 'intval', $list_ids ) ),
			'templateId'     => $template_id,
			'redirectionUrl' => $redirect_url,
		];
		$attributes = array_filter( $attributes, static fn( string $v ): bool => '' !== $v );
		if ( $attributes ) {
			$body['attributes'] = $attributes;
		}
		return $body;
	}

	/**
	 * Lists and active templates of the account (for choosing them in the settings).
	 *
	 * @return array{lists: array<int, array{id: int, name: string}>, templates: array<int, array{id: int, name: string}>}|\WP_Error
	 */
	public function options(): array|\WP_Error {
		$lists = $this->get( 'https://api.brevo.com/v3/contacts/lists?limit=50&offset=0&sort=desc' );
		if ( is_wp_error( $lists ) ) {
			return $lists;
		}
		$templates = $this->get( 'https://api.brevo.com/v3/smtp/templates?templateStatus=true&limit=100&offset=0&sort=desc' );
		if ( is_wp_error( $templates ) ) {
			return $templates;
		}
		$pick = static fn( array $rows ): array => array_values( array_map( static fn( array $r ): array => [ 'id' => (int) ( $r['id'] ?? 0 ), 'name' => (string) ( $r['name'] ?? '' ) ], $rows ) );
		return [ 'lists' => $pick( (array) ( $lists['lists'] ?? [] ) ), 'templates' => $pick( (array) ( $templates['templates'] ?? [] ) ) ];
	}

	/** @return array<string, mixed>|\WP_Error */
	private function get( string $url ): array|\WP_Error {
		$response = wp_remote_get( $url, [ 'timeout' => 15, 'headers' => [ 'api-key' => $this->api_key, 'accept' => 'application/json' ] ] );
		if ( is_wp_error( $response ) ) {
			return $response;
		}
		$code = (int) wp_remote_retrieve_response_code( $response );
		$body = json_decode( (string) wp_remote_retrieve_body( $response ), true );
		if ( $code < 200 || $code >= 300 ) {
			return new \WP_Error( 'bw_perma_forms_brevo', sprintf( 'Brevo %d: %s', $code, (string) ( $body['message'] ?? 'error' ) ) );
		}
		return is_array( $body ) ? $body : [];
	}

	/**
	 * Sends the double opt-in mail through Brevo.
	 *
	 * @param array<string, mixed> $payload
	 */
	public function double_opt_in( array $payload ): true|\WP_Error {
		$response = wp_remote_post(
			self::ENDPOINT,
			[
				'timeout' => 15,
				'headers' => [ 'api-key' => $this->api_key, 'accept' => 'application/json', 'content-type' => 'application/json' ],
				'body'    => (string) wp_json_encode( $payload ),
			]
		);
		if ( is_wp_error( $response ) ) {
			return $response;
		}
		$code = (int) wp_remote_retrieve_response_code( $response );
		if ( $code >= 200 && $code < 300 ) {
			return true;
		}
		$body = json_decode( (string) wp_remote_retrieve_body( $response ), true );
		return new \WP_Error( 'bw_perma_forms_brevo', sprintf( 'Brevo %d: %s', $code, (string) ( $body['message'] ?? 'error' ) ) );
	}
}
