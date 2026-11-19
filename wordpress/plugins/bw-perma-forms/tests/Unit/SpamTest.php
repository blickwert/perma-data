<?php
/**
 * Tests for the spam rules, the time token and the rate limiter.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Tests\Unit;

use Brain\Monkey\Functions;
use BW\PermaForms\Modules\SpamProtection\Service\RateLimiter;
use BW\PermaForms\Modules\SpamProtection\Service\SpamGuard;
use BW\PermaForms\Modules\SpamProtection\Service\TimeToken;

final class SpamTest extends TestCase {

	private function guard(): SpamGuard {
		return new SpamGuard( 4, 5, 1, SpamGuard::parse_blocklist( "Casino\n  viagra \n\n" ) );
	}

	public function test_clean_submission_passes(): void {
		$this->assertSame( '', $this->guard()->reason( '', 30, 1, 'Ich interessiere mich für Basic. www.example.at' ) );
	}

	public function test_each_rule(): void {
		$g = $this->guard();
		$this->assertSame( 'honeypot', $g->reason( 'http://spam', 30, 1, '' ) );
		$this->assertSame( 'missing_timestamp', $g->reason( '', null, 1, '' ) );
		$this->assertSame( 'too_fast', $g->reason( '', 2, 1, '' ) );
		$this->assertSame( 'rate_limit', $g->reason( '', 30, 6, '' ) );
		$this->assertSame( 'links', $g->reason( '', 30, 1, 'https://a.at und https://b.at' ) );
		$this->assertSame( 'blocked_word', $g->reason( '', 30, 1, 'Bestes CASINO online' ) );
	}

	public function test_time_token(): void {
		$token = TimeToken::create( 1000, 'geheim' );
		$this->assertSame( 25, TimeToken::elapsed( $token, 'geheim', 1025 ) );
		$this->assertNull( TimeToken::elapsed( $token, 'anders', 1025 ) );
		$this->assertNull( TimeToken::elapsed( '999.' . substr( $token, 5 ), 'geheim', 1025 ) );
		$this->assertNull( TimeToken::elapsed( '', 'geheim', 1025 ) );
	}

	public function test_rate_limiter_counts_within_window(): void {
		$store = [];
		Functions\when( 'wp_salt' )->justReturn( 'salt' );
		Functions\when( 'get_transient' )->alias( static function ( string $k ) use ( &$store ) {
			return $store[ $k ] ?? false;
		} );
		Functions\when( 'set_transient' )->alias( static function ( string $k, $v ) use ( &$store ): bool {
			$store[ $k ] = $v;
			return true;
		} );
		$l = new RateLimiter( 10 );
		$this->assertSame( 1, $l->hit( '1.2.3.4', 1000 ) );
		$this->assertSame( 2, $l->hit( '1.2.3.4', 1100 ) );
		$this->assertSame( 1, $l->hit( '5.6.7.8', 1100 ) );
		$this->assertSame( 2, $l->hit( '1.2.3.4', 1000 + 601 ) ); // the first hit is out of the 10-minute window
		$this->assertStringNotContainsString( '1.2.3.4', implode( '', array_keys( $store ) ) );
	}
}
