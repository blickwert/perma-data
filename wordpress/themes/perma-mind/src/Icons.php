<?php
/**
 * Inline SVG icons from assets/icons/ (stroke="currentColor", decorative).
 *
 * @package PermaMind
 */

declare(strict_types=1);

namespace BW\PermaMind;

final class Icons {

	/** @var array<string, string> */
	private static array $cache = [];

	/** @return list<string> */
	public static function names(): array {
		$files = glob( get_theme_file_path( 'assets/icons/*.svg' ) ) ?: [];
		return array_map( static fn( string $f ): string => basename( $f, '.svg' ), $files );
	}

	public static function svg( string $name, int $size = 24 ): string {
		$name = sanitize_key( $name );
		if ( ! isset( self::$cache[ $name ] ) ) {
			$path                 = get_theme_file_path( 'assets/icons/' . $name . '.svg' );
			self::$cache[ $name ] = is_readable( $path ) ? (string) file_get_contents( $path ) : '';
		}
		if ( '' === self::$cache[ $name ] ) {
			return '';
		}
		$size = max( 12, min( 128, $size ) );
		return (string) preg_replace(
			'/^<svg /',
			sprintf( '<svg width="%1$d" height="%1$d" aria-hidden="true" focusable="false" ', $size ),
			self::$cache[ $name ]
		);
	}
}
