"""Reader Module
"""
from __future__ import division
import numbers
from file_reader import FileReader
from ..algorithms.normalization.normalization_algorithms import NormalizationAlgorithms


class Reader(object):
    """Provides access to the data held in a DataFrame"""

    def __init__(self, file_path=None, dataframe=None,
                 first_index=None, header=True):
        """ ** It is recommended to initialize the Reader using
            the provided static methods **
            Instantiates a Reader taking the following parameters:
            [file_path]: (String) path to source file to be read
                         Must be set in case you want to load a new DF
            [dataframe]: (Pandas Dataframe) set in case you want to access
                         to an existing dataframe
            [first_index]: (int) first column with dimensional
                                     data, default=first numeric data
            [header]: (bool) if the first line of the file is a header
        """
        if not file_path is None:
            self._df = FileReader.read_file(file_path, header=header)
        else:
            if dataframe is None:
                raise ValueError("A source must be provided either from a "+
                                 "pandas.DataFrame object or a file source")
            #if not isinstance(dataframe, pd.DataFrame):
            #    raise TypeError("dataframe must be of value pandas.DataFrame")
            self._df = dataframe
        # Set first_index to 0 or the first Numeric element index
        if first_index is None:
            self._first_index = 0
            for i in xrange(len(self._df.columns)):
                if isinstance(self._df.iat[0, i], numbers.Number):
                    self._first_index = i
                    break
        else:
            self._first_index = first_index

    # Static method for intializing Reader objects
    @staticmethod
    def init_from_file(file_path, first_index=None, header=True):
        """Returns a Reader object that gets it dataframe from a file
            file_path: (String) path to source file to be read
            [first_index]: (int) first column with dimensional
                                     data, default=first numeric data            
            [header]: (bool) if the first line of the file is a header
        """
        return Reader(file_path=file_path, first_index=first_index, header=header)

    @staticmethod
    def init_from_dataframe(dataframe, first_index=None, header=True):
        """Returns a Reader object that uses a given dataframe
            dataframe: (Pandas Dataframe) set in case you want to access
                         to an existing dataframe
            [first_index]: (int) first column with dimensional
                                     data, default=first numeric data            
            [header]: (bool) if the first line of the file is a header

        """
        return Reader(dataframe=dataframe, first_index=first_index, header=header)

    def set_first_index(self, index):
        """Sets the index value of the first column holding dimensional data"""
        no_columns = len(self._df.columns)
        if index > no_columns:
            raise ValueError("The index value ({}) specified is greater "
                             .format(index) + "than the number of columns ({})"
                             .format(no_columns))

        self._first_index = index
    
    def get_dimension_values(self):
        """Returns: (pandas.Dataframe) read dimensional values
                    (pandas.Dataframe) normalized dimensional values
        """
        dimension_values_df_cp = self._df.ix[:,self._first_index:].copy()
        dimension_values_df_cp_norm = NormalizationAlgorithms.max_per_column(dimension_values_df_cp, inplace=False)
            
        return dimension_values_df_cp, dimension_values_df_cp_norm

    def get_dimension_labels(self):
        return list(self._df.columns.values[self._first_index:])
