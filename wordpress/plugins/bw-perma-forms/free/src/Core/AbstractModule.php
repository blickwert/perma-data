<?php
/**
 * Defaults for modules.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Core;

abstract class AbstractModule implements Module {

	public function __construct( protected readonly Settings $settings ) {}

	/** {@inheritDoc} */
	public function description(): string {
		return '';
	}

	/** {@inheritDoc} */
	public function requires(): array {
		return [];
	}

	/** {@inheritDoc} */
	public function enabled_by_default(): bool {
		return true;
	}
}
