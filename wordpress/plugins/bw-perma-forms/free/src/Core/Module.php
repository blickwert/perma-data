<?php
/**
 * Contract for a feature module.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Core;

interface Module {

	/** Stable id, stored in options. Never rename after a release. */
	public function id(): string;

	public function name(): string;

	public function description(): string;

	/** @return string[] Ids of modules this module needs. */
	public function requires(): array;

	public function enabled_by_default(): bool;

	/** Registers hooks. Only called for active modules. */
	public function register(): void;
}
