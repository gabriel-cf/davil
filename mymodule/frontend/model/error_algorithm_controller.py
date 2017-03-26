""" 
    Clustering controller
"""

from ...backend.algorithms.error.error_algorithms import ErrorAlgorithms
from ...backend.algorithms.normalization.normalization_algorithms import NormalizationAlgorithms

class ErrorAlgorithmController():
    """Controls the clustering of the values for the values dataframe"""

    ABSOLUTE_SUM_ID = "Absolute sum"
    SQUARE_SUM_ID = "Square sum"    
    MAXIMUM_ID = "Maximum value"
    DEFAULT_ALGORITHM_ID = ABSOLUTE_SUM_ID

    def __init__(self, point_source, axis_sources, algorithm_id=None):
        self._point_source = point_source
        self.update_error_algorithm(algorithm_id)
        self._axis_sources = axis_sources

    def update_error_algorithm(self, algorithm_id):
        """Updates the algorithm to the one matching the given ID or default
           if no match is possible
        """
        self._algorithm_id, self._algorithm = self.get_error_algorithm(algorithm_id)

    def calculate_error(self, values_df, vectors_df, mapped_points_df, normalized=True):
        """dimension_values_df: (pandas.Dataframe) values of the points
           algorithm: (String) cluster algorithm id
        """
        axis_error_df, point_error_df = self._algorithm(values_df, vectors_df, mapped_points_df)

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

    def get_error_algorithm(self, mapping_id):
        if mapping_id == ErrorAlgorithmController.ABSOLUTE_SUM_ID:
            return ErrorAlgorithmController.ABSOLUTE_SUM_ID, ErrorAlgorithms.abs_sum
        elif mapping_id == ErrorAlgorithmController.SQUARE_SUM_ID:
            return ErrorAlgorithmController.SQUARE_SUM_ID, ErrorAlgorithms.square_sum
        elif mapping_id == ErrorAlgorithmController.MAXIMUM_ID:
            return ErrorAlgorithmController.MAXIMUM_ID, ErrorAlgorithms.max_error
        elif mapping_id == ErrorAlgorithmController.DEFAULT_ALGORITHM_ID:            
            raise ValueError("DEFAULT_ALGORITHM_ID should be assigned to an existing CLUSTERING_ID")

        print "WARN: No valid error algorithm provided. Assigning default error algorithm "+"'{}'".format(ErrorAlgorithmController.DEFAULT_ALGORITHM_ID)
        return self.get_error_algorithm(ErrorAlgorithmController.DEFAULT_ALGORITHM_ID)

    def get_active_algorithm_id(self):
        return self._algorithm_id

    def get_all_options(self):
        return [ErrorAlgorithmController.ABSOLUTE_SUM_ID, 
                ErrorAlgorithmController.SQUARE_SUM_ID,
                ErrorAlgorithmController.MAXIMUM_ID]
