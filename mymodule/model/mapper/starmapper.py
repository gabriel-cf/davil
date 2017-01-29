""" Star Coordinates Mapper module
"""
import numpy as np
from mapper import Mapper

class StarMapper(Mapper):
    """Star class defining the methods for mapping points"""

    def map_points(self, axis_df, dimensional_values_df):
        """ Map points according to Star Coordinates setting
        """
        return np.dot(dimensional_values_df, axis_df)
