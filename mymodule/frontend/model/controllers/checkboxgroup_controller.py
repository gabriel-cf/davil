"""
    CheckboxGroupController Module
"""

from bokeh.io import push_notebook
from bokeh.models.widgets import CheckboxGroup

class CheckboxGroupController(object):
    """Controller used to handle the bokeh widget CheckboxGroup"""
    def get_active_axis_list(self):
            return [self._element_dict[axis_id].is_visible() for axis_id in self._axis_ids]

    def __init__(self, axis_ids, elements, mapper_controller,
                activation_list=None, start_activated=True):
        """Instantiates the controller, generating the CheckboxGroup
             axis_ids: (Iterable) List of axis' IDs
             elements: (List<AbstractFigureElement>) List of figure
                              elements that can be triggered to be hidden or shown
             on_click_function: (Func) function to be executed when a checkbox
                                is checked. Will happen after the element is hidden
             activation_list (default=[True..True] if start_activated [False..False]
                             otherwise): (List<Boolean>) Initial value of the checkboxes
             start_activated (default=True): default initial value of the checkboxes
        """
        if activation_list and len(axis_ids) != len(activation_list):
            raise ValueError("The length of the axis_ids{} must be the same"
                                .format(len(axis_ids)) 
                            + "as of the activation_list{}"
                                .format(len(activation_list)))
        self._axis_ids = axis_ids
        self._elements = elements
        self._mapper_controller = mapper_controller
        # Generate activation list
        self._element_dict = dict()
        if not activation_list:
            activation_list = [start_activated for i in 
                                xrange(0, len(self._elements))]

        # Asociate each element with its id in a dictionary
        for i in xrange(0, len(self._elements)):
            id_value = self._axis_ids[i]
            element = self._elements[i]
            element.visible(activation_list[i])
            self._element_dict[id_value] = element

        activation_list_index = [i for i in xrange(0, len(self._axis_ids)) if self._element_dict[self._axis_ids[i]].is_visible()]
        self._cb_group = CheckboxGroup(
            labels=self._axis_ids,
            active=activation_list_index
            )

        def update_axis(active_list):
            """This function will be called every time a checkbox is checked
               Will hide or show the selected axis and remap the points
            """
            # We iterate in the CheckboxGroup labels order because it is the
            # same used by the active_list parameter
            for i in xrange(0, len(self._cb_group.labels)):
                element_id = self._cb_group.labels[i]
                element = self._element_dict[element_id]
                # element.visible() will call remapping by default
                element.visible(i in active_list, remap=False)
            # remap once all axis have been updated
            self._mapper_controller.execute_mapping()

        self._cb_group.on_click(update_axis)
        update_axis(activation_list_index)

    def get_cb_group(self):
        """Returns the bokeh CheckboxGroup object"""
        return self._cb_group