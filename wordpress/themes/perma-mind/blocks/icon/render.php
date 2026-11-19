<?php
/**
 * Server-side render for bw/icon.
 *
 * @package PermaMind
 *
 * @var array<string, mixed> $attributes
 */

declare(strict_types=1);

use BW\PermaMind\Icons;

$bw_svg = Icons::svg( (string) ( $attributes['icon'] ?? 'check' ), (int) ( $attributes['size'] ?? 24 ) );
if ( '' === $bw_svg ) {
	return;
}
// The SVG comes from a theme file (trusted), the name is sanitized in Icons::svg().
printf( '<span %s>%s</span>', get_block_wrapper_attributes( [ 'class' => 'bw-icon' ] ), $bw_svg ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
