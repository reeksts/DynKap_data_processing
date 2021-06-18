class FigureFormatting:
	def __init__(self):
		'''
		Sizer parameter explanations:
			tick_size - size of the tick text
			tick_length - length of tick lines
			tick_width = width of tick lines
			tight_layout_rect (tight_layout_rect) - restricted plot area (left, bottom, right, top)

			line_width - width of plot lines
			legend_borderaxespad (borderaxespad) - pad outside the legend frame
			legend_handlelenght (handlelength) -  length of the handle in legend
			legend_loc (loc) - location of the legend anchor
		'''
		inch = 2.54
		pres_scaler = 1.2

		self.styler = {
			'light': {
				'name': 'light',
				'facecolor': 'white',
				'axis_facecolor': 'white',
				'label_color': 'black',
				'tick_color': 'black',
				'tick_label_color': 'black',
				'spine_color': 'black',
				'axis_label_color': 'black',
				'text_color': 'black',
				'aidline_color': 'black',
				'legend_text_color': 'black',
				'legend_edge_color': 'black',
				'legend_face_color': 'white',
				'legend_framealpha': 0.8,
				'legend_edge_color_rgba': (0, 0, 0, 0),
				'legend_face_color_rgba': (1, 1, 1, 0.5)},
			'dark': {
				'name': 'dark',
				'facecolor': 'black',
				'axis_facecolor': 'black',
				'label_color': 'white',
				'tick_color': '#999999',		# 999999 is grey
				'tick_label_color': 'white',
				'spine_color': '#999999',		# 999999 is grey
				'axis_label_color': 'white',
				'text_color': 'white',
				'aidline_color': 'white',
				'legend_text_color': 'white',
				'legend_edge_color': 'white',
				'legend_face_color': 'black',
				'legend_framealpha': 0.5,
				'legend_edge_color_rgba': (1, 1, 1, 0),
				'legend_face_color_rgba': (0, 0, 0, 0.5)}}

		self.paper_1x1_full_width = {
			'fig_type': 'paper',
			'tight_layout_pad': 0.2,
			'tight_layout_h_pad': 0.4,
			'figsize': (16/inch, 6/inch),
			'legend_size': 8,
			'label_size': 8,
			'tick_size': 8,
			'tick_length': 3,
			'tick_width': 1,
			'tick_rotation': 45,
			'spine_width': 1,
			'line_width': 1,
			'legend_handlelength': 3,
			'legend_borderaxespad': 0,
			'legend_bbox_to_anchor': (1.1, 0.5),
			'legend_loc': 'center left',
			'legend_labelspacing': 0.4,
			'labelpad': 3,
			'legend_frame_width': 0.5,
			'legend_edge_color': 'dimgray'}

		self.pres_1x1_full_width = {
			'fig_type': 'paper',
			'tight_layout_pad': 0.2,
			'tight_layout_h_pad': 0.4,
			'figsize': (pres_scaler*16/inch, pres_scaler*6/inch),
			'legend_size': 8,
			'label_size': 8,
			'tick_size': 8,
			'tick_length': 3,
			'tick_width': 0.5,   	# decreased
			'tick_rotation': 45,
			'spine_width': 0.5,   	# decreased
			'line_width': 1,
			'legend_handlelength': 3,
			'legend_borderaxespad': 0,
			'legend_bbox_to_anchor': (1.1, 0.5),
			'legend_loc': 'center left',
			'legend_labelspacing': 0.4,
			'labelpad': 3,
			'legend_frame_width': 0.5,
			'legend_edge_color': 'dimgray'}		# this has to be moved to styler

		self.paper_3x1_full_width = {
			'figsize': (16/inch, 12/inch),
			'tight_layout_pad': 0.2,
			'tight_layout_h_pad': 0.4,
			'legend_size': 8,
			'label_size': 8,
			'tick_size': 8,
			'tick_length': 3,
			'tick_width': 1,
			'tick_rotation': 45,
			'spine_width': 1,
			'hspace': 0.1,
			'line_width': 1,
			'legend_handlelength': 3,
			'legend_borderaxespad': 0,
			'legend_bbox_to_anchor': (1.1, 0.5),
			'legend_loc': 'center left',
			'legend_labelspacing': 0.3,
			'labelpad': 2,
			'legend_frame_width': 0.5,
			'legend_edge_color': 'dimgray'}

		self.pres_3x1_full_width = {
			'figsize': (pres_scaler*16/inch, pres_scaler*12/inch),
			'tight_layout_pad': 0.2,
			'tight_layout_h_pad': 0.6,
			'legend_size': 6,						# decreased
			'label_size': 6,						# decreased
			'tick_size': 6,
			'tick_length': 3,
			'tick_width': 0.5,						# decreased
			'tick_rotation': 45,
			'spine_width': 0.5,						# decreased
			'hspace': 0.6,							# increased
			'line_width': 0.6,						# decreased
			'legend_handlelength': 3,
			'legend_borderaxespad': 0,
			'legend_bbox_to_anchor': (1.06, 0.5),
			'legend_loc': 'center left',
			'legend_labelspacing': 0.6,				# increased
			'labelpad': 2,
			'legend_frame_width': 0.5,
			'legend_edge_color': 'dimgray'}

		self.paper_3x1_partial_width = {
			'figsize': (10/inch, 12/inch),
			'tight_layout_pad': 0.2,
			'tight_layout_rect': (0.02, 0.05, 0.81, 1.0),  # (left, bottom, right, top)
			'legend_size': 8,
			'label_size': 8,
			'tick_size': 8,
			'tick_length': 3,
			'tick_width': 1,
			'tick_rotation': 45,
			'spine_width': 1,
			'hspace': 0.1,
			'line_width': 1,
			'legend_handlelength': 3,
			'legend_borderaxespad': 0,
			'legend_bbox_to_anchor': (1.1, 0.5),  # not modified
			'legend_loc': 'center left',
			'marker_size': 5,
			'marker_edge_width': 1,
			'marker_face_color': 'none',
			'labelpad': 3,
			'legend_frame_width': 0.5,
			'legend_edge_color': 'dimgray'}

		self.pres_3x1_partial_width = {
			'figsize': (10 / inch, 12 / inch),			# THIS SIZE IS NOT MODIFIED!!!!
			'tight_layout_pad': 0.2,
			'tight_layout_rect': (0.02, 0.05, 0.81, 1.0),  # (left, bottom, right, top)
			'legend_size': 8,
			'label_size': 8,
			'tick_size': 8,
			'tick_length': 3,
			'tick_width': 1,
			'tick_rotation': 45,
			'spine_width': 1,
			'hspace': 0.1,
			'line_width': 1,
			'legend_handlelength': 3,
			'legend_borderaxespad': 0,
			'legend_bbox_to_anchor': (1.1, 0.5),  # not modified
			'legend_loc': 'center left',
			'marker_size': 5,
			'marker_edge_width': 1,
			'marker_face_color': 'none',
			'labelpad': 3,
			'legend_frame_width': 0.5,
			'legend_edge_color': 'dimgray'}

		self.paper_1x1_partial_width = {
			'figsize': (8/inch, 6/inch),
			'tight_layout_pad': 0.2,
			'tight_layout_rect': (0.02, 0.05, 0.81, 1.0),  # (left, bottom, right, top)
			'legend_size': 7,
			'label_size': 7,
			'tick_size': 7,
			'tick_length': 3,
			'tick_width': 1,
			'tick_rotation': 45,
			'spine_width': 1,
			'hspace': 0.1,
			'line_width': 1,
			'legend_handlelength': 3,
			'legend_borderaxespad': 0,
			'legend_bbox_to_anchor': (1.1, 0.5),  # not modified
			'legend_loc': 'center left',
			'marker_size': 5,
			'marker_edge_width': 1,
			'marker_face_color': 'none',
			'labelpad': 3,
			'legend_frame_width': 0.5,
			'legend_edge_color': 'dimgray'}

		self.pres_1x1_partial_width = {
			'figsize': (8 / inch, 6 / inch),					# THIS SIZE IS NOT MODIFIED!!!!
			'tight_layout_pad': 0.2,
			'tight_layout_rect': (0.02, 0.05, 0.81, 1.0),  # (left, bottom, right, top)
			'legend_size': 7,
			'label_size': 7,
			'tick_size': 7,
			'tick_length': 3,
			'tick_width': 1,
			'tick_rotation': 45,
			'spine_width': 1,
			'hspace': 0.1,
			'line_width': 1,
			'legend_handlelength': 3,
			'legend_borderaxespad': 0,
			'legend_bbox_to_anchor': (1.1, 0.5),  # not modified
			'legend_loc': 'center left',
			'marker_size': 5,
			'marker_edge_width': 1,
			'marker_face_color': 'none',
			'labelpad': 3,
			'legend_frame_width': 0.5,
			'legend_edge_color': 'dimgray'}

		self.paper_4x3_full_width = {
			'figsize': (16/inch, 14/inch),
			'legend_size': 6,
			'label_size': 6,
			'tick_size': 6,
			'tick_length': 1,
			'tick_width': 0.5,
			'tick_rotation': 45,
			'spine_width': 0.5,
			'hspace': 0.4,
			'wspace': 0.05,
			'line_width': 0.5,
			'legend_handlelength': 2,
			'legend_borderaxespad': 0,
			'legend_bbox_to_anchor': (1.1, 0.5),  # not modified
			'legend_loc': 'center left',
			'legend_labelspacing': 0.6,
			'marker_size': 2,
			'marker_edge_width': 0.5,
			'marker_face_color': 'none',
			'labelpad': 1,
			'legend_frame_width': 0.25,
			'legend_edge_color': 'dimgray'}

		self.pres_4x3_full_width = {
			'figsize': (pres_scaler*16 / inch, pres_scaler*14 / inch),
			'legend_size': 6,
			'label_size': 6,
			'tick_size': 6,
			'tick_length': 1,
			'tick_width': 0.5,
			'tick_rotation': 45,
			'spine_width': 0.5,
			'hspace': 0.4,
			'wspace': 0.05,
			'line_width': 0.5,
			'legend_handlelength': 2,
			'legend_borderaxespad': 0,
			'legend_bbox_to_anchor': (1.1, 0.5),  # not modified
			'legend_loc': 'center left',
			'legend_labelspacing': 0.6,
			'marker_size': 2,
			'marker_edge_width': 0.5,
			'marker_face_color': 'none',
			'labelpad': 1,
			'legend_frame_width': 0.15,
			'legend_edge_color': 'dimgray'}

		self.sizer = {'paper': {'1x1_full_width': self.paper_1x1_full_width,
								'1x1_partial_width': self.paper_1x1_partial_width,
								'3x1_full_width': self.paper_3x1_full_width,
								'3x1_partial_width': self.paper_3x1_partial_width,
								'4x3_full_width': self.paper_4x3_full_width},
					  'presentation': {'1x1_full_width': self.pres_1x1_full_width,
									   '1x1_partial_width': self.pres_1x1_partial_width,
									   '3x1_full_width': self.pres_3x1_full_width,
									   '3x1_partial_width': self.pres_3x1_partial_width,
									   '4x3_full_width': self.pres_4x3_full_width}}
