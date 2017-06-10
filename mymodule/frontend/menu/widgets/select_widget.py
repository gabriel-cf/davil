"""
    SelectWidget
"""
import logging
from bokeh.models.widgets import Select
from .abstract_widget import AbstractWidget


class SelectWidget(AbstractWidget):
    """Select class holding the common methods for widgets
    """
    LOGGER = logging.getLogger(__name__)

    @classmethod
    def init_select_widget(cls, title, update_value_callback, update_options_callback,
                           on_change_callback, value=None, options=None):
        if not value:
            value = cls.get_value_or_none(update_value_callback)
        if not options:
            options = cls.get_value_or_none(update_options_callback)

        select = Select(title=title,
                        value=value,
                        options=cls._sort_options(options))

        select.on_change('value', lambda attr, old, new: on_change_callback(new))
        return SelectWidget(select, update_value_callback, update_options_callback)

    def __init__(self, widget, update_value_callback, update_options_callback):
        super(SelectWidget, self).__init__(widget)
        self._update_value_callback = update_value_callback
        self._update_options_callback = update_options_callback

    def trigger(self):
        self.widget.trigger('value', self.widget.value, self.widget.value)

    def update_options(self):
        self.widget.options = self._update_options_callback()

    def update_value(self):
        self.widget.value = self._update_value_callback()

    def get_options(self):
        return self.widget.options

    def get_value(self):
        return self.widget.value
