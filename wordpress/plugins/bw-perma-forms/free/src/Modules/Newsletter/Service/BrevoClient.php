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
		$templates = $this->get( 'https://api.brevo.com/v3/smtp/templates?limit=100&offset=0&sort=desc' );
		if ( is_wp_error( $templates ) ) {
			return $templates;
		}
		$pick = static fn( array $rows ): array => array_values( array_map( static fn( array $r ): array => [ 'id' => (int) ( $r['id'] ?? 0 ), 'name' => (string) ( $r['name'] ?? '' ), 'active' => (bool) ( $r['isActive'] ?? true ), 'tag' => (string) ( $r['tag'] ?? '' ) ], $rows ) );
		return [ 'lists' => $pick( (array) ( $lists['lists'] ?? [] ) ), 'templates' => $pick( (array) ( $templates['templates'] ?? [] ) ) ];
	}

	/** First active sender of the account (needed for templates), null if none. @return array{name: string, email: string}|null */
	public function sender(): ?array {
		$r = $this->get( 'https://api.brevo.com/v3/senders' );
		foreach ( is_wp_error( $r ) ? [] : (array) ( $r['senders'] ?? [] ) as $s ) {
			if ( ! empty( $s['active'] ) && ! empty( $s['email'] ) ) {
				return [ 'name' => (string) ( $s['name'] ?? '' ), 'email' => (string) $s['email'] ];
			}
		}
		return null;
	}

	/** Id of a contact folder (first existing one, otherwise a new one). */
	public function folder_id( string $name ): int|\WP_Error {
		$r = $this->get( 'https://api.brevo.com/v3/contacts/folders?limit=50&offset=0' );
		if ( is_wp_error( $r ) ) {
			return $r;
		}
		$first = (array) ( $r['folders'][0] ?? [] );
		if ( ! empty( $first['id'] ) ) {
			return (int) $first['id'];
		}
		$created = $this->post( 'https://api.brevo.com/v3/contacts/folders', [ 'name' => $name ] );
		return is_wp_error( $created ) ? $created : (int) ( $created['id'] ?? 0 );
	}

	public function create_list( string $name, int $folder_id ): int|\WP_Error {
		$r = $this->post( 'https://api.brevo.com/v3/contacts/lists', [ 'name' => $name, 'folderId' => $folder_id ] );
		return is_wp_error( $r ) ? $r : (int) ( $r['id'] ?? 0 );
	}

	/**
	 * Creates an active transactional template.
	 *
	 * @param array<string, mixed> $template Brevo fields (templateName, subject, htmlContent, sender, tag …).
	 */
	public function create_template( array $template ): int|\WP_Error {
		$r = $this->post( 'https://api.brevo.com/v3/smtp/templates', $template + [ 'isActive' => true ] );
		return is_wp_error( $r ) ? $r : (int) ( $r['id'] ?? 0 );
	}

	/** Registers a marketing webhook for the URL unless one exists already; returns its id. */
	public function ensure_webhook( string $url, array $events ): int|\WP_Error {
		$r = $this->get( 'https://api.brevo.com/v3/webhooks?type=marketing' );
		// Brevo answers "Webhook record does not exist" instead of an empty list when there is none yet.
		if ( is_wp_error( $r ) && ! str_contains( $r->get_error_message(), 'does not exist' ) ) {
			return $r;
		}
		$r = is_wp_error( $r ) ? [] : $r;
		foreach ( (array) ( $r['webhooks'] ?? [] ) as $hook ) {
			if ( ( $hook['url'] ?? '' ) === $url ) {
				return (int) $hook['id'];
			}
		}
		$created = $this->post( 'https://api.brevo.com/v3/webhooks', [ 'url' => $url, 'type' => 'marketing', 'events' => $events, 'description' => 'PERMA Website: Newsletter-Status' ] );
		return is_wp_error( $created ) ? $created : (int) ( $created['id'] ?? 0 );
	}

	/**
	 * @param array<string, mixed> $body
	 * @return array<string, mixed>|\WP_Error
	 */
	private function post( string $url, array $body ): array|\WP_Error {
		return $this->request( 'POST', $url, $body );
	}

	/** @return array<string, mixed>|\WP_Error */
	private function get( string $url ): array|\WP_Error {
		return $this->request( 'GET', $url );
	}

	/**
	 * @param array<string, mixed>|null $body
	 * @return array<string, mixed>|\WP_Error
	 */
	private function request( string $method, string $url, ?array $body = null ): array|\WP_Error {
		$args = [ 'method' => $method, 'timeout' => 15, 'headers' => [ 'api-key' => $this->api_key, 'accept' => 'application/json', 'content-type' => 'application/json' ] ];
		if ( null !== $body ) {
			$args['body'] = (string) wp_json_encode( $body );
		}
		$response = wp_remote_request( $url, $args );
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
