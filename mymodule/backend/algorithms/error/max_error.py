"""
    Max Error
"""

from ...util.df_matrix_utils import DFMatrixUtils
from ...util.error_utils import ErrorUtils

MAX_ERROR_ID = "Max Error"

def max_error(values_df, vectors_df, mapped_points_df):
    """
        values_df: (pandas.DataFrame) product_id X dimensional_values
        vectors_df: (pandas.DataFrame) dimension_id X v_x,v_y columns
        mapped_points_df: (pandas.DataFrame) product_id X x,y columns
        Returns:
            (pandas.DataFrame) product_id X x,y columns where each cell contains
                the max error error for that point on the specific coordinate
            (pandas.DataFrame) vector_id X single column holding max errors
    """
    general_error_df = ErrorUtils.get_general_error_df(values_df, vectors_df, mapped_points_df)
    processed_error_df = DFMatrixUtils.max_by_axis(general_error_df, 1)
    vector_error_df = DFMatrixUtils.max_by_axis(general_error_df, 0)
    return vector_error_df, processed_error_df
