<?php
/**
 * Base test case with Brain Monkey set up.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Tests\Unit;

use Brain\Monkey;
use Brain\Monkey\Functions;

abstract class TestCase extends \PHPUnit\Framework\TestCase {

	protected function setUp(): void {
		parent::setUp();
		Monkey\setUp();
		Functions\stubTranslationFunctions();
		Functions\stubEscapeFunctions();
		Functions\stubs(
			[
				'is_email'                => static fn( string $e ): bool => false !== filter_var( $e, FILTER_VALIDATE_EMAIL ),
				'sanitize_text_field'     => static fn( $v ): string => trim( strip_tags( (string) $v ) ),
				'sanitize_textarea_field' => static fn( $v ): string => trim( strip_tags( (string) $v ) ),
				'sanitize_key'            => static fn( $v ): string => preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $v ) ),
				'wp_json_encode'          => static fn( $v ): string => (string) json_encode( $v ),
			]
		);
	}

	protected function tearDown(): void {
		Monkey\tearDown();
		parent::tearDown();
	}
}
