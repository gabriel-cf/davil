"""
    Dummy Mapper
"""

import random
import pandas as pd

DUMMY_COORDINATES_ID = "Dummy Coordinates"

def dummy_coordinates(dimensional_values_df, axis_vectors_df, weights_df=None,
                      normalized_weights=False, normalization_method=None):
    """ Maps the points to random coordinates
        dimensional_values_df: pandas.DataFrame Values per axis per product
        axis_vectors_df: pandas.DataFrame Vector values per X, Y components
        weights_df: pandas.DataFrame Weight value per vector
        [normalized_weights=False]: If the weights should be normalized
        [normalization_method=None]: Normalization method for weights
    """
    min_range = -2
    max_range = 2   
    n_points = len(dimensional_values_df.index)
    x_l = [random.uniform(min_range, max_range) for i in xrange(0, n_points)]
    y_l = [random.uniform(min_range, max_range) for i in xrange(0, n_points)]
    name_l = dimensional_values_df.index.tolist()

    return pd.DataFrame({'x':x_l, 'y':y_l}, index=name_l)
