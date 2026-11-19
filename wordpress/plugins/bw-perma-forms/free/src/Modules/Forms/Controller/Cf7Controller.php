<?php
/**
 * Connects the definitions with Contact Form 7: keeps the forms in sync, hands submissions to the other modules.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Forms\Controller;

use BW\PermaForms\Modules\Forms\Service\FormProvisioner;
use BW\PermaForms\Modules\Forms\Service\FormRegistry;

final class Cf7Controller {

	public function __construct(
		private readonly FormRegistry $registry,
		private readonly FormProvisioner $provisioner,
	) {}

	public function register(): void {
		add_action( 'admin_init', [ $this, 'sync' ] );
		add_action( 'bw_perma_forms_settings_updated', [ $this, 'sync' ] );
		add_filter( 'bw_perma_forms_form_key', [ $this, 'form_key' ], 10, 2 );
		add_filter( 'wpcf7_autop_or_not', [ $this, 'autop' ] );
		add_filter( 'shortcode_atts_wpcf7', [ $this, 'shortcode_atts' ], 10, 3 );
		add_filter( 'wpcf7_form_class_attr', [ $this, 'form_class' ] );
		add_action( 'wpcf7_before_send_mail', [ $this, 'before_send_mail' ], 10, 3 );
	}

	/** Creates missing and changed forms (cheap when nothing changed). */
	public function sync(): void {
		$this->provisioner->sync();
	}

	/** Answers "is this CF7 form one of ours?" for other modules. */
	public function form_key( string $key, int $cf7_id ): string {
		return $this->registry->key_for_cf7_id( $cf7_id ) ?: $key;
	}

	/** Our templates contain their own markup; CF7 must not add <p> and <br>. */
	public function autop( bool $autop ): bool {
		$form = \WPCF7_ContactForm::get_current();
		return $form && '' !== $this->registry->key_for_cf7_id( (int) $form->id() ) ? false : $autop;
	}

	/**
	 * Allows preselect attributes (e.g. interesse="…") on our forms' shortcodes.
	 *
	 * @param array<string, mixed> $out
	 * @param array<string, mixed> $pairs
	 * @param array<string, mixed> $atts
	 * @return array<string, mixed>
	 */
	public function shortcode_atts( array $out, array $pairs, array $atts ): array {
		foreach ( $this->registry->definitions() as $def ) {
			foreach ( array_keys( $def->preselect ) as $attr ) {
				if ( isset( $atts[ $attr ] ) ) {
					$out[ $attr ] = sanitize_text_field( (string) $atts[ $attr ] );
				}
			}
		}
		return $out;
	}

	public function form_class( string $class ): string {
		$form = \WPCF7_ContactForm::get_current();
		$key  = $form ? $this->registry->key_for_cf7_id( (int) $form->id() ) : '';
		return '' === $key ? $class : $class . ' bw-form bw-form--' . sanitize_html_class( $key );
	}

	/**
	 * Normalizes the submission and hands it to the other modules.
	 * A module can stop the submission (e.g. newsletter signup failed) via bw_perma_forms_before_submit.
	 *
	 * @param \WPCF7_ContactForm $form
	 * @param bool               $abort
	 * @param \WPCF7_Submission  $submission
	 */
	public function before_send_mail( $form, &$abort, $submission ): void {
		$key = $this->registry->key_for_cf7_id( (int) $form->id() );
		$def = '' === $key ? null : $this->registry->get( $key );
		if ( ! $def || ! $submission ) {
			return;
		}
		$data = $def->normalize( (array) $submission->get_posted_data() );
		/**
		 * Lets a module reject a submission before mails are sent.
		 *
		 * @param \WP_Error|null       $error
		 * @param string               $key  Form key.
		 * @param array<string, mixed> $data Normalized data.
		 */
		$error = apply_filters( 'bw_perma_forms_before_submit', null, $key, $data );
		if ( $error instanceof \WP_Error ) {
			$abort = true;
			$submission->set_response( $error->get_error_message() );
			return;
		}
		/**
		 * Fires for every accepted submission of our forms.
		 *
		 * @param string               $key  Form key (interest, contact, newsletter).
		 * @param array<string, mixed> $data Normalized data: email, first_name, last_name, profession, interests, message, newsletter_optin, extra.
		 */
		do_action( 'bw_perma_forms_submitted', $key, $data );
	}
}
