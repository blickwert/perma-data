import { __ } from '@wordpress/i18n';
import Link from './Link';

type Props = { title: string; actions?: React.ReactNode; current: 'contacts' | 'settings' };

/** Title row with the app tabs. */
export default function PageHeader( { title, actions, current }: Props ) {
	return (
		<div className="bwo-header">
			<div className="bwo-header__row">
				<h1 className="bwo-header__title">{ title }</h1>
				{ actions && <div className="bwo-header__actions">{ actions }</div> }
			</div>
			<nav className="bwo-tabs" aria-label={ __( 'Sections', 'bw-perma-forms' ) }>
				<Link to="/contacts" className={ 'contacts' === current ? 'bwo-tabs__tab is-active' : 'bwo-tabs__tab' }>
					{ __( 'Contacts', 'bw-perma-forms' ) }
				</Link>
				<Link to="/settings" className={ 'settings' === current ? 'bwo-tabs__tab is-active' : 'bwo-tabs__tab' }>
					{ __( 'Settings', 'bw-perma-forms' ) }
				</Link>
			</nav>
		</div>
	);
}
