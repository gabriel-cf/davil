"""
    Mapper Controller Module
"""
from bokeh.models import ColumnDataSource
from ....backend.algorithms.mapping.dummy_mapper import DummyMapper
from ....backend.algorithms.mapping.star_mapper import StarMapper
from generic_algorithm_controller import GenericAlgorithmController

class MapperController(GenericAlgorithmController):
    """Controller that handles mapping operations
       It keeps the original dimension values and vectors and enables options
       to perform remapping by modifying particular vectors (e.g hiding an axis)
    """

    DUMMY_MAPPER_ID = 'Dummy Coordinates'
    STAR_MAPPER_ID = 'Star Coordinates'
    DEFAULT_MAPPER_ID = DUMMY_MAPPER_ID

    @staticmethod
    def _get_algorithm_dict():
        """Returns a dictionary with the shape {Algorithm_id, Algorithm}"""
        algorithm_dict = dict()
        algorithm_dict[MapperController.STAR_MAPPER_ID] = StarMapper.map_points
        algorithm_dict[MapperController.DUMMY_MAPPER_ID] = DummyMapper.map_points
        return algorithm_dict

    def __init__(self, dimension_values_df, vectors_df, source_points=None,
                 mapping_id=DEFAULT_MAPPER_ID, animator=None):
        algorithm_dict = MapperController._get_algorithm_dict()
        super(MapperController, self).__init__(MapperController.DEFAULT_MAPPER_ID,
                                               algorithm_dict,
                                               active_algorithm_id=mapping_id)
        self._dimension_values_df = dimension_values_df
        self._vectors_df = vectors_df
        self._source_points = source_points
        self._animator = animator
        self._last_mapped_points_df = None
        self._ignored_axis_ids = set()

    def update_axis_status(self, axis_id, visible):
        """Adds an ID to the list of ignored axis if not visible, remove from it
           otherwise
           axis_id: (String) ID (name) of the axis as appears in the Dataframes
           visible: (Boolean) self explanatory
        """
        if visible:
            self._ignored_axis_ids.discard(axis_id)
        else:
            self._ignored_axis_ids.add(axis_id)

    def is_axis_visible(self, axis_id):
        return not axis_id in self._ignored_axis_ids

    def get_axis_status(self):
        """Returns: list of tuples (axis_id, visible) generated from the
           correlation between the vectors dataframe' index and the
           ignored_axis_ids set
        """
        return [(axis_id, self.is_axis_visible(axis_id)) \
                for axis_id in self._vectors_df.index.tolist()]

    def get_vectors(self):
        """ Will get the vectors filtered if there are any ignored axis
            Returns: (pandas.Dataframe) copied and possibly filtered
                     vectors dataframe
        """
        vectors_df_cp = self._vectors_df.copy()
        if self._ignored_axis_ids:
            #Will match indexes (axis=0)
            vectors_df_cp.drop(self._ignored_axis_ids, axis=0, inplace=True)

        return vectors_df_cp

    def get_dimension_values(self):
        """ Will get the dimension values filtered if there are any ignored axis
            Returns: (pandas.Dataframe) copied and possibly filtered
                     dimension values dataframe
        """
        dimension_values_df_cp = self._dimension_values_df.copy()
        if self._ignored_axis_ids:
            #Will match columns (axis=1)
            dimension_values_df_cp.drop(self._ignored_axis_ids, axis=1, inplace=True)

        return dimension_values_df_cp

    def get_filtered_mapping_df(self):
        """Returns: (pandas.Dataframe) copied and filtered dimension values
                    (pandas.Dataframe) copied and filtered vector values
        """
        return self.get_dimension_values(), self.get_vectors()

    def execute_mapping(self):
        """Will recalculate the mapping for the points
           Returns: (pandas.DataFrame) Mapped points with shape
                    (point_name X {x, y})
        """
        print "MAPPING WITH {}".format(self.get_active_algorithm_id())
        dimension_values_df = self._dimension_values_df
        vectors_df = self._vectors_df
        if self._ignored_axis_ids:
            dimension_values_df, vectors_df = self.get_filtered_mapping_df()
        mapped_points_df = self.execute_active_algorithm(dimension_values_df, 
                                                         vectors_df)

        if self._animator:
            self._animator.get_animation_sequence(self._last_mapped_points_df,
                                                  mapped_points_df)
        elif self._source_points:
            self._source_points.data['x'] = mapped_points_df['x']
            self._source_points.data['y'] = mapped_points_df['y']

        self._last_mapped_points_df = mapped_points_df
        return mapped_points_df

    def get_mapped_points(self):
        """Returns (pandas.DataFrame) last calculated mapped points"""
        return self._last_mapped_points_df

    def update_dimension_values(self, dimension_values_df):
        self._dimension_values_df = dimension_values_df

    def update_vector_values(self, axis_id, x1, y1):
        """Updates the vectors dataframe with the new coordinates 
           Typically used when an axis is resized
           axis_id: (String) self explanatory
           x1: (int) self explanatory
           y1: (int) self explanatory
        """
        # We assume that all axis start from the point (0,0)
        # Hence, all vectors are (x1 - 0), (y1 - 0)
        self._vectors_df.loc[axis_id:axis_id, 'x'] = x1
        self._vectors_df.loc[axis_id:axis_id, 'y'] = y1

    def update_animator(self, animator):
        """ animator: (MappingAnimator) animator in charge of reproducing the
            transition from the original points to the mapped ones

        """
        self._animator = animator
