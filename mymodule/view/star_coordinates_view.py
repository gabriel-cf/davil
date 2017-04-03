"""
    STAR COORDINATES VIEW
"""

from __future__ import division
from bokeh.layouts import row, column
from bokeh.plotting import figure
from bokeh.models import Label, ColumnDataSource, LabelSet, HoverTool, WheelZoomTool, PanTool, PolySelectTool, TapTool, ResizeTool, SaveTool, ResetTool

from ..backend.io.reader import Reader
from ..backend.util.axis_generator import AxisGenerator
from ..backend.util.df_matrix_utils import DFMatrixUtils

from ..frontend.model.controllers.mapper_controller import MapperController
from ..frontend.model.controllers.cluster_controller import ClusterController
from ..frontend.model.controllers.file_controller import FileController
from ..frontend.model.controllers.point_size_controller import PointSizeController
from ..frontend.model.controllers.error_controller import ErrorController
from ..frontend.model.controllers.axis_color_controller import AxisColorController
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
    def __init__(self, alias, file_path, random_weights=False, width=600, height=600):
        """Creates a new Star Coordinates View object and instantiates
           its elements
        """
        self._alias = alias
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
        self._layout = None
        self._drag_tool_sources = None
        self._sources_list = []
        self._axis_elements = dict()
        self._square_mapper = None
        self._source_points = None
        self._mapped_points = None
        self._checkboxes = None
        self._table_widget = None
        # Controllers
        self._mapper_controller = None
        self._cluster_controller = None
        self._file_controller = None
        self._axis_checkboxes = None
        self._point_size_controller = None
        self._error_controller = None
        self._axis_color_controller = None
        # Logic to initialize all the elements above
        self._init()

    # Private methods
    def _execute_mapping(self):
        self._mapped_points = self._mapper_controller.execute_mapping()
        self._execute_error_recalc()
    
    def _execute_error_recalc(self):
        mapped_points_df = self._mapper_controller.get_mapped_points()
        self._error_controller.calculate_error(self._dimension_values_df_norm,
                                               self._vectors_df,
                                               mapped_points_df)
        self._point_size_controller.update_sizes()

    def _update_layout(self):
        row1 = None
        row2 = None
        if self._checkboxes:
            row1 = row(self._figure, self._checkboxes.get_widget())
        else:
            row1 = row(self._figure)
        if self._table_widget:
            row2 = row(self._table_widget)
            self._layout = column(row1, row2)
        self._layout = row1

    # PUBLIC methods available to the model

    # UPDATE methods
    def update_mapping_algorithm(self, new):
        print "Updating mapping algorithm to {}".format(new)
        self._mapper_controller.update_algorithm(new)
        self._execute_mapping()

    def update_clustering_algorithm(self, new):
        print "Updating clustering algorithm to {}".format(new)
        self._cluster_controller.update_algorithm(new)
        self._cluster_controller.update_clusters(self._dimension_values_df_norm)

    def update_error_algorithm(self, new):
        print "Updating error algorithm to {}".format(new)
        self._error_controller.update_algorithm(new)
        self._execute_error_recalc()

    def update_axis_for_color(self, new):
        print "Updating base axis for color to {}".format(new)
        self._axis_color_controller.update_colors(new)

    def update_palette(self, new):
        self._axis_color_controller.update_palette(new)

    def update_axis_visibility(self, axis_id, is_visible):
        if not axis_id in self._axis_elements:
            ValueError("Could not update the visibility of the axis '{}'\
                        because it is not a valid axis".format(axis_id))
        self._mapper_controller.update_axis_status(axis_id, is_visible)
        if self._axis_elements[axis_id].visible(is_visible):
            self._execute_mapping()

    def update_initial_size_input(self, new):
        self._point_size_controller.set_initial_size(int(new))

    def update_final_size_input(self, new):
        self._point_size_controller.set_final_size(int(new))    

    # GET methods
    def get_alias(self):
      return self._alias

    def get_mapping_algorithm(self):
        return self._mapper_controller.get_active_algorithm_id()

    def get_mapping_options(self):
        return self._mapper_controller.get_all_options()

    def get_clustering_algorithm(self):
        return self._cluster_controller.get_active_algorithm_id()

    def get_clustering_options(self):
        return self._cluster_controller.get_all_options()

    def get_error_algorithm(self):
        return self._error_controller.get_active_algorithm_id()

    def get_error_options(self):
        return self._error_controller.get_all_options()

    def get_axis_status(self):
        """Returns a zipped list of [(axis_id, visible), ..]"""
        return self._mapper_controller.get_axis_status()

    def get_initial_size(self):
        return self._point_size_controller.get_initial_size()

    def get_final_size(self):
        return self._point_size_controller.get_final_size()

    def get_file(self):
        return self._file_controller.get_active_file()

    def get_available_files(self):
        return self._file_controller.get_available_files()

    def get_dimension_values_df(self):
        return self._dimension_values_df

    def get_available_axis_ids(self):
        return self._dimension_values_df_norm.columns.tolist()

    def get_available_palettes(self):
        return self._axis_color_controller.get_available_palettes()

    def get_layout(self, update=False):
        if update:
            self._update_layout()
        return self._layout

    def set_checkboxes(self, checkboxes):
        self._checkboxes = checkboxes
        self._checkboxes.update_view(self)
        self._update_layout()

    def set_table(self, table):
        self._table_widget = table
        self._update_layout()

    def init_square_mapper(self):
        def remap(attr, old, new):
            print "REMAP - DRAG && DROP"
            print self._square_mapper.glyph.name
            print self._square_mapper.glyph.x
            print self._square_mapper.glyph.y
            modified_axis_id = self._square_mapper.glyph.name
            self._mapper_controller.update_vector_values(modified_axis_id, self._square_mapper.glyph.x, self._square_mapper.glyph.y)
            # We need to manually update the source's value on the python's side
            #                                :(
            for source in self._sources_list:
                if source.data['name'][0] == modified_axis_id:
                    source.data['x1'][0] = self._square_mapper.glyph.x
                    source.data['y1'][0] = self._square_mapper.glyph.y
            self._execute_mapping()

        square = self._figure.square(x=0, y=0, name='remap', size=0)
        square.on_change('visible', remap)
        return square

    def redraw(self):
        # Redraw plot
        self._figure = self.init_figure()
        # Add tools to new plot
        self._figure.add_tools(DragTool(sources=self._drag_tool_sources,
                                        remap_square=self._square_mapper))
        # Redraw axis elements
        for source in self._sources_list:
            name = source.data['name'][0]
            is_visible = self._mapper_controller.is_axis_visible(name)
            self.add_axis_element(source, name, is_visible)
        # Redraw points    
        self.init_points(self._source_points)

    def _init(self):
        """Load data from file and initialize dataframe values"""
        self._file_controller = FileController(self._file_path)
        self._reader = Reader.init_from_file(self._file_controller.get_active_file())
        # Get the dimension labels (i.e. the names of the columns with numeric values)
        self._dimension_values_df, self._dimension_values_df_norm = self._reader.get_dimension_values()
        axis_ids = self._dimension_values_df_norm.columns.values.tolist()
        self._axis_df = AxisGenerator.generate_star_axis(axis_ids,
                                                         random_weights=self._random_weights)
        # Get the vector dataframe from the axis dataframe
        self._vectors_df = DFMatrixUtils.get_vectors(self._axis_df)

        # Initialize figure and axis
        self._figure = self.init_figure()
        self._sources_list = self.init_axis()        

        # Add our custom drag and drop tool for resizing axis
        self._drag_tool_sources = self.generate_drag_tool_sources(self._sources_list)
        self._square_mapper = self.init_square_mapper()
        self._figure.add_tools(DragTool(sources=self._drag_tool_sources,
                                        remap_square=self._square_mapper))
        # Initial mapping
        # Define the points source from the mapped values
        self._mapper_controller = MapperController(self._dimension_values_df_norm,
                                                   self._vectors_df)
        mapped_points_df = self._mapper_controller.execute_mapping()
        self._source_points = ColumnDataSource(mapped_points_df)
        self._source_points.add(mapped_points_df.index, name='name')
        # We assign to the mapper controller the animator
        mapping_animator = MappingAnimator(self._source_points)
        self._mapper_controller.update_animator(mapping_animator)

        self._cluster_controller = ClusterController(source=self._source_points)
        self._cluster_controller.update_clusters(self._dimension_values_df_norm)

        self._error_controller = ErrorController(self._source_points, self._sources_list,
                                                 algorithm_id=ErrorController.ABSOLUTE_SUM_ID)
        self._error_controller.calculate_error(self._dimension_values_df_norm,
                                               self._vectors_df,
                                               mapped_points_df)

        self._point_size_controller = PointSizeController(self._source_points)
        self._point_size_controller.update_sizes()

        self._axis_color_controller = AxisColorController(self._source_points, 
                                                          self._dimension_values_df_norm)

        self.init_points(self._source_points)
        self._layout = row(self._figure)

    def init_figure(self):
        """Updates the visual elements on the figure"""
        wheel_zoom_tool = WheelZoomTool()
        pan_tool = PanTool()
        resize_tool = ResizeTool()
        save_tool = SaveTool()
        reset_tool = ResetTool()
        figure_ = figure(tools=[wheel_zoom_tool, pan_tool, resize_tool, save_tool, reset_tool])
        figure_.toolbar.active_scroll = wheel_zoom_tool
        hover = HoverTool(
            tooltips=[
                ("name", "@name"),
                ("error", "@error")
            ])
        figure_.add_tools(hover)
        return figure_

    def generate_drag_tool_sources(self, axis_sources):
        """Create a source of sources. This Data Structure will allow the Drag Tool
           to go through all the available axis
        """
        drag_tool_sources = ColumnDataSource(dict(active_sources=[]))
        drag_tool_sources.data['active_sources'] = [source for source in axis_sources]
        return drag_tool_sources

    def add_axis_element(self, source, name, is_visible):
        segment = self._figure.segment(x0='x0',
                                       y0='y0',
                                       x1='x1',
                                       y1='y1',
                                       name=name,
                                       color='color',
                                       line_width='line_width',
                                       source=source)

        square = self._figure.square(x='x1',
                                     y='y1',
                                     source=source,
                                     name=name,
                                     size=StarCoordinatesView._SQUARE_SIZE,
                                     color=StarCoordinatesView._SQUARE_COLOR,
                                     alpha=StarCoordinatesView._SQUARE_ALPHA)

        axis_figure_element = AxisFigureElement(segment, square)
        axis_figure_element.visible(is_visible)
        self._axis_elements[axis_figure_element.get_identifier()] = axis_figure_element
        # Axis labels (name of their associated column)
        labels_dimensions = LabelSet(x='x1', y='y1', text='name', name='name', level='glyph',
                                     x_offset=5, y_offset=5, source=source,
                                     render_mode='canvas')
        self._figure.add_layout(labels_dimensions)


    def init_axis(self, activation_list=None):
        """Will render all axis (Segment, Square and Label) creating
           for each one a source and an AxisFigureElement

           [activation_list=None]: list with axis indexes to be visible
                                   by default. If none is specified, all
                                   of them will be visible

           Returns: (ColumnDataSource[]) list of sources (where each
                        source is the base source of one axis)
                    (AxisFigureElement[]) list of generated axis elements
        """
        sources_list = []
        # Segments and squares
        for i in xrange(0, len(self._axis_df['x0'])):
            x0 = self._axis_df['x0'][i]
            y0 = self._axis_df['y0'][i]
            x1 = self._axis_df['x1'][i]
            y1 = self._axis_df['y1'][i]
            error = 0
            name = self._axis_df.index.values[i]
            source = ColumnDataSource(dict(x0=[x0],
                                           y0=[y0],
                                           x1=[x1],
                                           y1=[y1],
                                           name=[name],
                                           error=[error],
                                           color=[StarCoordinatesView._SEGMENT_COLOR],
                                           line_width=[StarCoordinatesView._SEGMENT_WIDTH]))
            is_visible = not activation_list or i in activation_list
            axis_figure_element = self.add_axis_element(source, name, is_visible)
            # Add source to the list of sources for the error calculation upon axis
            sources_list.append(source)

        return sources_list

    def init_points(self, source_points):
        # Mapped points
        self._figure.circle('x',
                            'y',
                            size='size',
                            color='color',
                            alpha=StarCoordinatesView._CIRCLE_ALPHA,
                            source=source_points)
