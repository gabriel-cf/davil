"""
    Point Size controller
"""

from ...backend.util.line_equation import calculate_line_equation

class PointSizeController(object):
    """Object capable of setting sizes to points
        If there is an error value for the point, it will scale the size
        of the point between the size set for the minimum error and the size
        set for the maximum error, using a line function shaped by the points
        (0, initial_size) and (1, final_size)
    """

    # Size of the point when its error is 0
    DEFAULT_INITIAL_SIZE = 2
    # Size of the point when its error is 1
    DEFAULT_FINAL_SIZE = 12

    def __init__(self, source, 
                 initial_size=DEFAULT_INITIAL_SIZE, 
                 final_size=DEFAULT_FINAL_SIZE):
        self._source = source
        x0x1 = (0, 1)
        y0y1 = (initial_size, final_size)
        # y = mx + c        
        self._m, self._c = calculate_line_equation(x0x1, y0y1)
        self._intial_size = initial_size
        self._final_size = final_size

    def set_single_size(self, size):
        self._source.data['size'] = [size for i in xrange(0, len(self._source.data['x']))]

    def update_sizes(self):
        """Normalize sizes using the error normalized
        """
        self._source.data['size'] = self._m * self._source.data['error'] + self._c
