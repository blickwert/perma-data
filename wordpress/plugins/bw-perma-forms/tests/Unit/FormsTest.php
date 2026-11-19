<?php
/**
 * Tests for form helpers, normalization of the forms and CF7 properties.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Tests\Unit;

use BW\PermaForms\Modules\Contact\ContactModule;
use BW\PermaForms\Modules\Forms\Service\Fields;
use BW\PermaForms\Modules\Forms\Service\FormDefinition;
use BW\PermaForms\Modules\Forms\Service\FormProvisioner;
use BW\PermaForms\Modules\InterestList\InterestListModule;

final class FormsTest extends TestCase {

	public function test_split_name(): void {
		$this->assertSame( [ 'Anna Maria', 'Muster' ], Fields::split_name( '  Anna   Maria Muster ' ) );
		$this->assertSame( [ 'Anna', '' ], Fields::split_name( 'Anna' ) );
	}

	public function test_interest_normalize_maps_labels_and_optin(): void {
		$data = InterestListModule::normalize(
			[
				'vorname'    => 'Anna',
				'nachname'   => 'Muster',
				'email'      => 'a@example.at',
				'interesse'  => [ 'PERMA Clinical Expert', 'Positive Psychology Basic', 'Hack' ],
				'newsletter' => '1',
				'nachricht'  => ' Hallo ',
			]
		);
		$this->assertSame( [ 'basic', 'clinical' ], $data['interests'] );
		$this->assertTrue( $data['newsletter_optin'] );
		$this->assertSame( 'Hallo', $data['message'] );
		$this->assertFalse( InterestListModule::normalize( [ 'newsletter' => '' ] )['newsletter_optin'] );
	}

	public function test_contact_normalize(): void {
		$data = ContactModule::normalize( [ 'name' => 'Max Muster', 'email' => 'm@example.at', 'nachricht' => 'Frage' ] );
		$this->assertSame( 'Max', $data['first_name'] );
		$this->assertSame( 'Muster', $data['last_name'] );
		$this->assertSame( 'Frage', $data['message'] );
	}

	public function test_properties_turn_mails_on_and_off_and_hash_changes(): void {
		$def   = new FormDefinition( 'x', 'X', '[submit]', [ 'recipient' => 'a@example.at' ], [], [ 'mail_sent_ok' => 'Danke' ], 'skip_mail: on', static fn( array $p ): array => $p );
		$props = FormProvisioner::properties( $def, [ 'mail' => [ 'subject' => 'alt' ], 'messages' => [ 'spam' => 'S' ] ] );
		$this->assertTrue( $props['mail']['active'] );
		$this->assertSame( 'alt', $props['mail']['subject'] );
		$this->assertFalse( $props['mail_2']['active'] );
		$this->assertSame( [ 'spam' => 'S', 'mail_sent_ok' => 'Danke' ], $props['messages'] );
		$other = new FormDefinition( 'x', 'X', '[submit]', [ 'recipient' => 'b@example.at' ], [], [], '', static fn( array $p ): array => $p );
		$this->assertNotSame( $def->hash(), $other->hash() );
	}
}
