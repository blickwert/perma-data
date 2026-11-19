<?php
/**
 * Signed render time of a form (for the minimum fill time).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\SpamProtection\Service;

final class TimeToken {

	public static function create( int $time, string $secret ): string {
		return $time . '.' . hash_hmac( 'sha256', (string) $time, $secret );
	}

	/** Seconds since the token was created, null if the token is missing or forged. */
	public static function elapsed( string $token, string $secret, int $now ): ?int {
		$parts = explode( '.', $token, 2 );
		if ( 2 !== count( $parts ) || ! ctype_digit( $parts[0] ) ) {
			return null;
		}
		if ( ! hash_equals( hash_hmac( 'sha256', $parts[0], $secret ), $parts[1] ) ) {
			return null;
		}
		return $now - (int) $parts[0];
	}
}
