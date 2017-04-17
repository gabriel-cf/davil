"""
    Square Sum
"""

from .absolute_sum_error import absolute_sum

SQUARE_SUM_ID = "Square Sum"

def square_sum(values_df, vectors_df, mapped_points_df):
    """
        values_df: (pandas.DataFrame) product X dimension_value
        vectors_df: (pandas.DataFrame) dimension X v_x,v_y columns
        mapped_points_df: (pandas.DataFrame) product X x,y columns
        Returns:
            (pandas.DataFrame) product X x,y columns where each cell contains
        the error for that point on that coordenate component
            (int) square total error value

    """
    vector_error_df,\
    processed_error_df = absolute_sum(values_df, vectors_df, mapped_points_df)
    processed_error_df **= 2
    vector_error_df **= 2
    return vector_error_df, processed_error_df
