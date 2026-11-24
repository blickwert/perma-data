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

	/* Table of contents (legal pages): marks the section currently in view. */
	var tocLinks = document.querySelectorAll( '.bw-toc a[href^="#"]' );
	if ( tocLinks.length && 'IntersectionObserver' in window ) {
		var byId = {};
		var targets = [];
		tocLinks.forEach( function ( a ) {
			var target = document.getElementById( a.getAttribute( 'href' ).slice( 1 ) );
			if ( target ) {
				byId[ target.id ] = a;
				targets.push( target );
			}
		} );
		var mark = function () {
			var line = window.innerHeight * 0.3;
			var current = targets[ 0 ];
			targets.forEach( function ( el ) {
				if ( el.getBoundingClientRect().top <= line ) {
					current = el;
				}
			} );
			if ( window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2 ) {
				current = targets[ targets.length - 1 ]; /* page end: the last section cannot reach the line */
			}
			tocLinks.forEach( function ( a ) {
				var on = current && a === byId[ current.id ];
				a.classList.toggle( 'is-active', on );
				if ( on ) {
					a.setAttribute( 'aria-current', 'location' );
				} else {
					a.removeAttribute( 'aria-current' );
				}
			} );
		};
		var queued = false;
		window.addEventListener( 'scroll', function () {
			if ( ! queued ) {
				queued = true;
				window.requestAnimationFrame( function () {
					queued = false;
					mark();
				} );
			}
		}, { passive: true } );
		mark();
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
