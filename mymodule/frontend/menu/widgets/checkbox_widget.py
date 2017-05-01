"""
    Generic algorithm controller
"""
import logging
from bokeh.models.widgets import Dropdown
from .abstract_widget import AbstractWidget

class DropdownWidget(AbstractWidget):
    """Select class holding the common methods for widgets
    """
    LOGGER = logging.getLogger(__name__)

    @classmethod
    def init_dropdown_widget(cls, update_value_callback, update_options_callback,
                           on_change_callback, value=None, options=None):

        if not value:
            value = cls.get_value_or_none(update_value_callback)
        if not options:
            options = cls.get_value_or_none(update_options_callback)

        dropdown_button = Dropdown(label=value, menu=options)
        #on_change is set after the object is created due to dependencies
        return DropdownWidget(dropdown_button, update_value_callback,
                              update_options_callback, on_change_callback)

    def __init__(self, widget, update_value_callback, update_options_callback,
                 on_change_callback):
        super(DropdownWidget, self).__init__(widget)
        self._update_value_callback = update_value_callback
        self._update_options_callback = update_options_callback
        self._wrap_on_change_callback(on_change_callback)

    def trigger(self):
        self.widget.trigger('value', self.widget.value, self.widget.value)

    def update_options(self):
        self.widget.menu = self._update_options_callback()

    def update_value(self):
        self.widget.label = self._update_value_callback()

    def get_options(self):
        return self.widget.menu

    def get_value(self):
        return self.widget.active

    def _wrap_on_change_callback(self, callback):
        """Wraps the function and sets the label to the new selected value
        """
        def wrapped_on_change_callback(attr, old, new):
            """Bokeh on_change callback wrapper.
            """
            self.widget.label = new
            callback(new)

        self.widget.on_change('value', wrapped_on_change_callback)
