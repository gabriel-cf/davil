"""
    AutoCompleteInputWidget
"""
import logging
from bokeh.models.widgets.inputs import AutocompleteInput
from .abstract_widget import AbstractWidget


class AutocompleteInputWidget(AbstractWidget):
    """AutocompleteInputWidget class holding the common methods for widgets
    """
    LOGGER = logging.getLogger(__name__)

    @classmethod
    def init_autocomplete_widget(cls, update_value_callback, update_options_callback, 
                                 on_change_callback, value=None, options=None, title=None):
        if not value:
            value = cls.get_value_or_none(update_value_callback)
        if not options:
            options = cls.get_value_or_none(update_options_callback)

        autocomplete = AutocompleteInput(completions=options, title=title)
        autocomplete.on_change('value', lambda attr, old, new: on_change_callback(new))

        return AutocompleteInputWidget(autocomplete, update_value_callback, update_options_callback)

    def __init__(self, widget, update_value_callback, update_options_callback):
        super(AutocompleteInputWidget, self).__init__(widget)
        self._update_value_callback = update_value_callback
        self._update_options_callback = update_options_callback

    def trigger(self):
        self.widget.trigger('value', self.widget.value, self.widget.value)

    def update_options(self):
        self.widget.completions = self._update_options_callback()

    def update_value(self):
        value = self._update_value_callback()
        if value == self.NONE:
            value = ''
        self.widget.value = value

    def get_options(self):
        return self.widget.completions

    def get_value(self):
        return self.widget.value
