<?php
/**
 * Tests for the CSV export.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Tests\Unit;

use BW\PermaForms\Modules\Contacts\Model\Contact;
use BW\PermaForms\Modules\Contacts\Service\CsvExporter;

final class CsvExporterTest extends TestCase {

	public function test_header_rows_meta_columns_and_bom(): void {
		$c   = Contact::from_row( [ 'id' => 1, 'email' => 'a@example.at', 'first_name' => 'Ä', 'interests' => 'basic,clinical', 'notes' => "Zeile 1\r\nZeile 2" ] );
		$csv = ( new CsvExporter() )->build( [ $c ], [ 'mitgliedsnummer' ], static fn( int $id ): array => [ 'mitgliedsnummer' => 'M-1' ] );
		$this->assertStringStartsWith( "\xEF\xBB\xBF", $csv );
		$rows = array_map( static fn( string $l ): array => str_getcsv( $l, ';', '"', '' ), preg_split( '/\n(?=\d|$)/', substr( $csv, 3 ) ) );
		$this->assertSame( 'E-Mail', $rows[0][1] );
		$this->assertSame( 'mitgliedsnummer', end( $rows[0] ) );
		$this->assertStringContainsString( 'Basic, Clinical Expert', $csv );
		$this->assertStringContainsString( ';Interessent:in;', $csv );
		$this->assertStringContainsString( 'M-1', $csv );
		$this->assertStringContainsString( "Zeile 1\nZeile 2", $csv );
	}

	public function test_formulas_are_neutralized(): void {
		$this->assertSame( "'=HYPERLINK(1)", CsvExporter::cell( '=HYPERLINK(1)' ) );
		$this->assertSame( "'+43 1", CsvExporter::cell( '+43 1' ) );
		$this->assertSame( 'normal', CsvExporter::cell( 'normal' ) );
	}
}
