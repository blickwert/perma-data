/* Floating "Zur Interessentenliste" button: hidden while the hero (which has its own main button) is visible. */
( function () {
	var fab = document.querySelector( '.bw-fab' );
	var hero = document.querySelector( '.bw-hero, .bw-page-hero--offer' );
	if ( ! fab || ! hero || ! ( 'IntersectionObserver' in window ) ) {
		return;
	}
	new IntersectionObserver( function ( entries ) {
		fab.classList.toggle( 'is-hidden', entries[ 0 ].isIntersecting );
	} ).observe( hero );
}() );
