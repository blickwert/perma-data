<?php
/**
 * Custom blocks of the theme (blocks/<name>/block.json).
 *
 * @package PermaMind
 */

declare(strict_types=1);

namespace BW\PermaMind;

final class Blocks {

	public function boot(): void {
		add_action( 'init', [ $this, 'register' ] );
	}

	public function register(): void {
		register_block_type( get_theme_file_path( 'blocks/icon' ) );
		wp_add_inline_script(
			generate_block_asset_handle( 'bw/icon', 'editorScript' ),
			'window.bwPermaMindIcons = ' . wp_json_encode( Icons::names() ) . ';',
			'before'
		);
	}
}
