<?php
/**
 * Discovers modules, resolves dependencies and registers the active ones.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Core;

use BW\PermaForms\Modules\Contact\ContactModule;
use BW\PermaForms\Modules\Contacts\ContactsModule;
use BW\PermaForms\Modules\Forms\FormsModule;
use BW\PermaForms\Modules\InterestList\InterestListModule;
use BW\PermaForms\Modules\Newsletter\NewsletterModule;
use BW\PermaForms\Modules\SpamProtection\SpamProtectionModule;

final class ModuleManager {

	/** @var array<string, Module> */
	private array $modules = [];

	/** @var array<string, Module> */
	private array $active = [];

	public function __construct( private readonly Settings $settings ) {}

	/** Collects all modules (free modules plus those added by the filter). */
	public function discover(): void {
		$modules = [
			new ContactsModule( $this->settings ),
			new FormsModule( $this->settings ),
			new SpamProtectionModule( $this->settings ),
			new InterestListModule( $this->settings ),
			new ContactModule( $this->settings ),
			new NewsletterModule( $this->settings ),
		];
		/**
		 * Lets other plugins add modules.
		 *
		 * @param Module[] $modules
		 */
		$modules = (array) apply_filters( 'bw_perma_forms_register_modules', $modules, $this->settings );
		foreach ( $modules as $module ) {
			if ( $module instanceof Module ) {
				$this->modules[ $module->id() ] = $module;
			}
		}
	}

	/** Registers all active modules whose requirements are met. */
	public function register(): void {
		$this->active = $this->resolve();
		foreach ( $this->active as $module ) {
			$module->register();
		}
	}

	/**
	 * Active modules after dependency checks.
	 *
	 * @return array<string, Module>
	 */
	public function resolve(): array {
		$enabled = array_filter(
			$this->modules,
			fn( Module $m ): bool => $this->settings->module_enabled( $m->id(), $m->enabled_by_default() )
		);
		// Drop modules whose requirements are missing, repeat until stable.
		do {
			$before  = count( $enabled );
			$enabled = array_filter(
				$enabled,
				static fn( Module $m ): bool => [] === array_diff( $m->requires(), array_keys( $enabled ) )
			);
		} while ( count( $enabled ) !== $before );
		return $enabled;
	}

	/** @return array<string, Module> */
	public function all(): array {
		return $this->modules;
	}

	/** @return array<string, Module> */
	public function active(): array {
		return $this->active;
	}
}
