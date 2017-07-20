"""
    Square Sum
"""

from .absolute_sum_error import absolute_sum

SQUARE_SUM_ID = "Square Sum"

def square_sum(values_df, vectors_df, mapped_points_df):
    """
        values_df: (pandas.DataFrame) product_id X dimensional_values
        vectors_df: (pandas.DataFrame) dimension_id X v_x,v_y columns
        mapped_points_df: (pandas.DataFrame) product_id X x,y columns
        Returns:
            (pandas.DataFrame) product_id X x,y columns where each cell contains
                the max error error for that point on the specific coordinate
            (pandas.DataFrame) vector_id X single column holding square errors
    """
    # TODO gchicafernandez - Square Sum is not abs(X)^2. Needs to be reimplemented
    vector_error_df,\
    processed_error_df = absolute_sum(values_df, vectors_df, mapped_points_df)
    processed_error_df **= 2
    vector_error_df **= 2
    return vector_error_df, processed_error_df
