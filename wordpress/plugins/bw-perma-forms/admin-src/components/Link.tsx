import { navigate, hrefFor } from '../router';

type Props = { to: string; children: React.ReactNode; className?: string };

/** Link inside the app (no reload; opens in a new tab with modifier keys). */
export default function Link( { to, children, className }: Props ) {
	return (
		<a
			className={ className }
			href={ hrefFor( to ) }
			onClick={ ( e ) => {
				if ( e.metaKey || e.ctrlKey || e.shiftKey || 0 !== e.button ) {
					return;
				}
				e.preventDefault();
				navigate( to );
			} }
		>
			{ children }
		</a>
	);
}
