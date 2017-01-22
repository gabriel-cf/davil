""" Abstract Mapper module
"""
from abc import ABCMeta, abstractmethod


class Mapper(object):
    """Abstract class defining the methods for mapping points"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def map_points(self):
        """Calls the mapping algorithm of the subclass """
        pass
