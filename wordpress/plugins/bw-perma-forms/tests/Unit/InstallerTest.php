<?php
/**
 * Tests for the capability of the contact list (administrators and editors).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Tests\Unit;

use Brain\Monkey\Filters;
use Brain\Monkey\Functions;
use BW\PermaForms\Core\Installer;
use BW\PermaForms\Core\Plugin;

final class InstallerTest extends TestCase {

	public function test_upgrade_grants_contacts_capability_to_admins_and_editors_once(): void {
		$granted = [];
		$role    = static function ( string $name ) use ( &$granted ) {
			return new class( $name, $granted ) {
			public function __construct( private string $name, private array &$log ) {}
			public function add_cap( string $cap ): void {
				$this->log[] = $this->name . ':' . $cap;
			}
			};
		};
		Functions\when( 'get_option' )->alias( static fn( string $key ) => Installer::DB_VERSION_OPTION === $key ? Installer::DB_VERSION : false );
		Functions\when( 'get_role' )->alias( $role );
		Functions\expect( 'update_option' )->once()->with( Installer::CAPS_VERSION_OPTION, Installer::CAPS_VERSION, false );

		Installer::maybe_upgrade();

		$this->assertSame( [ 'administrator:' . Plugin::CONTACTS_CAPABILITY, 'editor:' . Plugin::CONTACTS_CAPABILITY ], $granted );
	}

	public function test_roles_can_be_changed_by_filter_and_missing_roles_are_skipped(): void {
		Functions\when( 'get_option' )->alias( static fn( string $key ) => Installer::DB_VERSION_OPTION === $key ? Installer::DB_VERSION : false );
		Functions\when( 'get_role' )->justReturn( null );
		Functions\when( 'update_option' )->justReturn( true );
		Filters\expectApplied( 'bw_perma_forms_contacts_roles' )->once()->andReturn( [ 'shop_manager' ] );

		Installer::maybe_upgrade();

		$this->assertTrue( true );
	}
}
