"""
    Dummy Clustering
"""

DUMMY_ID = "Dummy Clustering"

def dummy(values_df, n_clusters=5):
    """Will return a list with the category of each value"""
    labels = []
    for i in xrange(len(values_df.index)):
        labels.append(i % n_clusters)
    return labels
