"""
    Axis Color Controller
"""
import logging
import numpy as np
from pandas import DataFrame
from bokeh.palettes import inferno, grey, viridis

class ColorController(object):
    """Controls the color of the elements based on the selected method
       and the active palette. When coloring by classification only one
       type of palette will be available. The rest of palettes are
       available when an axis is selected
    """
    LOGGER = logging.getLogger(__name__)
    INFERNO_PALETTE_ID = 'inferno'
    GREY_PALETTE_ID = 'grey'
    VIRIDIS_PALETTE_ID = 'viridis'
    CLUSTER_CATEGORY_PALETTE_ID = 'cluster'
    DEFAULT_PALETTE_ID = INFERNO_PALETTE_ID
    GREY_PALETTE = list(reversed(grey(256)))
    INFERNO_PALETTE = inferno(256)
    VIRIDIS_PALETTE = viridis(256)
    # 23 RGB colors from Red to Pink for Clustering categorization
    # This palette is not for axis and should not show up in the list
    # of available palettes on the web application
    #CATEGORY_PALETTE = ['#ff0000', '#ff4000', '#ff8000', '#ffbf00',
    #                    '#ffff00', '#bfff00', '#80ff00', '#40ff00',
    #                    '#00ff00', '#00ff40', '#00ff80', '#00ffbf',
    #                    '#00ffff', '#00bfff', '#0080ff', '#0040ff',
    #                    '#0000ff', '#4000ff', '#8000ff', '#bf00ff',
    #                    '#ff00ff', '#ff00bf', '#ff0080']
    CATEGORY_PALETTE = ["red", "black", "orange", "green", "grey", "yellow", "navy"]
    NONE_PALETTE = ["navy"]
    NONE_PALETTE_ID = 'None'
    CATEGORY_METHOD_ID = 'Category'
    AXIS_METHOD_ID = 'Axis'
    NONE_METHOD_ID = 'None'
    NONE_AXIS_ID = 'None'
    DEFAULT_METHOD_ID = NONE_METHOD_ID

    @staticmethod
    def _get_axis_palette_dict():
        """Returns a dictionary of palettes {palette_id, palette}"""
        return dict({
            ColorController.INFERNO_PALETTE_ID: ColorController.INFERNO_PALETTE,
            ColorController.GREY_PALETTE_ID: ColorController.GREY_PALETTE,
            ColorController.VIRIDIS_PALETTE_ID: ColorController.VIRIDIS_PALETTE,
            ColorController.NONE_PALETTE_ID: ColorController.NONE_PALETTE
            })

    def __init__(self, input_data_controller, normalization_controller, classification_controller, 
                 source_points, palette_id=NONE_PALETTE_ID):
        self._palette_dict = ColorController._get_axis_palette_dict()
        self._input_data_controller = input_data_controller
        self._normalization_controller = normalization_controller
        self._classification_controller = classification_controller
        self._source_points = source_points
        self._active_palette_id = ColorController.NONE_PALETTE_ID
        self._selected_axis_id = ColorController.NONE_AXIS_ID
        self.update_palette(palette_id)
        self._active_method = ColorController.DEFAULT_METHOD_ID

    def update_palette(self, palette_id):
        if not palette_id in self._palette_dict:
            ColorController.LOGGER.warn("Palette id '%s' is not known", palette_id)
        else:
            self._active_palette_id = palette_id

    def update_colors(self):        
        """Update points' color accoring to selected method and axis or categories"""
        if self.in_category_mode():
            self._color_points_by_categories()
        elif self.in_axis_mode():
            self._color_points_by_axis()
        else:
            self._color_points_by_initial_settings()
        
    def update_method(self, method_id):
        #if not method_id in self.get_available_color_methods():
        #    raise ValueError("The selected coloring method '{}' is not known".format(method_id))
        self._active_method = method_id

    def update_selected_axis(self, axis_id):
        ColorController.LOGGER.debug("Updating axis ID to '%s'", axis_id)
        if not axis_id in self.get_available_axis_ids():
            raise ValueError("'{}' is not a valid axis".format(axis_id))
        self._selected_axis_id = axis_id

    def get_available_axis_ids(self):
        return [ColorController.NONE_AXIS_ID]\
                + self._input_data_controller.get_dimensional_labels()

    def get_selected_axis_id(self):
        return self._selected_axis_id

    def get_active_palette(self):
        return self._active_palette_id

    def get_active_color_method(self):
        return self._active_method

    def get_available_palettes(self):
        return self._palette_dict.keys()

    def get_available_color_methods(self):
        return [ColorController.AXIS_METHOD_ID,
                ColorController.CATEGORY_METHOD_ID,
                ColorController.NONE_METHOD_ID]

    def in_axis_mode(self):
        return self._active_method == ColorController.AXIS_METHOD_ID

    def in_category_mode(self):
        return self._active_method == ColorController.CATEGORY_METHOD_ID

    def _color_points_by_initial_settings(self):
        """Will set the color of all points based on the initial palette"""
        ColorController.LOGGER.debug("Coloring by initial settings")
        palette_index_list = np.zeros(self._input_data_controller.get_number_of_values())
        self._map_source_points_color(palette_index_list, ColorController.NONE_PALETTE)

    def _color_points_by_axis(self):
        # get index of colors, we normalize by Feature Scaling to get all values between 0 and 1
        # and then multiply by the length of the palette
        ColorController.LOGGER.debug("Coloring by axis '%s'", self._selected_axis_id)
        if self._selected_axis_id == ColorController.NONE_AXIS_ID:
            ColorController.LOGGER.warn("No coloring was made since selected axis was None")
            return
        active_palette = self._get_palette()
        values_df = self._input_data_controller.get_dimensional_values(filtered=False)
        column_norm = self._normalization_controller\
                      .normalize_feature_scaling(values_df)[self._selected_axis_id]
        palette_index_list = (column_norm * len(active_palette) - 1).astype(int)
        # map index with color in the palette and assign to the source_points
        self._map_source_points_color(palette_index_list, active_palette)

    def _color_points_by_categories(self):
        ColorController.LOGGER.debug("Coloring by category")
        categories = self._classification_controller.get_categories()
        if categories is None or len(categories) == 0:
            ColorController.LOGGER.warn("No coloring was made since no categories were found")
            return
        palette = ColorController.CATEGORY_PALETTE
        # Map each category into a specific index
        palette_index_list = self._get_palette_index_list(categories, palette)
        self._map_source_points_color(palette_index_list, ColorController.CATEGORY_PALETTE)

    def _map_source_points_color(self, palette_index_list, palette):
        max_index_list = max(palette_index_list)
        max_index_palette = len(palette) - 1
        if max_index_list > max_index_palette:
            ColorController.LOGGER.warn(("Max index (%s) in palette index list is"
                                         "higher than the palette one (%s), "
                                         "higher indexes will be assigned the "
                                         "highest palette value"),
                                        max_index_list, max_index_palette)
        self._source_points.data['color'] = [palette[min(max_index_palette, index)] \
                                             for index in palette_index_list]

    def _get_palette(self):
        return self._palette_dict[self._active_palette_id]

    def _get_palette_index_list(self, categories, palette):
        """Receives a list of category elements, of any type, and returns
           a list of numeric values which are the indexes of the palette
        """
        palette_index_list = []
        category_dict = dict()
        shift = 0
        for category in categories:
            if not category in category_dict:
                category_dict[category] = shift
                shift += 1
            palette_index_list.append(category_dict[category])
        # Once we have the categories indexed, we normalize and multiply
        # by the length of the palette in order to distribute the values
        #return palette_index_list
        _ = self._normalization_controller\
                .normalize_feature_scaling(DataFrame(palette_index_list))

        return (_ * (len(palette) - 1)).astype(int)[0]
