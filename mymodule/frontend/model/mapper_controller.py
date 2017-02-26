"""
    Mapper Controller Module
"""

from bokeh.models import ColumnDataSource
from ...backend.model.mapper.star_mapper import StarMapper

class MapperController(object):
    """Controller that handles mapping operations
       It keeps the original dimension values and vectors and enables options
       to perform remapping by modifying particular vectors (e.g hiding an axis)
    """
    def __init__(self, dimension_values_df, vectors_df):
        self._dimension_values_df = dimension_values_df
        self._vectors_df = vectors_df
        self._source_points = None

    def get_filtered_mapping_df(self, ignored_axis_ids):
        """ ignored_axis_ids: (List<String>) identifiers of ignored axis 
            Returns: (pandas.Dataframe) filtered dimension values
                     (pandas.Dataframe) filtered vector values
        """
        # Retrieve axis IDs (names of the columns)
        dimension_values_df_cp = self._dimension_values_df.copy()
        vectors_df_cp = self._vectors_df.copy()
        # In dimension they appear as columns (axis=1) 
        # and in vectors as indexes (axis=0)
        dimension_values_df_cp.drop(ignored_axis_ids, axis=1, inplace=True)
        vectors_df_cp.drop(ignored_axis_ids, axis=0, inplace=True)

        return dimension_values_df_cp, vectors_df_cp

    def execute_mapping(self, ignored_axis_ids = None):
        """Will recalculate the mapping for the points"""
        dimension_values_df = self._dimension_values_df
        vectors_df = self._vectors_df
        if ignored_axis_ids:
          dimension_values_df, vectors_df = self.get_filtered_mapping_df(ignored_axis_ids)
        mapped_points = StarMapper().map_points(dimension_values_df, vectors_df)

        if not self._source_points:
            self._source_points = ColumnDataSource(mapped_points)
            self._source_points.add(mapped_points.index, name='name')          
        else:
            self._source_points.data['x'] = mapped_points['x']
            self._source_points.data['y'] = mapped_points['y']

        return self._source_points

    def get_source_points(self):
        """Returns (ColumnDataSource) mapped source points"""
        return self._source_points
