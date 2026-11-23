<?php
/**
 * Images that live in the theme (logos, hero): adds width/height (no layout shift) and lazy loading for
 * images below the fold (footer logo). Media library images get this from WordPress itself.
 *
 * @package PermaMind
 */

declare(strict_types=1);

namespace BW\PermaMind;

final class ThemeImages {

	/** Block classes whose image is never in the first screen. */
	private const LAZY = [ 'bw-footer__logo' ];

	/** @var array<string, array{0: int, 1: int}|null> */
	private static array $sizes = [];

	public function boot(): void {
		add_filter( 'render_block_core/image', [ $this, 'render' ], 10, 2 );
	}

	/**
	 * @param array<string, mixed> $block
	 */
	public function render( string $html, array $block ): string {
		if ( ! preg_match( '~<img[^>]*\ssrc="([^"]+)"~', $html, $m ) || str_contains( $html, 'bw-hero__image' ) ) {
			return $html;
		}
		$size  = self::size( $m[1] );
		$class = (string) ( $block['attrs']['className'] ?? '' );
		$add   = '';
		if ( $size && ! preg_match( '~<img[^>]*\swidth=~', $html ) ) {
			$add .= sprintf( ' width="%d" height="%d"', $size[0], $size[1] );
		}
		foreach ( self::LAZY as $lazy ) {
			if ( str_contains( $class, $lazy ) && ! str_contains( $html, 'loading=' ) ) {
				$add .= ' loading="lazy"';
			}
		}
		return '' === $add ? $html : (string) preg_replace( '~<img~', '<img' . $add, $html, 1 );
	}

	/**
	 * Pixel size of a theme image (WebP/PNG/JPG via getimagesize, SVG via viewBox); null for other URLs.
	 *
	 * @return array{0: int, 1: int}|null
	 */
	public static function size( string $url ): ?array {
		if ( array_key_exists( $url, self::$sizes ) ) {
			return self::$sizes[ $url ];
		}
		$base = get_theme_file_uri( 'assets/images/' );
		$size = null;
		if ( str_starts_with( $url, $base ) ) {
			$path = get_theme_file_path( 'assets/images/' . basename( (string) wp_parse_url( $url, PHP_URL_PATH ) ) );
			if ( is_readable( $path ) ) {
				$size = str_ends_with( $path, '.svg' ) ? self::svg_size( (string) file_get_contents( $path ) ) : self::raster_size( $path );
			}
		}
		return self::$sizes[ $url ] = $size;
	}

	/** @return array{0: int, 1: int}|null */
	public static function svg_size( string $svg ): ?array {
		if ( preg_match( '~viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)\s*"~', $svg, $m ) ) {
			return [ (int) round( (float) $m[1] ), (int) round( (float) $m[2] ) ];
		}
		return null;
	}

	/** @return array{0: int, 1: int}|null */
	private static function raster_size( string $path ): ?array {
		$info = function_exists( 'wp_getimagesize' ) ? wp_getimagesize( $path ) : getimagesize( $path );
		return $info ? [ (int) $info[0], (int) $info[1] ] : null;
	}
}
