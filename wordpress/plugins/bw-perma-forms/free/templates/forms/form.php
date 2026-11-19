<?php
/**
 * Wrapper around a Contact Form 7 form.
 * Override in the theme: bw-perma-forms/forms/form.php
 *
 * @package BW\PermaForms
 *
 * @var array{key: string, html: string} $data
 */

declare(strict_types=1);

defined( 'ABSPATH' ) || exit;
?>
<div class="bw-perma-form bw-perma-form--<?php echo esc_attr( $data['key'] ); ?>">
	<?php do_action( 'bw_perma_forms_before_form', $data['key'] ); ?>
	<?php echo $data['html']; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- markup from Contact Form 7. ?>
</div>
