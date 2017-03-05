"""
    AxisFigureElement
"""

from abstract_figure_element import AbstractFigureElement

class AxisFigureElement(AbstractFigureElement):
    """Axis figure element composed by the bokeh elements Segment, Square,
       and optionally Label
    """
    MAPPER_CONTROLLER = None

    @staticmethod
    def set_mapper_controller(mapper_controller):
        """Sets the static mapper controller of the class"""
        AxisFigureElement.MAPPER_CONTROLLER = mapper_controller

    def __init__(self, segment, square, source, label=None):
        """Instantiates a new Axis element"""
        self._segment = segment
        self._square = square
        self._label = label
        self._source = source

    def visible(self, show, remap=False):
        """Will mark as visible or invisible all children elements
           visible: (Boolean)
        """
        if self._segment.visible != show:
            AxisFigureElement.MAPPER_CONTROLLER.update_axis_status(self.get_identifier(), show)
            self._segment.visible = show
            self._square.visible = show
            if self._label:
                self._label.visible = show
            if remap:
                print "ATTEMPTING MAPPING"
                AxisFigureElement.MAPPER_CONTROLLER.execute_mapping()

    def get_identifier(self):
        """Will return the identifier of the element"""
        return self._segment.name

    def is_visible(self):
        """Will return True if the element is visible"""
        return self._segment.visible
