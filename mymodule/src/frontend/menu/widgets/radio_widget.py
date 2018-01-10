"""
    RadioWidget
"""
import logging
from bokeh.models.widgets import RadioButtonGroup
from .abstract_widget import AbstractWidget

class RadioWidget(AbstractWidget):
    """Radio class holding the common methods for widgets
    """
    LOGGER = logging.getLogger(__name__)

    @classmethod
    def init_radio_widget(cls, update_value_callback, update_options_callback,
                           on_change_callback, value=None, options=None):

        if not value:
            value = cls.get_value_or_none(update_value_callback)
        if not options:
            options = cls.get_value_or_none(update_options_callback)

        radio_button = RadioButtonGroup(active=options.index(value), labels=options)
        #on_change is set after the object is created due to dependencies

        return RadioWidget(radio_button, update_value_callback,
                           update_options_callback, on_change_callback)

    def __init__(self, widget, update_value_callback, update_options_callback,
                 on_change_callback):
        super(RadioWidget, self).__init__(widget)
        self._update_value_callback = update_value_callback
        self._update_options_callback = update_options_callback
        self._wrap_on_change_callback(on_change_callback)

    def trigger(self):
        self.widget.trigger('active', self.widget.active, self.widget.active)

    def update_options(self):
        self.widget.labels = self._update_options_callback()

    def update_value(self):
        active_option = self._update_value_callback()
        self.widget.active = self.widget.labels.index(active_option)

    def get_options(self):
        return self.widget.labels

    def get_value(self):
        return self.widget.active

    def _wrap_on_change_callback(self, callback):
        """Wraps the function and maps the index held in 'new' to an option
           callback: (func) function that expects an option as parameter
        """
        def wrapped_on_change_callback(attr, old, new):
            """Bokeh on_change callback wrapper. The new value holds the active
               index of the newly selected option and needs to be translated
            """
            option = self.widget.labels[new]
            callback(option)

        self.widget.on_change('active', wrapped_on_change_callback)
