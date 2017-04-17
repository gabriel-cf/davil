"""
    Normalization controller
"""

import logging
import pandas as pd
from ....backend.algorithms.normalization.normalization_register import NormalizationRegister
from ....backend.algorithms.normalization.feature_scaling_normalization import FEATURE_SCALING_ID
from .abstract_algorithm_controller import AbstractAlgorithmController

class NormalizationController(AbstractAlgorithmController):
    """Controls the normalization applied to the values dataframe"""
    LOGGER = logging.getLogger(__name__)

    def __init__(self, algorithm_id=None):
        print "AAAAAAA"
        print NormalizationRegister.get_algorithm_dict()
        algorithm_dict = NormalizationRegister.get_algorithm_dict()
        super(NormalizationController, self).\
              __init__(FEATURE_SCALING_ID,
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
        self.update_algorithm(FEATURE_SCALING_ID)
        normalized_df = self.execute_active_algorithm(error_df, df_level=True)
        self.update_algorithm(active_algorithm_id)
        
        return normalized_df

