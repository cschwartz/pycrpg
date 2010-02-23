'''
    This file is part of pyCRPG
    Copyright (C) 2010 Christian Schwartz

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

    @author: Christian Schwartz
'''


import renderable
from enum import direction

class Cursor(renderable.Renderable):
    def __init__(self, surface, player):
        renderable.Renderable.__init__(self, surface, player.position)
        
        self._surface.set_alpha(128)
        self._do_show = False
        self._player = player
        
        self._relativePosition = direction.NoDirection

    @property
    def do_show(self):
        return self._do_show
    
    @do_show.setter
    def do_show(self, doShow):
        self._do_show = doShow
        print doShow
    
    @property
    def relative_position(self):
        return self._relativePosition
    
    def reset_to_player(self):
        self._position = self._player.position
        self._relativePosition = direction.NoDirection
    
    def render(self, target, offset):
        if self._do_show:
            target.blit(self._surface, (self._position + self._relativePosition.offset - offset) * self._size)
    
    def move(self, newDirection):
        if newDirection == self._relativePosition.opposite():
            self._relativePosition = direction.NoDirection
        else:
            self._relativePosition = newDirection             