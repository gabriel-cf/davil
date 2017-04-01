"""
    File Controller
"""

from os import path, listdir

class FileController(object):
    """Controller for selecting the input file"""
    DEFAULT_DIRECTORY = path.abspath(path.relpath(path.join('mymodule', 'resources')))
    print "DEFAULT: {}".format(DEFAULT_DIRECTORY)
    AVAILABLE_EXTENSIONS = ["CSV"]

    @staticmethod
    def _list_files(directory=DEFAULT_DIRECTORY):
        """Returns: (String[]) available files on the given directory"""
        def has_valid_extension(file_):
            """file: (String | File) filename
               Returns True if the file has an extension of AVAILABLE_EXTENSIONS
            """
            return file_.split('.')[-1].upper() in FileController.AVAILABLE_EXTENSIONS
        if not path.isdir(directory):
            raise ValueError("ERROR: '{}' is not a valid directory".format(directory))
        return [f for f in listdir(directory) if path.isfile(path.join(directory, f))
                and has_valid_extension(f)]

    def __init__(self, file_=None, directory=DEFAULT_DIRECTORY):
        """[file_=None]: initial active file, if none specified then it will take
           the first one of the given directory
           [directory=DEFAULT_DIRECTORY]: self explanatory
        """
        self._directory = directory
        self._files = FileController._list_files(directory=directory)
        print "Available files: {}".format(self._files)
        self._active_file = file_
        if not self._active_file and len(self._files) > 0:
            self._active_file = self._files[0]

    def update_active_file(self, new_file):
        """Self explanatory"""
        self._active_file = path.join(self._directory, new_file)

    def get_active_file(self):
        """Self explanatory"""
        return self._active_file

    def get_available_files(self):
        """Self explanatory"""
        return FileController._list_files(self._directory)
