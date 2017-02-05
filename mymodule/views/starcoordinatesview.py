"""
    STAR COORDINATES VIEW
"""

from __future__ import division
from os import path
import random
from math import cos, sin, radians
from bokeh.layouts import widgetbox, row
from bokeh.io import output_notebook, curdoc, show, push_notebook
from bokeh.plotting import figure, show
from bokeh.models import Label, ColumnDataSource, LabelSet, HoverTool, WheelZoomTool, PanTool, PolySelectTool, TapTool, CustomJS
from bokeh.models.widgets import CheckboxGroup 
from bokeh.models.layouts import HBox

from ..model.mapper.starmapper import StarMapper
from ..io.reader import Reader
from ..util.axisgenerator import AxisGenerator
from ..util.dfmatrixutils import DFMatrixUtils

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
    def __init__(self, file_path, random_weights=False, r=1, width=600, height=400):
        self._random_weights = random_weights
        self._width = width
        self._height = height
        self._file_path = file_path
        self._reader = None
        self._figure = None
        # Generated from mapping
        self._axis_df = None
        self._dimension_values_df = None
        self._vectors_df = None
        self._mapped_points = None
        # Figure elements
        self._segments = []
        self._points = []
        self._squares = []
        self._checkboxes = None #Checkboxes
        self._row_plot = None
        self._source_points = None
        self._circle_glyph = None

    def get_filtered_mapping_df(self, ignored_axis_col_indexes):
      # Retrieve axis ids (names of the columns)
      ignored_axis_ids = self._dimension_values_df.columns[[ignored_axis_col_indexes]]
      dimension_values_df_cp = self._dimension_values_df.copy()
      vectors_df_cp = self._vectors_df.copy()
      # In dimension they appear as columns and in vectors as indexes
      dimension_values_df_cp.drop(ignored_axis_ids, axis=1, inplace=True)
      vectors_df_cp.drop(ignored_axis_ids, axis=0, inplace=True)

      return dimension_values_df_cp, vectors_df_cp

    def execute_mapping(self, 
                       ignored_axis_col_indexes = None):
        """Will recalculate the mapping for te points"""
        dimension_values_df = self._dimension_values_df
        vectors_df = self._vectors_df
        if not ignored_axis_col_indexes is None:
          dimension_values_df, vectors_df = self.get_filtered_mapping_df(ignored_axis_col_indexes)
        
        self._mapped_points = StarMapper().map_points(dimension_values_df, 
                                                      vectors_df)


        if self._source_points is None:
          self._source_points = ColumnDataSource(self._mapped_points)
          self._source_points.add(self._mapped_points.index, name='names')
        else:
          self._source_points.data['x'] = self._mapped_points['x']
          self._source_points.data['y'] = self._mapped_points['y']

        if self._circle_glyph is None:
          self._circle_glyph = self._figure.circle('x', 'y', size=StarCoordinatesView._CIRCLE_SIZE, 
                                        color=StarCoordinatesView._CIRCLE_COLOR, 
                                        alpha=StarCoordinatesView._CIRCLE_ALPHA, 
                                        source=self._source_points)
          self._circle_glyph.data_source = self._source_points

    def init_checkboxes(self):
      cb_group = CheckboxGroup(
        labels=self._axis_df.index.tolist(),
        active=[i for i in xrange(0, len(self._axis_df.index))])

      def update_axis_checkbox(new):
        print "Updating axis: {}".format(cb_group.active)
        switch = cb_group.active
        ignored_axis_col_indexes = []
        for i in xrange(0, len(self._segments)):
            if i in switch:
              self._segments[i].visible = True 
              self._squares[i].visible = True
            else:
              self._segments[i].visible = False 
              self._squares[i].visible = False
              ignored_axis_col_indexes.append(i)

        self.execute_mapping(ignored_axis_col_indexes=ignored_axis_col_indexes)
        push_notebook()


      cb_group.on_click(update_axis_checkbox)
      return cb_group

    def init(self):
        """Load data from file and initialize dataframe values
            Can be used to reset the original values
        """
        self._figure = figure(width=self._width, height=self._height, 
                              tools=[WheelZoomTool(), PanTool()])

        if self._reader is None:
            self._reader = Reader.init_from_file(self._file_path)
        # Get the dimension labels (i.e. the names of the columns with numeric values)
        self._dimension_values_df = self._reader.get_dimension_values()
        self._axis_df = AxisGenerator.generate_star_axis(self._dimension_values_df.columns.values, 
                                                   random_weights=self._random_weights)

        # Map points using vectors from the axis
        self._vectors_df = DFMatrixUtils.get_vectors(self._axis_df)#(axis_df_filtered)

        hover = HoverTool(
                tooltips=[
                    ("name", "@names")
                ]
            )
        self._figure.add_tools(hover)
        cb_group = self.init_checkboxes()
        
        self._row_plot = row(self._figure, widgetbox(cb_group), width=1000)
        curdoc().add_root(self._row_plot)
        curdoc().title = "Star Coordinates"
        output_notebook()

    def update_figure(self):
        """Updates the visual elements on the figure"""

        self._segments = []
        self._squares = []
        self._points = []
        # Segments and squares
        for i in xrange(0, len(self._axis_df['x0'])):
            self._segments.append(self._figure.segment(x0=self._axis_df['x0'][i], 
                                                       y0=self._axis_df['y0'][i], 
                                                       x1=self._axis_df['x1'][i], 
                                                       y1=self._axis_df['y1'][i],
                                                       name=self._axis_df.index.values[i], 
                                                       color=StarCoordinatesView._SEGMENT_COLOR, 
                                                       line_width=StarCoordinatesView._SEGMENT_WIDTH))

            self._squares.append(self._figure.square(x=self._axis_df['x1'][i], 
                                                     y=self._axis_df['y1'][i],
                                                     size=StarCoordinatesView._SQUARE_SIZE, 
                                                     color=StarCoordinatesView._SQUARE_COLOR, 
                                                     alpha=StarCoordinatesView._SQUARE_ALPHA))

        source_dimensions = ColumnDataSource(self._axis_df)
        source_dimensions.add(self._axis_df.index, name='names')
        labels_dimensions = LabelSet(x='x1', y='y1', text='names', level='glyph',
                                     x_offset=5, y_offset=5, source=source_dimensions, 
                                     render_mode='canvas')

        self._figure.add_layout(labels_dimensions)

    def update_weights(self, show=True):
        # Update weights
        self.execute_mapping()
        if show:
            self.update_figure()

    def update_vectors(self, show=True):
        # Update vectors
        self.execute_mapping()
        if show:
            self.update_figure()

    def update_axis(self, **kwargs):
            print "updating plot"
            for x in xrange(0, len(self._segments)):
                self._segments[x].visible = kwargs[self._segments[x].name]
                self._squares[x].visible = self._segments[x].visible

            push_notebook()

    def run(self):
        if self._figure is None:
            self.init()

        self.execute_mapping()
        self.update_figure()
