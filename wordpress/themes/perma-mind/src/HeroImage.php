<?php
/**
 * Hero images: combines the two image blocks (desktop + mobile) into one responsive <picture>,
 * adds srcset (smaller theme variants), sizes, width/height and fetchpriority, so each device downloads
 * one image in a fitting size as early as possible. In the editor both stay separate image blocks.
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
		if ( ! preg_match( '/(^|\s)bw-hero(\s|$)/', $class ) || ! str_contains( $html, 'bw-hero__image--' ) ) {
			return $html;
		}
		return self::combine( $html, [ self::class, 'srcset' ], [ ThemeImages::class, 'size' ] );
	}

	/**
	 * Pure HTML transformation (testable without WordPress).
	 *
	 * @param callable(string): string                    $srcset_for Returns "url w, url w" for an image URL ('' if none).
	 * @param callable(string): array{0: int, 1: int}|null $size_for   Width and height of an image URL.
	 */
	public static function combine( string $html, callable $srcset_for, callable $size_for ): string {
		$mobile_src = '';
		if ( preg_match( '~<figure[^>]*bw-hero__image--mobile[^>]*>.*?</figure>~s', $html, $mobile )
			&& preg_match( '~<img[^>]*\ssrc="([^"]+)"~', $mobile[0], $m ) ) {
			$mobile_src = $m[1];
			$html       = str_replace( $mobile[0], '', $html );
		}
		return (string) preg_replace_callback(
			'~(<figure[^>]*bw-hero__image--desktop[^>]*>)\s*<img([^>]*)\ssrc="([^"]+)"([^>]*)>~s',
			static function ( array $m ) use ( $mobile_src, $srcset_for, $size_for ): string {
				$src    = $m[3];
				$attrs  = rtrim( $m[2] . $m[4], " /\t\n" ); // drop the self-closing slash
				$extra  = ' fetchpriority="high" decoding="async" sizes="100vw"';
				$srcset = $srcset_for( $src );
				if ( '' !== $srcset ) {
					$extra .= ' srcset="' . $srcset . '"';
				}
				$size = $size_for( $src );
				if ( $size && ! str_contains( $attrs, 'width=' ) ) {
					$extra .= sprintf( ' width="%d" height="%d"', $size[0], $size[1] );
				}
				$attrs = (string) preg_replace( '~\s(loading|decoding|fetchpriority)="[^"]*"~', '', $attrs );
				$img   = '<img' . $attrs . ' src="' . $src . '"' . $extra . '>';
				if ( '' === $mobile_src ) {
					return $m[1] . $img;
				}
				$mobile_srcset = $srcset_for( $mobile_src ) ?: $mobile_src;
				$source        = sprintf( '<source media="(max-width: %dpx)" srcset="%s" sizes="100vw">', self::MOBILE_MAX, $mobile_srcset );
				return $m[1] . '<picture>' . $source . $img . '</picture>';
			},
			$html,
			1
		);
	}

	/** srcset of a theme image: the image itself plus smaller variants named <name>-<width>.webp next to it. */
	public static function srcset( string $url ): string {
		$base = get_theme_file_uri( 'assets/images/' );
		if ( ! str_starts_with( $url, $base ) ) {
			return '';
		}
		$file = substr( $url, strlen( $base ) );
		$stem = pathinfo( $file, PATHINFO_FILENAME );
		$ext  = pathinfo( $file, PATHINFO_EXTENSION );
		$list = [];
		foreach ( glob( get_theme_file_path( 'assets/images/' . $stem . '-*.' . $ext ) ) ?: [] as $variant ) {
			if ( preg_match( '/-(\d+)\.' . preg_quote( $ext, '/' ) . '$/', $variant, $w ) ) {
				$list[ (int) $w[1] ] = $base . basename( $variant );
			}
		}
		$size = ThemeImages::size( $url );
		if ( $size ) {
			$list[ $size[0] ] = $url;
		}
		ksort( $list );
		return implode( ', ', array_map( static fn( int $w, string $u ): string => esc_url( $u ) . ' ' . $w . 'w', array_keys( $list ), $list ) );
	}
}
