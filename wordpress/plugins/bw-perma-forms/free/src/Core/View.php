<?php
/**
 * Renders PHP templates; the theme can override them under bw-perma-forms/<area>/.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Core;

final class View {

	/** Finds a template in the theme first, then in the plugin. */
	public static function locate( string $template ): string {
		$theme = locate_template( 'bw-perma-forms/' . $template );
		$file  = $theme ?: BW_PERMA_FORMS_DIR . 'templates/' . $template;
		/** Lets other code use a different template file. */
		return (string) apply_filters( 'bw_perma_forms_template', $file, $template );
	}

	/**
	 * Renders a template with prepared data and returns the HTML.
	 *
	 * @param array<string, mixed> $data
	 */
	public static function render( string $template, array $data = [] ): string {
		$file = self::locate( $template );
		if ( ! is_readable( $file ) ) {
			return '';
		}
		ob_start();
		( static function ( string $__file, array $data ): void {
			include $__file;
		} )( $file, $data );
		return (string) ob_get_clean();
	}
}
