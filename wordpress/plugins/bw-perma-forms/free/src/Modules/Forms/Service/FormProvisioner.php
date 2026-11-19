<?php
/**
 * Creates and updates the Contact Form 7 forms from the definitions (the plugin is the source of truth).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Forms\Service;

class FormProvisioner {

	public function __construct( private readonly FormRegistry $registry ) {}

	/**
	 * Creates missing forms and updates changed ones.
	 *
	 * @param bool $force Also rewrite forms whose definition did not change (e.g. after manual edits in CF7).
	 * @return array<string, string> key => created|updated|unchanged|failed
	 */
	public function sync( bool $force = false ): array {
		if ( ! class_exists( '\WPCF7_ContactForm' ) ) {
			return [];
		}
		$result = [];
		$stored = $this->registry->stored();
		foreach ( $this->registry->definitions() as $key => $def ) {
			$id   = (int) ( $stored[ $key ]['id'] ?? 0 );
			$form = $id ? \WPCF7_ContactForm::get_instance( $id ) : null;
			if ( $form && ! $force && ( $stored[ $key ]['hash'] ?? '' ) === $def->hash() ) {
				$result[ $key ] = 'unchanged';
				continue;
			}
			$state = $form ? 'updated' : 'created';
			$form  = $form ?: \WPCF7_ContactForm::get_template( [ 'title' => $def->title ] );
			$form->set_title( $def->title );
			$form->set_properties( self::properties( $def, $form->get_properties() ) );
			$saved = (int) $form->save();
			if ( $saved > 0 ) {
				$this->registry->remember( $key, $saved, $def->hash() );
				$result[ $key ] = $state;
			} else {
				$result[ $key ] = 'failed';
			}
		}
		return $result;
	}

	/**
	 * CF7 properties for a definition.
	 *
	 * @param array<string, mixed> $current
	 * @return array<string, mixed>
	 */
	public static function properties( FormDefinition $def, array $current ): array {
		$mail             = array_merge( (array) ( $current['mail'] ?? [] ), $def->mail );
		$mail['active']   = [] !== $def->mail;
		$mail_2           = array_merge( (array) ( $current['mail_2'] ?? [] ), $def->mail_2 );
		$mail_2['active'] = [] !== $def->mail_2;
		return [
			'form'                => $def->template,
			'mail'                => $mail,
			'mail_2'              => $mail_2,
			'messages'            => array_merge( (array) ( $current['messages'] ?? [] ), $def->messages ),
			'additional_settings' => $def->additional_settings,
		];
	}
}
