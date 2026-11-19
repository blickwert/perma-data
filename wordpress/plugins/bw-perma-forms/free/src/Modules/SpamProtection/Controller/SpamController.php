<?php
/**
 * Adds the honeypot and time token to our forms and rejects spam in Contact Form 7.
 * Cloudflare Turnstile itself comes from Contact Form 7 (Integration › Turnstile).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\SpamProtection\Controller;

use BW\PermaForms\Modules\SpamProtection\Service\RateLimiter;
use BW\PermaForms\Modules\SpamProtection\Service\SpamGuard;
use BW\PermaForms\Modules\SpamProtection\Service\TimeToken;

final class SpamController {

	public const HONEYPOT = 'bw_website';
	public const TOKEN    = '_bw_perma_ts';

	public function __construct(
		private readonly SpamGuard $guard,
		private readonly RateLimiter $limiter,
	) {}

	public function register(): void {
		add_filter( 'wpcf7_form_hidden_fields', [ $this, 'hidden_fields' ] );
		add_filter( 'wpcf7_form_elements', [ $this, 'honeypot' ] );
		add_filter( 'wpcf7_spam', [ $this, 'check' ], 20, 2 );
	}

	/**
	 * @param array<string, string> $fields
	 * @return array<string, string>
	 */
	public function hidden_fields( array $fields ): array {
		if ( $this->current_is_ours() ) {
			$fields[ self::TOKEN ] = TimeToken::create( time(), wp_salt( 'nonce' ) );
		}
		return $fields;
	}

	public function honeypot( string $html ): string {
		if ( ! $this->current_is_ours() ) {
			return $html;
		}
		// Hidden from people and assistive tech; bots fill every field.
		return $html . '<div class="bw-form__hp" aria-hidden="true"><label>Website <input type="text" name="' . self::HONEYPOT . '" value="" tabindex="-1" autocomplete="off"></label></div>';
	}

	/**
	 * @param bool              $spam
	 * @param \WPCF7_Submission $submission
	 */
	public function check( $spam, $submission ): bool {
		if ( $spam || ! $submission ) {
			return (bool) $spam;
		}
		$form = $submission->get_contact_form();
		if ( ! $form || '' === (string) apply_filters( 'bw_perma_forms_form_key', '', (int) $form->id() ) ) {
			return false;
		}
		// phpcs:disable WordPress.Security.NonceVerification.Missing -- CF7 verifies the request; we only read our own fields.
		$honeypot = isset( $_POST[ self::HONEYPOT ] ) ? sanitize_text_field( wp_unslash( (string) $_POST[ self::HONEYPOT ] ) ) : '';
		$token    = isset( $_POST[ self::TOKEN ] ) ? sanitize_text_field( wp_unslash( (string) $_POST[ self::TOKEN ] ) ) : '';
		// phpcs:enable
		$text   = implode( "\n", array_filter( array_map( static fn( $v ): string => is_array( $v ) ? implode( ' ', $v ) : (string) $v, (array) $submission->get_posted_data() ) ) );
		$reason = $this->guard->reason(
			$honeypot,
			TimeToken::elapsed( $token, wp_salt( 'nonce' ), time() ),
			$this->limiter->hit( (string) $submission->get_meta( 'remote_ip' ), time() ),
			$text
		);
		if ( '' === $reason ) {
			return false;
		}
		$submission->add_spam_log( [ 'agent' => 'bw-perma-forms', 'reason' => $reason ] );
		return true;
	}

	private function current_is_ours(): bool {
		$form = class_exists( '\WPCF7_ContactForm' ) ? \WPCF7_ContactForm::get_current() : null;
		return $form && '' !== (string) apply_filters( 'bw_perma_forms_form_key', '', (int) $form->id() );
	}
}
