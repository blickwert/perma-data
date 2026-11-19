<?php
/**
 * Free-form extra fields per contact (WordPress metadata API on bw_perma_contactmeta).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Repository;

class MetaRepository {

	/** @return array<string, string> Single values per key. */
	public function all( int $contact_id ): array {
		$out = [];
		foreach ( (array) get_metadata( Tables::META_TYPE, $contact_id ) as $key => $values ) {
			if ( ! str_starts_with( (string) $key, '_' ) ) {
				$out[ (string) $key ] = (string) ( $values[0] ?? '' );
			}
		}
		ksort( $out );
		return $out;
	}

	public function set( int $contact_id, string $key, string $value ): void {
		if ( '' === $value ) {
			delete_metadata( Tables::META_TYPE, $contact_id, $key );
			return;
		}
		update_metadata( Tables::META_TYPE, $contact_id, $key, $value );
	}

	public function delete_all( int $contact_id ): void {
		foreach ( array_keys( $this->all( $contact_id ) ) as $key ) {
			delete_metadata( Tables::META_TYPE, $contact_id, $key );
		}
	}

	/** @return string[] All meta keys in use (columns for the CSV export). */
	public function keys(): array {
		global $wpdb;
		$keys = (array) $wpdb->get_col( 'SELECT DISTINCT meta_key FROM ' . Tables::meta() . " WHERE meta_key NOT LIKE '\\_%' ORDER BY meta_key" );
		return array_map( 'strval', $keys );
	}
}
