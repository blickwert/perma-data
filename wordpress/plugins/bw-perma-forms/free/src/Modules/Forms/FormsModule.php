<?php
/**
 * Shared form infrastructure: definitions, Contact Form 7 sync, block and submission dispatch.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Forms;

use BW\PermaForms\Core\AbstractModule;
use BW\PermaForms\Modules\Forms\Controller\BlockController;
use BW\PermaForms\Modules\Forms\Controller\Cf7Controller;
use BW\PermaForms\Modules\Forms\Controller\RestController;
use BW\PermaForms\Modules\Forms\Service\FormProvisioner;
use BW\PermaForms\Modules\Forms\Service\FormRegistry;

final class FormsModule extends AbstractModule {

	/** {@inheritDoc} */
	public function id(): string {
		return 'forms';
	}

	/** {@inheritDoc} */
	public function name(): string {
		return __( 'Forms (Contact Form 7)', 'bw-perma-forms' );
	}

	/** {@inheritDoc} */
	public function register(): void {
		$registry    = new FormRegistry();
		$provisioner = new FormProvisioner( $registry );
		( new BlockController( $registry ) )->register();
		( new RestController( $registry, $provisioner ) )->register();
		if ( class_exists( '\WPCF7_ContactForm' ) ) {
			( new Cf7Controller( $registry, $provisioner ) )->register();
		}
	}
}
