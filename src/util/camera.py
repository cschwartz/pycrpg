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


from numpy import array, floor
import position

class Camera(position.Position):
    def __init__(self, size, player, tilesize = array((32, 32))):
        self._offset = floor(size / tilesize / 2)
        self._player = player
        self._size = size
        self._tilesize = tilesize
        position.Position.__init__(self, self._player.position - self._offset)

        self._player.addObserver(self)
                
    def move(self, direction):
        self._position = self._player.position - self._offset
        
    def is_visible(self, position):
        return self._player.is_visible(position)

    def was_visible(self, position):
        return self._player.was_visible(position)
    
    def notify_observer(self, origin, property, args):
        if property == "move":
            (direction, success) = args
            if success:# and not self.getNoCameraMovementRect(array((3, 3))).contains(self.player.getAbsoluteBoundingBox()):
                self.move(direction)
                                              
          