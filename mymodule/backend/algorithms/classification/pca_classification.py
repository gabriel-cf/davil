"""
    PCA
"""

from sklearn.decomposition import PCA
from ...util.df_matrix_utils import DFMatrixUtils

PCA_ID = "PCA"

def pca(values_df):
    pca_ = PCA(n_components=2)
    pca_.fit(values_df)
    ones_mx = DFMatrixUtils.get_diagonal_ones_matrix(values_df)
    positions_matrix = pca_.transform(ones_mx)
    positions_df = DFMatrixUtils.to_df(positions_matrix,
                                       index=values_df.columns,
                                       columns=['x', 'y'])
    return positions_df
