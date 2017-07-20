"""
    Mapper Controller Module
"""
import logging
from ....backend.algorithms.mapping.mapping_register import MappingRegister
from ....backend.algorithms.mapping.star_coordinates_mapper import STAR_COORDINATES_ID
from .abstract_algorithm_controller import AbstractAlgorithmController

class MapperController(AbstractAlgorithmController):
    """Controller that handles mapping operations
       It keeps the original dimension values and vectors and enables options
       to perform remapping by modifying particular vectors (e.g hiding an axis)
    """
    LOGGER = logging.getLogger(__name__)

    def __init__(self, input_data_controller, vector_controller, normalization_controller,
                 source_points=None, mapping_id=None, animator=None):
        algorithm_dict = MappingRegister.get_algorithm_dict()
        super(MapperController, self).__init__(STAR_COORDINATES_ID,
                                               algorithm_dict,
                                               active_algorithm_id=mapping_id,
                                               none_algorithm=False)
        self._input_data_controller = input_data_controller
        self._vector_controller = vector_controller
        self._normalization_controller = normalization_controller
        self._source_points = source_points
        self._animator = animator
        self._last_mapped_points_df = None

    def execute_mapping(self):
        """Will recalculate the mapping for the points
           Returns: (pandas.DataFrame) Mapped points with shape
                    (point_name X {x, y})
        """
        # Note: under the covers these values are filtered according to the
        # ignored labels set of InputDataController
        dimension_values_df_norm = self._normalization_controller.get_last_normalized_values()
        vectors_df = self._vector_controller.get_vectors()
        MapperController.LOGGER.debug("Mapping with %s", self.get_active_algorithm_id())
        mapped_points_df = self.execute_active_algorithm(dimension_values_df_norm,
                                                         vectors_df)
        if self._animator:
            MapperController.LOGGER.debug("Executing animation")
            self._animator.get_animation_sequence(self._last_mapped_points_df,
                                                  mapped_points_df)
        self._last_mapped_points_df = mapped_points_df
        if self._source_points:
            self._update_source_points(mapped_points_df)

        return mapped_points_df

    def get_mapped_points(self):
        return self._last_mapped_points_df

    def set_animator(self, animator):
        """ animator: (MappingAnimator) animator in charge of reproducing the
            transition from the original points to the mapped ones
        """
        MapperController.LOGGER.debug("Updating animator")
        self._animator = animator

    def set_source_points(self, source_points):
        self._source_points = source_points

    def _update_source_points(self, mapped_points_df):
        self._source_points.data['x'] = mapped_points_df['x']
        self._source_points.data['y'] = mapped_points_df['y']
