"""
    Absolute Sum Error
"""

from ...util.df_matrix_utils import DFMatrixUtils
from ...util.error_utils import ErrorUtils

ABSOLUTE_SUM_ID = "Absolute Sum"

def absolute_sum(values_df, vectors_df, mapped_points_df):
    """
        values_df: (pandas.DataFrame) product X dimension_value
        vectors_df: (pandas.DataFrame) dimension X v_x,v_y columns
        mapped_points_df: (pandas.DataFrame) product X x,y columns
        Returns:
            (pandas.DataFrame) product X x,y columns where each cell contains
                the error for that point on that coordenate component
            (pandas.DataFrame) vector X error
    """
    general_error_df = ErrorUtils.get_general_error_df(values_df, vectors_df, mapped_points_df)
    processed_error_df = DFMatrixUtils.sum_by_axis(general_error_df, 1)
    vector_error_df = DFMatrixUtils.sum_by_axis(general_error_df, 0)
    return vector_error_df, processed_error_df
