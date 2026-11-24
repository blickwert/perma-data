<?php
/**
 * Theme setup: assets, block styles, pattern categories, custom blocks.
 *
 * @package PermaMind
 */

declare(strict_types=1);

namespace BW\PermaMind;

final class Theme {

	public const SLUG    = 'perma-mind';
	public const VERSION = '0.10.3';

	private static ?Theme $instance = null;

	public static function instance(): Theme {
		return self::$instance ??= new self();
	}

	public function boot(): void {
		add_action( 'after_setup_theme', [ $this, 'setup' ] );
		add_action( 'wp_enqueue_scripts', [ $this, 'enqueue' ] );
		add_action( 'init', [ $this, 'register' ] );
		( new Blocks() )->boot();
		( new HeroImage() )->boot();
		( new ThemeImages() )->boot();
	}

	public function setup(): void {
		add_theme_support( 'wp-block-styles' );
		add_theme_support( 'editor-styles' );
		remove_theme_support( 'core-block-patterns' );
		add_editor_style( [ 'assets/css/tokens.css', 'assets/css/components.css' ] );
		load_theme_textdomain( self::SLUG, get_template_directory() . '/languages' );
	}

	public function enqueue(): void {
		$uri = get_theme_file_uri( 'assets/css/' );
		// The tokens are small: inline them instead of one more render-blocking request.
		wp_register_style( 'bw-perma-mind-tokens', false, [], self::VERSION );
		wp_add_inline_style( 'bw-perma-mind-tokens', (string) file_get_contents( get_theme_file_path( 'assets/css/tokens.css' ) ) );
		wp_enqueue_style( 'bw-perma-mind-tokens' );
		wp_enqueue_style( 'bw-perma-mind-components', $uri . 'components.css', [ 'bw-perma-mind-tokens' ], $this->asset_version( 'components.css' ) );
		wp_enqueue_script( 'bw-perma-mind-front', get_theme_file_uri( 'assets/js/front.js' ), [], self::VERSION, [ 'strategy' => 'defer', 'in_footer' => true ] );
	}

	public function register(): void {
		register_block_pattern_category( self::SLUG, [ 'label' => __( 'PERMA Mind: Abschnitte', 'perma-mind' ) ] );
		register_block_pattern_category( self::SLUG . '-pages', [ 'label' => __( 'PERMA Mind: Seiten', 'perma-mind' ) ] );
		BlockStyles::register();
	}

	private function asset_version( string $file ): string {
		$path = get_theme_file_path( 'assets/css/' . $file );
		return is_readable( $path ) ? self::VERSION . '.' . (string) filemtime( $path ) : self::VERSION;
	}
}
