"""
    Clustering controller
"""
import logging
from ....backend.algorithms.clustering.clustering_register import ClusteringRegister
from ....backend.algorithms.clustering.dummy_clustering import DUMMY_ID
from .abstract_algorithm_controller import AbstractAlgorithmController

class ClusterController(AbstractAlgorithmController):
    """Controls the clustering of the values for the values dataframe"""
    LOGGER = logging.getLogger(__name__)

    def __init__(self, normalization_controller, algorithm_id=None, n_clusters=3):
        algorithm_dict = ClusteringRegister.get_algorithm_dict()
        super(ClusterController, self).\
              __init__(DUMMY_ID,
                       algorithm_dict,
                       active_algorithm_id=algorithm_id,
                       none_algorithm=True)
        self._normalization_controller = normalization_controller
        self._clustering_dic = dict()
        self._n_clusters = n_clusters

    def execute_clustering(self):
        """dimension_values_df_norm: (pandas.Dataframe) values of the points
        """
        if not self.has_active_algorithm():
            ClusterController.LOGGER.warn("Could not execute clustering because "
                                          "there is no active algorithm")
            return
        dimension_values_df_norm = self._normalization_controller.get_last_normalized_values()
        algorithm_id = self.get_active_algorithm_id()
        categories = None
        pair_key = (algorithm_id, self._n_clusters)
        if pair_key in self._clustering_dic:
            categories = self._clustering_dic[pair_key]
        else:
            categories = self.execute_active_algorithm(dimension_values_df_norm,
                                                       n_clusters=self._n_clusters)
            self._clustering_dic[pair_key] = categories

    def update_number_of_clusters(self, n_clusters):
        if n_clusters < 3:
            raise ValueError('The number of clusters must be greater than 2.\
                             Received {}'.format(n_clusters))
        self._n_clusters = n_clusters

    def get_number_of_clusters(self):
        return self._n_clusters

    def get_categories(self):        
        active_algorithm_id = self.get_active_algorithm_id() 
        pair_key = (active_algorithm_id, self._n_clusters)
        if not pair_key in self._clustering_dic:
            ClusterController.LOGGER.warn("""No categories were found for pair
                                             (%s, %s)""", active_algorithm_id,
                                             self._n_clusters)
            return []
        categories = self._clustering_dic[pair_key]
        # Return a copy
        return categories[:]
