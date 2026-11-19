<?php
/**
 * Newsletter form and signup via Brevo (double opt-in by Brevo).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Newsletter;

use BW\PermaForms\Core\AbstractModule;
use BW\PermaForms\Modules\Forms\Service\Fields;
use BW\PermaForms\Modules\Forms\Service\FormDefinition;
use BW\PermaForms\Modules\Newsletter\Controller\NewsletterController;
use BW\PermaForms\Modules\Newsletter\Service\BrevoClient;
use BW\PermaForms\Modules\Newsletter\Service\NewsletterService;

final class NewsletterModule extends AbstractModule {

	/** Option of the Brevo plugin that holds its API key (used when no own key is set). */
	public const BREVO_PLUGIN_KEY_OPTION = 'sib_api_key_v3';

	/** {@inheritDoc} */
	public function id(): string {
		return 'newsletter';
	}

	/** {@inheritDoc} */
	public function name(): string {
		return __( 'Newsletter (Brevo)', 'bw-perma-forms' );
	}

	/** {@inheritDoc} */
	public function requires(): array {
		return [ 'forms' ];
	}

	/** {@inheritDoc} */
	public function register(): void {
		add_filter( 'bw_perma_forms_definitions', [ $this, 'add_definition' ] );
		$lists   = array_filter( array_map( 'intval', explode( ',', $this->settings->string( 'brevo_list_ids' ) ) ) );
		$service = new NewsletterService(
			new BrevoClient( self::api_key( $this->settings->string( 'brevo_api_key' ) ) ),
			$lists,
			$this->settings->int( 'brevo_doi_template_id' ),
			$this->settings->url( 'brevo_redirect_url' )
		);
		( new NewsletterController( $service ) )->register();
		add_filter( 'bw_perma_forms_settings_response', [ $this, 'settings_response' ] );
	}

	/**
	 * @param array<string, mixed> $response
	 * @return array<string, mixed>
	 */
	public function settings_response( array $response ): array {
		return $response + [
			'has_brevo_plugin' => '' !== (string) get_option( self::BREVO_PLUGIN_KEY_OPTION, '' ),
			'webhook_url'      => NewsletterController::webhook_url(),
		];
	}

	/** Own key from the settings, otherwise the key of the connected Brevo plugin. */
	public static function api_key( string $own ): string {
		return '' !== $own ? $own : (string) get_option( self::BREVO_PLUGIN_KEY_OPTION, '' );
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
<div class="bw-form__field"><label class="bw-form__label" for="bw-nl-email">E-Mail-Adresse</label>[email* email id:bw-nl-email class:bw-form__input autocomplete:email]</div>
<div class="bw-form__field"><label class="bw-form__label" for="bw-nl-vorname">Vorname <span class="bw-form__optional">(optional)</span></label>[text vorname id:bw-nl-vorname class:bw-form__input autocomplete:given-name]</div>
<div class="bw-form__check">[acceptance consent class:bw-form__checkbox]Ich möchte den Newsletter der PERMA Mind Academy erhalten. Ich kann mich jederzeit wieder abmelden. Informationen zur Verarbeitung meiner Angaben finde ich in der <a href="{$privacy}">Datenschutzerklärung</a>.[/acceptance]</div>
[turnstile]
[submit class:bw-form__submit "Newsletter abonnieren"]
HTML;
		return new FormDefinition(
			key: 'newsletter',
			title: 'PERMA: Newsletter',
			template: $template,
			mail: [],
			mail_2: [],
			messages: [
				'mail_sent_ok'        => 'Bitte bestätige deine Newsletter-Anmeldung über den Link in unserer E-Mail.',
				'accept_terms'        => 'Bitte bestätige, dass du den Newsletter erhalten möchtest.',
				'spam'                => 'Die Anmeldung konnte nicht gesendet werden. Bitte versuche es noch einmal.',
			],
			// The confirmation mail comes from Brevo (double opt-in), CF7 sends nothing.
			additional_settings: 'skip_mail: on',
			normalize: [ self::class, 'normalize' ],
		);
	}

	/**
	 * @param array<string, mixed> $posted
	 * @return array<string, mixed>
	 */
	public static function normalize( array $posted ): array {
		return [
			'email'            => Fields::text( $posted, 'email' ),
			'first_name'       => Fields::text( $posted, 'vorname' ),
			'interests'        => [],
			'message'          => '',
			'newsletter_optin' => true,
			'extra'            => [],
		];
	}
}
