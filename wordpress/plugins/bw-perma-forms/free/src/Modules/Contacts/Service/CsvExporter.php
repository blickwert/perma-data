<?php
/**
 * Builds the CSV export of the contact database (Excel-friendly: UTF-8 with BOM, semicolons).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Service;

use BW\PermaForms\Modules\Contacts\Model\Contact;

final class CsvExporter {

	public const DELIMITER = ';';

	/** @var array<string, string> column => header */
	private const COLUMNS = [
		'id'         => 'ID',
		'email'      => 'E-Mail',
		'first_name' => 'Vorname',
		'last_name'  => 'Nachname',
		'phone'      => 'Telefon',
		'profession' => 'Beruf / Ausbildung',
		'status'     => 'Status',
		'interests'  => 'Interessen',
		'newsletter' => 'Newsletter',
		'source'     => 'Quelle',
		'notes'      => 'Notizen',
		'created_at' => 'Erstellt (UTC)',
		'updated_at' => 'Geändert (UTC)',
	];

	/** @var array<string, array<string, string>> Readable values for coded columns (the export is for people, not machines). */
	private const VALUES = [
		'status'     => [ 'prospect' => 'Interessent:in', 'inquiry' => 'Anfrage', 'member' => 'Mitglied', 'former' => 'Ehemaliges Mitglied' ],
		'newsletter' => [ 'none' => 'nein', 'pending' => 'Bestätigung offen', 'subscribed' => 'angemeldet', 'unsubscribed' => 'abgemeldet' ],
		'interests'  => [ 'basic' => 'Basic', 'advanced' => 'Advanced', 'clinical' => 'Clinical Expert' ],
		'source'     => [ 'interest' => 'Interessentenliste', 'contact' => 'Kontaktformular', 'newsletter' => 'Newsletter' ],
	];

	/**
	 * CSV text for the given contacts; extra fields become additional columns.
	 *
	 * @param Contact[]                          $contacts
	 * @param string[]                           $meta_keys
	 * @param callable(int): array<string,string> $meta_for Returns the extra fields of a contact.
	 */
	public function build( array $contacts, array $meta_keys, callable $meta_for ): string {
		$out = fopen( 'php://temp', 'r+' );
		fwrite( $out, "\xEF\xBB\xBF" );
		fputcsv( $out, array_merge( array_values( self::COLUMNS ), $meta_keys ), self::DELIMITER, '"', '' );
		foreach ( $contacts as $contact ) {
			$row  = $contact->to_array();
			$meta = $meta_for( $contact->id );
			$line = [];
			foreach ( array_keys( self::COLUMNS ) as $col ) {
				$line[] = self::cell( self::readable( $col, $row[ $col ] ) );
			}
			foreach ( $meta_keys as $key ) {
				$line[] = self::cell( (string) ( $meta[ $key ] ?? '' ) );
			}
			fputcsv( $out, $line, self::DELIMITER, '"', '' );
		}
		rewind( $out );
		$csv = (string) stream_get_contents( $out );
		fclose( $out );
		return $csv;
	}

	/** Value of a column as text people understand (codes translated, lists joined). */
	public static function readable( string $col, mixed $value ): string {
		$map = self::VALUES[ $col ] ?? null;
		if ( is_array( $value ) ) {
			return implode( ', ', array_map( static fn( $v ): string => $map[ $v ] ?? (string) $v, $value ) );
		}
		return null === $map ? (string) $value : ( $map[ (string) $value ] ?? (string) $value );
	}

	/** Neutralizes spreadsheet formulas (CSV injection) and line breaks. */
	public static function cell( string $value ): string {
		$value = str_replace( [ "\r\n", "\r" ], "\n", $value );
		if ( '' !== $value && in_array( $value[0], [ '=', '+', '-', '@', "\t" ], true ) ) {
			$value = "'" . $value;
		}
		return $value;
	}

	public static function filename(): string {
		return 'kontakte-' . gmdate( 'Y-m-d' ) . '.csv';
	}
}
