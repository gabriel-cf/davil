"""
    Normalization methods
"""
from __future__ import division
from ...util.df_matrix_utils import DFMatrixUtils

class NormalizationAlgorithms(object):
    """Algorithms to normalize pandas.DataFrame objects"""

    @staticmethod
    def feature_scaling(df, df_level=False):
        """Feature scaling normalization
           df: (pandas.DataFrame) dataframe with the values to normalize
           [maximum=None]: (Number) Maximum value
           [minimum=None]: (Number) Minimum value
           [df_level=False]: (Boolean) Whether values maximum/minimum
           should be taken from dataframe or column level
        """
        def _normalize_column(column, maximum=None, minimum=None):
            def _normalize_value(x, maximum, minimum):
                diff = maximum - minimum
                if diff < 0:
                    return 0
                elif diff == 0:
                    return 1
                res = (x - minimum) / diff
                return 1 if res > 1 else res

            maximum = maximum if maximum else max(column)
            minimum = minimum if minimum else min(column)
            return [_normalize_value(x, maximum, minimum) for x in column]

        maximum = None
        minimum = None
        if df_level:
            maximum = DFMatrixUtils.get_max_value(df)
            minimum = DFMatrixUtils.get_min_value(df)

        df = df.apply(lambda column: _normalize_column(column,
                                                       maximum=maximum,
                                                       minimum=minimum), axis=0)
        return df

    @staticmethod
    def centered(df, df_level=False):
        """ Will normalize the DataFrame according to their mean and
            maximum and minimum values by substracting the mean.
            df: (pandas.DataFrame) dataframe with the values to normalize
            [df_level=False]: (Boolean) Whether values maximum/minimum/mean
            should be taken from dataframe or column level
        """
        def _normalize_column(column, maximum=None, minimum=None, mean=None):
            def _normalize_value(x, maximum=None, minimum=None, mean=None):
                diff = maximum - minimum
                if diff < 0:
                    return 0
                elif diff == 0:
                    return 1
                res = (x - mean) / diff
                return 1 if res > 1 else res

            maximum = maximum if maximum else max(column)
            minimum = minimum if minimum else min(column)
            mean = mean if mean else DFMatrixUtils.get_mean_value(column)
            normalized = [_normalize_value(x, maximum, minimum, mean) for x in column]
            return normalized

        maximum = None
        minimum = None
        df_mean = None
        if df_level:
            maximum = DFMatrixUtils.get_max_value(df)
            minimum = DFMatrixUtils.get_min_value(df)
            df_mean = DFMatrixUtils.get_mean_value(df)

        df = df.apply(lambda column: _normalize_column(column,
                                                       maximum=maximum,
                                                       minimum=minimum,
                                                       mean=df_mean), axis=0)
        return df

    @staticmethod
    def standardized(df, df_level=False):
        """ Will normalize the DataFrame according to their mean and
            standard deviation. This makes the normalized values to
            have variance and standard deviation.
            df: (pandas.DataFrame) dataframe with the values to normalize
            [df_level=False]: (Boolean) Whether values mean/std
            should be taken from dataframe or column level
        """
        def _normalize_column(column, mean=None, std=None):
            def _normalize_value(x, mean, std):
                return (x - mean) / std

            mean = mean if mean else DFMatrixUtils.get_mean_value(column)
            std = std if std else DFMatrixUtils.get_std_value(column)
            normalized = [_normalize_value(x, mean, std) for x in column]
            return normalized

        df_mean = None
        df_std = None
        if df_level:
            df_mean = DFMatrixUtils.get_mean_value(df)
            df_std = DFMatrixUtils.get_std_value(df)

        df = df.apply(lambda column: _normalize_column(column,
                                                       mean=df_mean,
                                                       std=df_std), axis=0)
        return df    
