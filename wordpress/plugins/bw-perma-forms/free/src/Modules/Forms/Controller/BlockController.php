<?php
/**
 * Block bw/perma-form and shortcode [bw_perma_form]: outputs one of the forms on a page.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Forms\Controller;

use BW\PermaForms\Core\View;
use BW\PermaForms\Modules\Forms\Service\FormRegistry;

final class BlockController {

	public function __construct( private readonly FormRegistry $registry ) {}

	public function register(): void {
		add_action( 'init', [ $this, 'register_block' ] );
		add_shortcode( 'bw_perma_form', [ $this, 'shortcode' ] );
	}

	public function register_block(): void {
		wp_register_style( 'bw-perma-forms', plugins_url( 'assets/css/forms.css', BW_PERMA_FORMS_FILE ), [], BW_PERMA_FORMS_VERSION );
		register_block_type(
			BW_PERMA_FORMS_DIR . 'blocks/perma-form',
			[ 'render_callback' => fn( array $attributes ): string => $this->render( (string) ( $attributes['form'] ?? '' ), (string) ( $attributes['preselect'] ?? '' ) ) ]
		);
		wp_set_script_translations( generate_block_asset_handle( 'bw/perma-form', 'editorScript' ), 'bw-perma-forms', BW_PERMA_FORMS_DIR . 'languages' );
		wp_add_inline_script(
			generate_block_asset_handle( 'bw/perma-form', 'editorScript' ),
			'window.bwPermaForms = ' . wp_json_encode( [ 'forms' => array_map( static fn( $d ): string => $d->title, $this->registry->definitions() ) ] ) . ';',
			'before'
		);
	}

	/** @param array<string, string>|string $atts */
	public function shortcode( array|string $atts ): string {
		$atts = shortcode_atts( [ 'form' => '', 'preselect' => '' ], (array) $atts, 'bw_perma_form' );
		return $this->render( sanitize_key( $atts['form'] ), sanitize_key( $atts['preselect'] ) );
	}

	/** HTML of a form; empty if the form or Contact Form 7 is missing. */
	public function render( string $key, string $preselect = '' ): string {
		$def = $this->registry->get( $key );
		$id  = $this->registry->cf7_id( $key );
		if ( ! $def || ! $id || ! function_exists( 'wpcf7_contact_form' ) ) {
			return '';
		}
		$attrs = '';
		foreach ( $def->preselect as $attr => $values ) {
			if ( isset( $values[ $preselect ] ) ) {
				$attrs .= sprintf( ' %s="%s"', $attr, esc_attr( $values[ $preselect ] ) );
			}
		}
		wp_enqueue_style( 'bw-perma-forms' );
		return View::render(
			'forms/form.php',
			[
				'key'  => $key,
				'html' => do_shortcode( sprintf( '[contact-form-7 id="%d"%s]', $id, $attrs ) ),
			]
		);
	}
}
