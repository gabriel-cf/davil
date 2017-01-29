"""File Reader
"""
from os.path import isfile
import pandas as pd

class FileReader(object):
    """ Static class used for reading a .csv file and 
        returning a Pandas DataFrame
    """

    FILE_EXTENSION = "CSV"
    DELIMITER = ';'
    USE = ("USE: Files must have .'{}' extension. "+
           "The default delimiter is = '{}'").format(FILE_EXTENSION, DELIMITER)

    @staticmethod
    def read_file(file_path, delimiter=DELIMITER, header=True, index_col=0):
        """ Reads the file from the given path
            Returns a Pandas DataFrame

            file_path --> (String) path to source file
            [delimiter] --> (String) delimiter of file. Default = ';'
            [header] --> (Boolean) True if the first line is the header
            [index_col] --> (int) column with the id / name of each product
        """
        print file_path
        if (file_path.split('.')[-1].upper() == FileReader.FILE_EXTENSION
                and isfile(file_path)):
            dataframe = None
            if header:
                dataframe = pd.read_csv(file_path, sep=delimiter, 
                                        index_col=index_col)
            else:
                dataframe = pd.read_csv(file_path, sep=delimiter, 
                                        header=None, index_col=index_col)
            return dataframe
        else:
            raise ValueError("'{}' was not a valid file\n{}"
                             .format(file_path, FileReader.USE))
