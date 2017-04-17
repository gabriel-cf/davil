"""
    Classification Register
"""

import logging
from .lda_classification import lda, LDA_ID
from .pca_classification import pca, PCA_ID

class ClassificationRegister(object):
    """
        Class that registers the available algorithms
    """
    LOGGER = logging.getLogger(__name__)
    # dictionary with the shape {Algorithm_id, Algorithm} 
    # holding all registered algorithms
    ALGORITHM_DIC = dict({
        LDA_ID: lda,
        PCA_ID: pca
        })

    @staticmethod
    def register_algorithm(algorithm_id, algorithm):
        ClassificationRegister.LOGGER.debug("Registering algorithm '%s'", algorithm_id)
        ClassificationRegister.ALGORITHM_DIC[algorithm_id] = algorithm

    @staticmethod
    def get_algorithm_dict():
        """
            Returns the dictionary of available algorithms
        """
        return ClassificationRegister.ALGORITHM_DIC
