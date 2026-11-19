<?php
/**
 * Test bootstrap: Composer autoload, WordPress constants and small class stubs (no WordPress needed).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

require dirname( __DIR__ ) . '/vendor/autoload.php';

defined( 'ABSPATH' ) || define( 'ABSPATH', __DIR__ . '/' );
defined( 'ARRAY_A' ) || define( 'ARRAY_A', 'ARRAY_A' );

if ( ! class_exists( 'WP_Error' ) ) {
	/** Minimal WP_Error for unit tests. */
	class WP_Error {
		public function __construct( public string $code = '', public string $message = '', public mixed $data = null ) {}

		public function get_error_code(): string {
			return $this->code;
		}

		public function get_error_message(): string {
			return $this->message;
		}
	}
}
