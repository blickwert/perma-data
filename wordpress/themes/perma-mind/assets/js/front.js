/* Small front-end helpers of the theme (no framework). */
( function () {
	var reduceMotion = window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;

	/* Floating "Zur Interessentenliste" button: hidden while the hero (which has its own main button) is visible. */
	var fab = document.querySelector( '.bw-fab' );
	var hero = document.querySelector( '.bw-hero, .bw-page-hero--offer' );
	if ( fab && hero && 'IntersectionObserver' in window ) {
		new IntersectionObserver( function ( entries ) {
			fab.classList.toggle( 'is-hidden', entries[ 0 ].isIntersecting );
		} ).observe( hero );
	}

	/* Profile highlights on mobile: one item at a time, advances every 4 s; pauses for a while after the visitor swipes. */
	var list = document.querySelector( '.bw-highlights__list' );
	var mobile = window.matchMedia( '(max-width: 820px)' );
	if ( ! list || reduceMotion ) {
		return;
	}
	var pausedUntil = 0;
	[ 'touchstart', 'pointerdown', 'wheel', 'focusin' ].forEach( function ( type ) {
		list.addEventListener( type, function () {
			pausedUntil = Date.now() + 10000;
		}, { passive: true } );
	} );
	window.setInterval( function () {
		if ( ! mobile.matches || Date.now() < pausedUntil || document.hidden ) {
			return;
		}
		var width = list.clientWidth;
		var next = Math.round( list.scrollLeft / width ) + 1;
		list.scrollTo( { left: next * width >= list.scrollWidth - 1 ? 0 : next * width } );
	}, 4000 );
}() );
