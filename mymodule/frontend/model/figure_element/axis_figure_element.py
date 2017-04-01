"""
    AxisFigureElement
"""

from abstract_figure_element import AbstractFigureElement

class AxisFigureElement(AbstractFigureElement):
    """Axis figure element composed by the bokeh elements Segment, Square,
       and optionally Label
    """

    def __init__(self, segment, square, label=None):
        """Instantiates a new Axis element"""
        self._segment = segment
        self._square = square
        self._label = label

    def visible(self, show):
        """Will mark as visible or invisible all elements
           visible: (Boolean)
        """
        self._segment.visible = show
        self._square.visible = show
        if self._label:
            self._label.visible = show

    def get_identifier(self):
        """Will return the identifier of the element"""
        return self._segment.name

    def is_visible(self):
        """Will return True if the element is visible"""
        return self._segment.visible
