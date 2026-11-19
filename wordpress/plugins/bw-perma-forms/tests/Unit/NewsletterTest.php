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
use BW\PermaForms\Modules\Newsletter\Service\BrevoSetup;
use BW\PermaForms\Modules\Newsletter\Service\NewsletterService;

final class NewsletterTest extends TestCase {

	public function test_payload(): void {
		$p = BrevoClient::payload( 'a@example.at', [ '3', 5 ], 12, 'https://x.at/ok', [ 'FIRSTNAME' => 'Anna', 'LASTNAME' => '' ] );
		$this->assertSame( [ 3, 5 ], $p['includeListIds'] );
		$this->assertSame( 12, $p['templateId'] );
		$this->assertSame( [ 'FIRSTNAME' => 'Anna' ], $p['attributes'] );
		$this->assertArrayNotHasKey( 'attributes', BrevoClient::payload( 'a@example.at', [ 3 ], 12, 'u' ) );
	}

	public function test_doi_template_meets_brevo_rules(): void {
		$t = BrevoSetup::template( [ 'name' => '', 'email' => 'news@example.at' ], 'PERMA Mind Academy' );
		$this->assertSame( 'optin', $t['tag'] );
		$this->assertStringContainsString( '{{ doubleoptin }}', $t['htmlContent'] );
		$this->assertSame( [ 'name' => 'PERMA Mind Academy', 'email' => 'news@example.at' ], $t['sender'] );
	}

	public function test_setup_stops_without_sender(): void {
		$client = $this->createMock( BrevoClient::class );
		$client->method( 'options' )->willReturn( [ 'lists' => [], 'templates' => [] ] );
		$client->method( 'sender' )->willReturn( null );
		$client->expects( $this->never() )->method( 'create_template' );
		$this->assertInstanceOf( \WP_Error::class, ( new BrevoSetup( $client ) )->run( false, true, 'X' ) );
	}

	public function test_setup_reuses_existing_list_and_template(): void {
		$client = $this->createMock( BrevoClient::class );
		$client->method( 'options' )->willReturn( [
			'lists'     => [ [ 'id' => 4, 'name' => BrevoSetup::LIST_NAME, 'active' => true, 'tag' => '' ] ],
			'templates' => [ [ 'id' => 9, 'name' => BrevoSetup::TEMPLATE_NAME, 'active' => true, 'tag' => 'optin' ] ],
		] );
		$client->expects( $this->never() )->method( 'create_list' );
		$client->expects( $this->never() )->method( 'create_template' );
		$this->assertSame( [ 'list_id' => 4, 'template_id' => 9 ], ( new BrevoSetup( $client ) )->run( true, true, 'X' ) );
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
