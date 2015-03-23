# Copyright 2015 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""

======
Map
======

.. currentmodule:: bqplot.map

.. autosummary::
   :toctree: generate/

   Map
"""
from IPython.utils.traitlets import (Unicode, List, Dict, Float, Bool,
                                     Instance, Tuple)
from IPython.html.widgets import DOMWidget, CallbackDispatcher, register, Color

from .scales import ColorScale
from .axes import Axis


@register('bqplot.Map')
class Map(DOMWidget):

    """Class to generate an interactive geographical map.

    Map Drawing Attributes
    ------------------
    min_width: int (default: 800)
        minimum width of the entire map
    min_height: int (default: 600)
        minimum height of the entire map
    fig_margin: dict (default: {top: 0, bottom: 20, left: 0, right: 0}
        margin for the map plot area with respect to the entire display
        area

    Display Attributes
    ------------------
    default_color: Color or None (default: None)
        default color for items of the map when no color data is passed
    tooltip_color: color (default: None)
        color for the background of the tooltip
    text_color: color (default: None)
        color for the text inside a tooltip
    text_format: string (default: '.2f')
        format for the text inside a tooltip
    selected_styles: Dict (default: {'selected_fill': 'Red', 'selected_stroke': None, 'selected_stroke_width': 5.0})
        Dictionary containing the styles for selected subunits
    hovered_styles: Dict (default: {'hovered_fill': 'Orange', 'hovered_stroke': None, 'hovered_stroke_width': 5.0})
        Dictionary containing the styles for hovered subunits

    Data Attributes
    ---------------
    color: Dict or None (default: None)
        dictionary containing the data associated with every country for the
        color scale

    Other Attributes
    ----------------
    selected: List (default: [])
        list containing the selected countries in the map
    enable_select: bool (default: True)
        boolean to control the ability to select the countries of the map by
        clicking
    enable_hover: bool (default: True)
        boolean to control if the map should be aware of which country is being
        hovered on. If it is set to False, tooltip will not be displayed
    text_data: Dict or None (default: None)
        dictionary containing the text data associated with every country for
        the tooltip
    color_scale: ColorScale or None (default: None)
        ColorScale Instance for the color of each country in the map. Required
        when color data is passed
    axis: ColorAxis or None (default: None)
        ColorAxis Instance if one needs to be displayed
    display_tooltip: bool (default: True)
        boolean to control whether tooltips are displayed or not
    map_data: tuple (default: ("worldmap", "nbextensions/bqplot/WorldMapData")
        tuple containing which map is to be displayed
    """
    fig_margin = Dict(dict(top=0, bottom=20, left=0, right=0), sync=True)   # Margin with respect to the parent. Width, height etc are determined by this
    min_width = Float(800.0, sync=True)
    min_height = Float(600.0, sync=True)

    enable_hover = Bool(True, sync=True)
    hovered_styles = Dict({'hovered_fill': 'Orange', 'hovered_stroke': None,
                           'hovered_stroke_width': 5.0}, allow_none=True, sync=True)

    stroke_color = Color(sync=True, allow_none=True)
    default_color = Color(sync=True, allow_none=True)
    color = Dict(sync=True)
    color_scale = Instance(ColorScale, sync=True)

    enable_select = Bool(True, sync=True)
    selected = List([], sync=True)
    selected_styles = Dict({'selected_fill': 'Red', 'selected_stroke': None,
                            'selected_stroke_width': 5.0}, allow_none=True, sync=True)

    axis = Instance(Axis, sync=True)

    tooltip_color = Color('White', sync=True)
    display_tooltip = Bool(True, sync=True)
    text_data = Dict(sync=True)
    text_color = Color('Black', sync=True)
    tooltip_format = Unicode('.2f', sync=True)
    tooltip_widget = Instance(DOMWidget, sync=True)

    map_data = Tuple(Unicode, Unicode, default_value=("worldmap",
                                                      "nbextensions/bqplot/WorldMapData"), sync=True)

    def __init__(self, **kwargs):
        """Constructor for WorldMapWidget"""
        super(Map, self).__init__(**kwargs)
        self._ctrl_click_handlers = CallbackDispatcher()
        self._hover_handlers = CallbackDispatcher()
        self.on_msg(self._handle_button_msg)

    def on_ctrl_click(self, callback, remove=False):
        self._ctrl_click_handlers.register_callback(callback, remove=remove)

    def on_hover(self, callback, remove=False):
        self._hover_handlers.register_callback(callback, remove=remove)

    def _handle_button_msg(self, _, content):
        if content.get('event', '') == 'click':
            self._ctrl_click_handlers(self, content)
        if content.get('event', '') == 'hover':
            self._hover_handlers(self, content)

    _view_name = Unicode('Map', sync=True)
    _view_module = Unicode('nbextensions/bqplot/Map', sync=True)
