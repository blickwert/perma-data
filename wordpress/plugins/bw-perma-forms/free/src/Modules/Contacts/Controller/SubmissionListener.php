<?php
/**
 * Stores form submissions and newsletter state changes announced by other modules.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Controller;

use BW\PermaForms\Modules\Contacts\Service\ContactService;

final class SubmissionListener {

	public function __construct( private readonly ContactService $service ) {}

	public function register(): void {
		add_action( 'bw_perma_forms_submitted', [ $this, 'on_submitted' ], 10, 2 );
		add_action( 'bw_perma_forms_newsletter_state', [ $this, 'on_newsletter_state' ], 10, 3 );
	}

	/**
	 * @param array<string, mixed> $data
	 */
	public function on_submitted( string $form, array $data ): void {
		$this->service->record_submission( $form, $data );
	}

	public function on_newsletter_state( string $email, string $state, string $first_name = '' ): void {
		$this->service->set_newsletter( $email, $state, $first_name );
	}
}
