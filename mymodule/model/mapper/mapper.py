""" Abstract Mapper module
"""
from abc import ABCMeta, abstractmethod
from ..axis import Axis


class Mapper(object):
    """Abstract class defining the methods for mapping points"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def map_points(self, axis_l):
        """Calls the mapping algorithm of the subclass
			axis_l --> (model.axis Axis) object representing an Axis
        """
        # Check types
        #if (! axis_l):
        #	return None
        #if (all(isinstance(axis, Axis) for axis in axis_l):
        pass
