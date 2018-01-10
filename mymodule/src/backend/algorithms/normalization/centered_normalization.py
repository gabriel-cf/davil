"""
    Centered
"""

from __future__ import division
from ...util.df_matrix_utils import DFMatrixUtils

CENTERED_ID = "Centered"

def centered(df, df_level=False):
    """ Will normalize the DataFrame according to their mean and
        maximum and minimum values by substracting the mean.
        df: (pandas.DataFrame) any dataframe of numeric values to normalize
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
