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
from bokeh.models.widgets import CheckboxGroup, DataTable, DateFormatter, TableColumn, Select
from bokeh.models.layouts import HBox

from ..backend.model.mapper.star_mapper import StarMapper
from ..backend.io.reader import Reader
from ..backend.util.axis_generator import AxisGenerator
from ..backend.util.df_matrix_utils import DFMatrixUtils

from ..frontend.model.mapper_controller import MapperController
from ..frontend.model.cluster_controller import ClusterController
from ..frontend.model.file_controller import FileController
from ..frontend.model.axis_checkboxgroup import AxisCheckboxGroup
from ..frontend.model.figure_element.axis_figure_element import AxisFigureElement
from ..frontend.extension.dragtool import DragTool
from ..frontend.animation.mapping_animator import MappingAnimator


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
    def __init__(self, file_path, random_weights=False, width=600, height=600, doc=None):
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
        self._doc = doc if doc else curdoc()
        self._figure = None
        self._sources = None
        self._axis_elements = []
        self._segments = []
        self._points = []
        self._squares = []
        self._square_mapper = None
        self._checkboxes = None
        self._select = None
        self._row_plot = None        
        self._source_points = None
        # Controllers
        self._mapper_controller = None
        self._cluster_controller = None
        self._file_controller = None
        self._axis_checkboxes = None
        
        self.init_file_controller()
        self._root = None

    def clear(self):
        self._reader = None        
        # Elements generated from mapping
        self._axis_df = None
        self._dimension_values_df = None
        self._dimension_values_df_norm = None
        self._vectors_df = None
        # Figure elements
        self._figure = None
        self._sources = None
        self._axis_elements = []
        self._segments = []
        self._points = []
        self._squares = []
        self._square_mapper = None
        self._checkboxes = None
        self._select = None
        self._source_points = None
        # Controllers
        self._mapper_controller = None
        self._cluster_controller = None
        self._axis_checkboxes = None



    def init_table(self):
        """Generates the info table"""
        source = ColumnDataSource(self._dimension_values_df)
        source.add(self._dimension_values_df.index, name='name')
        columns = [TableColumn(field=field, title=field)
                   for field in self._dimension_values_df.columns.values]
        columns.insert(0, TableColumn(field='name', title='name'))
        data_table = DataTable(source=source, columns=columns, width=1000, height=600)

        return data_table

    def init_square_mapper(self):
      def remap(attr, old, new):
        print "REMAP - DRAG && DROP"
        print self._square_mapper.glyph.name
        print self._square_mapper.glyph.x
        print self._square_mapper.glyph.y
        modified_axis_id = self._square_mapper.glyph.name
        self._mapper_controller.update_vector_values(modified_axis_id, self._square_mapper.glyph.x, self._square_mapper.glyph.y)
        self._mapper_controller.execute_mapping()

      square = self._figure.square(x=0, y=0, name='remap', size=0)
      square.on_change('visible', remap)
      return square

    def init_mapping_select(self):             
      def select_mapping_algorithm(attr, old, new):
        print "Updating mapping algorithm to {}".format(new)
        self._mapper_controller.update_mapping_algorithm(new)
        self._mapper_controller.execute_mapping()

      active_mapper = self._mapper_controller.get_active_mapper_id()
      select =  Select(title="Mapping Algorithm:",
                      value=active_mapper,
                      options=[MapperController.STAR_MAPPER_ID,
                               MapperController.DEFAULT_MAPPER_ID])
      select.on_change('value', select_mapping_algorithm)
      return select

    def init_clustering_select(self):             
      def select_clustering_algorithm(attr, old, new):
        print "Updating clustering algorithm to {}".format(new)
        self._cluster_controller.update_clusters(self._dimension_values_df_norm, new)

      active_algorithm = self._cluster_controller.get_active_algorithm_id()
      select =  Select(title="Clustering Algorithm:",
                      value=active_algorithm,
                      options=[ClusterController.KMEANS_CLUSTERING_ID,
                               ClusterController.DEFAULT_CLUSTERING_ID])
      select.on_change('value', select_clustering_algorithm)
      return select

    def init_file_select(self):             
      def select_file(attr, old, new):
        print "Loading new file '{}'".format(new)        
        self._file_controller.update_active_file(new)
        print "File loaded"
        self.clear()
        self.init()

      available_files = self._file_controller.get_available_files()
      active_file = self._file_controller.get_active_file()
      select =  Select(title="Select source file:",
                       value=active_file,
                       options=available_files)
      select.on_change('value', select_file)
      return select

    def init_file_controller(self):
        self._file_controller = FileController(file=self._file_path)
        self._file_select = self.init_file_select()                

    def init(self):
        """Load data from file and initialize dataframe values
            Can be used to reset the original values
        """
        self._reader = Reader.init_from_file(self._file_controller.get_active_file())
        # Get the dimension labels (i.e. the names of the columns with numeric values)
        self._dimension_values_df, self._dimension_values_df_norm = self._reader.get_dimension_values()
        axis_ids = self._dimension_values_df_norm.columns.values.tolist()
        self._axis_df = AxisGenerator.generate_star_axis(axis_ids,
                                                   random_weights=self._random_weights)
        # Map points using vectors from the axis
        self._vectors_df = DFMatrixUtils.get_vectors(self._axis_df)
        self._mapper_controller = MapperController(self._dimension_values_df_norm,
                                                  self._vectors_df, animator=MappingAnimator())
        activation_list = []
        start_activated = True
        self.init_figure()
        # We need to provide the AxisFigureElement class with a mapper controller
        # so it can execute mapping upon modification of its values

        AxisFigureElement.set_mapper_controller(self._mapper_controller)
        self.init_axis()
        self._square_mapper = self.init_square_mapper()
        self._figure.add_tools(DragTool(sources=self._sources, remap_square=self._square_mapper))
        
        self._axis_checkboxes = AxisCheckboxGroup(axis_ids, self._axis_elements, 
                                                  self._mapper_controller,
                                                  activation_list=activation_list,
                                                  start_activated=start_activated) 
        cb_group = self._axis_checkboxes.get_cb_group()
        data_table = self.init_table()
        select_mapping  = self.init_mapping_select()        
        # Initial mapping
        source_points = self._mapper_controller.execute_mapping()
        self._cluster_controller = ClusterController(source=source_points)
        self._cluster_controller.update_clusters(self._dimension_values_df_norm)
        select_clustering = self.init_clustering_select()
        self.init_points(source_points)

        row_plot = column([row(widgetbox(select_mapping), widgetbox(select_clustering)),
                           row(self._figure, widgetbox(cb_group)),
                           widgetbox(data_table)])

        if self._root is None:
            self._root = column(row(widgetbox(self._file_select)), row_plot, responsive=True)
            self._doc.add_root(self._root)
        else:
            print self._root.children
            self._root.children[1] = row_plot
        self._doc.title = "Star Coordinates"
        return self._row_plot

    def init_figure(self, source_points=None):
        """Updates the visual elements on the figure"""
        wheel_zoom_tool = WheelZoomTool()
        pan_tool = PanTool()
        resize_tool = ResizeTool()
        save_tool = SaveTool()
        reset_tool = ResetTool()
        self._figure = figure(tools=[wheel_zoom_tool, pan_tool, resize_tool, save_tool, reset_tool])
        self._figure.toolbar.active_scroll = wheel_zoom_tool
        hover = HoverTool(
              tooltips=[
                  ("name", "@name")
              ]
          )
        self._figure.add_tools(hover)

    def init_axis(self, activation_list=None):
      # Segments and squares
      # Create a source of sources. This Data Structure will allow the Drag Tool
      # to navigate through the available axis
      self._sources = ColumnDataSource(dict(active_sources=[]))
      for i in xrange(0, len(self._axis_df['x0'])):
        source = ColumnDataSource(dict(x0=[self._axis_df['x0'][i]],
                                       y0=[self._axis_df['y0'][i]],
                                       x1=[self._axis_df['x1'][i]],
                                       y1=[self._axis_df['y1'][i]],
                                       name=[self._axis_df.index.values[i]]))

        segment = self._figure.segment(x0='x0',
                                       y0='y0',
                                       x1='x1', 
                                       y1='y1',
                                       source=source,
                                       name=self._axis_df.index.values[i],
                                       color=StarCoordinatesView._SEGMENT_COLOR,
                                       line_width=StarCoordinatesView._SEGMENT_WIDTH)
        
        square = self._figure.square(x='x1', 
                                     y='y1',
                                     source=source,
                                     name=self._axis_df.index.values[i],
                                     size=StarCoordinatesView._SQUARE_SIZE, 
                                     color=StarCoordinatesView._SQUARE_COLOR, 
                                     alpha=StarCoordinatesView._SQUARE_ALPHA)

        axis_figure_element = AxisFigureElement(segment, square, source)
        is_visible = not activation_list or i in activation_list
        # Configure visibility without remapping (will be executed afterwards)
        axis_figure_element.visible(is_visible, remap=False)
        if is_visible:
          self._sources.data['active_sources'].append(source)

        self._axis_elements.append(AxisFigureElement(segment, square, source))
        # Axis labels
        labels_dimensions = LabelSet(x='x1', y='y1', text='name', name='name', level='glyph',
                                     x_offset=5, y_offset=5, source=source, 
                                     render_mode='canvas')        
        self._figure.add_layout(labels_dimensions)
        
    def init_points(self, source_points):
      # Mapped points
      self._figure.circle('x', 'y', size=StarCoordinatesView._CIRCLE_SIZE,  
                                    color='color',                                     
                                    alpha=StarCoordinatesView._CIRCLE_ALPHA, 
                                    source=source_points)              
