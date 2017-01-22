""" Dummy Mapper module
"""
import random
from sympy import Point
from mapper import Mapper

class DummyMapper(Mapper):
    """Dummy class defining the methods for mapping points"""

    MAX_POINTS = 50
    MIN_RANGE = -10
    MAX_RANGE = 10

    def map_points(self, **kwargs):
        """Dummy mapping implementation"""
        point_l = []

        for _ in xrange(0, DummyMapper.MAX_POINTS):
            x0 = random.randint(DummyMapper.MIN_RANGE, DummyMapper.MAX_RANGE)
            y0 = random.randint(DummyMapper.MIN_RANGE, DummyMapper.MAX_RANGE)
            point_l.append(Point(x0, y0))

        return point_l

    def __init__(self):
        pass
