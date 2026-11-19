import apiFetch from '@wordpress/api-fetch';

const ns = () => window.bwPermaFormsAdmin.restNs;

export const get = < T, >( path: string ): Promise< T > => apiFetch< T >( { path: `/${ ns() }${ path }` } );

export const post = < T, >( path: string, data: unknown ): Promise< T > =>
	apiFetch< T >( { path: `/${ ns() }${ path }`, method: 'POST', data } );

export const del = < T, >( path: string ): Promise< T > => apiFetch< T >( { path: `/${ ns() }${ path }`, method: 'DELETE' } );

/** Error text from an apiFetch error. */
export const errorMessage = ( e: unknown ): string =>
	( e as { message?: string } )?.message || String( e );
