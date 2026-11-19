<?php
/**
 * Interest list form: courses (multiple choice), optional newsletter opt-in, confirmation mail.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\InterestList;

use BW\PermaForms\Core\AbstractModule;
use BW\PermaForms\Modules\Forms\Service\Fields;
use BW\PermaForms\Modules\Forms\Service\FormDefinition;

final class InterestListModule extends AbstractModule {

	/** Course key => label shown in the form (labels are posted values). */
	public const COURSES = [
		'basic'    => 'Positive Psychology Basic',
		'advanced' => 'Positive Psychology Advanced',
		'clinical' => 'PERMA Clinical Expert',
	];

	/** {@inheritDoc} */
	public function id(): string {
		return 'interest-list';
	}

	/** {@inheritDoc} */
	public function name(): string {
		return __( 'Interest list', 'bw-perma-forms' );
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
		$privacy = esc_url( $this->settings->url( 'privacy_url' ) );
		$courses = implode( ' ', array_map( static fn( string $l ): string => '"' . $l . '"', self::COURSES ) );
		$template = <<<HTML
<div class="bw-form__row">
<div class="bw-form__field"><label class="bw-form__label" for="bw-il-vorname">Vorname</label>[text* vorname id:bw-il-vorname class:bw-form__input autocomplete:given-name]</div>
<div class="bw-form__field"><label class="bw-form__label" for="bw-il-nachname">Nachname</label>[text* nachname id:bw-il-nachname class:bw-form__input autocomplete:family-name]</div>
</div>
<div class="bw-form__field"><label class="bw-form__label" for="bw-il-email">E-Mail-Adresse</label>[email* email id:bw-il-email class:bw-form__input autocomplete:email]</div>
<fieldset class="bw-form__group"><legend class="bw-form__label">Ich interessiere mich für</legend>[checkbox* interesse use_label_element class:bw-form__options default:shortcode_attr {$courses}]</fieldset>
<div class="bw-form__field"><label class="bw-form__label" for="bw-il-beruf">Beruf oder bisherige Ausbildung <span class="bw-form__optional">(optional)</span></label>[text beruf id:bw-il-beruf class:bw-form__input]</div>
<div class="bw-form__field"><label class="bw-form__label" for="bw-il-nachricht">Deine Nachricht an uns <span class="bw-form__optional">(optional)</span></label>[textarea nachricht id:bw-il-nachricht class:bw-form__input x4]</div>
<p class="bw-form__hint">Mit deinem Eintrag nehmen wir dich in die Interessentenliste für deine ausgewählten Ausbildungen auf. Du erhältst dazu Informationen und später die Unterlagen für die verbindliche Anmeldung per E-Mail. Informationen zur Verarbeitung deiner Angaben findest du in unserer <a href="{$privacy}">Datenschutzerklärung</a>.</p>
<div class="bw-form__check">[acceptance newsletter optional class:bw-form__checkbox]Ja, ich möchte zusätzlich den Newsletter der PERMA Mind Academy mit Informationen zu Ausbildungen und Seminarterminen erhalten. Ich kann mich jederzeit wieder abmelden.[/acceptance]</div>
[turnstile]
[submit class:bw-form__submit "Unverbindlich eintragen"]
HTML;
		$done = 'Danke für dein Interesse an der PERMA Mind Academy. Du bist unverbindlich in der Interessentenliste für deine ausgewählten Ausbildungen eingetragen. Sobald die jeweilige Ausschreibung vorliegt, senden wir dir die Unterlagen für die verbindliche Anmeldung. Dein Eintrag reserviert noch keinen Platz.';
		return new FormDefinition(
			key: 'interest',
			title: 'PERMA: Interessentenliste',
			template: $template,
			mail: [
				'recipient'          => $this->settings->string( 'recipient' ),
				'sender'             => Fields::sender(),
				'subject'            => 'Interessentenliste: [vorname] [nachname] ([interesse])',
				'additional_headers' => 'Reply-To: [email]',
				'body'               => "Neuer Eintrag in die Interessentenliste\n\nName: [vorname] [nachname]\nE-Mail: [email]\nInteresse: [interesse]\nBeruf oder Ausbildung: [beruf]\nNewsletter gewünscht: [newsletter]\n\nNachricht:\n[nachricht]\n\n-- \nGesendet über [_site_url]",
				'use_html'           => false,
				'exclude_blank'      => true,
			],
			mail_2: [
				'recipient'          => '[email]',
				'sender'             => Fields::sender(),
				'subject'            => 'Deine Eintragung in die Interessentenliste der PERMA Mind Academy',
				'additional_headers' => 'Reply-To: ' . $this->settings->string( 'recipient' ),
				'body'               => "Hallo [vorname],\n\n{$done}\n\nDeine Auswahl: [interesse]\n\nHerzliche Grüße\nPERMA Mind Academy\n[_site_url]",
				'use_html'           => false,
				'exclude_blank'      => false,
			],
			messages: [
				'mail_sent_ok' => $done,
				'mail_sent_ng' => 'Dein Eintrag konnte gerade nicht gespeichert werden. Bitte versuche es später noch einmal oder schreib uns eine E-Mail.',
				'spam'         => 'Dein Eintrag konnte nicht gesendet werden. Bitte versuche es noch einmal.',
			],
			additional_settings: '',
			normalize: [ self::class, 'normalize' ],
			preselect: [ 'interesse' => self::COURSES ],
		);
	}

	/**
	 * Contact fields from the posted interest form.
	 *
	 * @param array<string, mixed> $posted
	 * @return array<string, mixed>
	 */
	public static function normalize( array $posted ): array {
		$labels = Fields::list( $posted, 'interesse' );
		return [
			'email'            => Fields::text( $posted, 'email' ),
			'first_name'       => Fields::text( $posted, 'vorname' ),
			'last_name'        => Fields::text( $posted, 'nachname' ),
			'profession'       => Fields::text( $posted, 'beruf' ),
			'interests'        => array_values( array_keys( array_intersect( self::COURSES, $labels ) ) ),
			'message'          => Fields::text( $posted, 'nachricht' ),
			'newsletter_optin' => Fields::checked( $posted, 'newsletter' ),
			'extra'            => [],
		];
	}
}
