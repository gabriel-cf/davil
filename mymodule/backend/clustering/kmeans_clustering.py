""" 
    K-Means Clustering algorithm
"""

from sklearn.cluster import KMeans

class KMeansClustering():
    """Cluster values of a dataframe using sklearn K-Means implementation"""
    
    @staticmethod
    def categorize_values(values_df, n_clusters=5):
        """Will return a list with the category of each value"""
        m = values_df.as_matrix()
        km = KMeans(n_clusters=n_clusters)
        km.fit(m)
        labels = km.labels_
        return labels