"""
    Normalization Register
"""
import logging
from .feature_scaling_normalization import feature_scaling, FEATURE_SCALING_ID
from .standardized_normalization import standardized, STANDARDIZED_ID
from .centered_normalization import centered, CENTERED_ID

class NormalizationRegister(object):
    """
        Class that registers the available algorithms
    """
    LOGGER = logging.getLogger(__name__)
    # dictionary with the shape {Algorithm_id, Algorithm}
    # holding all registered algorithms
    ALGORITHM_DIC = dict({
        FEATURE_SCALING_ID: feature_scaling,
        STANDARDIZED_ID: standardized,
        CENTERED_ID: centered
        })

    @staticmethod
    def get_algorithm_dict():
        """
            Returns the dictionary of available algorithms
        """
        return NormalizationRegister.ALGORITHM_DIC
