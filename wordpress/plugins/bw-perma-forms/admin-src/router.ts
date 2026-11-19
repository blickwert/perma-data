import { useEffect, useState } from '@wordpress/element';

/** Current app path from ?path=… (same scheme as the PHP menu links). */
export const currentPath = (): string =>
	new URLSearchParams( window.location.search ).get( 'path' ) || '/contacts';

export const hrefFor = ( path: string ): string =>
	`${ window.bwPermaFormsAdmin.adminUrl }&path=${ encodeURIComponent( path ) }`;

/** Changes the page without reloading. */
export const navigate = ( path: string ): void => {
	window.history.pushState( {}, '', hrefFor( path ) );
	window.dispatchEvent( new Event( 'bw-perma-forms-navigate' ) );
};

export const usePath = (): string => {
	const [ path, setPath ] = useState( currentPath() );
	useEffect( () => {
		const update = () => setPath( currentPath() );
		window.addEventListener( 'popstate', update );
		window.addEventListener( 'bw-perma-forms-navigate', update );
		return () => {
			window.removeEventListener( 'popstate', update );
			window.removeEventListener( 'bw-perma-forms-navigate', update );
		};
	}, [] );
	return path;
};
