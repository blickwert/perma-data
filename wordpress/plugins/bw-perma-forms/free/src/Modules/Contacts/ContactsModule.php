<?php
/**
 * Contact database: every person from the forms, extendable for members (extra fields), CSV export.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Contacts;

use BW\PermaForms\Core\AbstractModule;
use BW\PermaForms\Modules\Contacts\Controller\ExportController;
use BW\PermaForms\Modules\Contacts\Controller\PrivacyController;
use BW\PermaForms\Modules\Contacts\Controller\RestController;
use BW\PermaForms\Modules\Contacts\Controller\SubmissionListener;
use BW\PermaForms\Modules\Contacts\Repository\ContactRepository;
use BW\PermaForms\Modules\Contacts\Repository\MetaRepository;
use BW\PermaForms\Modules\Contacts\Repository\SubmissionRepository;
use BW\PermaForms\Modules\Contacts\Repository\Tables;
use BW\PermaForms\Modules\Contacts\Service\ContactService;
use BW\PermaForms\Modules\Contacts\Service\CsvExporter;

final class ContactsModule extends AbstractModule {

	/** {@inheritDoc} */
	public function id(): string {
		return 'contacts';
	}

	/** {@inheritDoc} */
	public function name(): string {
		return __( 'Contact database', 'bw-perma-forms' );
	}

	/** {@inheritDoc} */
	public function register(): void {
		Tables::register();
		$contacts    = new ContactRepository();
		$meta        = new MetaRepository();
		$service     = new ContactService( $contacts, new SubmissionRepository(), $meta );
		( new SubmissionListener( $service ) )->register();
		( new RestController( $contacts, $service ) )->register();
		( new ExportController( $contacts, $meta, new CsvExporter() ) )->register();
		( new PrivacyController( $contacts, $service ) )->register();
		add_filter( 'bw_perma_forms_admin_data', [ $this, 'admin_data' ] );
	}

	/**
	 * @param array<string, mixed> $data
	 * @return array<string, mixed>
	 */
	public function admin_data( array $data ): array {
		return $data + [
			'exportUrl'  => ExportController::url(),
			'statuses'   => \BW\PermaForms\Modules\Contacts\Model\Contact::STATUSES,
			'interests'  => \BW\PermaForms\Modules\Contacts\Model\Contact::INTERESTS,
			'newsletter' => \BW\PermaForms\Modules\Contacts\Model\Contact::NEWSLETTER,
		];
	}
}
