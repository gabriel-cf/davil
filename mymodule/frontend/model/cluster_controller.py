""" 
    Clustering controller
"""

from ...backend.clustering.kmeans_clustering import KMeansClustering
from ...backend.clustering.dummy_clustering import DummyClustering
import pandas as pd

class ClusterController():
    """Controls the clustering of the values for the values dataframe"""

    DUMMY_CLUSTERING_ID = "Dummy Clustering"
    KMEANS_CLUSTERING_ID = "K-Means Clustering"
    DEFAULT_CLUSTERING_ID = DUMMY_CLUSTERING_ID
    CLUSTERING_COLOR_COLUMN = 'color'
    DEFAULT_LABEL_COLORS = ["red", "navy", "green", "orange", "grey"]

    def __init__(self, algorithm_id=None, source=None, label_colors=DEFAULT_LABEL_COLORS):
        self._clustering_dic = dict()
        self._algorithm_id, self._algorithm = self.get_clustering_algorithm(algorithm_id)
        self._label_colors = label_colors
        self._source = source

    def update_clusters(self, dimension_values_df, algorithm_id=DEFAULT_CLUSTERING_ID):
        """dimension_values_df: (pandas.Dataframe) values of the points
           algorithm: (String) cluster algorithm id
        """
        self._algorithm_id, self._algorithm = self.get_clustering_algorithm(algorithm_id)
        labels = None
        if algorithm_id in self._clustering_dic:
            labels = self._clustering_dic[algorithm_id]
        else:
            #if 'color' in dimension_values_df.columns:
            #    self..drop('color', axis=1, inplace=True)            
            labels = self._algorithm(dimension_values_df, n_clusters=3)
            self._clustering_dic[algorithm_id] = labels

        colors = [self._label_colors[i] for i in labels]
        if self._source:
            self._source.data['color'] = pd.Series(colors, index=dimension_values_df.index)


    def get_clustering_algorithm(self, mapping_id):
        if mapping_id == ClusterController.KMEANS_CLUSTERING_ID:
            return ClusterController.KMEANS_CLUSTERING_ID, KMeansClustering.categorize_values
        elif mapping_id == ClusterController.DUMMY_CLUSTERING_ID:
            return ClusterController.DUMMY_CLUSTERING_ID, DummyClustering.categorize_values
        elif mapping_id == ClusterController.DEFAULT_CLUSTERING_ID:            
            raise ValueError("DEFAULT_CLUSTERING_ID should be assigned to an existing CLUSTERING_ID")

        print "WARN: No valid clustering algorithm provided. Assigning default mapper "+"'{}'".format(ClusterController.DEFAULT_CLUSTERING_ID)
        return self.get_clustering_algorithm(ClusterController.DEFAULT_CLUSTERING_ID)

    def get_active_algorithm_id(self):
        return self._algorithm_id

