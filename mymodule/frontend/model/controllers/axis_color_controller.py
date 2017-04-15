"""
    Axis Color Controller
"""
from bokeh.palettes import inferno, grey, viridis

class AxisColorController(object):
    """docstring for AxisColorController"""
    INFERNO_PALETTE_ID = 'inferno'
    GREY_PALETTE_ID = 'grey'
    VIRIDIS_PALETTE_ID = 'viridis'
    DEFAULT_PALETTE_ID = INFERNO_PALETTE_ID
    GREY_PALETTE = list(reversed(grey(256)))
    INFERNO_PALETTE = inferno(256)
    VIRIDIS_PALETTE = viridis(256)

    def __init__(self, source_points, dimension_values_df_norm, palette_id=DEFAULT_PALETTE_ID):
        self._source_points = source_points
        self._dimension_values_df_norm = dimension_values_df_norm
        self._palette = None
        self._last_selected_id = None
        self.update_palette(palette_id)
        
    def update_palette(self, palete_id):
        if palete_id == AxisColorController.INFERNO_PALETTE_ID:
            self._palette = AxisColorController.INFERNO_PALETTE
        elif palete_id == AxisColorController.GREY_PALETTE_ID:
            self._palette = AxisColorController.GREY_PALETTE
        elif palete_id == AxisColorController.VIRIDIS_PALETTE_ID:
            self._palette = AxisColorController.VIRIDIS_PALETTE
        if self._last_selected_id:
            self.update_colors()

    def update_colors(self, axis_id=None):
        #TODO - Control that the axis id is in the dataframe
        if not axis_id:
            axis_id = self._last_selected_id
        # get index of colors
        column_result = (self._dimension_values_df_norm[axis_id] * len(self._palette)).astype(int)
        # map index with color in the palette and assign to the source_points
        self._source_points.data['color'] = [self._palette[min(len(self._palette) - 1, index)] \
                                             for index in column_result]
        self._last_selected_id = axis_id

    def get_available_palettes(self):
        return [AxisColorController.GREY_PALETTE_ID,
                AxisColorController.INFERNO_PALETTE_ID,
                AxisColorController.VIRIDIS_PALETTE_ID]

