"""
    AxisFigureElement
"""

import logging
from abstract_figure_element import AbstractFigureElement

class AxisFigureElement(AbstractFigureElement):
    """Axis figure element composed by the bokeh elements Segment, Square,
       and optionally Label
    """
    LOGGER = logging.getLogger(__name__)

    def __init__(self, segment, square, label=None):
        """Instantiates a new Axis element"""
        self._segment = segment
        self._square = square
        self._label = label

    def visible(self, show):
        """Will mark as visible or invisible all elements
           show: (Boolean) Self explanatory
           Returns: (Boolean) True if its visibility has changed
        """
        if show != self._segment.visible:
            self._segment.visible = show
            self._square.visible = show
            if self._label:
                self._label.visible = show
            return True
        return False

    def get_identifier(self):
        """Will return the identifier of the element"""
        return self._segment.name

    def is_visible(self):
        """Will return True if the element is visible"""
        return self._segment.visible
