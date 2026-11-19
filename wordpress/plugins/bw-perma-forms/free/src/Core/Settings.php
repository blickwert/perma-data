<?php
/**
 * Plugin settings stored in one option (no secrets in code).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Core;

final class Settings {

	public const OPTION = 'bw_perma_forms_settings';

	/** @var array<string, mixed> */
	private const DEFAULTS = [
		'recipient'              => 'bw-cms@blickwert.at',
		'privacy_url'            => '/datenschutz/',
		'brevo_api_key'          => '',
		'brevo_list_ids'         => '',
		'brevo_doi_template_id'  => 0,
		'brevo_redirect_url'     => '/newsletter-bestaetigt/',
		'spam_min_seconds'       => 4,
		'spam_rate_limit'        => 5,
		'spam_rate_window'       => 10,
		'spam_max_links'         => 1,
		'spam_blocklist'         => '',
		'modules'                => [],
	];

	/** @var array<string, mixed>|null */
	private ?array $cache = null;

	/** @return array<string, mixed> */
	public static function defaults(): array {
		return self::DEFAULTS;
	}

	/** @return array<string, mixed> */
	public function all(): array {
		if ( null === $this->cache ) {
			$stored      = get_option( self::OPTION, [] );
			$this->cache = array_merge( self::DEFAULTS, is_array( $stored ) ? $stored : [] );
		}
		return $this->cache;
	}

	public function get( string $key ): mixed {
		return $this->all()[ $key ] ?? null;
	}

	public function string( string $key ): string {
		return (string) $this->get( $key );
	}

	public function int( string $key ): int {
		return (int) $this->get( $key );
	}

	public function module_enabled( string $id, bool $default ): bool {
		$modules = (array) $this->get( 'modules' );
		return array_key_exists( $id, $modules ) ? (bool) $modules[ $id ] : $default;
	}

	/**
	 * Validates and stores the given values; unknown keys are ignored.
	 *
	 * @param array<string, mixed> $values
	 * @return array<string, mixed> The stored settings.
	 */
	public function update( array $values ): array {
		$current = $this->all();
		foreach ( $values as $key => $value ) {
			if ( ! array_key_exists( $key, self::DEFAULTS ) ) {
				continue;
			}
			$current[ $key ] = self::sanitize( $key, $value );
		}
		update_option( self::OPTION, $current, false );
		$this->cache = null;
		return $this->all();
	}

	/** Sanitizes one value by its key. */
	public static function sanitize( string $key, mixed $value ): mixed {
		return match ( $key ) {
			'recipient'                                    => sanitize_email( (string) $value ),
			'privacy_url', 'brevo_redirect_url'            => esc_url_raw( (string) $value ) ?: ( str_starts_with( (string) $value, '/' ) ? sanitize_text_field( (string) $value ) : '' ),
			'brevo_api_key'                                => sanitize_text_field( (string) $value ),
			'brevo_list_ids'                               => implode( ',', array_filter( array_map( 'absint', explode( ',', (string) $value ) ) ) ),
			'brevo_doi_template_id', 'spam_min_seconds',
			'spam_rate_limit', 'spam_rate_window',
			'spam_max_links'                               => absint( $value ),
			'spam_blocklist'                               => sanitize_textarea_field( (string) $value ),
			'modules'                                      => array_map( 'boolval', is_array( $value ) ? $value : [] ),
			default                                        => $value,
		};
	}

	/** Absolute URL for a setting that may hold a site-relative path. */
	public function url( string $key ): string {
		$value = $this->string( $key );
		return str_starts_with( $value, '/' ) ? home_url( $value ) : $value;
	}
}
