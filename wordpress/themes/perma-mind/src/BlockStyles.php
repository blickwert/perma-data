<?php
/**
 * Named block styles: editors pick these instead of setting colors or spacing per block.
 * The CSS for every style lives in assets/css/components.css (.is-style-<name>).
 *
 * @package PermaMind
 */

declare(strict_types=1);

namespace BW\PermaMind;

final class BlockStyles {

	/** @var array<string, array<string, string>> block name => [ style slug => label ] */
	private const STYLES = [
		'core/group'  => [
			'section-tint'     => 'Abschnitt Mint',
			'section-neutral'  => 'Abschnitt Neutral',
			'section-navy'     => 'Abschnitt Navy',
			'gradient-hero'    => 'Hero-Verlauf',
			'gradient-page'    => 'Seitenkopf-Verlauf',
			'accent-blue'      => 'Akzent Blau',
			'accent-purple'    => 'Akzent Lila',
			'accent-orange'    => 'Akzent Orange',
			'accent-green'     => 'Akzent Grün',
			'accent-red'       => 'Akzent Rot',
		],
		'core/button' => [
			'secondary' => 'Sekundär (Kontur)',
			'light'     => 'Hell',
			'accent'    => 'Akzent (Verlauf)',
			'arrow'     => 'Link mit Pfeil',
		],
		'core/list'   => [
			'facts' => 'Fakten (Punkt in Akzentfarbe)',
			'steps' => 'Schritte (nummeriert)',
			'perma' => 'PERMA-Liste',
		],
	];

	public static function register(): void {
		foreach ( self::STYLES as $block => $styles ) {
			foreach ( $styles as $name => $label ) {
				register_block_style( $block, [ 'name' => $name, 'label' => $label ] );
			}
		}
		add_action( 'enqueue_block_editor_assets', [ self::class, 'remove_core_styles' ] );
	}

	/**
	 * Core "outline" duplicates our "secondary" button style. Core registers it in JavaScript only,
	 * so it has to be removed there (unregister_block_style() in PHP would raise a notice).
	 */
	public static function remove_core_styles(): void {
		// Filter at registration time: an unregister call on domReady runs before the core blocks are registered.
		wp_add_inline_script(
			'wp-blocks',
			"wp.hooks.addFilter( 'blocks.registerBlockType', 'perma-mind/button-styles', function ( settings, name ) { return 'core/button' === name ? Object.assign( {}, settings, { styles: ( settings.styles || [] ).filter( function ( s ) { return 'outline' !== s.name; } ) } ) : settings; } );",
			'after'
		);
	}
}
