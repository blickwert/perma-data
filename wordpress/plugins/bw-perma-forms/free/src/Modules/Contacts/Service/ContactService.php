<?php
/**
 * Business rules of the contact database: merge form submissions into one record per e-mail address.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Service;

use BW\PermaForms\Modules\Contacts\Model\Contact;
use BW\PermaForms\Modules\Contacts\Repository\ContactRepository;
use BW\PermaForms\Modules\Contacts\Repository\MetaRepository;
use BW\PermaForms\Modules\Contacts\Repository\SubmissionRepository;

class ContactService {

	public function __construct(
		private readonly ContactRepository $contacts,
		private readonly SubmissionRepository $submissions,
		private readonly MetaRepository $meta,
	) {}

	/**
	 * Saves a submission: creates or updates the contact and adds a history entry.
	 *
	 * @param array<string, mixed> $data Normalized form data (email, first_name, last_name, profession, interests, message, extra).
	 * @return int Contact id, 0 if the e-mail address is invalid.
	 */
	public function record_submission( string $form, array $data ): int {
		$email = self::normalize_email( (string) ( $data['email'] ?? '' ) );
		if ( '' === $email ) {
			return 0;
		}
		$existing = $this->contacts->find_by_email( $email );
		$fields   = self::merge( $existing, $form, $data );
		if ( $existing ) {
			$this->contacts->update( $existing->id, $fields );
			$id = $existing->id;
		} else {
			$id = $this->contacts->insert( [ 'email' => $email ] + $fields );
			if ( 0 === $id ) {
				return 0;
			}
		}
		$this->submissions->add(
			$id,
			$form,
			Contact::parse_interests( implode( ',', (array) ( $data['interests'] ?? [] ) ) ),
			(string) ( $data['message'] ?? '' ),
			(array) ( $data['extra'] ?? [] )
		);
		$contact = $this->contacts->find( $id );
		if ( $contact ) {
			/**
			 * Fires after a form submission was stored in the contact database.
			 *
			 * @param Contact $contact
			 * @param string  $form Form key (interest, contact, newsletter).
			 */
			do_action( 'bw_perma_forms_contact_saved', $contact, $form );
		}
		return $id;
	}

	/**
	 * Fields to store for a submission (pure rule, no database access).
	 * Names and profession are only overwritten with non-empty values, interests are added up,
	 * the status never goes back (a member stays a member).
	 *
	 * @param array<string, mixed> $data
	 * @return array<string, mixed>
	 */
	public static function merge( ?Contact $existing, string $form, array $data ): array {
		$fields = [];
		foreach ( [ 'first_name', 'last_name', 'profession', 'phone' ] as $key ) {
			$value = trim( (string) ( $data[ $key ] ?? '' ) );
			if ( '' !== $value ) {
				$fields[ $key ] = $value;
			}
		}
		$new_interests       = Contact::parse_interests( implode( ',', (array) ( $data['interests'] ?? [] ) ) );
		$fields['interests'] = Contact::parse_interests( implode( ',', array_merge( $existing?->interests ?? [], $new_interests ) ) );

		$wanted = 'interest' === $form ? 'prospect' : ( 'contact' === $form ? 'inquiry' : '' );
		if ( null === $existing ) {
			$fields['status'] = $wanted ?: 'prospect';
			$fields['source'] = $form;
		} elseif ( 'prospect' === $wanted && 'inquiry' === $existing->status ) {
			$fields['status'] = 'prospect';
		}
		return $fields;
	}

	/**
	 * Sets the newsletter state of an address; creates the contact if needed.
	 */
	public function set_newsletter( string $email, string $state, string $first_name = '' ): int {
		$email = self::normalize_email( $email );
		if ( '' === $email || ! in_array( $state, Contact::NEWSLETTER, true ) ) {
			return 0;
		}
		$existing = $this->contacts->find_by_email( $email );
		if ( $existing ) {
			$fields = [ 'newsletter' => $state ];
			if ( '' !== $first_name && '' === $existing->first_name ) {
				$fields['first_name'] = $first_name;
			}
			$this->contacts->update( $existing->id, $fields );
			return $existing->id;
		}
		return $this->contacts->insert( [ 'email' => $email, 'first_name' => $first_name, 'newsletter' => $state, 'status' => 'prospect', 'source' => 'newsletter' ] );
	}

	/**
	 * Updates a contact from the admin.
	 *
	 * @param array<string, mixed> $input Allowed: email, first_name, last_name, phone, profession, status, interests, newsletter, notes, meta (key => value).
	 * @return Contact|\WP_Error
	 */
	public function update( int $id, array $input ): Contact|\WP_Error {
		$contact = $this->contacts->find( $id );
		if ( ! $contact ) {
			return new \WP_Error( 'bw_perma_forms_not_found', __( 'Contact not found.', 'bw-perma-forms' ), [ 'status' => 404 ] );
		}
		$fields = [];
		foreach ( [ 'first_name', 'last_name', 'phone', 'profession' ] as $key ) {
			if ( isset( $input[ $key ] ) ) {
				$fields[ $key ] = sanitize_text_field( (string) $input[ $key ] );
			}
		}
		if ( isset( $input['notes'] ) ) {
			$fields['notes'] = sanitize_textarea_field( (string) $input['notes'] );
		}
		if ( isset( $input['email'] ) ) {
			$email = self::normalize_email( (string) $input['email'] );
			$other = '' === $email ? null : $this->contacts->find_by_email( $email );
			if ( '' === $email || ( $other && $other->id !== $id ) ) {
				return new \WP_Error( 'bw_perma_forms_email', __( 'The e-mail address is invalid or already used by another contact.', 'bw-perma-forms' ), [ 'status' => 400 ] );
			}
			$fields['email'] = $email;
		}
		if ( isset( $input['status'] ) && in_array( $input['status'], Contact::STATUSES, true ) ) {
			$fields['status'] = $input['status'];
		}
		if ( isset( $input['newsletter'] ) && in_array( $input['newsletter'], Contact::NEWSLETTER, true ) ) {
			$fields['newsletter'] = $input['newsletter'];
		}
		if ( isset( $input['interests'] ) ) {
			$fields['interests'] = Contact::parse_interests( implode( ',', (array) $input['interests'] ) );
		}
		$this->contacts->update( $id, $fields );
		foreach ( (array) ( $input['meta'] ?? [] ) as $key => $value ) {
			$key = sanitize_key( (string) $key );
			if ( '' !== $key && ! str_starts_with( $key, '_' ) ) {
				$this->meta->set( $id, $key, sanitize_textarea_field( (string) $value ) );
			}
		}
		$updated = $this->contacts->find( $id );
		/**
		 * Fires after a contact was changed in the admin.
		 *
		 * @param Contact $updated
		 */
		do_action( 'bw_perma_forms_contact_updated', $updated );
		return $updated;
	}

	/**
	 * Contact with extra fields and submission history.
	 *
	 * @return array<string, mixed>|null
	 */
	public function detail( int $id ): ?array {
		$contact = $this->contacts->find( $id );
		if ( ! $contact ) {
			return null;
		}
		return $contact->to_array() + [
			'meta'        => $this->meta->all( $id ),
			'submissions' => $this->submissions->for_contact( $id ),
		];
	}

	/** Deletes a contact with all extra fields and submissions (GDPR erasure). */
	public function delete( int $id ): bool {
		$this->submissions->delete_for_contact( $id );
		$this->meta->delete_all( $id );
		return $this->contacts->delete( $id );
	}

	public static function normalize_email( string $email ): string {
		$email = strtolower( trim( $email ) );
		return is_email( $email ) ? $email : '';
	}
}
