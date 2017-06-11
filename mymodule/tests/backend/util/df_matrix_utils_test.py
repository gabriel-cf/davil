import unittest
import pandas as pd
import numpy as np
from ....src.backend.util.df_matrix_utils import DFMatrixUtils

class DFMatrixUtilsTest(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])

    def test_get_vectors(self):
        x0, x1, y0, y1 = (0, 3, 7, 2)
        points_df = pd.DataFrame([[x0, x1, y0, y1]], columns=['x0', 'x1', 'y0', 'y1'])
        vector_df = DFMatrixUtils.get_vectors(points_df)
        self.assertEqual(vector_df['x'][0], 3, 'Incorrect vector X component')
        self.assertEqual(vector_df['y'][0], -5, 'Incorrect vector Y component')

    def test_get_total_sum(self):
        self.assertEqual(DFMatrixUtils.get_total_sum(self.df), 10, 'Incorrect total sum value')

    def test_get_max_value(self):
        self.assertEqual(DFMatrixUtils.get_max_value(self.df), 4, 'Incorrect max value')

    def test_get_min_value(self):
        self.assertEqual(DFMatrixUtils.get_min_value(self.df), 1, 'Incorrect min value')

    def test_get_mean_value(self):
        self.assertEqual(DFMatrixUtils.get_mean_value(self.df), 2.5, 'Incorrect mean value')

    def test_get_std_value(self):
        std = DFMatrixUtils.get_std_value(self.df)
        self.assertTrue(std > 1.11 and std < 1.12, 'Incorrect std value')

    def test_sum_by_axis(self):
        column_sums = DFMatrixUtils.sum_by_axis(self.df, 0)[0]
        sum_a = sum(self._get_column('a'))
        sum_b = sum(self._get_column('b'))
        self.assertEqual(sum_a, column_sums['a'], "Incorrect column 'a' sum")
        self.assertEqual(sum_b, column_sums['b'], "Incorrect column 'b' sum")

        row_sums = DFMatrixUtils.sum_by_axis(self.df, 1)[0]
        sum_0 = sum(self._get_row(0))
        sum_1 = sum(self._get_row(1))
        self.assertEqual(sum_0, row_sums[0], 'Incorrect row 0 sum')
        self.assertEqual(sum_1, row_sums[1], 'Incorrect row 1 sum')

    def test_max_by_axis(self):
        max_a = max(self._get_column('a'))
        max_b = max(self._get_column('b'))
        column_maxs = DFMatrixUtils.max_by_axis(self.df, 0)[0]
        self.assertEqual(max_a, column_maxs['a'], "Incorrect column 'a' max value")
        self.assertEqual(max_b, column_maxs['b'], "Incorrect column 'b' max value")

        max_0 = max(self._get_row(0))
        max_1 = max(self._get_row(1))
        row_maxs = DFMatrixUtils.max_by_axis(self.df, 1)[0]
        self.assertEqual(max_0, row_maxs[0], "Incorrect row 0 max value")
        self.assertEqual(max_1, row_maxs[1], "Incorrect row 1 max value")

    def test_mean_by_axis(self):
        mean_a = np.mean(self._get_column('a'))
        mean_b = np.mean(self._get_column('b'))
        column_means = DFMatrixUtils.mean_by_axis(self.df, 0)[0]
        self.assertEqual(mean_a, column_means['a'], "Incorrect column 'a' mean value")
        self.assertEqual(mean_b, column_means['b'], "Incorrect column 'b' mean value")

        mean_0 = np.mean(self._get_row(0))
        mean_1 = np.mean(self._get_row(1))
        row_means = DFMatrixUtils.mean_by_axis(self.df, 1)[0]
        self.assertEqual(mean_0, row_means[0], "Incorrect row 0 mean value")
        self.assertEqual(mean_1, row_means[1], "Incorrect row 1 mean value")

    def test_std_by_axis(self):
        std_a = np.std(self._get_column('a'), ddof=1)
        std_b = np.std(self._get_column('b'), ddof=1)
        column_stds = DFMatrixUtils.std_by_axis(self.df, 0)[0]
        self.assertEqual(std_a, column_stds['a'], "Incorrect column 'a' std value")
        self.assertEqual(std_b, column_stds['b'], "Incorrect column 'b' std value")

        std_0 = np.std(self._get_row(0), ddof=1)
        std_1 = np.std(self._get_row(1), ddof=1)
        row_stds = DFMatrixUtils.std_by_axis(self.df, 1)[0]
        self.assertEqual(std_0, row_stds[0], "Incorrect row 0 std value")
        self.assertEqual(std_1, row_stds[1], "Incorrect row 1 std value")

    def test_get_diagonal_ones_matrix(self):
        diagonal_df = DFMatrixUtils.get_diagonal_ones_matrix(self.df)
        for i in range(0, len(self.df.columns)):
            self.assertEqual(diagonal_df[i][i], 1)

    def test_to_df(self):
        df_mx = self.df.as_matrix()
        converted_df = DFMatrixUtils.to_df(df_mx, index=self.df.index, columns=self.df.columns)
        self.assertTrue(self.df.equals(converted_df))

    def _get_row(self, idx):
        df_mx = self.df.as_matrix()
        return [value for value in df_mx[idx]]

    def _get_column(self, label):
        return [value for value in self.df[label]]
