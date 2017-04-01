"""
    Clustering controller
"""

import pandas as pd
from ....backend.algorithms.clustering.kmeans_clustering import KMeansClustering
from ....backend.algorithms.clustering.dummy_clustering import DummyClustering
from generic_algorithm_controller import GenericAlgorithmController

class ClusterController(GenericAlgorithmController):
    """Controls the clustering of the values for the values dataframe"""

    DUMMY_CLUSTERING_ID = "Dummy Clustering"
    KMEANS_CLUSTERING_ID = "K-Means Clustering"
    DEFAULT_CLUSTERING_ID = DUMMY_CLUSTERING_ID
    CLUSTERING_COLOR_COLUMN = 'color'
    DEFAULT_LABEL_COLORS = ["red", "navy", "green", "orange", "grey"]

    @staticmethod
    def _get_algorithm_dict():
        """Returns a dictionary with the shape {Algorithm_id, Algorithm}"""
        algorithm_dict = dict()
        algorithm_dict[ClusterController.KMEANS_CLUSTERING_ID] \
            = KMeansClustering.categorize_values
        algorithm_dict[ClusterController.DUMMY_CLUSTERING_ID] \
            = DummyClustering.categorize_values
        return algorithm_dict

    def __init__(self, algorithm_id=None, source=None, label_colors=None):
        algorithm_dict = ClusterController._get_algorithm_dict()
        super(ClusterController, self).\
              __init__(ClusterController.DEFAULT_CLUSTERING_ID,
                       algorithm_dict,
                       active_algorithm_id=algorithm_id)
        self._clustering_dic = dict()
        self._label_colors = label_colors
        if not self._label_colors:
            self._label_colors = ClusterController.DEFAULT_LABEL_COLORS
        self._source = source

    def update_clusters(self, dimension_values_df):
        """dimension_values_df: (pandas.Dataframe) values of the points
        """
        algorithm_id = super(ClusterController, self).get_active_algorithm_id()
        super(ClusterController, self).update_algorithm(algorithm_id)
        labels = None
        if algorithm_id in self._clustering_dic:
            labels = self._clustering_dic[algorithm_id]
        else:
            labels = super(ClusterController, self).\
                     execute_active_algorithm(dimension_values_df,
                                              n_clusters=4)
            self._clustering_dic[algorithm_id] = labels

        colors = [self._label_colors[i] for i in labels]
        if self._source:
            self._source.data['color'] \
                = pd.Series(colors, index=dimension_values_df.index)
