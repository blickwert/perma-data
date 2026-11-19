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
		// Core "outline" duplicates our "secondary" button style.
		unregister_block_style( 'core/button', 'outline' );
	}
}
