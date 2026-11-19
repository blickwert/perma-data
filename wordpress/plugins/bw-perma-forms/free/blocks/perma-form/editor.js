/* Editor UI for bw/perma-form: choose the form and the preselected course; preview rendered by the server. */
( function ( wp ) {
	const { registerBlockType } = wp.blocks;
	const { createElement: el, Fragment } = wp.element;
	const { InspectorControls, useBlockProps } = wp.blockEditor;
	const { PanelBody, SelectControl, Disabled } = wp.components;
	const { __ } = wp.i18n;
	const ServerSideRender = wp.serverSideRender;
	const forms = ( window.bwPermaForms && window.bwPermaForms.forms ) || {};

	registerBlockType( 'bw/perma-form', {
		edit: ( { attributes, setAttributes } ) =>
			el( Fragment, null,
				el( InspectorControls, null,
					el( PanelBody, { title: __( 'Form', 'bw-perma-forms' ) },
						el( SelectControl, {
							label: __( 'Form', 'bw-perma-forms' ),
							value: attributes.form,
							options: Object.keys( forms ).map( ( key ) => ( { label: forms[ key ], value: key } ) ),
							onChange: ( form ) => setAttributes( { form } ),
							__next40pxDefaultSize: true,
							__nextHasNoMarginBottom: true,
						} ),
						'interest' === attributes.form && el( SelectControl, {
							label: __( 'Preselected course', 'bw-perma-forms' ),
							value: attributes.preselect,
							options: [
								{ label: __( 'None', 'bw-perma-forms' ), value: '' },
								{ label: 'Positive Psychology Basic', value: 'basic' },
								{ label: 'Positive Psychology Advanced', value: 'advanced' },
								{ label: 'PERMA Clinical Expert', value: 'clinical' },
							],
							onChange: ( preselect ) => setAttributes( { preselect } ),
							__next40pxDefaultSize: true,
							__nextHasNoMarginBottom: true,
						} )
					)
				),
				el( 'div', useBlockProps(), el( Disabled, null, el( ServerSideRender, { block: 'bw/perma-form', attributes } ) ) )
			),
		save: () => null,
	} );
}( window.wp ) );
