""" Abstract Mapper module
"""
from abc import ABCMeta, abstractmethod
from ..axis import Axis


class Mapper(object):
    """Abstract class defining the methods for mapping points"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def map_points(self, dimensional_values_df, axis_vectors_df, weights_df,
                   normalized_weights=False, normalization_method=None):
        """Calls the mapping algorithm of the subclass
            dimensional_values_df: pandas.Dataframe Values per axis per product
            axis_vectors_df: pandas.Dataframe Vector values per X, Y components
            weights_df: pandas.Dataframe Weight value per vector
            [normalized_weights=False]: If the weights should be normalized
            [normalization_method=None]: Normalization method for weights
        """
        # Check types
        #if (! axis_l):
        #	return None
        #if (all(isinstance(axis, Axis) for axis in axis_l):
        pass
