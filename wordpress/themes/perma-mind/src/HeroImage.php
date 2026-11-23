<?php
/**
 * Combines the two hero image blocks (desktop + mobile) into one responsive <picture>,
 * so each device downloads only its image. In the editor both stay separate image blocks.
 *
 * @package PermaMind
 */

declare(strict_types=1);

namespace BW\PermaMind;

final class HeroImage {

	/** Viewport width below which the portrait image is used (matches the 821px breakpoint in components.css). */
	public const MOBILE_MAX = 820;

	public function boot(): void {
		add_filter( 'render_block_core/group', [ $this, 'render' ], 10, 2 );
	}

	/**
	 * @param array<string, mixed> $block
	 */
	public function render( string $html, array $block ): string {
		$class = (string) ( $block['attrs']['className'] ?? '' );
		if ( ! str_contains( $class, 'bw-hero' ) || ! str_contains( $html, 'bw-hero__image--mobile' ) ) {
			return $html;
		}
		return self::combine( $html );
	}

	/** Pure HTML transformation (testable without WordPress). */
	public static function combine( string $html ): string {
		if ( ! preg_match( '~<figure[^>]*bw-hero__image--mobile[^>]*>.*?</figure>~s', $html, $mobile ) ) {
			return $html;
		}
		if ( ! preg_match( '~<img[^>]*\ssrc="([^"]+)"~', $mobile[0], $src ) ) {
			return $html;
		}
		$html = str_replace( $mobile[0], '', $html );
		$source = sprintf( '<source media="(max-width: %dpx)" srcset="%s">', self::MOBILE_MAX, $src[1] );
		return (string) preg_replace(
			'~(<figure[^>]*bw-hero__image--desktop[^>]*>)\s*(<img[^>]*>)~s',
			'$1<picture>' . $source . '$2</picture>',
			$html,
			1
		);
	}
}
