<?php
/**
 * Newsletter signup with double opt-in through Brevo.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Newsletter\Service;

class NewsletterService {

	/**
	 * @param int[] $list_ids
	 */
	public function __construct(
		private readonly BrevoClient $client,
		private readonly array $list_ids,
		private readonly int $template_id,
		private readonly string $redirect_url,
	) {}

	public function ready(): bool {
		return $this->client->configured() && [] !== $this->list_ids && $this->template_id > 0;
	}

	/** Starts the double opt-in; the address is "pending" until the person confirms in Brevo's mail. */
	public function subscribe( string $email, string $first_name = '' ): true|\WP_Error {
		if ( ! $this->ready() ) {
			return new \WP_Error( 'bw_perma_forms_newsletter_setup', 'Brevo is not configured (API key, list, double opt-in template).' );
		}
		$result = $this->client->double_opt_in(
			BrevoClient::payload( $email, $this->list_ids, $this->template_id, $this->redirect_url, [ 'FIRSTNAME' => $first_name ] )
		);
		if ( true === $result ) {
			/**
			 * Fires when the newsletter state of an address changes.
			 *
			 * @param string $email
			 * @param string $state none|pending|subscribed|unsubscribed
			 * @param string $first_name
			 */
			do_action( 'bw_perma_forms_newsletter_state', $email, 'pending', $first_name );
		}
		return $result;
	}

	/** State for a Brevo webhook event ('' if the event does not change the newsletter state). */
	public static function state_for_event( string $event ): string {
		$event = strtolower( str_replace( [ '_', '-' ], '', $event ) );
		return match ( $event ) {
			'listaddition', 'contactadded'                  => 'subscribed',
			'unsubscribe', 'unsubscribed', 'contactdeleted' => 'unsubscribed',
			default                                         => '',
		};
	}
}
