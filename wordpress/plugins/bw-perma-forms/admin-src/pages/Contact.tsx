import { __, sprintf } from '@wordpress/i18n';
import { useEffect, useState } from '@wordpress/element';
import { Button, CheckboxControl, Notice, SelectControl, Snackbar, Spinner, TextControl, TextareaControl } from '@wordpress/components';
import { del, errorMessage, get, post } from '../api';
import PageHeader from '../components/PageHeader';
import Link from '../components/Link';
import { navigate } from '../router';
import type { ContactDetail } from '../types';
import { formLabel, formatDate, interestLabel, newsletterLabel, statusLabel } from '../labels';

/** One contact: edit fields, status, courses, extra fields; history of submissions; delete. */
export default function Contact( { id }: { id: number } ) {
	const data = window.bwPermaFormsAdmin;
	const [ contact, setContact ] = useState< ContactDetail | null >( null );
	const [ newKey, setNewKey ] = useState( '' );
	const [ busy, setBusy ] = useState( false );
	const [ error, setError ] = useState( '' );
	const [ saved, setSaved ] = useState( false );

	useEffect( () => {
		get< ContactDetail >( `/contacts/${ id }` ).then( setContact ).catch( ( e ) => setError( errorMessage( e ) ) );
	}, [ id ] );

	if ( ! contact ) {
		return error ? <Notice status="error" isDismissible={ false }>{ error }</Notice> : <Spinner />;
	}

	const field = ( key: 'first_name' | 'last_name' | 'email' | 'phone' | 'profession' ) => ( value: string ) =>
		setContact( { ...contact, [ key ]: value } );

	const save = () => {
		setBusy( true );
		post< ContactDetail >( `/contacts/${ id }`, contact )
			.then( ( c ) => {
				setContact( c );
				setError( '' );
				setSaved( true );
			} )
			.catch( ( e ) => setError( errorMessage( e ) ) )
			.finally( () => setBusy( false ) );
	};

	const remove = () => {
		// eslint-disable-next-line no-alert
		if ( ! window.confirm( __( 'Delete this contact with all submissions? This cannot be undone.', 'bw-perma-forms' ) ) ) {
			return;
		}
		setBusy( true );
		del( `/contacts/${ id }` )
			.then( () => navigate( '/contacts' ) )
			.catch( ( e ) => {
				setError( errorMessage( e ) );
				setBusy( false );
			} );
	};

	const name = `${ contact.first_name } ${ contact.last_name }`.trim() || contact.email;

	return (
		<>
			<PageHeader current="contacts" title={ name } actions={ <Link to="/contacts">{ __( '← All contacts', 'bw-perma-forms' ) }</Link> } />
			{ error && <Notice status="error" isDismissible={ false }>{ error }</Notice> }
			<div className="bwo-columns">
				<div className="bwo-card">
					<h2>{ __( 'Contact details', 'bw-perma-forms' ) }</h2>
					<div className="bwo-grid">
						<TextControl label={ __( 'First name', 'bw-perma-forms' ) } value={ contact.first_name } onChange={ field( 'first_name' ) } __next40pxDefaultSize __nextHasNoMarginBottom />
						<TextControl label={ __( 'Last name', 'bw-perma-forms' ) } value={ contact.last_name } onChange={ field( 'last_name' ) } __next40pxDefaultSize __nextHasNoMarginBottom />
						<TextControl label={ __( 'E-mail', 'bw-perma-forms' ) } type="email" value={ contact.email } onChange={ field( 'email' ) } __next40pxDefaultSize __nextHasNoMarginBottom />
						<TextControl label={ __( 'Phone', 'bw-perma-forms' ) } value={ contact.phone } onChange={ field( 'phone' ) } __next40pxDefaultSize __nextHasNoMarginBottom />
					</div>
					<TextControl label={ __( 'Profession or previous training', 'bw-perma-forms' ) } value={ contact.profession } onChange={ field( 'profession' ) } __next40pxDefaultSize __nextHasNoMarginBottom />
					<div className="bwo-grid">
						<SelectControl label={ __( 'Status', 'bw-perma-forms' ) } value={ contact.status } options={ ( data.statuses ?? [] ).map( ( s ) => ( { label: statusLabel( s ), value: s } ) ) } onChange={ ( status ) => setContact( { ...contact, status } ) } __next40pxDefaultSize __nextHasNoMarginBottom />
						<SelectControl label={ __( 'Newsletter', 'bw-perma-forms' ) } value={ contact.newsletter } options={ ( data.newsletter ?? [] ).map( ( s ) => ( { label: newsletterLabel( s ), value: s } ) ) } onChange={ ( newsletter ) => setContact( { ...contact, newsletter } ) } help={ __( 'Usually set by Brevo; change only to correct it.', 'bw-perma-forms' ) } __next40pxDefaultSize __nextHasNoMarginBottom />
					</div>
					<fieldset className="bwo-fieldset">
						<legend>{ __( 'Courses of interest', 'bw-perma-forms' ) }</legend>
						{ ( data.interests ?? [] ).map( ( i ) => (
							<CheckboxControl
								key={ i }
								label={ interestLabel( i ) }
								checked={ contact.interests.includes( i ) }
								onChange={ ( on ) => setContact( { ...contact, interests: on ? [ ...contact.interests, i ] : contact.interests.filter( ( x ) => x !== i ) } ) }
								__nextHasNoMarginBottom
							/>
						) ) }
					</fieldset>
					<TextareaControl label={ __( 'Notes (internal)', 'bw-perma-forms' ) } value={ contact.notes } onChange={ ( notes ) => setContact( { ...contact, notes } ) } rows={ 4 } __nextHasNoMarginBottom />
				</div>
				<div className="bwo-card">
					<h2>{ __( 'Extra fields', 'bw-perma-forms' ) }</h2>
					<p className="bwo-help">{ __( 'Free fields for later member data (e.g. address, membership number). Every field becomes a column in the CSV export. An empty value deletes the field.', 'bw-perma-forms' ) }</p>
					{ Object.entries( contact.meta ).map( ( [ key, value ] ) => (
						<TextControl key={ key } label={ key } value={ value } onChange={ ( v ) => setContact( { ...contact, meta: { ...contact.meta, [ key ]: v } } ) } __next40pxDefaultSize __nextHasNoMarginBottom />
					) ) }
					<div className="bwo-inline">
						<TextControl label={ __( 'New field (name)', 'bw-perma-forms' ) } value={ newKey } onChange={ setNewKey } placeholder="mitgliedsnummer" __next40pxDefaultSize __nextHasNoMarginBottom />
						<Button
							variant="secondary"
							disabled={ '' === newKey.trim() }
							onClick={ () => {
								const key = newKey.trim().toLowerCase().replace( /[^a-z0-9_-]/g, '_' );
								setContact( { ...contact, meta: { ...contact.meta, [ key ]: contact.meta[ key ] ?? '' } } );
								setNewKey( '' );
							} }
							__next40pxDefaultSize
						>
							{ __( 'Add', 'bw-perma-forms' ) }
						</Button>
					</div>
					<h2>{ __( 'History', 'bw-perma-forms' ) }</h2>
					<p className="bwo-help">
						{ sprintf( /* translators: 1: date, 2: form */ __( 'Created %1$s via %2$s.', 'bw-perma-forms' ), formatDate( contact.created_at ), formLabel( contact.source ) ) }
					</p>
					<ul className="bwo-history">
						{ contact.submissions.map( ( s ) => (
							<li key={ s.id }>
								<strong>{ formLabel( s.form ) }</strong> · { formatDate( s.created_at ) }
								{ s.interests.length > 0 && <> · { s.interests.map( interestLabel ).join( ', ' ) }</> }
								{ s.message && <p>{ s.message }</p> }
							</li>
						) ) }
					</ul>
				</div>
			</div>
			<div className="bwo-actions">
				<Button variant="primary" onClick={ save } isBusy={ busy } disabled={ busy } __next40pxDefaultSize>
					{ __( 'Save', 'bw-perma-forms' ) }
				</Button>
				<Button variant="tertiary" isDestructive onClick={ remove } disabled={ busy } __next40pxDefaultSize>
					{ __( 'Delete contact', 'bw-perma-forms' ) }
				</Button>
			</div>
			{ saved && <Snackbar onRemove={ () => setSaved( false ) }>{ __( 'Saved.', 'bw-perma-forms' ) }</Snackbar> }
		</>
	);
}
