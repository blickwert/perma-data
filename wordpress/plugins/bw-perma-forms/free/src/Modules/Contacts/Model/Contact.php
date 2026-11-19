<?php
/**
 * One person in the contact database (prospect now, member later).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Model;

final class Contact {

	public const STATUSES   = [ 'prospect', 'inquiry', 'member', 'former' ];
	public const NEWSLETTER = [ 'none', 'pending', 'subscribed', 'unsubscribed' ];
	public const INTERESTS  = [ 'basic', 'advanced', 'clinical' ];

	/**
	 * @param string[] $interests
	 */
	public function __construct(
		public readonly int $id,
		public readonly string $email,
		public readonly string $first_name = '',
		public readonly string $last_name = '',
		public readonly string $phone = '',
		public readonly string $profession = '',
		public readonly string $status = 'prospect',
		public readonly array $interests = [],
		public readonly string $newsletter = 'none',
		public readonly string $source = '',
		public readonly string $notes = '',
		public readonly string $created_at = '',
		public readonly string $updated_at = '',
	) {}

	/**
	 * Builds a contact from a database row.
	 *
	 * @param array<string, mixed> $row
	 */
	public static function from_row( array $row ): self {
		return new self(
			id: (int) ( $row['id'] ?? 0 ),
			email: (string) ( $row['email'] ?? '' ),
			first_name: (string) ( $row['first_name'] ?? '' ),
			last_name: (string) ( $row['last_name'] ?? '' ),
			phone: (string) ( $row['phone'] ?? '' ),
			profession: (string) ( $row['profession'] ?? '' ),
			status: (string) ( $row['status'] ?? 'prospect' ),
			interests: self::parse_interests( (string) ( $row['interests'] ?? '' ) ),
			newsletter: (string) ( $row['newsletter'] ?? 'none' ),
			source: (string) ( $row['source'] ?? '' ),
			notes: (string) ( $row['notes'] ?? '' ),
			created_at: (string) ( $row['created_at'] ?? '' ),
			updated_at: (string) ( $row['updated_at'] ?? '' ),
		);
	}

	/** @return string[] Known interest keys from a comma list, in canonical order. */
	public static function parse_interests( string $list ): array {
		$given = array_map( 'trim', explode( ',', strtolower( $list ) ) );
		return array_values( array_intersect( self::INTERESTS, $given ) );
	}

	public function name(): string {
		return trim( $this->first_name . ' ' . $this->last_name );
	}

	/** @return array<string, mixed> */
	public function to_array(): array {
		return [
			'id'         => $this->id,
			'email'      => $this->email,
			'first_name' => $this->first_name,
			'last_name'  => $this->last_name,
			'phone'      => $this->phone,
			'profession' => $this->profession,
			'status'     => $this->status,
			'interests'  => $this->interests,
			'newsletter' => $this->newsletter,
			'source'     => $this->source,
			'notes'      => $this->notes,
			'created_at' => $this->created_at,
			'updated_at' => $this->updated_at,
		];
	}
}
