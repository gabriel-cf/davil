"""
    Feature Scaling
"""

from __future__ import division
from ...util.df_matrix_utils import DFMatrixUtils

FEATURE_SCALING_ID = "Feature Scaling"

def feature_scaling(df, df_level=False):
    """Feature scaling normalization
       df: (pandas.DataFrame) dataframe with the values to normalize
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
