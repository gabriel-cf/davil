"""
    Generic algorithm controller
"""
import logging
from abc import ABCMeta

class AbstractAlgorithmController(object):
    """Abstract class holding the common methods for all algorithm controllers
       like the MapperController or the ClusterController
       Works based on a dictionary of algorithm ids with algorithm functions
    """
    __metaclass__ = ABCMeta
    LOGGER = logging.getLogger(__name__)
    NONE_ALGORITHM_ID = 'None'

    def __init__(self, default_algorithm_id, algorithm_dict,
                 active_algorithm_id=None,
                 none_algorithm=False):
        """default_algorithm_id: (String) algorithm id to be used by default
           algorithm_dict: (Dictionary) with shape {Algorithm_id, Algorithm}
           [active_algorithm_id=None]: active algorithm id
           [none_algorithm=False]: set to True to count with a None option
        """
        self._algorithm_dict = algorithm_dict
        if none_algorithm:
            self._algorithm_dict[AbstractAlgorithmController.NONE_ALGORITHM_ID] = None
        if not default_algorithm_id in algorithm_dict:
            raise ValueError('The default algorithm id must be included with the\
                             algorithm dictionary')            
        self._default_algorithm_id = default_algorithm_id
        self._active_algorithm_id, \
        self._active_algorithm = self._get_algorithm(active_algorithm_id)        

    def update_algorithm(self, algorithm_id):
        """Updates the algorithm to the one matching the given ID or default
           if no match is possible
        """
        self._active_algorithm_id, \
        self._active_algorithm = self._get_algorithm(algorithm_id)

    def _get_algorithm(self, algorithm_id):
        """algorithm_id: (String) ID of the algorithm to be retrieved
           Returns: (String) algorithm_id (which can be the same or default if
           none was matched)
                    (Func) algorithm function
        """
        if algorithm_id in self._algorithm_dict:
            return algorithm_id, self._algorithm_dict[algorithm_id]
        AbstractAlgorithmController\
          .LOGGER.warn("No valid algorithm provided. Assigning default algorithm '%s'" \
                       , self._default_algorithm_id)
        return self._default_algorithm_id, \
               self._algorithm_dict[self._default_algorithm_id]

    def get_active_algorithm_id(self):
        """Self explanatory"""
        return self._active_algorithm_id

    def execute_active_algorithm(self, *args, **kwargs):
        """Will execute the given algorithm id using as many arguments and
           key arguments as provided
        """
        if not self.has_active_algorithm():
          raise ValueError('No active algorithm has been defined')
        return self._active_algorithm(*args, **kwargs)

    def get_all_options(self):
        """Returns a list of the available algorithm ids
           (i.e. the keys of the dictionary)
        """
        return self._algorithm_dict.keys()

    def has_active_algorithm(self):
        return self.get_active_algorithm_id() != AbstractAlgorithmController.NONE_ALGORITHM_ID


