import { __, sprintf } from '@wordpress/i18n';
import { useEffect, useState } from '@wordpress/element';
import { Button, Notice, SearchControl, SelectControl, Spinner } from '@wordpress/components';
import { addQueryArgs } from '@wordpress/url';
import { get, errorMessage } from '../api';
import PageHeader from '../components/PageHeader';
import Link from '../components/Link';
import type { Contact } from '../types';
import { formatDate, interestLabel, newsletterLabel, statusLabel } from '../labels';

const PER_PAGE = 50;

type Filters = { search: string; status: string; interest: string; newsletter: string };

const options = ( values: string[] | undefined, label: ( v: string ) => string, all: string ) => [
	{ label: all, value: '' },
	...( values ?? [] ).map( ( v ) => ( { label: label( v ), value: v } ) ),
];

/** Contact list with search, filters, paging and CSV export. */
export default function Contacts() {
	const data = window.bwPermaFormsAdmin;
	const [ filters, setFilters ] = useState< Filters >( { search: '', status: '', interest: '', newsletter: '' } );
	const [ page, setPage ] = useState( 1 );
	const [ items, setItems ] = useState< Contact[] >( [] );
	const [ total, setTotal ] = useState( 0 );
	const [ loading, setLoading ] = useState( true );
	const [ error, setError ] = useState( '' );

	useEffect( () => {
		setLoading( true );
		const timer = window.setTimeout( () => {
			get< { items: Contact[]; total: number } >( addQueryArgs( '/contacts', { ...filters, page, per_page: PER_PAGE } ) )
				.then( ( r ) => {
					setItems( r.items );
					setTotal( r.total );
					setError( '' );
				} )
				.catch( ( e ) => setError( errorMessage( e ) ) )
				.finally( () => setLoading( false ) );
		}, 250 );
		return () => window.clearTimeout( timer );
	}, [ filters, page ] );

	const set = ( key: keyof Filters ) => ( value: string | undefined ) => {
		setPage( 1 );
		setFilters( { ...filters, [ key ]: value ?? '' } );
	};
	const pages = Math.max( 1, Math.ceil( total / PER_PAGE ) );
	const exportUrl = data.exportUrl ? addQueryArgs( data.exportUrl, filters ) : '';

	return (
		<>
			<PageHeader
				current="contacts"
				title={ __( 'Contacts', 'bw-perma-forms' ) }
				actions={
					exportUrl && (
						<Button variant="secondary" href={ exportUrl } __next40pxDefaultSize>
							{ __( 'Download CSV', 'bw-perma-forms' ) }
						</Button>
					)
				}
			/>
			<div className="bwo-filters">
				<SearchControl
					label={ __( 'Search name, e-mail, profession', 'bw-perma-forms' ) }
					value={ filters.search }
					onChange={ set( 'search' ) }
					__nextHasNoMarginBottom
				/>
				<SelectControl label={ __( 'Status', 'bw-perma-forms' ) } value={ filters.status } options={ options( data.statuses, statusLabel, __( 'All', 'bw-perma-forms' ) ) } onChange={ set( 'status' ) } __next40pxDefaultSize __nextHasNoMarginBottom />
				<SelectControl label={ __( 'Course', 'bw-perma-forms' ) } value={ filters.interest } options={ options( data.interests, interestLabel, __( 'All', 'bw-perma-forms' ) ) } onChange={ set( 'interest' ) } __next40pxDefaultSize __nextHasNoMarginBottom />
				<SelectControl label={ __( 'Newsletter', 'bw-perma-forms' ) } value={ filters.newsletter } options={ options( data.newsletter, newsletterLabel, __( 'All', 'bw-perma-forms' ) ) } onChange={ set( 'newsletter' ) } __next40pxDefaultSize __nextHasNoMarginBottom />
			</div>
			{ error && <Notice status="error" isDismissible={ false }>{ error }</Notice> }
			<p className="bwo-count">
				{ loading ? <Spinner /> : sprintf( /* translators: %d: number of contacts */ __( '%d contacts', 'bw-perma-forms' ), total ) }
			</p>
			<table className="widefat striped bwo-table">
				<thead>
					<tr>
						<th>{ __( 'Name', 'bw-perma-forms' ) }</th>
						<th>{ __( 'E-mail', 'bw-perma-forms' ) }</th>
						<th>{ __( 'Status', 'bw-perma-forms' ) }</th>
						<th>{ __( 'Courses', 'bw-perma-forms' ) }</th>
						<th>{ __( 'Newsletter', 'bw-perma-forms' ) }</th>
						<th>{ __( 'Created', 'bw-perma-forms' ) }</th>
					</tr>
				</thead>
				<tbody>
					{ items.map( ( c ) => (
						<tr key={ c.id }>
							<td>
								<Link to={ `/contacts/${ c.id }` }>{ `${ c.first_name } ${ c.last_name }`.trim() || __( '(no name)', 'bw-perma-forms' ) }</Link>
							</td>
							<td>{ c.email }</td>
							<td><span className={ `bwo-badge bwo-badge--${ c.status }` }>{ statusLabel( c.status ) }</span></td>
							<td>{ c.interests.map( interestLabel ).join( ', ' ) }</td>
							<td>{ newsletterLabel( c.newsletter ) }</td>
							<td>{ formatDate( c.created_at ) }</td>
						</tr>
					) ) }
					{ ! loading && 0 === items.length && (
						<tr>
							<td colSpan={ 6 }>{ __( 'No contacts found.', 'bw-perma-forms' ) }</td>
						</tr>
					) }
				</tbody>
			</table>
			{ pages > 1 && (
				<div className="bwo-pager">
					<Button variant="tertiary" size="compact" disabled={ page <= 1 } onClick={ () => setPage( page - 1 ) }>
						{ __( 'Previous', 'bw-perma-forms' ) }
					</Button>
					<span>{ sprintf( /* translators: 1: page, 2: pages */ __( 'Page %1$d of %2$d', 'bw-perma-forms' ), page, pages ) }</span>
					<Button variant="tertiary" size="compact" disabled={ page >= pages } onClick={ () => setPage( page + 1 ) }>
						{ __( 'Next', 'bw-perma-forms' ) }
					</Button>
				</div>
			) }
		</>
	);
}
