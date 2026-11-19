import { __ } from '@wordpress/i18n';
import { useEffect, useState } from '@wordpress/element';
import { Button, Notice, SelectControl, Snackbar, Spinner, TextControl, TextareaControl } from '@wordpress/components';
import { errorMessage, get, post } from '../api';
import PageHeader from '../components/PageHeader';

type Values = Record< string, string | number >;
type SettingsResponse = {
	values: Values;
	has_own_api_key: boolean;
	has_brevo_plugin?: boolean;
	webhook_url?: string;
	turnstile_url: string;
};
type BrevoOptions = { lists: { id: number; name: string }[]; templates: { id: number; name: string }[] };
type FormStatus = { key: string; title: string; cf7_id: number; edit_url: string; in_sync: boolean };

/** Recipient, Brevo, spam thresholds and the status of the Contact Form 7 forms. */
export default function Settings() {
	const [ data, setData ] = useState< SettingsResponse | null >( null );
	const [ values, setValues ] = useState< Values >( {} );
	const [ apiKey, setApiKey ] = useState( '' );
	const [ forms, setForms ] = useState< { cf7_active: boolean; forms: FormStatus[] } | null >( null );
	const [ brevo, setBrevo ] = useState< BrevoOptions | null >( null );
	const [ brevoError, setBrevoError ] = useState( '' );
	const [ busy, setBusy ] = useState( false );
	const [ error, setError ] = useState( '' );
	const [ saved, setSaved ] = useState( '' );

	const load = ( r: SettingsResponse ) => {
		setData( r );
		setValues( r.values );
		setApiKey( '' );
	};

	useEffect( () => {
		get< SettingsResponse >( '/settings' ).then( load ).catch( ( e ) => setError( errorMessage( e ) ) );
		get< { cf7_active: boolean; forms: FormStatus[] } >( '/forms' ).then( setForms ).catch( () => setForms( null ) );
		get< BrevoOptions >( '/brevo/options' ).then( setBrevo ).catch( ( e ) => setBrevoError( errorMessage( e ) ) );
	}, [] );

	if ( ! data ) {
		return error ? <Notice status="error" isDismissible={ false }>{ error }</Notice> : <Spinner />;
	}

	const text = ( key: string, label: string, help?: string, type: 'text' | 'email' | 'number' = 'text' ) => (
		<TextControl
			label={ label }
			help={ help }
			type={ type }
			value={ String( values[ key ] ?? '' ) }
			onChange={ ( v ) => setValues( { ...values, [ key ]: v } ) }
			__next40pxDefaultSize
			__nextHasNoMarginBottom
		/>
	);

	const save = () => {
		setBusy( true );
		post< SettingsResponse >( '/settings', { ...values, brevo_api_key: apiKey } )
			.then( ( r ) => {
				load( r );
				setError( '' );
				setSaved( __( 'Settings saved.', 'bw-perma-forms' ) );
				return get< { cf7_active: boolean; forms: FormStatus[] } >( '/forms' ).then( setForms );
			} )
			.catch( ( e ) => setError( errorMessage( e ) ) )
			.finally( () => setBusy( false ) );
	};

	const sync = () => {
		setBusy( true );
		post< { cf7_active: boolean; forms: FormStatus[] } >( '/forms/sync', {} )
			.then( ( r ) => {
				setForms( r );
				setSaved( __( 'Forms rewritten.', 'bw-perma-forms' ) );
			} )
			.catch( ( e ) => setError( errorMessage( e ) ) )
			.finally( () => setBusy( false ) );
	};

	const keyHelp = data.has_own_api_key
		? __( 'An own key is stored. Leave empty to keep it, enter "-" to remove it.', 'bw-perma-forms' )
		: data.has_brevo_plugin
		? __( 'Empty: the key of the connected Brevo plugin is used.', 'bw-perma-forms' )
		: __( 'No key yet: connect the Brevo plugin or enter an API key here.', 'bw-perma-forms' );

	return (
		<>
			<PageHeader current="settings" title={ __( 'Settings', 'bw-perma-forms' ) } />
			{ error && <Notice status="error" isDismissible={ false }>{ error }</Notice> }
			<div className="bwo-columns">
				<div className="bwo-card">
					<h2>{ __( 'Forms', 'bw-perma-forms' ) }</h2>
					{ text( 'recipient', __( 'Recipient of form mails', 'bw-perma-forms' ), __( 'Interest list and contact form go to this address.', 'bw-perma-forms' ), 'email' ) }
					{ text( 'privacy_url', __( 'Privacy policy (link in the forms)', 'bw-perma-forms' ), __( 'Path on this site (e.g. /datenschutz/) or full URL.', 'bw-perma-forms' ) ) }
					<h3>{ __( 'Contact Form 7', 'bw-perma-forms' ) }</h3>
					{ forms && ! forms.cf7_active && <Notice status="warning" isDismissible={ false }>{ __( 'Contact Form 7 is not active.', 'bw-perma-forms' ) }</Notice> }
					<ul className="bwo-list">
						{ forms?.forms.map( ( f ) => (
							<li key={ f.key }>
								{ f.edit_url ? <a href={ f.edit_url }>{ f.title }</a> : f.title } ·{ ' ' }
								{ f.cf7_id ? ( f.in_sync ? __( 'up to date', 'bw-perma-forms' ) : __( 'will be updated', 'bw-perma-forms' ) ) : __( 'not created yet', 'bw-perma-forms' ) }
							</li>
						) ) }
					</ul>
					<p className="bwo-help">{ __( 'The plugin writes these forms itself. Changes in Contact Form 7 are overwritten when the plugin changes the form.', 'bw-perma-forms' ) }</p>
					<Button variant="secondary" onClick={ sync } disabled={ busy } __next40pxDefaultSize>
						{ __( 'Rewrite forms now', 'bw-perma-forms' ) }
					</Button>
					<h3>{ __( 'Cloudflare Turnstile', 'bw-perma-forms' ) }</h3>
					<p className="bwo-help">
						{ __( 'Turnstile keys are entered in Contact Form 7; the widget then appears in all forms.', 'bw-perma-forms' ) }{ ' ' }
						<a href={ data.turnstile_url }>{ __( 'Open Contact Form 7 › Integration', 'bw-perma-forms' ) }</a>
					</p>
				</div>
				<div className="bwo-card">
					<h2>{ __( 'Newsletter (Brevo)', 'bw-perma-forms' ) }</h2>
					<TextControl label={ __( 'Brevo API key', 'bw-perma-forms' ) } help={ keyHelp } type="password" autoComplete="off" value={ apiKey } onChange={ setApiKey } __next40pxDefaultSize __nextHasNoMarginBottom />
					{ brevoError && <Notice status="warning" isDismissible={ false }>{ brevoError }</Notice> }
					{ brevo ? (
						<>
							<SelectControl
								label={ __( 'Newsletter list', 'bw-perma-forms' ) }
								value={ String( values.brevo_list_ids ?? '' ).split( ',' )[ 0 ] }
								options={ [ { label: __( '– choose –', 'bw-perma-forms' ), value: '' }, ...brevo.lists.map( ( l ) => ( { label: `${ l.name } (#${ l.id })`, value: String( l.id ) } ) ) ] }
								onChange={ ( v ) => setValues( { ...values, brevo_list_ids: v } ) }
								__next40pxDefaultSize
								__nextHasNoMarginBottom
							/>
							<SelectControl
								label={ __( 'Double opt-in template', 'bw-perma-forms' ) }
								help={ __( 'Brevo template of type "Double opt-in confirmation".', 'bw-perma-forms' ) }
								value={ String( values.brevo_doi_template_id ?? '' ) }
								options={ [ { label: __( '– choose –', 'bw-perma-forms' ), value: '0' }, ...brevo.templates.map( ( t ) => ( { label: `${ t.name } (#${ t.id })`, value: String( t.id ) } ) ) ] }
								onChange={ ( v ) => setValues( { ...values, brevo_doi_template_id: v } ) }
								__next40pxDefaultSize
								__nextHasNoMarginBottom
							/>
						</>
					) : (
						<>
							{ text( 'brevo_list_ids', __( 'List ID(s)', 'bw-perma-forms' ), __( 'Brevo list for the newsletter; several separated by commas.', 'bw-perma-forms' ) ) }
							{ text( 'brevo_doi_template_id', __( 'Double opt-in template ID', 'bw-perma-forms' ), __( 'Brevo template of type "Double opt-in confirmation".', 'bw-perma-forms' ), 'number' ) }
						</>
					) }
					{ text( 'brevo_redirect_url', __( 'Page after confirming', 'bw-perma-forms' ), __( 'Brevo sends people here after they clicked the confirmation link.', 'bw-perma-forms' ) ) }
					{ data.webhook_url && (
						<>
							<h3>{ __( 'Webhook for Brevo', 'bw-perma-forms' ) }</h3>
							<p className="bwo-help">{ __( 'Enter this address in Brevo (Settings › Webhooks, marketing events "List addition" and "Unsubscribed"); the contact list then shows confirmed and unsubscribed addresses.', 'bw-perma-forms' ) }</p>
							<code className="bwo-code">{ data.webhook_url }</code>
						</>
					) }
					<h2>{ __( 'Spam protection', 'bw-perma-forms' ) }</h2>
					<div className="bwo-grid">
						{ text( 'spam_min_seconds', __( 'Minimum fill time (seconds)', 'bw-perma-forms' ), undefined, 'number' ) }
						{ text( 'spam_max_links', __( 'Max. links per submission', 'bw-perma-forms' ), undefined, 'number' ) }
						{ text( 'spam_rate_limit', __( 'Max. submissions per visitor', 'bw-perma-forms' ), undefined, 'number' ) }
						{ text( 'spam_rate_window', __( '… within minutes', 'bw-perma-forms' ), undefined, 'number' ) }
					</div>
					<TextareaControl label={ __( 'Blocked words (one per line)', 'bw-perma-forms' ) } value={ String( values.spam_blocklist ?? '' ) } onChange={ ( v ) => setValues( { ...values, spam_blocklist: v } ) } rows={ 4 } __nextHasNoMarginBottom />
				</div>
			</div>
			<div className="bwo-actions">
				<Button variant="primary" onClick={ save } isBusy={ busy } disabled={ busy } __next40pxDefaultSize>
					{ __( 'Save settings', 'bw-perma-forms' ) }
				</Button>
			</div>
			{ saved && <Snackbar onRemove={ () => setSaved( '' ) }>{ saved }</Snackbar> }
		</>
	);
}
