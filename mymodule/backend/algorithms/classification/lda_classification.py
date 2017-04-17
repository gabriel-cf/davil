"""
    LDA
"""

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from ...util.df_matrix_utils import DFMatrixUtils

LDA_ID = "LDA"

def lda(values_df, classes):
    lda_ = LDA(n_components=2)
    lda_.fit(values_df, classes)
    ones_mx = DFMatrixUtils.get_diagonal_ones_matrix(values_df)
    positions_matrix = lda_.transform(ones_mx)
    positions_df = DFMatrixUtils.to_df(positions_matrix,
                                       index=values_df.columns,
                                       columns=['x', 'y'])
    return positions_df
