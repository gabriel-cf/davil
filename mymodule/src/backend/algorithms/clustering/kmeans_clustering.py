"""
    K-Means Clustering algorithm
"""

from sklearn.cluster import KMeans

KMEANS_ID = "K-Means"

def kmeans(values_df, n_clusters=5):
    """values_df: (pandas.DataFrame) product_id X dimensional_values
       [n_clusters=5] (int) number of clusters
       Returns: (List<String>) list of category labels matching input values
    """
    m = values_df.as_matrix()
    km = KMeans(n_clusters=n_clusters)
    km.fit(m)
    labels = km.labels_
    return labels
