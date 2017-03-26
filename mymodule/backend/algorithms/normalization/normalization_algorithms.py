"""
    Normalization methods
"""
from __future__ import division
from ...util.df_matrix_utils import DFMatrixUtils

def _normalize_column(column, max_df_value=None):
    """method for the pandas.DataFrame.apply() function
       Normalize taking the maximum value as reference
       column: (pandas.Series) column to be normalized
       [max_df_value=None]: (int) global maximum value
    """
    column_norm = []
    for x in column:
        max_value = max_df_value if max_df_value else max(column)
        # Check for infinite divisions
        if max_value == 0:
            column_norm.append(0)
        else:
            column_norm.append(x / max_value)                    

    return column_norm

class NormalizationAlgorithms(object):
    """Algorithms to normalize pandas.DataFrame objects"""

    @staticmethod
    def max_per_column(df, inplace=False):
        if not inplace:
            df = df.copy()
        df = df.apply(lambda column: _normalize_column(column), axis=0)

        return df

    @staticmethod
    def max_per_dataframe(df, inplace=False):
        if not inplace:
            df = df.copy()
        max_df_value = DFMatrixUtils.get_max_value(df)
        df = df.apply(lambda column: _normalize_column(column, max_df_value=max_df_value), axis=0)
        return df
