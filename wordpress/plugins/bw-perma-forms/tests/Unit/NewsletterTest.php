<?php
/**
 * Tests for the Brevo payload, webhook states and the signup service.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Tests\Unit;

use Brain\Monkey\Actions;
use BW\PermaForms\Modules\Newsletter\Service\BrevoClient;
use BW\PermaForms\Modules\Newsletter\Service\NewsletterService;

final class NewsletterTest extends TestCase {

	public function test_payload(): void {
		$p = BrevoClient::payload( 'a@example.at', [ '3', 5 ], 12, 'https://x.at/ok', [ 'FIRSTNAME' => 'Anna', 'LASTNAME' => '' ] );
		$this->assertSame( [ 3, 5 ], $p['includeListIds'] );
		$this->assertSame( 12, $p['templateId'] );
		$this->assertSame( [ 'FIRSTNAME' => 'Anna' ], $p['attributes'] );
		$this->assertArrayNotHasKey( 'attributes', BrevoClient::payload( 'a@example.at', [ 3 ], 12, 'u' ) );
	}

	public function test_webhook_states(): void {
		$this->assertSame( 'subscribed', NewsletterService::state_for_event( 'list_addition' ) );
		$this->assertSame( 'subscribed', NewsletterService::state_for_event( 'listAddition' ) );
		$this->assertSame( 'unsubscribed', NewsletterService::state_for_event( 'unsubscribe' ) );
		$this->assertSame( '', NewsletterService::state_for_event( 'opened' ) );
	}

	public function test_subscribe_needs_configuration(): void {
		$client = $this->createMock( BrevoClient::class );
		$client->method( 'configured' )->willReturn( true );
		$client->expects( $this->never() )->method( 'double_opt_in' );
		$service = new NewsletterService( $client, [], 12, 'u' );
		$this->assertInstanceOf( \WP_Error::class, $service->subscribe( 'a@example.at' ) );
	}

	public function test_subscribe_marks_pending_on_success(): void {
		$client = $this->createMock( BrevoClient::class );
		$client->method( 'configured' )->willReturn( true );
		$client->expects( $this->once() )->method( 'double_opt_in' )->willReturn( true );
		Actions\expectDone( 'bw_perma_forms_newsletter_state' )->once()->with( 'a@example.at', 'pending', 'Anna' );
		$this->assertTrue( ( new NewsletterService( $client, [ 3 ], 12, 'u' ) )->subscribe( 'a@example.at', 'Anna' ) );
	}

	public function test_failed_signup_does_not_mark_pending(): void {
		$client = $this->createMock( BrevoClient::class );
		$client->method( 'configured' )->willReturn( true );
		$client->method( 'double_opt_in' )->willReturn( new \WP_Error( 'x', 'down' ) );
		Actions\expectDone( 'bw_perma_forms_newsletter_state' )->never();
		$this->assertInstanceOf( \WP_Error::class, ( new NewsletterService( $client, [ 3 ], 12, 'u' ) )->subscribe( 'a@example.at' ) );
	}
}
