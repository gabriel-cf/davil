"""
    SliderWidget
"""
import logging
from bokeh.models.widgets import Slider
from .abstract_widget import AbstractWidget

class SliderWidget(AbstractWidget):
    """Select class holding the common methods for widgets
    """
    LOGGER = logging.getLogger(__name__)

    @classmethod
    def init_slider_widget(cls, update_value_callback, on_change_callback,
                           title="Default", start=1, end=10, step=1, value=None):
        if not value:
            value = cls.get_value_or_none(update_value_callback)

        slider = Slider(start=start, end=end, value=value, step=step, title=title)
        slider.on_change('value', on_change_callback)

        return SliderWidget(slider, update_value_callback)

    def __init__(self, widget, update_value_callback):
        super(SliderWidget, self).__init__(widget)
        self._update_value_callback = update_value_callback

    def trigger(self):
        self.widget.trigger('value', self.widget.value, self.widget.value)

    def update_options(self):
        """Slider does not have a choice"""
        pass

    def update_value(self):
        self.widget.value = self._update_value_callback()

    def get_options(self):
        """Slider does not have a choice"""
        return self.NONE

    def get_value(self):
        return self.widget.value
