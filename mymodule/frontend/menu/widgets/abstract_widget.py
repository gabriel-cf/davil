"""
    Generic algorithm controller
"""
import logging
import traceback
from abc import ABCMeta, abstractmethod

class AbstractWidget(object):
    """Abstract class holding the common methods for widgets
    """
    __metaclass__ = ABCMeta
    LOGGER = logging.getLogger(__name__)

    NONE = 'None'

    def __init__(self, widget):
        self.widget = widget # Note that it is public

    @abstractmethod
    def trigger(self):
        pass

    @abstractmethod
    def update_options(self):
        pass

    @abstractmethod
    def update_value(self):
        pass

    @abstractmethod
    def get_options(self):
        pass

    @abstractmethod
    def get_value(self):
        pass

    def update_all(self):
        self.update_value()
        self.update_options()

    @classmethod
    def _sort_options(cls, options):
        """Custom sort of options coming from backend
           Will position first 'None' if found
        """
        res_options = []
        if AbstractWidget.NONE in options:
            res_options.append(AbstractWidget.NONE)
            options.remove(AbstractWidget.NONE)
        options.sort()
        return res_options + options

    @classmethod
    def get_value_or_none(cls, callback):
        """Executes the callback without parameters if no value is retrieved
           assigns NONE
        """
        if callback:
            try:
                value = callback()
                if not value is None: 
                    return value
            except Exception as e:
                cls.LOGGER.warn("Could not determine value, assigning None")
                cls.LOGGER.debug(traceback.format_exc())
        return cls.NONE