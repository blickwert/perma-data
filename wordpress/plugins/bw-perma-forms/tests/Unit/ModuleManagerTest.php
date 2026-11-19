<?php
/**
 * Tests for module discovery and dependency resolution.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Tests\Unit;

use Brain\Monkey\Functions;
use BW\PermaForms\Core\ModuleManager;
use BW\PermaForms\Core\Settings;

final class ModuleManagerTest extends TestCase {

	private function manager( array $modules_option ): ModuleManager {
		Functions\when( 'get_option' )->justReturn( [ 'modules' => $modules_option ] );
		$m = new ModuleManager( new Settings() );
		$m->discover();
		return $m;
	}

	public function test_all_modules_active_by_default(): void {
		$active = array_keys( $this->manager( [] )->resolve() );
		sort( $active );
		$this->assertSame( [ 'contact', 'contacts', 'forms', 'interest-list', 'newsletter', 'spam-protection' ], $active );
	}

	public function test_modules_needing_forms_are_dropped_with_it(): void {
		$active = array_keys( $this->manager( [ 'forms' => false ] )->resolve() );
		$this->assertSame( [ 'contacts' ], $active );
	}
}
