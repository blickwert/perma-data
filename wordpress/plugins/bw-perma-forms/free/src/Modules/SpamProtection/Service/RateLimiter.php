<?php
/**
 * Counts submissions per visitor in a time window (transients, only a hash of the IP address is used).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\SpamProtection\Service;

class RateLimiter {

	public function __construct( private readonly int $window_minutes ) {}

	/** Registers a submission and returns the number of submissions in the window (including this one). */
	public function hit( string $ip, int $now ): int {
		if ( '' === $ip || $this->window_minutes <= 0 ) {
			return 0;
		}
		$key    = 'bw_pf_rl_' . substr( hash_hmac( 'sha256', $ip, wp_salt( 'nonce' ) ), 0, 32 );
		$window = $this->window_minutes * 60;
		$times  = array_filter( (array) get_transient( $key ), static fn( $t ): bool => is_int( $t ) && $t > $now - $window );
		$times[] = $now;
		set_transient( $key, array_values( $times ), $window );
		return count( $times );
	}
}
