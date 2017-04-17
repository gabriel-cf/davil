"""
    Standardized
"""

from __future__ import division
from ...util.df_matrix_utils import DFMatrixUtils

STANDARDIZED_ID = "Standardized"

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
