<?php
/**
 * Spam protection for all forms: honeypot, minimum fill time, rate limit, link and word filter.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\SpamProtection;

use BW\PermaForms\Core\AbstractModule;
use BW\PermaForms\Modules\SpamProtection\Controller\SpamController;
use BW\PermaForms\Modules\SpamProtection\Service\RateLimiter;
use BW\PermaForms\Modules\SpamProtection\Service\SpamGuard;

final class SpamProtectionModule extends AbstractModule {

	/** {@inheritDoc} */
	public function id(): string {
		return 'spam-protection';
	}

	/** {@inheritDoc} */
	public function name(): string {
		return __( 'Spam protection', 'bw-perma-forms' );
	}

	/** {@inheritDoc} */
	public function requires(): array {
		return [ 'forms' ];
	}

	/** {@inheritDoc} */
	public function register(): void {
		$guard = new SpamGuard(
			$this->settings->int( 'spam_min_seconds' ),
			$this->settings->int( 'spam_rate_limit' ),
			$this->settings->int( 'spam_max_links' ),
			SpamGuard::parse_blocklist( $this->settings->string( 'spam_blocklist' ) )
		);
		( new SpamController( $guard, new RateLimiter( $this->settings->int( 'spam_rate_window' ) ) ) )->register();
	}
}
