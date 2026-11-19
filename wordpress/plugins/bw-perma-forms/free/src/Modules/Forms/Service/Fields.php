<?php
/**
 * Small helpers to read Contact Form 7 posted data.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Forms\Service;

final class Fields {

	/** @param array<string, mixed> $posted */
	public static function text( array $posted, string $name ): string {
		$v = $posted[ $name ] ?? '';
		return trim( is_array( $v ) ? (string) reset( $v ) : (string) $v );
	}

	/**
	 * @param array<string, mixed> $posted
	 * @return string[]
	 */
	public static function list( array $posted, string $name ): array {
		return array_values( array_filter( array_map( 'trim', array_map( 'strval', (array) ( $posted[ $name ] ?? [] ) ) ) ) );
	}

	/** @param array<string, mixed> $posted */
	public static function checked( array $posted, string $name ): bool {
		$v = $posted[ $name ] ?? '';
		return is_array( $v ) ? [] !== array_filter( $v ) : ! in_array( (string) $v, [ '', '0' ], true );
	}

	/**
	 * Splits a full name into first and last name (last word = last name).
	 *
	 * @return array{0: string, 1: string}
	 */
	public static function split_name( string $name ): array {
		$name = trim( preg_replace( '/\s+/', ' ', $name ) ?? '' );
		$pos  = strrpos( $name, ' ' );
		return false === $pos ? [ $name, '' ] : [ substr( $name, 0, $pos ), substr( $name, $pos + 1 ) ];
	}

	/** Sender address on the site's own domain (avoids spam flags). */
	public static function sender(): string {
		$host = (string) wp_parse_url( home_url(), PHP_URL_HOST );
		$host = preg_replace( '/^www\./', '', $host );
		return '[_site_title] <wordpress@' . $host . '>';
	}
}
