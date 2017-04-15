"""
    Clustering controller
"""

from ....backend.algorithms.error.error_algorithms import ErrorAlgorithms
from ....backend.algorithms.normalization.normalization_algorithms import NormalizationAlgorithms
from generic_algorithm_controller import GenericAlgorithmController

class ErrorController(GenericAlgorithmController):
    """Controls the clustering of the values for the values dataframe"""
    ABSOLUTE_SUM_ID = "Absolute sum"
    SQUARE_SUM_ID = "Square sum"
    MAXIMUM_ID = "Maximum value"
    DEFAULT_ALGORITHM_ID = ABSOLUTE_SUM_ID

    @staticmethod
    def _get_algorithm_dict():
        """Returns a dictionary with the shape {Algorithm_id, Algorithm}"""
        algorithm_dict = dict()
        algorithm_dict[ErrorController.ABSOLUTE_SUM_ID] = ErrorAlgorithms.abs_sum
        algorithm_dict[ErrorController.SQUARE_SUM_ID] = ErrorAlgorithms.square_sum
        algorithm_dict[ErrorController.MAXIMUM_ID] = ErrorAlgorithms.max_error
        return algorithm_dict

    def __init__(self, point_source, axis_sources, normalization_controller,
                 algorithm_id=None):
        algorithm_dict = ErrorController._get_algorithm_dict()
        super(ErrorController, self).__init__(ErrorController.DEFAULT_ALGORITHM_ID,
                                              algorithm_dict,
                                              active_algorithm_id=algorithm_id)
        self._point_source = point_source
        self._axis_sources = axis_sources
        self._normalization_controller = normalization_controller
        self._last_axis_error_s = None
        self._last_point_error_s = None

    def calculate_error(self, values_df, vectors_df, mapped_points_df):
        """values_df: (pandas.DataFrame) product X dimension_value
           vectors_df: (pandas.DataFrame) dimension X v_x,v_y columns
           mapped_points_df: (pandas.DataFrame) product X x,y columns
           Returns: (pandas.Series) error value for each axis
                    (pandas.Series) error value for each point
        """
        axis_error_df, \
        point_error_df = self.execute_active_algorithm(values_df,
                                                       vectors_df,
                                                       mapped_points_df)
        # Normalize the error values at DataFrame level (i.e. comparing all matrix values)
        axis_error_df = self._normalization_controller.normalize_errors(axis_error_df)
        point_error_df = self._normalization_controller.normalize_errors(point_error_df)

        point_error_s = point_error_df[0]
        axis_error_s = axis_error_df[0]
        self._point_source.data['error'] = point_error_s
        # Go through the axis sources and update (or initialize) the error
        # Note: every axis has its own source
        for i in xrange(0, len(self._axis_sources)):
            if not 'error' in self._axis_sources[i].data:
                self._axis_sources[i].data['error'] = [axis_error_s[i]]
            else:
                patch_error = {
                    # Assigned as: (indexToReplace, newValue)
                    'error': [(0, axis_error_s[i])]
                }
                self._axis_sources[i].patch(patch_error)

        self._last_axis_error_s = axis_error_s
        self._last_point_error_s = point_error_s
        return axis_error_s, point_error_s

    def get_last_axis_error(self):
        """Returns (pandas.Series) last calculated error value for each axis"""
        if self._last_axis_error_s is None or self._last_axis_error_s.empty:
            print "WARN: Attempted to retrieve the latest axis error \
                   calculation but there is none"
        return self._last_axis_error_s

    def get_last_point_error(self):
        """Returns (pandas.Series) last calculated error value for each point"""
        if self._last_point_error_s is None or self._last_point_error_s.empty:
            print "WARN: Attempted to retrieve the latest point error \
                   calculation but there is none"
        return self._last_point_error_s
