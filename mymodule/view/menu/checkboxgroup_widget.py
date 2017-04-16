"""
    CheckboxGroupGenerator
"""
import logging
from bokeh.layouts import widgetbox
from bokeh.models.widgets import CheckboxGroup

class CheckboxGroupWidget(object):
    """Generator for bokeh CheckboxGroup widgets"""
    LOGGER = logging.getLogger(__name__)

    @staticmethod
    def _checkbox_update_element(active_list, labels, view_action):
        """Generic function designed to be executed every time a checkbox is checked
           It will call the view informing that the element has been checked
           or unchecked

           active_list: (int[]) list provided by the on_click method of the
                        checkboxgroup
           labels: (String[]) ID labels matching the indexes of the active_list
           view_action: (Func(String, Boolean)) call (to the view) to be executed
        """
        for i in xrange(0, len(labels)):
            element_id = labels[i]
            checked = i in active_list
            view_action(element_id, checked)

    @staticmethod
    def init_axis_checkboxes(view, callback):
        """Generates a group of checkboxes whose function is to activate or
           deactivate the visibility of the axis of the view
        """
        # Get a zipped list of [(element_id, isVisible), ..]
        axis_visibility_list = view.get_axis_status()
        _ = zip(*axis_visibility_list)
        axis_id_l = [element_id for element_id in _[0]]
        CheckboxGroupWidget.LOGGER.debug("Axis visibility: %s", _[1])
        axis_visibility_l = [i for i in xrange(0, len(_[1])) if _[1][i]]
        cb_group = CheckboxGroup(
            labels=axis_id_l,
            active=axis_visibility_l
            )
        cb_group.on_click(lambda active_list: CheckboxGroupWidget._checkbox_update_element\
                                              (active_list, cb_group.labels, 
                                               callback))
        return cb_group

    def __init__(self, view):
        self._view = view
        self._callback = view.update_axis_visibility
        self._checkboxes = CheckboxGroupWidget.init_axis_checkboxes(self._view, self._callback)

    def get_widget(self):
        return widgetbox(self._checkboxes, name='checkboxes')

    def update_view(self, new_view):
        if self._view != new_view:
            self._view = new_view
            self._callback = new_view.update_axis_visibility
            self._checkboxes = CheckboxGroupWidget.init_axis_checkboxes(self._view, self._callback)
