<?php
/**
 * Describes one form: its Contact Form 7 template, mails and messages, and how posted data is normalized.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Forms\Service;

final class FormDefinition {

	/**
	 * @param array<string, mixed>                                   $mail      CF7 mail property (empty: no mail).
	 * @param array<string, mixed>                                   $mail_2    CF7 mail_2 property (confirmation to the sender).
	 * @param array<string, string>                                  $messages  CF7 messages to override.
	 * @param callable(array<string, mixed>): array<string, mixed>   $normalize Maps CF7 posted data to the contact fields.
	 * @param array<string, string>                                  $preselect Shortcode attribute => default value source (e.g. interesse).
	 */
	public function __construct(
		public readonly string $key,
		public readonly string $title,
		public readonly string $template,
		public readonly array $mail,
		public readonly array $mail_2,
		public readonly array $messages,
		public readonly string $additional_settings,
		private readonly mixed $normalize,
		public readonly array $preselect = [],
	) {}

	/**
	 * Normalized data of a submission.
	 *
	 * @param array<string, mixed> $posted
	 * @return array<string, mixed>
	 */
	public function normalize( array $posted ): array {
		return ( $this->normalize )( $posted );
	}

	/** Fingerprint of everything that ends up in the CF7 form (to detect changes). */
	public function hash(): string {
		return md5( (string) wp_json_encode( [ $this->title, $this->template, $this->mail, $this->mail_2, $this->messages, $this->additional_settings ] ) );
	}
}
