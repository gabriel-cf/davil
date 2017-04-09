"""
    DataFrame Matrix Utils module
"""
from __future__ import division
import pandas as pd

class DFMatrixUtils(object):
    """Static methods for performing operations on a dataframe matrix"""

    @staticmethod
    def get_vectors(axis_points_df):
        """ Receives a dataframe of columns x0,x1,y0,y1 and returns
            a DataFrame with two columns holding Vx and Vy
        """
        def get_vector(x0, x1, y0, y1):
            v_x = x1 - x0
            v_y = y1 - y0
            return v_x, v_y

        # Create new DataFrame obtaining the normalized vectors from the points
        vector_matrix = []
        for _, row in axis_points_df.iterrows():
            vector_matrix.append(get_vector(row['x0'], row['x1'], row['y0'], row['y1']))
        vectors_df = pd.DataFrame(vector_matrix, index=axis_points_df.index, columns=["x", "y"])

        return vectors_df

    @staticmethod
    def get_total_sum(df):
        """ df: (Number) dataframe holding the numeric values
            Returns: (int) total sum of all the dataframe elements
        """
        if len(df.columns) == 1:
            return int(df.sum(0))
        return int(df.sum(0).sum(0))

    @staticmethod
    def get_max_value(df):
        """ df: (Number) dataframe holding the numeric values
            Returns: (int) max value of the dataframe
        """
        if len(df.columns) == 1:
            return int(df.max(0))
        return int(df.max(0).max(0))

    @staticmethod
    def get_min_value(df):
        """ df: (Number) dataframe holding the numeric values
            Returns: (int) min value of the dataframe
        """
        if len(df.columns) == 1:
            return int(df.min(0))
        return int(df.min(0).min(0))

    @staticmethod
    def sum_by_axis(df, axis):
        """ df: (Number) dataframe holding the numeric values
            axis: (int) 0 -> sum columns ; 1 -> sum rows
            Returns: (pandas.DataFrame) axis with the rows or columns added
        """
        return pd.DataFrame(df.sum(axis))

    @staticmethod
    def max_by_axis(df, axis):
        """ df: (Number) dataframe holding the numeric values
            axis: (int) 0 -> sum columns ; 1 -> sum rows
            Returns: (pandas.DataFrame) axis with the rows or columns added
        """
        return pd.DataFrame(df.max(axis))
