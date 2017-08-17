"""
    Point Controller
"""
import logging
from bokeh.models import ColumnDataSource


class PointController(object):
    """Controls the point column data source"""
    LOGGER = logging.getLogger(__name__)

    @staticmethod
    def _get_unique_names(names):
        """Due to limitations when searching for a point, we need to guarantee
           that all names are unique. Secondly name will be name_2, third
           name_3 and so on.
        """

        new_names = []
        counter_dict = dict()
        for name in names:
            if name in counter_dict:
                new_name = "{}_{}".format(name, counter_dict[name])
                counter_dict[name] += 1
                name = new_name
            else:
                counter_dict[name] = 2
            new_names.append(name)

        return new_names

    def __init__(self, input_data_controller, classification_controller):
        """input_data_controller: (InputDataController)"""
        self._source = ColumnDataSource()
        unique_names = PointController._get_unique_names(input_data_controller.get_element_names())
        self.add_attribute('name', unique_names)
        self.add_attribute('category', classification_controller.get_categories())
        self.add_attribute('color', [])
        self.add_attribute('error', [])
        self.add_attribute('size', [])
        self.add_attribute('x', [])
        self.add_attribute('y', [])

    def get_source(self):
        return self._source
        
    def get_point_names(self):
        return [name for name in self._source.data['name']]

    def get_number_of_points(self):
        return len(self._source.data['name'])

    def is_valid_point(self, name):
        return name in self._source.data['name']

    def update_coordinates(self, x, y):
        self._source.data['x'] = x
        self._source.data['y'] = y

    def update_categories(self, categories):
        self._source.data['category'] = categories

    def update_colors(self, colors):
        self._source.data['color'] = colors

    def update_errors(self, errors):
        self._source.data['error'] = errors

    def update_sizes(self, sizes):
        self._source.data['size'] = sizes

    def add_attribute(self, attr_name, items):
        self._source.add(items, name=attr_name)
