"""
    Clustering controller
"""
import logging
from ....backend.algorithms.error.error_register import ErrorRegister
from ....backend.algorithms.error.absolute_sum_error import ABSOLUTE_SUM_ID
from .abstract_algorithm_controller import AbstractAlgorithmController

class ErrorController(AbstractAlgorithmController):
    """Controls the error value of the points"""
    LOGGER = logging.getLogger(__name__)

    def __init__(self, normalization_controller, vector_controller, mapper_controller,
                 point_controller, axis_sources, algorithm_id=None):
        algorithm_dict = ErrorRegister.get_algorithm_dict()
        super(ErrorController, self).__init__(ABSOLUTE_SUM_ID,
                                              algorithm_dict,
                                              active_algorithm_id=algorithm_id,
                                              none_algorithm=False)
        self._normalization_controller = normalization_controller
        self._vector_controller = vector_controller
        self._mapper_controller = mapper_controller
        self._point_controller = point_controller
        self._axis_sources = axis_sources
        self._last_axis_error_s = None
        self._last_point_error_s = None
        self._last_axis_error_s_norm = None
        self._last_point_error_s_norm = None

    def calculate_error(self):
        """values_df_norm: (pandas.DataFrame) product X dimension_value
           vectors_df: (pandas.DataFrame) dimension X v_x,v_y columns
           mapped_points_df: (pandas.DataFrame) product X x,y columns
           Returns: (pandas.Series) error value for each axis
                    (pandas.Series) error value for each point
        """
        values_df_norm = self._normalization_controller.get_last_normalized_values()
        vectors_df = self._vector_controller.get_vectors()
        mapped_points_df = self._mapper_controller.get_mapped_points()
        axis_error_df, \
        point_error_df = self.execute_active_algorithm(values_df_norm,
                                                       vectors_df,
                                                       mapped_points_df)
        # Normalize the error values at DataFrame level (i.e. comparing all matrix values)
        self._last_axis_error_s_norm = self._normalization_controller\
                                        .normalize_feature_scaling(axis_error_df, df_level=True)[0]
        self._last_point_error_s_norm = self._normalization_controller\
                                        .normalize_feature_scaling(point_error_df, df_level=True)[0]

        point_error_s = point_error_df[0]
        axis_error_s = axis_error_df[0]
        self._point_controller.update_errors(point_error_s)
        # Go through the axis sources and update (or initialize) the error
        # Note: every axis has its own source
        for i in xrange(0, len(self._axis_sources)):
            axis_id = self._axis_sources[i].data['name'][0]
            if not axis_id in axis_error_df.index:
                continue
            new_value = axis_error_df.at[axis_id, 0]
            if not 'error' in self._axis_sources[i].data:
                self._axis_sources[i].data['error'] = [new_value]
            else:
                patch_error = {
                    # Assigned as: (indexToReplace, newValue)
                    'error': [(0, new_value)]
                }
                self._axis_sources[i].patch(patch_error)

        self._last_axis_error_s = axis_error_s
        self._last_point_error_s = point_error_s
        return axis_error_s, point_error_s

    def get_last_axis_error(self, normalized=False):
        """Returns (pandas.Series) last calculated error value for each axis"""
        last_axis_error = self._last_axis_error_s
        if normalized:
            last_axis_error = self._last_axis_error_s_norm

        if last_axis_error is None or last_axis_error.empty:
            ErrorController.LOGGER.warn("Attempted to retrieve the latest axis error \
                   calculation but there is none")
        return last_axis_error

    def get_last_point_error(self, normalized=False):
        """Returns (pandas.Series) last calculated error value for each point"""
        last_point_error = self._last_axis_error_s
        if normalized:
            last_point_error = self._last_point_error_s_norm

        if last_point_error is None or last_point_error.empty:
            ErrorController.LOGGER.warn("Attempted to retrieve the latest point error \
                   calculation but there is none")
        return last_point_error
