"""
    Hover Controller
"""

import logging
from copy import copy
from bokeh.models import HoverTool

class HoverController(object):
    """This class controls the elements displayed by the hover of a given view"""

    @staticmethod
    def _get_formatted_property(property_name):
        """property_name: (String)
           Returns: (String, String) property and property preceded by '@'
        """
        return str(property_name), "@{}".format(property_name)

    @staticmethod
    def _get_sorted_elements(element_index_tuples):
        """element_index_tuples: ([(String, Integer)]) list of tuples (property, index)
           Returns: (List<String>) properties sorted by index
        """
        element_index_tuples.sort(key=lambda property_index: property_index[1])
        return list(zip(*element_index_tuples)[0])

    LOGGER = logging.getLogger(__name__)

    DEFAULT_TOOLTIPS = ['error']

    def __init__(self, figure, properties=None, active_properties=None):
            
        self._figure = figure
        self._hover = None
        self._property_dict = dict()

        self._original_tools = copy(self._figure.tools)
        
        new_hover = HoverTool()
        self._hover = new_hover
        self._figure.add_tools(self._hover)

        if properties:
            self.set_properties(properties, active_properties=active_properties)

    def set_new_figure(self, figure):
        self._figure = figure
        self._refresh_hover_tool()


    def _refresh_hover_tool(self):
        """This is the only way I have found to update the tooltips added to the HoverTool.
           Direct edition of the tooltips list caused the hover to stop working.
           Removal of the HoverTool from the self._figure.toolbar.tools and addition of a new
           one resulted on erratic behavior.

           Considerations: this is actually adding a new reference to the same tool every time
           which may result in performance issues if the user switches many times.
        """
        self._hover.plot = None
        self._figure.add_tools(self._hover)
        

    def get_available_properties(self):
        """Returns available properties (selected and non-selected"""
        property_index_tuples = zip(self._property_dict.keys(), self._property_dict.values())
        return HoverController._get_sorted_elements(property_index_tuples)

    def get_active_properties(self):
        """Returns: (List<String>) hover tooltips (active properties)"""
        active_tips = zip(*self._hover.tooltips)
        if active_tips:
            print "I AM HERE"
            print list(zip(*self._hover.tooltips)[0])
            return list(zip(*self._hover.tooltips)[0])
        return []

    def is_active_property(self, property_name):
        """property_name: (String)
           Returns: (Boolean)
        """
        return property_name in self.get_active_properties()

    def toggle_property(self, property_name):
        """Adds a property to the hover if not present, removes otherwise
           property_name: (String)
        """
        if not self._hover:
            raise ValueError('Cannot toggle property on non-existing hover tool')
        if property_name not in self.get_available_properties():
            raise ValueError('Cannot toggle non-available property')

        if self.is_active_property(property_name):
            HoverController.LOGGER.info("Removing property '%s' from hover", property_name)
            self._remove_property(property_name)
        else:
            HoverController.LOGGER.info("Adding property '%s' to hover", property_name)
            self._add_property(property_name)
            self._sort_properties()

        self._refresh_hover_tool()

    def set_properties(self, properties, active_properties=None):
        """Clean and set hover properties according to input list
           It also saves the position of each property so it can be
           placed back when toggling
           properties: List<String> properties selectable in the hover
           [active_properties=None] List<String> properties active by default
        """
        properties = HoverController.DEFAULT_TOOLTIPS + properties
        self._hover.tooltips = []
        i = 0
        for new_property in properties:
            self._property_dict[new_property] = i
            if active_properties and new_property in active_properties:
                self._add_property(new_property)
            i += 1

        self._refresh_hover_tool()

    def _remove_property(self, property_name):        
        if not self._hover.tooltips is None:
            self._hover.tooltips.remove(HoverController._get_formatted_property(property_name))

    def _add_property(self, property_name):
        if not self._hover.tooltips is None:
            self._hover.tooltips.append(HoverController._get_formatted_property(property_name))

    def _sort_properties(self):
        property_index_tuples = [(HoverController._get_formatted_property(active_property),
                                  self._property_dict[active_property])
                                 for active_property in self.get_active_properties()]

        self._hover.tooltips = HoverController._get_sorted_elements(property_index_tuples)
