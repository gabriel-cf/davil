""" Star Coordinates Mapper module
"""
import numpy as np
from mapper import Mapper

class StarMapper(Mapper):
    """Star class defining the methods for mapping points"""

    def map_points(self, dimensional_values_df, axis_df ):
        """ Map points according to Star Coordinates setting
        """
        mapped_points = dimensional_values_df.dot(axis_df)
        mapped_points.columns = ['x', 'y']
        return mapped_points
