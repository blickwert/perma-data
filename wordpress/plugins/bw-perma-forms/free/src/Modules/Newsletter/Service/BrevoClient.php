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
