"""
    Clustering Register
"""

import logging
from .dummy_clustering import dummy, DUMMY_ID
from .kmeans_clustering import kmeans, KMEANS_ID

class ClusteringRegister(object):
    """
        Class that registers the available algorithms
    """
    LOGGER = logging.getLogger(__name__)
    # dictionary with the shape {Algorithm_id, Algorithm} 
    # holding all registered algorithms
    ALGORITHM_DIC = dict({
        DUMMY_ID: dummy,
        KMEANS_ID: kmeans
        })

    @staticmethod
    def get_algorithm_dict():
        """
            Returns the dictionary of available algorithms
        """
        return ClusteringRegister.ALGORITHM_DIC
