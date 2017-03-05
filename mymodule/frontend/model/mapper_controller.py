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
        self._ignored_axis_ids = set()

    def update_axis_status(self, axis_id, visible):
        """Adds an ID to the list of ignored axis if not visible, remove from it
           otherwise
           axis_id: (String) ID (name) of the axis as appears in the Dataframes
        """
        if visible:
            self._ignored_axis_ids.discard(axis_id)
        else:            
            self._ignored_axis_ids.add(axis_id)

    def get_vectors(self):
        """ [self._ignored_axis_ids=None]: (List<String>) identifiers of ignored axis 
            Returs: (pandas.Dataframe) vectors dataframe
        """
        vectors_df_cp = self._vectors_df.copy()
        if self._ignored_axis_ids:
            #match indexes (axis=0)
            vectors_df_cp.drop(self._ignored_axis_ids, axis=0, inplace=True)

        return vectors_df_cp

    def get_dimension_values(self):
        """ [self._ignored_axis_ids=None]: (List<String>) identifiers of ignored axis 
            Returs: (pandas.Dataframe) dimension values dataframe
        """
        dimension_values_df_cp = self._dimension_values_df.copy()
        if self._ignored_axis_ids:
            # match columns (axis=1)
            dimension_values_df_cp.drop(self._ignored_axis_ids, axis=1, inplace=True)

        return dimension_values_df_cp

    def get_filtered_mapping_df(self,):
        """ self._ignored_axis_ids: (List<String>) identifiers of ignored axis 
            Returns: (pandas.Dataframe) filtered dimension values
                     (pandas.Dataframe) filtered vector values
        """
        return self.get_dimension_values(), self.get_vectors()

    def execute_mapping(self):
        """Will recalculate the mapping for the points"""
        dimension_values_df = self._dimension_values_df
        vectors_df = self._vectors_df
        if self._ignored_axis_ids:
          dimension_values_df, vectors_df = self.get_filtered_mapping_df()
        mapped_points = StarMapper().map_points(dimension_values_df, vectors_df)

        print "EXECUTING MAPPING"
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

    def update_vector_values(self, axis_id, x1, y1, x0=0, y0=0):
        self._vectors_df.loc[axis_id:axis_id, 'v_x'] = x1 - x0
        self._vectors_df.loc[axis_id:axis_id, 'v_y'] = y1 - y0
