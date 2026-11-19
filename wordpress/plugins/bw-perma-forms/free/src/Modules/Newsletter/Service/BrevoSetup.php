<?php
/**
 * Creates what the newsletter needs in Brevo: a list and the double opt-in confirmation template.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Newsletter\Service;

class BrevoSetup {

	public const LIST_NAME     = 'Newsletter PERMA Mind Academy';
	public const TEMPLATE_NAME = 'PERMA Newsletter – Bestätigung (Double-Opt-in)';

	public function __construct( private readonly BrevoClient $client ) {}

	/**
	 * Creates the list and/or template if wanted and returns their ids.
	 *
	 * @param string $webhook_url Where Brevo reports confirmations and unsubscribes ('' = no webhook).
	 * @return array{list_id: int, template_id: int, webhook_id?: int}|\WP_Error
	 */
	public function run( bool $create_list, bool $create_template, string $site_name, string $webhook_url = '' ): array|\WP_Error {
		$result = [ 'list_id' => 0, 'template_id' => 0 ];
		if ( '' !== $webhook_url ) {
			$hook = $this->client->ensure_webhook( $webhook_url, [ 'listAddition', 'unsubscribed', 'contactDeleted' ] );
			if ( is_wp_error( $hook ) ) {
				return $hook;
			}
			$result['webhook_id'] = $hook;
		}
		// Reuse what an earlier run created (same name), so repeating the setup creates no duplicates.
		$existing = $this->client->options();
		if ( is_wp_error( $existing ) ) {
			return $existing;
		}
		foreach ( $existing['lists'] as $list ) {
			if ( self::LIST_NAME === $list['name'] ) {
				$result['list_id'] = $list['id'];
				$create_list       = false;
			}
		}
		foreach ( $existing['templates'] as $template ) {
			if ( self::TEMPLATE_NAME === $template['name'] && $template['active'] ) {
				$result['template_id'] = $template['id'];
				$create_template       = false;
			}
		}
		if ( $create_list ) {
			$folder = $this->client->folder_id( 'PERMA Mind Academy' );
			if ( is_wp_error( $folder ) ) {
				return $folder;
			}
			$list = $this->client->create_list( self::LIST_NAME, $folder );
			if ( is_wp_error( $list ) ) {
				return $list;
			}
			$result['list_id'] = $list;
		}
		if ( $create_template ) {
			$sender = $this->client->sender();
			if ( null === $sender ) {
				return new \WP_Error( 'bw_perma_forms_brevo_sender', 'Brevo has no active sender address. Add and verify one in Brevo (Senders, Domains & Dedicated IPs).' );
			}
			$template = $this->client->create_template( self::template( $sender, $site_name ) );
			if ( is_wp_error( $template ) ) {
				return $template;
			}
			$result['template_id'] = $template;
		}
		return $result;
	}

	/**
	 * Brevo template for the double opt-in mail. Brevo needs the tag "optin" and the {{ doubleoptin }} link.
	 * Mail HTML needs inline styles (mail clients ignore stylesheets); colours from the PERMA design tokens.
	 *
	 * @param array{name: string, email: string} $sender
	 * @return array<string, mixed>
	 */
	public static function template( array $sender, string $site_name ): array {
		$html = <<<'HTML'
<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bitte bestätige deine Anmeldung</title></head>
<body style="margin:0;padding:0;background:#F7F9FB;font-family:Roboto,Arial,sans-serif;color:#00416B;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F7F9FB;"><tr><td align="center" style="padding:32px 16px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#FFFFFF;border-radius:12px;border-top:6px solid #16A5D2;">
<tr><td style="padding:32px 32px 8px;font-size:12px;letter-spacing:0.24em;text-transform:uppercase;font-weight:bold;">PERMA Mind Academy</td></tr>
<tr><td style="padding:8px 32px 0;font-family:Montserrat,Arial,sans-serif;font-size:26px;line-height:1.3;">Bitte bestätige deine Anmeldung</td></tr>
<tr><td style="padding:16px 32px 0;font-size:16px;line-height:1.7;">Hallo,<br>danke für dein Interesse am Newsletter der PERMA Mind Academy. Bitte bestätige mit einem Klick, dass du ihn erhalten möchtest.</td></tr>
<tr><td style="padding:24px 32px;"><a href="{{ doubleoptin }}" style="display:inline-block;padding:14px 28px;border-radius:999px;background:#00416B;color:#FFFFFF;text-decoration:none;font-weight:bold;">Anmeldung bestätigen</a></td></tr>
<tr><td style="padding:0 32px 32px;font-size:14px;line-height:1.7;color:#386B8C;">Wenn du dich nicht angemeldet hast, ignoriere diese E-Mail einfach. Ohne Bestätigung erhältst du keinen Newsletter.</td></tr>
</table></td></tr></table>
</body></html>
HTML;
		return [
			'templateName' => self::TEMPLATE_NAME,
			'subject'      => 'Bitte bestätige deine Newsletter-Anmeldung',
			'sender'       => [ 'name' => '' !== $sender['name'] ? $sender['name'] : $site_name, 'email' => $sender['email'] ],
			'htmlContent'  => $html,
			'tag'          => 'optin',
		];
	}
}
