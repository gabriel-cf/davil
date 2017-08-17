##################################################
######THIS DOES NOT WORK IN > Bokeh 0.12.3########
###Due to a change in the CoffeeScript compiler###
##################################################

from bokeh.models import Tool, ColumnDataSource
from bokeh.core.properties import Instance
from bokeh.models.renderers import GlyphRenderer


class DragTool(Tool):
    __implementation__ = """
GestureTool = require "models/tools/gestures/gesture_tool"
p = require "core/properties"
class DragToolView extends GestureTool.View
  active_source = null
  initialize: (options) ->
    super(options)
    @listenTo(@model, 'change:active', @_active_change)

  _pan_start: (e) ->
    frame = @plot_model.frame
    canvas = @plot_view.canvas
    vx = canvas.sx_to_vx(e.bokeh.sx)
    vy = canvas.sy_to_vy(e.bokeh.sy)
    x = frame.x_mappers['default'].map_from_target(vx)
    y = frame.y_mappers['default'].map_from_target(vy)
    min_distance = null
    closer_source = null
    active_sources = @model.sources.data.active_sources
    for i in [0..active_sources.length - 1]
      a = x - active_sources[i].data.x1
      b = y - active_sources[i].data.y1
      d = Math.sqrt(a**2 + b**2)
      if (min_distance == null || d < min_distance)
        min_distance = d
        closer_source = active_sources[i]
    active_source = closer_source
    return null

  _pan: (e) ->
    frame = @plot_model.frame
    canvas = @plot_view.canvas
    vx = canvas.sx_to_vx(e.bokeh.sx)
    vy = canvas.sy_to_vy(e.bokeh.sy)
    x = frame.x_mappers['default'].map_from_target(vx)
    y = frame.y_mappers['default'].map_from_target(vy)
    active_source.data.x1[0] = x
    active_source.data.y1[0] = y

    active_source.trigger('change')

  _pan_end: (e) ->
    @model.remap_square.glyph.name = active_source.data['name'][0]
    @model.remap_square.glyph.x = active_source.data['x1'][0]
    @model.remap_square.glyph.y = active_source.data['y1'][0]
    @model.remap_square.visible = !@model.remap_square.visible
    @model.remap_square.trigger('change')

    return null

class DragTool extends GestureTool.Model
  default_view: DragToolView
  type: "DragTool"
  tool_name: "Drag Span"
  icon: "bk-tool-icon-lasso-select"
  event_type: "pan"
  default_order: 12
  @define {
      sources:                [ p.Instance ]
      remap_square:           [ p.Instance ]
    }
module.exports =
  Model: DragTool
  View: DragToolView
    """

    sources = Instance(ColumnDataSource)
    remap_square = Instance(GlyphRenderer)
