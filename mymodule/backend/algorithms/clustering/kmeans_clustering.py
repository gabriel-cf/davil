"""
    K-Means Clustering algorithm
"""

from sklearn.cluster import KMeans

KMEANS_ID = "K-Means"

def kmeans(values_df, n_clusters=5):
    """Will return a list with the category of each value"""
    m = values_df.as_matrix()
    km = KMeans(n_clusters=n_clusters)
    km.fit(m)
    labels = km.labels_
    return labels
