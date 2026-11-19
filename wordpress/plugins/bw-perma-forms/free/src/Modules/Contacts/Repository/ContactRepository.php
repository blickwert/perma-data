<?php
/**
 * Loads and stores contacts in {prefix}bw_perma_contacts.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Repository;

use BW\PermaForms\Modules\Contacts\Model\Contact;

class ContactRepository {

	private const COLUMNS = [ 'email', 'first_name', 'last_name', 'phone', 'profession', 'status', 'interests', 'newsletter', 'source', 'notes' ];

	public function find( int $id ): ?Contact {
		global $wpdb;
		$row = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . Tables::contacts() . ' WHERE id = %d', $id ), ARRAY_A );
		return $row ? Contact::from_row( $row ) : null;
	}

	public function find_by_email( string $email ): ?Contact {
		global $wpdb;
		$row = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . Tables::contacts() . ' WHERE email = %s', $email ), ARRAY_A );
		return $row ? Contact::from_row( $row ) : null;
	}

	/**
	 * Inserts a contact and returns its id (0 on failure).
	 *
	 * @param array<string, mixed> $fields
	 */
	public function insert( array $fields ): int {
		global $wpdb;
		$now  = current_time( 'mysql', true );
		$data = $this->columns( $fields ) + [ 'notes' => '', 'created_at' => $now, 'updated_at' => $now ];
		return false === $wpdb->insert( Tables::contacts(), $data ) ? 0 : (int) $wpdb->insert_id;
	}

	/**
	 * Updates the given columns of a contact.
	 *
	 * @param array<string, mixed> $fields
	 */
	public function update( int $id, array $fields ): bool {
		global $wpdb;
		$data = $this->columns( $fields );
		if ( [] === $data ) {
			return true;
		}
		$data['updated_at'] = current_time( 'mysql', true );
		return false !== $wpdb->update( Tables::contacts(), $data, [ 'id' => $id ] );
	}

	public function delete( int $id ): bool {
		global $wpdb;
		return (bool) $wpdb->delete( Tables::contacts(), [ 'id' => $id ] );
	}

	/**
	 * Searches contacts.
	 *
	 * @param array{search?: string, status?: string, interest?: string, newsletter?: string} $filters
	 * @return array{items: Contact[], total: int}
	 */
	public function search( array $filters, int $page = 1, int $per_page = 50 ): array {
		global $wpdb;
		[ $where, $args ] = $this->where( $filters );
		$table  = Tables::contacts();
		$total  = (int) $wpdb->get_var( $args ? $wpdb->prepare( "SELECT COUNT(*) FROM {$table} {$where}", $args ) : "SELECT COUNT(*) FROM {$table} {$where}" );
		$limit  = $per_page > 0 ? $wpdb->prepare( ' LIMIT %d OFFSET %d', $per_page, max( 0, ( $page - 1 ) * $per_page ) ) : '';
		$sql    = "SELECT * FROM {$table} {$where} ORDER BY created_at DESC, id DESC" . $limit;
		$rows   = (array) $wpdb->get_results( $args ? $wpdb->prepare( $sql, $args ) : $sql, ARRAY_A );
		return [ 'items' => array_map( [ Contact::class, 'from_row' ], $rows ), 'total' => $total ];
	}

	/**
	 * WHERE clause and arguments for the filters (values only via prepare()).
	 *
	 * @param array<string, string> $filters
	 * @return array{0: string, 1: array<int, string>}
	 */
	private function where( array $filters ): array {
		global $wpdb;
		$parts = [];
		$args  = [];
		if ( ! empty( $filters['search'] ) ) {
			$like    = '%' . $wpdb->esc_like( $filters['search'] ) . '%';
			$parts[] = '(email LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR profession LIKE %s)';
			array_push( $args, $like, $like, $like, $like );
		}
		if ( ! empty( $filters['status'] ) ) {
			$parts[] = 'status = %s';
			$args[]  = $filters['status'];
		}
		if ( ! empty( $filters['newsletter'] ) ) {
			$parts[] = 'newsletter = %s';
			$args[]  = $filters['newsletter'];
		}
		if ( ! empty( $filters['interest'] ) ) {
			$parts[] = 'FIND_IN_SET(%s, interests) > 0';
			$args[]  = $filters['interest'];
		}
		return [ $parts ? 'WHERE ' . implode( ' AND ', $parts ) : '', $args ];
	}

	/**
	 * Keeps known columns; interests are stored as a comma list.
	 *
	 * @param array<string, mixed> $fields
	 * @return array<string, string>
	 */
	private function columns( array $fields ): array {
		$out = [];
		foreach ( self::COLUMNS as $col ) {
			if ( array_key_exists( $col, $fields ) ) {
				$out[ $col ] = 'interests' === $col && is_array( $fields[ $col ] ) ? implode( ',', $fields[ $col ] ) : (string) $fields[ $col ];
			}
		}
		return $out;
	}
}
