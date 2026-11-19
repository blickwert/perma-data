<?php
/**
 * Collects the form definitions of all modules and maps them to Contact Form 7 form ids.
 *
 * @package BW\PermaForms
 */

declare(strict_types=1);

namespace BW\PermaForms\Modules\Forms\Service;

class FormRegistry {

	public const OPTION = 'bw_perma_forms_cf7_forms';

	/** @var array<string, FormDefinition>|null */
	private ?array $definitions = null;

	/** @return array<string, FormDefinition> */
	public function definitions(): array {
		if ( null === $this->definitions ) {
			/**
			 * Modules add their forms here.
			 *
			 * @param FormDefinition[] $definitions
			 */
			$list              = (array) apply_filters( 'bw_perma_forms_definitions', [] );
			$this->definitions = [];
			foreach ( $list as $def ) {
				if ( $def instanceof FormDefinition ) {
					$this->definitions[ $def->key ] = $def;
				}
			}
		}
		return $this->definitions;
	}

	public function get( string $key ): ?FormDefinition {
		return $this->definitions()[ $key ] ?? null;
	}

	/** @return array<string, array{id: int, hash: string}> */
	public function stored(): array {
		$map = get_option( self::OPTION, [] );
		return is_array( $map ) ? $map : [];
	}

	public function cf7_id( string $key ): int {
		return (int) ( $this->stored()[ $key ]['id'] ?? 0 );
	}

	/** Form key of a CF7 form id, '' if the form is not one of ours. */
	public function key_for_cf7_id( int $id ): string {
		foreach ( $this->stored() as $key => $entry ) {
			if ( (int) $entry['id'] === $id && $id > 0 ) {
				return (string) $key;
			}
		}
		return '';
	}

	public function remember( string $key, int $id, string $hash ): void {
		$map         = $this->stored();
		$map[ $key ] = [ 'id' => $id, 'hash' => $hash ];
		update_option( self::OPTION, $map, false );
	}
}
