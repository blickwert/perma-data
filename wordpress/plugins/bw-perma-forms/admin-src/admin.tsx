import { createRoot } from '@wordpress/element';
import Contacts from './pages/Contacts';
import Contact from './pages/Contact';
import Settings from './pages/Settings';
import { usePath } from './router';
import './admin.scss';

/** Picks the page for the current path. */
function App() {
	const path = usePath();
	const contact = path.match( /^\/contacts\/(\d+)$/ );
	if ( contact ) {
		return <Contact id={ Number( contact[ 1 ] ) } />;
	}
	if ( '/settings' === path ) {
		return <Settings />;
	}
	return <Contacts />;
}

const root = document.getElementById( 'bw-perma-forms-app' );
if ( root ) {
	createRoot( root ).render( <App /> );
}
