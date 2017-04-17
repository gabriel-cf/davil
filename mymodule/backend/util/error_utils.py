"""
    ErrorUtils
"""

class ErrorUtils(object):
    """Class holding common utils for error algorithms"""
    
    @staticmethod
    def get_general_error_df(values_df, vectors_df, mapped_points_df):
        """ 
            values_df: (pandas.DataFrame) product X dimension_value
            vectors_df: (pandas.DataFrame) dimension X v_x,v_y columns
            mapped_points_df: (pandas.DataFrame) product X x,y columns
            Returns: (pandas.DataFrame) product X x,y columns where each cell contains
            the absolute error value for that point on that coordenate component
        """
        def get_column_error(column, vectors_df, mapped_points_df_t):
            column_expected_x = (column * vectors_df['x']).abs()
            column_expected_y = (column * vectors_df['y']).abs()
            column_index = column.name
            column_mapped_x = mapped_points_df_t[column_index]['x']
            column_mapped_y = mapped_points_df_t[column_index]['y']
            column_error_x = (column_expected_x - column_mapped_x).abs()
            column_error_y = (column_expected_y - column_mapped_y).abs()
            column_error = column_error_x + column_error_y
            return column_error

        values_df_t_cp = values_df.transpose()
        mapped_points_df_t = mapped_points_df.transpose()
        # Avoid duplicated names assigning new column IDs
        column_ids = [i for i in xrange(0, len(values_df_t_cp.columns))]
        values_df_t_cp.columns = column_ids
        mapped_points_df_t.columns = column_ids
        values_df_t_cp = values_df_t_cp.apply(lambda column: get_column_error(column, vectors_df, mapped_points_df_t), axis=0)
        general_error_df = values_df_t_cp.transpose()
        return general_error_df
