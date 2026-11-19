<?php
/**
 * Decides whether a submission is spam (honeypot, minimum fill time, rate limit, links, blocked words).
 * Pure rules without WordPress calls, so they are easy to test.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\SpamProtection\Service;

final class SpamGuard {

	/**
	 * @param string[] $blocklist Lower-case words or phrases.
	 */
	public function __construct(
		private readonly int $min_seconds,
		private readonly int $rate_limit,
		private readonly int $max_links,
		private readonly array $blocklist,
	) {}

	/**
	 * Reason why the submission is spam, or '' if it looks fine.
	 *
	 * @param string   $honeypot Value of the hidden field (must stay empty).
	 * @param int|null $elapsed  Seconds since the form was rendered, null if the time token is missing or forged.
	 * @param int      $recent   Submissions from the same address in the rate window, including this one.
	 * @param string   $text     All text the visitor entered.
	 */
	public function reason( string $honeypot, ?int $elapsed, int $recent, string $text ): string {
		if ( '' !== trim( $honeypot ) ) {
			return 'honeypot';
		}
		if ( null === $elapsed ) {
			return 'missing_timestamp';
		}
		if ( $elapsed < $this->min_seconds ) {
			return 'too_fast';
		}
		if ( $this->rate_limit > 0 && $recent > $this->rate_limit ) {
			return 'rate_limit';
		}
		if ( self::count_links( $text ) > $this->max_links ) {
			return 'links';
		}
		$lower = mb_strtolower( $text );
		foreach ( $this->blocklist as $word ) {
			if ( '' !== $word && str_contains( $lower, $word ) ) {
				return 'blocked_word';
			}
		}
		return '';
	}

	public static function count_links( string $text ): int {
		return (int) preg_match_all( '~(https?://|www\.|\[url|<a\s)~i', $text );
	}

	/** @return string[] Lower-case, trimmed, non-empty lines. */
	public static function parse_blocklist( string $lines ): array {
		return array_values( array_filter( array_map( static fn( string $l ): string => mb_strtolower( trim( $l ) ), preg_split( '/\R/', $lines ) ?: [] ) ) );
	}
}
