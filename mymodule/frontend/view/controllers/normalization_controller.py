"""
    Normalization controller
"""

import logging
from collections import Counter
from ....backend.algorithms.normalization.normalization_register import NormalizationRegister
from ....backend.algorithms.normalization.feature_scaling_normalization import FEATURE_SCALING_ID
from .abstract_algorithm_controller import AbstractAlgorithmController

class NormalizationController(AbstractAlgorithmController):
    """Controls the normalization applied to the values dataframe"""
    LOGGER = logging.getLogger(__name__)

    def __init__(self, input_data_controller, algorithm_id=None):
        algorithm_dict = NormalizationRegister.get_algorithm_dict()
        self._input_data_controller = input_data_controller
        super(NormalizationController, self).\
              __init__(FEATURE_SCALING_ID,
                       algorithm_dict,
                       active_algorithm_id=algorithm_id,
                       none_algorithm=False)
        self._last_normalized_values_df = None

    def execute_normalization(self):
        """[df_level=False]: (Boolean) Whether values maximum/minimum"""
        NormalizationController.LOGGER.debug("Normalizing values using %s",
                                             self.get_active_algorithm_id())
        values_df = self._input_data_controller.get_dimensional_values()
        normalized_df = self.execute_active_algorithm(values_df,
                                                      df_level=False)
        self._last_normalized_values_df = normalized_df
        return normalized_df

    def get_last_normalized_values(self):
        if self._should_update_last_values():
            self.execute_normalization()
        return self._last_normalized_values_df

    def normalize_feature_scaling(self, df, df_level=False):
        """Use Feature Scaling to get the values normalized between [0,1]
           This method is oriented to controllers that should not deal with the
           active algorithm
        """
        # We swap temporaly to feature scaling and use it for the normalization
        active_algorithm_id = self.get_active_algorithm_id()
        self.update_algorithm(FEATURE_SCALING_ID)
        normalized_df = self.execute_active_algorithm(df, df_level=df_level)
        self.update_algorithm(active_algorithm_id)

        return normalized_df

    def _should_update_last_values(self):
        """Returns: (Boolean) True if the last normalized DataFrame labels differ
           from those of the filtered dimensional labels
        """
        if self._last_normalized_values_df is None:
            return True
        # Compare if the filtered labels have exactly the same elements
        # as the last normalized DataFrame
        return Counter(self._input_data_controller.get_dimensional_labels(filtered=True))\
                != Counter(self._last_normalized_values_df.columns.values.tolist())
         