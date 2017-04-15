""" 
    Classification algorithms
"""

from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from ...util.df_matrix_utils import DFMatrixUtils

class ClassificationAlgorithms():
    """Algorithms to determine the initial position of the axis according
       to the original values through decomposition of their dimensions
    """
    @staticmethod
    def pca(values_df):
        pca = PCA(n_components=2)
        pca.fit(values_df)
        ones_mx = DFMatrixUtils.get_diagonal_ones_matrix(values_df)
        positions_matrix = pca.transform(ones_mx)
        positions_df = DFMatrixUtils.to_df(positions_matrix, 
                                           index=values_df.columns,
                                           columns=['x', 'y'])
        return positions_df

    @staticmethod
    def lda(values_df, classes):
        lda = LDA(n_components=2)
        lda.fit(values_df, classes)
        ones_mx = DFMatrixUtils.get_diagonal_ones_matrix(values_df)
        positions_matrix = lda.transform(ones_mx)
        positions_df = DFMatrixUtils.to_df(positions_matrix,
                                           index=values_df.columns,
                                           columns=['x', 'y'])
        return positions_df
