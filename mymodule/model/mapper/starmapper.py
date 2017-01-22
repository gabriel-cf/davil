""" Dummy Mapper module
"""
import random
from sympy import Point, Segment
from mapper import Mapper

class StarMapper(Mapper):
    """Star class defining the methods for mapping points"""

    MAX_POINTS = 50
    MIN_RANGE = -10
    MAX_RANGE = 10
    KWARG_AXIS_LIST = 'axis_list'

    def map_points(self, **kwargs):
        """ Map points using Star Coordinates
            required kwargs:
            'axis_list': sympy.geometry.line.LinearEntity[] (Typically Segment)
        """
        axis_list = kwargs[StarMapper.KWARG_AXIS_LIST]
        if axis_list is None or len(axis_list == 0):
            raise TypeError("Star Coordinates mapping require a list " 
                + "with at least one valid axis under the kwarg '{}'"
                .format(StarMapper.KWARG_AXIS_LIST))

        point_l = []

        for _ in xrange(0, StarMapper.MAX_POINTS):
            x0 = random.randint(StarMapper.MIN_RANGE, StarMapper.MAX_RANGE)
            y0 = random.randint(StarMapper.MIN_RANGE, StarMapper.MAX_RANGE)
            point_l.append(Point(x0, y0))

        return point_l

    def __init__(self):
        pass
