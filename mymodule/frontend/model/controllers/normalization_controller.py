"""
    Normalization controller
"""

import logging
import pandas as pd
from ....backend.algorithms.normalization.normalization_algorithms import NormalizationAlgorithms
from ....backend.algorithms.clustering.dummy_clustering import DummyClustering
from generic_algorithm_controller import GenericAlgorithmController

class NormalizationController(GenericAlgorithmController):
    """Controls the normalization applied to the values dataframe"""
    LOGGER = logging.getLogger(__name__)
    FEATURE_SCALING_NORMALIZATION_ID = "Feature Scaling"
    STANDARDIZED_NORMALIZATION_ID = "Standardization"
    CENTERED_NORMALIZATION_ID = "Centered"
    DEFAULT_NORMALIZATION_ID = FEATURE_SCALING_NORMALIZATION_ID
    ###

    @staticmethod
    def _get_algorithm_dict():
        """Returns a dictionary with the shape {Algorithm_id, Algorithm}"""
        algorithm_dict = dict()
        algorithm_dict[NormalizationController.FEATURE_SCALING_NORMALIZATION_ID]\
            = NormalizationAlgorithms.feature_scaling
        algorithm_dict[NormalizationController.STANDARDIZED_NORMALIZATION_ID] \
            = NormalizationAlgorithms.standardized
        algorithm_dict[NormalizationController.CENTERED_NORMALIZATION_ID] \
            = NormalizationAlgorithms.centered
        return algorithm_dict

    def __init__(self, algorithm_id=None):
        algorithm_dict = NormalizationController._get_algorithm_dict()
        super(NormalizationController, self).\
              __init__(NormalizationController.DEFAULT_NORMALIZATION_ID,
                       algorithm_dict,
                       active_algorithm_id=algorithm_id)
        self._last_normalized_df = None

    def normalize(self, values_df, df_level=False):
        """values_df: (pandas.Dataframe)
           [df_level=False]: (Boolean) Whether values maximum/minimum
        """
        NormalizationController.LOGGER.debug("Normalizing values using %s",
                                             self.get_active_algorithm_id())
        normalized_df = self.execute_active_algorithm(values_df,
                                                      df_level=df_level)
        return normalized_df

    def normalize_errors(self, error_df):
        # We swap temporaly to feature scaling and use it for the normalization
        active_algorithm_id = self.get_active_algorithm_id()
        self.update_algorithm(NormalizationController.FEATURE_SCALING_NORMALIZATION_ID)
        normalized_df = self.execute_active_algorithm(error_df, df_level=True)
        self.update_algorithm(active_algorithm_id)
        
        return normalized_df

