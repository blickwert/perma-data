/* Editor UI for bw/icon: choose symbol and size; preview rendered by the server. No build step. */
( function ( wp ) {
	const { registerBlockType } = wp.blocks;
	const { createElement: el, Fragment } = wp.element;
	const { InspectorControls, useBlockProps } = wp.blockEditor;
	const { PanelBody, SelectControl, RangeControl } = wp.components;
	const ServerSideRender = wp.serverSideRender;
	const icons = ( window.bwPermaMindIcons || [] ).map( ( n ) => ( { label: n, value: n } ) );

	registerBlockType( 'bw/icon', {
		edit: ( { attributes, setAttributes } ) =>
			el( Fragment, null,
				el( InspectorControls, null,
					el( PanelBody, { title: 'Symbol' },
						el( SelectControl, { label: 'Symbol', value: attributes.icon, options: icons, onChange: ( icon ) => setAttributes( { icon } ) } ),
						el( RangeControl, { label: 'Größe (px)', value: attributes.size, min: 16, max: 96, onChange: ( size ) => setAttributes( { size } ) } )
					)
				),
				el( 'span', useBlockProps(), el( ServerSideRender, { block: 'bw/icon', attributes: { icon: attributes.icon, size: attributes.size } } ) )
			),
		save: () => null,
	} );
}( window.wp ) );
