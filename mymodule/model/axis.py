"""
    Axis module
"""
import logging
from sympy import Segment


class Axis(object):
    """ Axis holding a segment, a label and the dimension identifier
        All axis share a CENTRE point where they part from
    """

    CENTRE = (0, 0)
    LOGGER = logging.getLogger("Axis")
    LOGGER.setLevel(logging.DEBUG)

    def __init__(self, label, dimension, segment, show=True):
        """ label --> (String) displayable name of this axis
            dimension --> (String) id of the dimension that the axis represents
            segment --> (sympy.geometry.line.Segment) segment of this axis
        """
        self._label = label
        self._dimension = dimension
        self._segment = segment
        self._show = show

    def get_angle(self):
        """Returns the angle in radians"""
        return self._segment.angle_between(Segment((0,0), (1,0)))

    def get_label(self):
        """Returns the (String) label of the axis"""
        return self._label


    def get_segment(self):
        """Returns the (sympy.geometry.line.Segment) segment of the axis"""
        return self._segment

    def set_label(self, label_name):
        """ Sets the label to the given name
            label_name --> (String) new label name
        """
        self._label = label_name

    def get_dimension(self):
        """Returns the (String) value of the dimension"""
        return self._dimension

    def get_segment_points(self):
        """ Returns the segment defined by two tuples where each tuple
            holds two float values (x, y) defining the point
        """
        def convert_points(point):
            """ Takes a sympy Point and extracts its float values"""
            x, y = point
            p = (float(x), float(y))
            return p

        p0 = convert_points(self._segment.p1)
        p1 = convert_points(self._segment.p2)
        return p0, p1

    def get_segment_end_point(self):
        """Returns the end point of the axis as a tuple of (float, float)"""
        p0, p1 = self.get_segment_points()
        if self._segment.length == 0:
            Axis.LOGGER.warning("Returning end point of a segment of length 0")
            return p0
        # Return the edge point (not the centre)
        return p1 if Axis.CENTRE == p0 else p0

    def is_visible(self):
        """Determines whether the axis should be visible or not"""
        return self._show and self._segment.length > 0
