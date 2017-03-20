"""
    File Controller
"""

from os import path, listdir

class FileController(object):
    DEFAULT_DIRECTORY = path.abspath(path.relpath(path.join('mymodule', 'resources')))
    print "DEFAULT: {}".format(DEFAULT_DIRECTORY)
    AVAILABLE_EXTENSIONS = ["CSV"]

    def list_files(self, directory):
        def has_valid_extension(file):
            return f.split('.')[-1].upper() in FileController.AVAILABLE_EXTENSIONS
        if not path.isdir(directory):
            raise ValueError("ERROR: '{}' is not a valid directory".format(directory))
        return [f for f in listdir(directory) if path.isfile(path.join(directory, f)) 
                and has_valid_extension(file)]

    """Controller for selecting the input file"""
    def __init__(self, file=None, directory=DEFAULT_DIRECTORY):        
        self._directory = directory
        self._files = self.list_files(directory)
        print "Available files: {}".format(self._files)
        self._active_file = file
        if not self._active_file and len(self._files) > 0:
            self._active_file = self._files[0]

    def update_active_file(self, new_file):
        self._active_file = path.join(self._directory, new_file)

    def get_active_file(self):
        return self._active_file

    def get_available_files(self):
        return self.list_files(self._directory)
