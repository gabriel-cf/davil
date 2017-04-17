"""
    DataFrame Matrix Utils module
"""

from __future__ import division
import logging
import pandas as pd
import numpy as np

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
        """ df: (pandas.DataFrame || pandas.Series)
            Returns: (int) total sum of the matrix
        """
        return np.sum(df.as_matrix())

    @staticmethod
    def get_max_value(df):
        """ df: (pandas.DataFrame || pandas.Series)
            Returns: (int) max value of the matrix
        """
        return np.max(df.as_matrix())

    @staticmethod
    def get_min_value(df):
        """ df: (pandas.DataFrame || pandas.Series)
            Returns: (int) min value of the matrix
        """
        return np.min(df.as_matrix())

    @staticmethod
    def get_mean_value(df):
        """ df: (pandas.DataFrame || pandas.Series)
            Returns: (int) mean value of the matrix
        """
        return np.mean(df.as_matrix())

    @staticmethod
    def get_std_value(df):
        """ df: (pandas.DataFrame || pandas.Series)
            Returns: (int) std value of the matrix
        """
        return np.std(df.as_matrix())

    @staticmethod
    def sum_by_axis(df, axis):
        """ df: (Number) dataframe holding the numeric values
            axis: (int) 0 -> sum columns (up-down) ; 1 -> sum rows (left-right)
            Returns: (pandas.DataFrame) column with the added value of each axis
        """
        return pd.DataFrame(df.sum(axis))

    @staticmethod
    def max_by_axis(df, axis):
        """ df: (Number) dataframe holding the numeric values
            axis: (int) 0 -> sum columns ; 1 -> sum rows
            Returns: (pandas.DataFrame) column with max of the axis
        """
        return pd.DataFrame(df.max(axis))

    @staticmethod
    def mean_by_axis(df, axis):
        """ df: (Number) dataframe holding the numeric values
            axis: (int) 0 -> sum columns ; 1 -> sum rows
            Returns: (pandas.DataFrame) column with the mean of the axis
        """
        return pd.DataFrame(df.mean(axis))

    @staticmethod
    def std_by_axis(df, axis):
        """ df: (Number) dataframe holding the numeric values
            axis: (int) 0 -> sum columns ; 1 -> sum rows
            Returns: (pandas.DataFrame) column with the standard deviation 
                     of the axis
        """
        return pd.DataFrame(df.std(axis))

    @staticmethod
    def get_diagonal_ones_matrix(df):
        return np.diag(np.ones(len(df.columns)))

    @staticmethod
    def to_df(matrix, index=None, columns=None):
        return pd.DataFrame(matrix, index=index, columns=columns)
