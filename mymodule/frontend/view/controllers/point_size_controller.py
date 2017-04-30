"""
    Point Size controller
"""
import logging
from ....backend.util.line_equation import calculate_line_equation

class PointSizeController(object):
    """Object capable of setting sizes to points
       If there is an error value for the point, it will scale the size
       of the point between the size set for the minimum error and the size
       set for the maximum error, using a line function shaped by the points
       (0, initial_size) and (1, final_size)
    """
    LOGGER = logging.getLogger(__name__)
    # Size of the point with MIN error
    DEFAULT_INITIAL_SIZE = 4
    # Size of the point with MAX error
    DEFAULT_FINAL_SIZE = 12
    MIN_SIZE = 1

    @staticmethod
    def _calculate_line_equation(initial_size, final_size):
        x0x1 = (0, 1)
        y0y1 = (initial_size, final_size)
        # y = mx + c
        return calculate_line_equation(x0x1, y0y1)

    @staticmethod
    def _get_valid_size(size):
        """Will return the original size or the minimum valid one"""
        size = int(size)
        return size if size >= PointSizeController.MIN_SIZE \
                    else PointSizeController.MIN_SIZE

    def __init__(self, error_controller, source,
                 initial_size=DEFAULT_INITIAL_SIZE,
                 final_size=DEFAULT_FINAL_SIZE):
        """source: (ColumnDataSource) shared datasource holding the points
                    where the size of the points will be updated
           [initial_size=DEFAULT_INITIAL_SIZE]: (int >= 0)
           [initial_size=DEFAULT_FINAL_SIZE]: (int >= 0)
        """
        self._error_controller = error_controller
        self._source = source
        self._m, self._c = self._calculate_line_equation(initial_size, final_size)
        self._initial_size = initial_size
        self._final_size = final_size

    def set_single_size(self, new_size):
        """Sets a common size for all the source points
           new_size: (int) self explanatory
        """
        new_size = PointSizeController._get_valid_size(new_size)
        self._source.data['size'] = [new_size for i in xrange(0, len(self._source.data['x']))]

    def set_initial_size(self, new_size):
        """new_size: (int >= MIN_SIZE) self explanatory"""        
        self._initial_size = PointSizeController._get_valid_size(new_size)
        self.update_sizes()

    def set_final_size(self, new_size):
        """new_size: (int >= MIN_SIZE) self explanatory"""
        self._final_size = PointSizeController._get_valid_size(new_size)
        self.update_sizes()

    def get_initial_size(self):
        """Self explanatory"""
        return self._initial_size

    def get_final_size(self):
        """Self explanatory"""
        return self._final_size

    def update_sizes(self):
        """Normalize the source point sizes using the normalized error
           We cannot use the error of the source because internally Bokeh turns
           it into an array.
        """
        point_error_s = self._error_controller.get_last_point_error()
        PointSizeController.LOGGER.debug("Updating sizes: %s-%s",
                                         self._initial_size, self._final_size)
        self._m, self._c = self._calculate_line_equation(self._initial_size, self._final_size)
        self._source.data['size'] = self._m * point_error_s + self._c
