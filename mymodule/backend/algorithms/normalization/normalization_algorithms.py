"""
    Normalization methods
"""
from __future__ import division
from ...util.df_matrix_utils import DFMatrixUtils

class NormalizationAlgorithms(object):
    """Algorithms to normalize pandas.DataFrame objects"""

    @staticmethod
    def feature_scaling(x, xmax, xmin):
        """Feature scaling normalization
           x: (Number) Value to normalize
           xmax: (Number) Maximum value
           xmin: (Number) Minimum value
        """
        diff = xmax - xmin
        if diff < 0:
            return 0
        elif diff == 0:
            return 1
        res = (x - xmin) / diff
        return 1 if res > 1 else res

    @staticmethod
    def normalize_column(column, algorithm, minimum=None, maximum=None):
        """ Normalizes the column values.
            column: (Iterable) column to be normalized
            [min=None]: (int) predefined minimum value
            [max=None]: (int) predefined maximum value
        """
        max_value = maximum if maximum else max(column)
        min_value = minimum if minimum else min(column)
        return [algorithm(x, max_value, min_value) for x in column]

    @staticmethod
    def max_per_column(df, inplace=False):
        if not inplace:
            df = df.copy()
        df = df.apply(lambda column: NormalizationAlgorithms\
                                    .normalize_column(column, 
                                                      NormalizationAlgorithms.feature_scaling),
                                                      axis=0)
        return df

    @staticmethod
    def max_per_dataframe(df, inplace=False):
        if not inplace:
            df = df.copy()
        max_df_value = DFMatrixUtils.get_max_value(df)
        min_df_value = DFMatrixUtils.get_min_value(df)
        df = df.apply(lambda column: NormalizationAlgorithms\
                                     .normalize_column(column,
                                                       NormalizationAlgorithms.feature_scaling,
                                                       maximum=max_df_value,
                                                       minimum=min_df_value),
                      axis=0)
        return df
