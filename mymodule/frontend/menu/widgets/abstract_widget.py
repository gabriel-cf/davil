"""
    AbstractWidget
"""
import logging
import traceback
from abc import ABCMeta, abstractmethod

class AbstractWidget(object):
    """Abstract class holding the common methods for widgets. Bokeh has its
       own trigger and similar methods. By wrapping them in our logic we can
       build more complex functionality
    """
    __metaclass__ = ABCMeta
    LOGGER = logging.getLogger(__name__)

    NONE = 'None'

    def __init__(self, widget):
        """ Set widget public property.
            widget: (Bokeh Widget) a plain Bokeh widget
        """
        self.widget = widget

    @abstractmethod
    def trigger(self):
        """Execute all callbacks linked to a change of value"""
        pass

    @abstractmethod
    def update_options(self):
        """Execute callback to update the user displayable options"""
        pass

    @abstractmethod
    def update_value(self):
        """Execute callback to update active value"""
        pass

    @abstractmethod
    def get_options(self):
        """Returns: (String) list of all available options"""
        pass

    @abstractmethod
    def get_value(self):
        """Returns: (Object) current value. Its type may change depending on
           the widget type"""
        pass

    def update_all(self):
        self.update_value()
        self.update_options()

    @classmethod
    def _sort_options(cls, options):
        """Custom sort of options coming from backend
           Will position first 'None' if found
           options: (List<String>)
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
