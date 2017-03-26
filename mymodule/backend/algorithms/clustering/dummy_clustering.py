""" 
    Dummy Clustering algorithm
"""

class DummyClustering():
    """Cluster values of a dataframe using dummy implementation"""
    
    @staticmethod
    def categorize_values(values_df, n_clusters=5):
        """Will return a list with the category of each value"""
        labels = []
        for i in xrange(len(values_df.index)):
            labels.append(i % n_clusters)
        return labels