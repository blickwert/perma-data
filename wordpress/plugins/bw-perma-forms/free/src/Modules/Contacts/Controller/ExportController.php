<?php
/**
 * CSV download of the contact database (admin-post.php, nonce + capability).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts\Controller;

use BW\PermaForms\Core\Plugin;
use BW\PermaForms\Modules\Contacts\Repository\ContactRepository;
use BW\PermaForms\Modules\Contacts\Repository\MetaRepository;
use BW\PermaForms\Modules\Contacts\Service\CsvExporter;

final class ExportController {

	public const ACTION = 'bw_perma_forms_export';

	public function __construct(
		private readonly ContactRepository $contacts,
		private readonly MetaRepository $meta,
		private readonly CsvExporter $exporter,
	) {}

	public function register(): void {
		add_action( 'admin_post_' . self::ACTION, [ $this, 'download' ] );
	}

	/** Base URL of the download link (the app adds the filters). */
	public static function url(): string {
		// Not wp_nonce_url(): that one escapes & to &amp; for HTML, the app needs a plain URL.
		return add_query_arg( [ 'action' => self::ACTION, '_wpnonce' => wp_create_nonce( self::ACTION ) ], admin_url( 'admin-post.php' ) );
	}

	public function download(): void {
		if ( ! current_user_can( Plugin::CONTACTS_CAPABILITY ) ) {
			wp_die( esc_html__( 'You are not allowed to export contacts.', 'bw-perma-forms' ), 403 );
		}
		check_admin_referer( self::ACTION );
		$filters = RestController::filters( wp_unslash( $_GET ) ); // phpcs:ignore WordPress.Security.ValidatedSanitizedInput.InputNotSanitized -- sanitized in filters().
		$result  = $this->contacts->search( $filters, 1, 0 );
		$csv     = $this->exporter->build( $result['items'], $this->meta->keys(), fn( int $id ): array => $this->meta->all( $id ) );
		nocache_headers();
		header( 'Content-Type: text/csv; charset=utf-8' );
		header( 'Content-Disposition: attachment; filename="' . CsvExporter::filename() . '"' );
		header( 'Content-Length: ' . strlen( $csv ) );
		echo $csv; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- CSV file, cells neutralized in CsvExporter.
		exit;
	}
}
