import { __ } from '@wordpress/i18n';

export const statusLabel = ( s: string ): string =>
	( {
		prospect: __( 'Prospect', 'bw-perma-forms' ),
		inquiry: __( 'Inquiry', 'bw-perma-forms' ),
		member: __( 'Member', 'bw-perma-forms' ),
		former: __( 'Former member', 'bw-perma-forms' ),
	} )[ s ] ?? s;

export const interestLabel = ( s: string ): string =>
	( {
		basic: 'Basic',
		advanced: 'Advanced',
		clinical: 'Clinical Expert',
	} )[ s ] ?? s;

export const newsletterLabel = ( s: string ): string =>
	( {
		none: __( 'No', 'bw-perma-forms' ),
		pending: __( 'Confirmation pending', 'bw-perma-forms' ),
		subscribed: __( 'Subscribed', 'bw-perma-forms' ),
		unsubscribed: __( 'Unsubscribed', 'bw-perma-forms' ),
	} )[ s ] ?? s;

export const formLabel = ( s: string ): string =>
	( {
		interest: __( 'Interest list', 'bw-perma-forms' ),
		contact: __( 'Contact form', 'bw-perma-forms' ),
		newsletter: __( 'Newsletter', 'bw-perma-forms' ),
	} )[ s ] ?? s;

/** Database time (UTC) as local date and time. */
export const formatDate = ( utc: string ): string => {
	if ( ! utc ) {
		return '';
	}
	const d = new Date( utc.replace( ' ', 'T' ) + 'Z' );
	return d.toLocaleString( document.documentElement.lang || undefined, { dateStyle: 'medium', timeStyle: 'short' } );
};
