<?php
/**
 * Tests for ContactService (merge rules, recording, admin updates).
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Tests\Unit;

use Brain\Monkey\Actions;
use BW\PermaForms\Modules\Contacts\Model\Contact;
use BW\PermaForms\Modules\Contacts\Repository\ContactRepository;
use BW\PermaForms\Modules\Contacts\Repository\MetaRepository;
use BW\PermaForms\Modules\Contacts\Repository\SubmissionRepository;
use BW\PermaForms\Modules\Contacts\Service\ContactService;

final class ContactServiceTest extends TestCase {

	private function contact( array $over = [] ): Contact {
		return Contact::from_row( $over + [ 'id' => 7, 'email' => 'anna@example.at', 'first_name' => 'Anna', 'last_name' => 'Muster', 'status' => 'prospect', 'interests' => 'basic', 'newsletter' => 'none', 'source' => 'interest' ] );
	}

	public function test_new_contact_from_interest_list_is_prospect_with_source(): void {
		$fields = ContactService::merge( null, 'interest', [ 'first_name' => 'Anna', 'last_name' => 'Muster', 'interests' => [ 'clinical', 'basic' ] ] );
		$this->assertSame( 'prospect', $fields['status'] );
		$this->assertSame( 'interest', $fields['source'] );
		$this->assertSame( [ 'basic', 'clinical' ], $fields['interests'] );
	}

	public function test_new_contact_from_contact_form_is_inquiry(): void {
		$this->assertSame( 'inquiry', ContactService::merge( null, 'contact', [] )['status'] );
	}

	public function test_interests_add_up_and_empty_values_do_not_overwrite(): void {
		$fields = ContactService::merge( $this->contact(), 'interest', [ 'first_name' => '', 'last_name' => 'Neu', 'interests' => [ 'advanced' ] ] );
		$this->assertSame( [ 'basic', 'advanced' ], $fields['interests'] );
		$this->assertArrayNotHasKey( 'first_name', $fields );
		$this->assertSame( 'Neu', $fields['last_name'] );
		$this->assertArrayNotHasKey( 'status', $fields );
	}

	public function test_inquiry_becomes_prospect_but_member_stays_member(): void {
		$this->assertSame( 'prospect', ContactService::merge( $this->contact( [ 'status' => 'inquiry' ] ), 'interest', [] )['status'] );
		$this->assertArrayNotHasKey( 'status', ContactService::merge( $this->contact( [ 'status' => 'member' ] ), 'interest', [] ) );
		$this->assertArrayNotHasKey( 'status', ContactService::merge( $this->contact( [ 'status' => 'member' ] ), 'contact', [] ) );
	}

	public function test_unknown_interests_are_dropped(): void {
		$this->assertSame( [ 'basic' ], ContactService::merge( null, 'interest', [ 'interests' => [ 'basic', 'evil' ] ] )['interests'] );
	}

	public function test_record_submission_creates_contact_and_history(): void {
		$contacts = $this->createMock( ContactRepository::class );
		$subs     = $this->createMock( SubmissionRepository::class );
		$contacts->method( 'find_by_email' )->with( 'anna@example.at' )->willReturn( null );
		$contacts->expects( $this->once() )->method( 'insert' )->with( $this->callback( static fn( array $f ): bool => 'anna@example.at' === $f['email'] && 'prospect' === $f['status'] ) )->willReturn( 7 );
		$contacts->method( 'find' )->willReturn( $this->contact() );
		$subs->expects( $this->once() )->method( 'add' )->with( 7, 'interest', [ 'basic' ], 'Hallo', [] );
		Actions\expectDone( 'bw_perma_forms_contact_saved' )->once();
		$service = new ContactService( $contacts, $subs, $this->createMock( MetaRepository::class ) );
		$this->assertSame( 7, $service->record_submission( 'interest', [ 'email' => ' Anna@Example.at ', 'interests' => [ 'basic' ], 'message' => 'Hallo' ] ) );
	}

	public function test_record_submission_rejects_invalid_email(): void {
		$contacts = $this->createMock( ContactRepository::class );
		$contacts->expects( $this->never() )->method( 'insert' );
		$service = new ContactService( $contacts, $this->createMock( SubmissionRepository::class ), $this->createMock( MetaRepository::class ) );
		$this->assertSame( 0, $service->record_submission( 'interest', [ 'email' => 'kein-mail' ] ) );
	}

	public function test_update_refuses_email_of_another_contact(): void {
		$contacts = $this->createMock( ContactRepository::class );
		$contacts->method( 'find' )->willReturn( $this->contact() );
		$contacts->method( 'find_by_email' )->willReturn( $this->contact( [ 'id' => 9, 'email' => 'other@example.at' ] ) );
		$contacts->expects( $this->never() )->method( 'update' );
		$service = new ContactService( $contacts, $this->createMock( SubmissionRepository::class ), $this->createMock( MetaRepository::class ) );
		$this->assertInstanceOf( \WP_Error::class, $service->update( 7, [ 'email' => 'other@example.at' ] ) );
	}

	public function test_update_whitelists_status_and_stores_meta(): void {
		$contacts = $this->createMock( ContactRepository::class );
		$meta     = $this->createMock( MetaRepository::class );
		$contacts->method( 'find' )->willReturn( $this->contact() );
		$contacts->expects( $this->once() )->method( 'update' )->with( 7, [ 'status' => 'member' ] );
		$meta->expects( $this->once() )->method( 'set' )->with( 7, 'mitgliedsnummer', 'M-12' );
		Actions\expectDone( 'bw_perma_forms_contact_updated' )->once();
		$service = new ContactService( $contacts, $this->createMock( SubmissionRepository::class ), $meta );
		$service->update( 7, [ 'status' => 'member', 'newsletter' => 'bogus', 'meta' => [ 'mitgliedsnummer' => 'M-12', '_secret' => 'x' ] ] );
	}

	public function test_set_newsletter_creates_contact_when_unknown(): void {
		$contacts = $this->createMock( ContactRepository::class );
		$contacts->method( 'find_by_email' )->willReturn( null );
		$contacts->expects( $this->once() )->method( 'insert' )->with( $this->callback( static fn( array $f ): bool => 'pending' === $f['newsletter'] && 'newsletter' === $f['source'] ) )->willReturn( 3 );
		$service = new ContactService( $contacts, $this->createMock( SubmissionRepository::class ), $this->createMock( MetaRepository::class ) );
		$this->assertSame( 3, $service->set_newsletter( 'neu@example.at', 'pending', 'Neu' ) );
		$this->assertSame( 0, $service->set_newsletter( 'neu@example.at', 'kaputt' ) );
	}
}
