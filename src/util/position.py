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


from numpy import array

class Position(object):
    def __init__(self, position):
        self._position = array(position)
        
    @property
    def position(self):
        if self._position != None:
            return self._position
        else:
            return None
        
    @position.setter
    def position(self, position):
        self._position = position
        
    @classmethod
    def loadPositionData(cls, positionElement):
        positionElements = positionElement.getElementsByTagName('position')
        if positionElements != None and len(positionElements) != 0:
            positionElement = positionElements[0]
            x = int(positionElement.getAttribute('x'))
            y = int(positionElement.getAttribute('y'))
            return array((x, y))
        else:
            return None