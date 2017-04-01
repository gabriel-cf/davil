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

    def __init__(self, point_source, axis_sources, algorithm_id=None):
        algorithm_dict = ErrorController._get_algorithm_dict()
        super(ErrorController, self).__init__(ErrorController.DEFAULT_ALGORITHM_ID,
                                              algorithm_dict,
                                              active_algorithm_id=algorithm_id)
        self._point_source = point_source
        self._axis_sources = axis_sources

    def calculate_error(self, values_df, vectors_df, mapped_points_df, normalized=True):
        """dimension_values_df: (pandas.Dataframe) values of the points
           algorithm: (String) cluster algorithm id
        """
        axis_error_df, \
        point_error_df = super(ErrorController, self)\
                              .execute_active_algorithm(values_df,
                                                        vectors_df,
                                                        mapped_points_df)
        if normalized:
            axis_error_df = NormalizationAlgorithms.max_per_dataframe(axis_error_df)
            point_error_df = NormalizationAlgorithms.max_per_dataframe(point_error_df)

        self._point_source.data['error'] = point_error_df[0]
        for i in xrange(0, len(self._axis_sources)):
            if not 'error' in self._axis_sources[i].data:
                self._axis_sources[i].data['error'] = [axis_error_df[0][i]]
            else:
                patch_error = {
                    'error': [(0, axis_error_df[0][i])]
                }
                self._axis_sources[i].patch(patch_error)

        return axis_error_df, point_error_df
