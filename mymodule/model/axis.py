"""
    Axis module
"""
from sympy import Segment


class Axis(object):
    """Axis holding a segment, a label and the dimension identifier"""

    def __init__(self, label, dimension, segment):
        """ label --> (String) displayable name of this axis
            dimension --> (String) id of the dimension that the axis represents
            segment --> (sympy.geometry.line.Segment) segment of this axis
        """
        self._label = label
        self._dimension = dimension
        self._segment = segment

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
