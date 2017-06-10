"""
    CheckboxGroupWidget
"""
import logging
from bokeh.models.widgets import CheckboxGroup
from .abstract_widget import AbstractWidget

class CheckboxGroupWidget(AbstractWidget):
    """CheckboxGroupWidget class holding the common methods for widgets
    """
    LOGGER = logging.getLogger(__name__)

    @staticmethod
    def _translate_to_active_list(id_values, options):
        return [options.index(value) for value in id_values]

    @classmethod
    def init_checkbox_widget(cls, update_value_callback, update_options_callback,
                             on_change_callback, value=None, options=None):
        if not options:
            options = cls.get_value_or_none(update_options_callback)
            if options == cls.NONE:
                options = []

        if not value:
            id_values = cls.get_value_or_none(update_value_callback)
            if id_values != cls.NONE and len(options) > 0:
                value = CheckboxGroupWidget._translate_to_active_list(id_values, options)
            else:
                value = []

        checkbox = CheckboxGroup(active=value, labels=options)
        #on_change is set after the object is created due to dependencies
        return CheckboxGroupWidget(checkbox, update_value_callback,
                                   update_options_callback, on_change_callback)

    def __init__(self, widget, update_value_callback, update_options_callback,
                 on_change_callback):
        super(CheckboxGroupWidget, self).__init__(widget)
        self._update_value_callback = update_value_callback
        self._update_options_callback = update_options_callback
        self._last_active_list = widget.active
        self._wrap_on_change_callback(on_change_callback)

    def trigger(self):
        self.widget.trigger('active', self.widget.active, self.widget.active)

    def update_options(self):
        self.widget.labels = self._update_options_callback()

    def update_value(self):
        id_values = self._update_value_callback()
        options = self.widget.labels
        self.widget.active = CheckboxGroupWidget._translate_to_active_list(id_values, options)

    def update_all(self):
        # Override to switch normal order
        self.update_options()
        self.update_value()

    def get_options(self):
        return self.widget.labels

    def get_value(self):
        return self.widget.active

    def _wrap_on_change_callback(self, callback):
        """Wraps the function and sets the label to the newly selected value
        """
        def wrapped_on_change_callback(new):
            """Bokeh on_change callback wrapper.
            """
            # Translate id with index in the options list
            options = self.widget.labels
            new_active_list = new
            for i in xrange(0, len(options)):
                # If it was active before and now it is not or vice versa
                is_active = i in new_active_list
                was_active = i in self._last_active_list
                if (is_active and not was_active)\
                or (not is_active and was_active):
                    callback((options[i], is_active))

            self._last_active_list = new

        self.widget.on_click(wrapped_on_change_callback)
