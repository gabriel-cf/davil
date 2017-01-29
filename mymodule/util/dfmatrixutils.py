"""
    DataFrame Matrix Utils module
"""
from __future__ import division
import pandas as pd
import math


class DFMatrixUtils(object):
    """Static methods for extracting data from a pandas.DataFrame"""
    
    @staticmethod
    def get_vectors(axis_points_df):
        """ Receives a dataframe of columns x0,x1,y0,y1 and returns
            a DataFrame with two columns holding Vx and Vy
        """
        def get_normalized_vector(x0, x1, y0, y1):
            v_x = x1 - x0
            v_y = y1 - y0
            norm = math.sqrt(v_x ** 2 + v_y **2)
            return v_x / norm, v_y / norm

        # Create new DataFrame obtaining the normalized vectors from the points
        vector_matrix = []
        for index, row in axis_points_df.iterrows():
            vector_matrix.append(get_normalized_vector(row['x0'], row['x1'], row['y0'], row['y1']))
        vectors_df = pd.DataFrame(vector_matrix, index=axis_points_df.index, columns=["v_x", "v_y"])

        return vectors_df
