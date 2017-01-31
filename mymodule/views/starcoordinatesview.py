"""
    STAR COORDINATES VIEW
"""

from __future__ import division
from os import path
import random
from sympy import Point, Segment
from math import cos, sin, radians
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, show
from bokeh.models import Label, ColumnDataSource, LabelSet, HoverTool, WheelZoomTool, PanTool, PolySelectTool

from ..model.axis import Axis

from ..model.mapper.starmapper import StarMapper
from ..io.reader import Reader
from ..util.axisgenerator import AxisGenerator
from ..util.dfmatrixutils import DFMatrixUtils

class StarCoordinatesView(object):
    """A view with all the necessary logic for displaying it on bokeh"""
    def __init__(self, file_path, random_weights=True, width=600, height=400):
        super(StarCoordinatesView, self).__init__()
        self._file_path = file_path
        self._random_weights = random_weights
        self._width = width
        self._height = height

    def run(self):
        ## INTERNAL MAPPING  ##
        output_notebook()
        reader = Reader.init_from_file(self._file_path)
        dimension_labels = reader.get_dimension_labels()
        dimension_values_df = reader.get_dimension_values()
        axis_df = AxisGenerator.generate_star_axis(dimension_labels, 
                                                   random_weights=self._random_weights)

        # Map points using vectors from the axis
        vectors_df = DFMatrixUtils.get_vectors(axis_df)
        mapped_points = StarMapper().map_points(vectors_df, dimension_values_df)

        ## PLOT IN BOKEH ##

        # Create sources from axis and mapped data
        # Dimension related data (axis)
        source_dimensions = ColumnDataSource(data=dict(x=axis_df['x1'],
                                            y=axis_df['y1'],
                                            names=axis_df.index))

        labels_dimensions = LabelSet(x='x', y='y', text='names', level='glyph',
                      x_offset=5, y_offset=5, source=source_dimensions, render_mode='canvas')

        mapped_points_x = []
        mapped_points_y = []

        for mpx, mpy in mapped_points:
            mapped_points_x.append(mpx)
            mapped_points_y.append(mpy)

        # Point related data (products)
        source_points = ColumnDataSource(data=dict(x=mapped_points_x,
                                            y=mapped_points_y,
                                            names=dimension_values_df.index))

        labels_points = LabelSet(x='x', y='y', text='names', level='glyph',
                      x_offset=5, y_offset=5, source=source_points, render_mode='canvas')

        # Define fields that will appear when hovering over an element
        hover = HoverTool(
                tooltips=[
                    ("name", "@names")
                ]
            )

        TOOLS = 'box_zoom,box_select,resize,reset'

        # Generate figure and add elements
        p = figure(width=self._width, height=self._height, tools=[WheelZoomTool(), PanTool(), hover])

        p.segment(x0=axis_df['x0'], y0=axis_df['y0'], x1=axis_df['x1'], y1=axis_df['y1'], color="#F4A582", line_width=2)
        p.square('x', 'y', size=7, color="#74ADD1", alpha=0.5, source=source_dimensions)

        """ Alternative:
        for index, row in axis_df.iterrows():
            p.segment(x0=row['x0'], y0=row['y0'], x1=row['x1'], y1=row['y1'], color="#F4A582", line_width=2)
            p.square(x=row['x1'], y=row['y1'], size=7, color="#74ADD1", alpha=0.5)
            label = Label(x=row['x1'], y=row['y1'], x_units='screen', y_units='screen', text=index, render_mode='css',
              border_line_color='black', border_line_alpha=1.0,
              background_fill_color='white', background_fill_alpha=1.0)
        """

        p.add_layout(labels_dimensions)
        p.circle('x', 'y', size=5, color="navy", alpha=0.5, source=source_points)

        show(p)
