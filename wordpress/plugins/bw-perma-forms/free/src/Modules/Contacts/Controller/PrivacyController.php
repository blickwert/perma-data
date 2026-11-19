<?php
/**
 * Hooks the contact database into the WordPress privacy tools (export and erase personal data).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Controller;

use BW\PermaForms\Modules\Contacts\Repository\ContactRepository;
use BW\PermaForms\Modules\Contacts\Service\ContactService;

final class PrivacyController {

	public function __construct(
		private readonly ContactRepository $contacts,
		private readonly ContactService $service,
	) {}

	public function register(): void {
		add_filter( 'wp_privacy_personal_data_exporters', [ $this, 'exporters' ] );
		add_filter( 'wp_privacy_personal_data_erasers', [ $this, 'erasers' ] );
	}

	/** @param array<string, mixed> $exporters */
	public function exporters( array $exporters ): array {
		$exporters['bw-perma-forms'] = [ 'exporter_friendly_name' => __( 'PERMA contacts', 'bw-perma-forms' ), 'callback' => [ $this, 'export' ] ];
		return $exporters;
	}

	/** @param array<string, mixed> $erasers */
	public function erasers( array $erasers ): array {
		$erasers['bw-perma-forms'] = [ 'eraser_friendly_name' => __( 'PERMA contacts', 'bw-perma-forms' ), 'callback' => [ $this, 'erase' ] ];
		return $erasers;
	}

	/** @return array{data: array<int, mixed>, done: bool} */
	public function export( string $email ): array {
		$contact = $this->contacts->find_by_email( strtolower( $email ) );
		if ( ! $contact ) {
			return [ 'data' => [], 'done' => true ];
		}
		$detail = (array) $this->service->detail( $contact->id );
		$items  = [];
		foreach ( [ 'email', 'first_name', 'last_name', 'phone', 'profession', 'status', 'newsletter', 'created_at' ] as $key ) {
			$items[] = [ 'name' => $key, 'value' => (string) $detail[ $key ] ];
		}
		$items[] = [ 'name' => 'interests', 'value' => implode( ', ', (array) $detail['interests'] ) ];
		foreach ( (array) $detail['meta'] as $key => $value ) {
			$items[] = [ 'name' => (string) $key, 'value' => (string) $value ];
		}
		foreach ( (array) $detail['submissions'] as $s ) {
			$items[] = [ 'name' => 'submission ' . $s['created_at'] . ' (' . $s['form'] . ')', 'value' => (string) $s['message'] ];
		}
		return [
			'data' => [ [ 'group_id' => 'bw-perma-contacts', 'group_label' => __( 'PERMA contacts', 'bw-perma-forms' ), 'item_id' => 'contact-' . $contact->id, 'data' => $items ] ],
			'done' => true,
		];
	}

	/** @return array{items_removed: bool, items_retained: bool, messages: string[], done: bool} */
	public function erase( string $email ): array {
		$contact = $this->contacts->find_by_email( strtolower( $email ) );
		$removed = $contact ? $this->service->delete( $contact->id ) : false;
		return [ 'items_removed' => $removed, 'items_retained' => false, 'messages' => [], 'done' => true ];
	}
}
