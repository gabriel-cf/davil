"""
    Mapper Controller Module
"""
from bokeh.models import ColumnDataSource
from ...backend.algorithms.mapping.dummy_mapper import DummyMapper
from ...backend.algorithms.mapping.star_mapper import StarMapper

class MapperController(object):
    """Controller that handles mapping operations
       It keeps the original dimension values and vectors and enables options
       to perform remapping by modifying particular vectors (e.g hiding an axis)
    """

    DUMMY_MAPPER_ID = 'Dummy Coordinates'
    STAR_MAPPER_ID = 'Star Coordinates'
    DEFAULT_MAPPER_ID = DUMMY_MAPPER_ID
    
    def __init__(self, dimension_values_df, vectors_df, 
                 mapping_id=DEFAULT_MAPPER_ID, animator=None):
        self._dimension_values_df = dimension_values_df
        self._vectors_df = vectors_df
        self._source_points = None
        self._ignored_axis_ids = set()
        self._mapper_id, self._mapper = self.get_mapping_algorithm(mapping_id)
        self._animator = animator
        self._last_mapped_points_df = None

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
        mapped_points = self._mapper.map_points(dimension_values_df, vectors_df)

        print "EXECUTING MAPPING"
        if not self._source_points:            
            self._source_points = ColumnDataSource(mapped_points)
            self._source_points.add(mapped_points.index, name='name') 
            if self._animator:
                self._animator.add_source_points(self._source_points)      
        else:
            if self._animator:
                self._animator.get_animation_sequence(self._last_mapped_points_df,
                                                      mapped_points)
            else:
                self._source_points.data['x'] = mapped_points['x']
                self._source_points.data['y'] = mapped_points['y']
        self._last_mapped_points_df = mapped_points
        return self._source_points

    def get_source_points(self):
        """Returns (ColumnDataSource) mapped source points"""
        return self._source_points

    def get_active_mapper_id(self):
        return self._mapper_id

    def update_vector_values(self, axis_id, x1, y1, x0=0, y0=0):
        self._vectors_df.loc[axis_id:axis_id, 'v_x'] = x1 - x0
        self._vectors_df.loc[axis_id:axis_id, 'v_y'] = y1 - y0  

    def get_mapping_algorithm(self, mapping_id):
        if mapping_id == MapperController.STAR_MAPPER_ID:
            return MapperController.STAR_MAPPER_ID, StarMapper()
        elif mapping_id == MapperController.DUMMY_MAPPER_ID:  
            return MapperController.DUMMY_MAPPER_ID, DummyMapper()            
        elif mapping_id == MapperController.DEFAULT_MAPPER_ID:            
            raise ValueError("DEFAULT_MAPPER_ID should be assigned to an existing MAPPER_ID")

        print "WARN: No valid mapper provided. Assigning default mapper "+"'{}'".format(MapperController.DEFAULT_MAPPER_ID)
        return self.get_mapping_algorithm(MapperController.DEFAULT_MAPPER_ID)  

    def update_mapping_algorithm(self, mapping_id):
        self._mapper_id, self._mapper = self.get_mapping_algorithm(mapping_id)
        # recalculate cost in animator
        #self._animator