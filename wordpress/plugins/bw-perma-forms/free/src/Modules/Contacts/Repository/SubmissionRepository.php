<?php
/**
 * Stores every form submission of a contact (history).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Repository;

class SubmissionRepository {

	/**
	 * Adds a submission.
	 *
	 * @param string[]             $interests
	 * @param array<string, mixed> $data Extra fields (no IP addresses).
	 */
	public function add( int $contact_id, string $form, array $interests, string $message, array $data ): int {
		global $wpdb;
		$ok = $wpdb->insert(
			Tables::submissions(),
			[
				'contact_id' => $contact_id,
				'form'       => $form,
				'interests'  => implode( ',', $interests ),
				'message'    => $message,
				'data'       => (string) wp_json_encode( $data ),
				'created_at' => current_time( 'mysql', true ),
			]
		);
		return false === $ok ? 0 : (int) $wpdb->insert_id;
	}

	/** @return array<int, array<string, mixed>> Newest first. */
	public function for_contact( int $contact_id ): array {
		global $wpdb;
		$rows = (array) $wpdb->get_results(
			$wpdb->prepare( 'SELECT * FROM ' . Tables::submissions() . ' WHERE contact_id = %d ORDER BY created_at DESC, id DESC', $contact_id ),
			ARRAY_A
		);
		return array_map(
			static fn( array $r ): array => [
				'id'         => (int) $r['id'],
				'form'       => (string) $r['form'],
				'interests'  => array_values( array_filter( explode( ',', (string) $r['interests'] ) ) ),
				'message'    => (string) $r['message'],
				'data'       => (array) json_decode( (string) $r['data'], true ),
				'created_at' => (string) $r['created_at'],
			],
			$rows
		);
	}

	public function delete_for_contact( int $contact_id ): void {
		global $wpdb;
		$wpdb->delete( Tables::submissions(), [ 'contact_id' => $contact_id ] );
	}
}
