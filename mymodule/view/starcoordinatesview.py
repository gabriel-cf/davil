"""
    STAR COORDINATES VIEW
"""

from __future__ import division
from os import path
import random
from math import cos, sin, radians
from bokeh.layouts import widgetbox, row, column
from bokeh.io import output_notebook, curdoc, show, push_notebook
from bokeh.plotting import figure, show
from bokeh.models import Label, ColumnDataSource, LabelSet, HoverTool, WheelZoomTool, PanTool, PolySelectTool, TapTool, ResizeTool, SaveTool, ResetTool, CustomJS
from bokeh.models.widgets import CheckboxGroup, DataTable, DateFormatter, TableColumn
from bokeh.models.layouts import HBox

from ..backend.model.mapper.starmapper import StarMapper
from ..backend.io.reader import Reader
from ..backend.util.axisgenerator import AxisGenerator
from ..backend.util.dfmatrixutils import DFMatrixUtils

from ..frontend.model.mapper_controller import MapperController
from ..frontend.model.axis_checkboxgroup import AxisCheckboxGroup
from ..frontend.model.figure_element.axis_figure_element import AxisFigureElement

class StarCoordinatesView(object):

    _SEGMENT_COLOR = "#F4A582"
    _SEGMENT_WIDTH = 2

    _SQUARE_SIZE = 7
    _SQUARE_COLOR = "#74ADD1"
    _SQUARE_ALPHA = 0.5

    _CIRCLE_SIZE = 5
    _CIRCLE_COLOR = "navy"
    _CIRCLE_ALPHA = 0.5

    """A view with all the necessary logic for displaying it on bokeh"""
    def __init__(self, file_path, random_weights=False, width=600, height=600):
        """Creates a new Star Coordinates View object and instantiates 
           its elements
        """

        # Configuration elements
        self._random_weights = random_weights
        self._width = width
        self._height = height
        self._file_path = file_path
        self._reader = None        
        # Elements generated from mapping
        self._axis_df = None
        self._dimension_values_df = None
        self._dimension_values_df_norm = None
        self._vectors_df = None
        # Figure elements
        self._figure = None
        self._axis_elements = []
        self._segments = []
        self._points = []
        self._squares = []
        self._checkboxes = None
        self._row_plot = None
        self._source_points = None
        # Controllers
        self._mapper_controller = None
        self._axis_checkboxes = None
        
    #def init_mapping(self, ignored_axis_indexes = None):
    #    """Will return a ColumnDataSource with the mapped points"""
    #    return self._mapper_controller.execute_mapping()        

    def init_table(self):
      """Generates the info table"""
      data = dict(
            dates=[],
            downloads=[],
            )
      source = ColumnDataSource(self._dimension_values_df)
      source.add(self._dimension_values_df.index, name='name')
      columns = [TableColumn(field=field, title=field) 
                      for field in self._dimension_values_df.columns.values]
      columns.insert(0, TableColumn(field='name', title='name'))
      data_table = DataTable(source=source, columns=columns, width=1000, height=600)

      return data_table

    def init(self):
        """Load data from file and initialize dataframe values
            Can be used to reset the original values
        """

        if self._reader is None:
            self._reader = Reader.init_from_file(self._file_path)
        # Get the dimension labels (i.e. the names of the columns with numeric values)
        self._dimension_values_df, self._dimension_values_df_norm = self._reader.get_dimension_values()
        axis_ids = self._dimension_values_df_norm.columns.values.tolist()
        self._axis_df = AxisGenerator.generate_star_axis(axis_ids, 
                                                   random_weights=self._random_weights)

        # Map points using vectors from the axis
        self._vectors_df = DFMatrixUtils.get_vectors(self._axis_df)

        self._mapper_controller = MapperController(self._dimension_values_df_norm, 
                                                  self._vectors_df)
                
        self.init_figure()
        self.init_axis()
        self._axis_checkboxes = AxisCheckboxGroup(axis_ids, self._axis_elements, 
                                                  self._mapper_controller,
                                                  activation_list=None,
                                                  start_activated=False)
        source_points = self._mapper_controller.get_source_points()
        self.init_points(source_points)

        cb_group = self._axis_checkboxes.get_cb_group()
        data_table = self.init_table()
        
        self._row_plot = column([row(self._figure, widgetbox(cb_group)), widgetbox(data_table)])
        curdoc().add_root(self._row_plot)
        curdoc().title = "Star Coordinates"
        output_notebook()

    def init_figure(self, source_points=None):
        """Updates the visual elements on the figure"""
        wheel_zoom_tool = WheelZoomTool()
        pan_tool = PanTool()
        resize_tool = ResizeTool()
        save_tool = SaveTool()
        reset_tool = ResetTool()
        self._figure = figure(width=self._width, height=self._height, 
                              tools=[wheel_zoom_tool, pan_tool, resize_tool, save_tool, reset_tool])
        self._figure.toolbar.active_scroll = wheel_zoom_tool
        hover = HoverTool(
              tooltips=[
                  ("name", "@name")
              ]
          )
        self._figure.add_tools(hover)

    def init_axis(self):
      # Segments and squares
      for i in xrange(0, len(self._axis_df['x0'])):
          segment = self._figure.segment(x0=self._axis_df['x0'][i], 
                                         y0=self._axis_df['y0'][i], 
                                         x1=self._axis_df['x1'][i], 
                                         y1=self._axis_df['y1'][i],
                                         name=self._axis_df.index.values[i], 
                                         color=StarCoordinatesView._SEGMENT_COLOR, 
                                         line_width=StarCoordinatesView._SEGMENT_WIDTH)
          
          square = self._figure.square(x=self._axis_df['x1'][i], 
                                       y=self._axis_df['y1'][i],
                                       name=self._axis_df.index.values[i],
                                       size=StarCoordinatesView._SQUARE_SIZE, 
                                       color=StarCoordinatesView._SQUARE_COLOR, 
                                       alpha=StarCoordinatesView._SQUARE_ALPHA)

          self._axis_elements.append(AxisFigureElement(segment, square))
      # Axis labels
      source_dimensions = ColumnDataSource(self._axis_df)
      source_dimensions.add(self._axis_df.index, name='names')
      labels_dimensions = LabelSet(x='x1', y='y1', text='names', name='names', level='glyph',
                                   x_offset=5, y_offset=5, source=source_dimensions, 
                                   render_mode='canvas')        
      self._figure.add_layout(labels_dimensions)
        
    def init_points(self, source_points):
      # Mapped points
      self._figure.circle('x', 'y', size=StarCoordinatesView._CIRCLE_SIZE, 
                                      color=StarCoordinatesView._CIRCLE_COLOR, 
                                      alpha=StarCoordinatesView._CIRCLE_ALPHA, 
                                      source=source_points)              
