"""
Copyright (c) 2016-2018, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Sep 26, 2016

@author: jrm
"""
from atom.api import (
   Atom, Event, List, Tuple, Bool, Int, Enum, Typed, ForwardTyped, observe,
   Dict, Str, Float, set_default
)
from enaml.core.declarative import d_
from enaml.colors import ColorMember
from enaml.widgets.control import Control, ProxyControl

from ..shape import BBox


class ViewerSelectionEvent(Atom):
    #: Selected shape or shapes
    selection = List()
    
    #: Parameters such as coodrinates or selection area
    parameters = Tuple()
    
    #: Selection callback parameters
    options = Dict()
    
    
class ProxyOccViewer(ProxyControl):
    """ The abstract definition of a proxy Viewer object.
    """
    #: A reference to the Viewer declaration.
    declaration = ForwardTyped(lambda: OccViewer)

    def set_position(self, position):
        raise NotImplementedError
    
    def set_pan(self, position):
        raise NotImplementedError
    
    def set_background_gradient(self, gradient):
        raise NotImplementedError
    
    def set_rotation(self, rotation):
        raise NotImplementedError
    
    def set_selection_mode(self, mode):
        raise NotImplementedError
    
    def set_selected(self, position):
        raise NotImplementedError
    
    def set_selected_area(self, area):
        raise NotImplementedError
    
    def set_double_buffer(self, enabled):
        raise NotImplementedError
    
    def set_display_mode(self, mode):
        raise NotImplementedError
    
    def set_trihedron_mode(self, mode):
        raise NotImplementedError
    
    def set_view_mode(self, mode):
        raise NotImplementedError
    
    def set_shadows(self, enabled):
        raise NotImplementedError
    
    def set_reflections(self, enabled):
        raise NotImplementedError
    
    def set_antialiasing(self, enabled):
        raise NotImplementedError
    
    def set_lock_rotation(self, locked):
        raise NotImplementedError
    
    def set_lock_zoom(self, locked):
        raise NotImplementedError
    
    def fit_all(self):
        raise NotImplementedError
    
    def fit_selection(self):
        raise NotImplementedError
    
    def take_screenshot(self, filename):
        raise NotImplementedError
    
    def zoom_factor(self, zoom):
        raise NotImplementedError

    
class ProxyOccViewerClippedPlane(ProxyControl):
    #: A reference to the ClippedPlane declaration.
    declaration = ForwardTyped(lambda: OccViewerClippedPlane)
    
    def set_enabled(self, enabled):
        raise NotImplementedError
    
    def set_capping(self, enabled):
        raise NotImplementedError
    
    def set_capping_hashed(self, enabled):
        raise NotImplementedError
    
    def set_capping_color(self, color):
        raise NotImplementedError
    
    def set_position(self, position):
        raise NotImplementedError
    
    def set_direction(self, direction):
        raise NotImplementedError
    

class OccViewer(Control):
    """ A widget to view OpenCascade shapes.
    """
    #: A reference to the ProxySpinBox object.
    proxy = Typed(ProxyOccViewer)
    
    #: Bounding box of displayed shapes. A tuple of the following values
    #: (xmin, ymin, zmin, xmax, ymax, zmax). 
    bbox = d_(Typed(BBox), writable=False)
    
    #: Display mode
    display_mode = d_(Enum('shaded', 'hlr', 'wireframe'))
    
    #: Selection mode
    selection_mode = d_(Enum('shape', 'neutral', 'face', 'edge', 'vertex'))
    
    #: Selected items
    selection = d_(Event(ViewerSelectionEvent), writable=False)
    
    #: View direction
    view_mode = d_(Enum('iso', 'top', 'bottom', 'left', 'right', 'front',
                        'rear'))
    
    #: Selection event
    #reset_view = d_(Event(),writable=False)
    
    #: Show tahedron
    trihedron_mode = d_(Enum('right-lower', 'right-upper', 'left-lower', 
                             'left-upper'))
    
    #: Background gradient
    background_gradient = d_(Tuple(Int(), default=(206, 215, 222,
                                                   128, 128, 128)))
    
    #: Display shadows
    shadows = d_(Bool(False))
    
    #: Display reflections
    reflections = d_(Bool(True))
    
    #: Enable antialiasing
    antialiasing = d_(Bool(True))

    #: View expands freely in width by default.
    hug_width = set_default('ignore')
    
    #: View expands freely in height by default.
    hug_height = set_default('ignore')
    
    #: Lock rotation so the mouse cannot not rotate
    lock_rotation = d_(Bool())
    
    #: Lock zoom so the mouse wheel cannot not zoom
    lock_zoom = d_(Bool())
    
    #: Events
    #: Raise StopIteration to indicate handling should stop
    key_pressed = d_(Event(), writable=False)
    mouse_pressed = d_(Event(), writable=False)
    mouse_released = d_(Event(), writable=False)
    mouse_wheeled = d_(Event(), writable=False)
    mouse_moved = d_(Event(), writable=False)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('position', 'display_mode', 'view_mode', 'trihedron_mode',
             'selection_mode', 'background_gradient', 'double_buffer',
             'shadows', 'reflections', 'antialiasing', 'lock_rotation', 
             'lock_zoom')
    def _update_proxy(self, change):
        """ An observer which sends state change to the proxy.
        """
        # The superclass handler implementation is sufficient.
        super(OccViewer, self)._update_proxy(change)

    # -------------------------------------------------------------------------
    # Viewer API
    # -------------------------------------------------------------------------
    def fit_all(self):
        """ Zoom in and center on all item(s) """
        self.proxy.fit_all()
        
    def fit_selection(self):
        """ Zoom in and center on the selected item(s) """
        self.proxy.fit_selection()
        
    def take_screenshot(self, filename):
        """ Take a screenshot and save it with the given filename """
        self.proxy.take_screenshot(filename)
        
    def zoom_factor(self, factor):
        """ Zoom in by a given factor """
        self.proxy.zoom_factor(factor)


class OccViewerClippedPlane(Control):
    #: A reference to the ProxySpinBox object.
    proxy = Typed(ProxyOccViewerClippedPlane)
    
    #: Enabled
    enabled = d_(Bool(True))
    
    #: Capping
    capping = d_(Bool(True))
    
    #: Hatched
    capping_hatched = d_(Bool(True))
    
    #: Color
    capping_color = d_(ColorMember())
    
    #: Position
    position = d_(Tuple(Float(strict=False), default=(0, 0, 0)))
    
    #: Direction
    direction = d_(Tuple(Float(strict=False), default=(1, 0, 0)))
    
    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('position', 'direction', 'enabled', 'capping', 'capping_hatched', 
             'capping_color')
    def _update_proxy(self, change):
        """ An observer which sends state change to the proxy.
        """
        # The superclass handler implementation is sufficient.
        super(OccViewerClippedPlane, self)._update_proxy(change)
