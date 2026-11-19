<?php
/**
 * Contact form: name, e-mail, message; mail to the configured recipient.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contact;

use BW\PermaForms\Core\AbstractModule;
use BW\PermaForms\Modules\Forms\Service\Fields;
use BW\PermaForms\Modules\Forms\Service\FormDefinition;

final class ContactModule extends AbstractModule {

	/** {@inheritDoc} */
	public function id(): string {
		return 'contact';
	}

	/** {@inheritDoc} */
	public function name(): string {
		return __( 'Contact form', 'bw-perma-forms' );
	}

	/** {@inheritDoc} */
	public function requires(): array {
		return [ 'forms' ];
	}

	/** {@inheritDoc} */
	public function register(): void {
		add_filter( 'bw_perma_forms_definitions', [ $this, 'add_definition' ] );
	}

	/**
	 * @param array<int, FormDefinition> $definitions
	 * @return array<int, FormDefinition>
	 */
	public function add_definition( array $definitions ): array {
		$definitions[] = $this->definition();
		return $definitions;
	}

	public function definition(): FormDefinition {
		$privacy  = esc_url( $this->settings->url( 'privacy_url' ) );
		$template = <<<HTML
<div class="bw-form__field"><label class="bw-form__label" for="bw-kf-name">Name</label>[text* name id:bw-kf-name class:bw-form__input autocomplete:name]</div>
<div class="bw-form__field"><label class="bw-form__label" for="bw-kf-email">E-Mail-Adresse</label>[email* email id:bw-kf-email class:bw-form__input autocomplete:email]</div>
<div class="bw-form__field"><label class="bw-form__label" for="bw-kf-nachricht">Nachricht</label>[textarea* nachricht id:bw-kf-nachricht class:bw-form__input x4]</div>
<p class="bw-form__hint">Informationen zur Verarbeitung deiner Angaben findest du in unserer <a href="{$privacy}">Datenschutzerklärung</a>.</p>
[turnstile]
[submit class:bw-form__submit "Nachricht senden"]
HTML;
		return new FormDefinition(
			key: 'contact',
			title: 'PERMA: Kontakt',
			template: $template,
			mail: [
				'recipient'          => $this->settings->string( 'recipient' ),
				'sender'             => Fields::sender(),
				'subject'            => 'Kontaktanfrage von [name]',
				'additional_headers' => 'Reply-To: [email]',
				'body'               => "Neue Nachricht über das Kontaktformular\n\nName: [name]\nE-Mail: [email]\n\nNachricht:\n[nachricht]\n\n-- \nGesendet über [_site_url]",
				'use_html'           => false,
				'exclude_blank'      => false,
			],
			mail_2: [],
			messages: [
				'mail_sent_ok' => 'Danke für deine Nachricht. Wir melden uns per E-Mail bei dir.',
				'mail_sent_ng' => 'Deine Nachricht konnte gerade nicht gesendet werden. Bitte versuche es später noch einmal.',
				'spam'         => 'Deine Nachricht konnte nicht gesendet werden. Bitte versuche es noch einmal.',
			],
			additional_settings: '',
			normalize: [ self::class, 'normalize' ],
		);
	}

	/**
	 * @param array<string, mixed> $posted
	 * @return array<string, mixed>
	 */
	public static function normalize( array $posted ): array {
		[ $first, $last ] = Fields::split_name( Fields::text( $posted, 'name' ) );
		return [
			'email'            => Fields::text( $posted, 'email' ),
			'first_name'       => $first,
			'last_name'        => $last,
			'interests'        => [],
			'message'          => Fields::text( $posted, 'nachricht' ),
			'newsletter_optin' => false,
			'extra'            => [],
		];
	}
}
