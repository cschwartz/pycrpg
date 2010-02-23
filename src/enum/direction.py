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
import random

class Direction(object):
    NoDirection = 0
    Up = 1
    Right = 2
    Down = 3
    Left = 4
    
    def __init__(self, newDirection):
        self._direction = newDirection
        
    def moveFrom(self, position):
        newPosition = position.copy()
        if self._direction == Direction.Right:
            newPosition[0] += 1
        elif self._direction == Direction.Left:
            newPosition[0] -= 1
        elif self._direction == Direction.Up:
            newPosition[1] -= 1
        elif self._direction == Direction.Down:
            newPosition[1] += 1
        
        return newPosition
    
    def opposite(self):
        if self._direction == Direction.NoDirection:
            return NoDirection
        elif self._direction == Direction.Up:
            return Down
        elif self._direction == Direction.Right:
            return Left
        elif self._direction == Direction.Down:
            return Up
        elif self._direction == Direction.Left:
            return Right
    
    @property
    def offset(self):
        offset = None
        if self._direction == Direction.NoDirection:
            offset = array((0, 0))
        elif self._direction == Direction.Up:
            offset = array((0, -1))
        elif self._direction == Direction.Down:
            offset = array((0, 1))
        elif self._direction == Direction.Right:
            offset = array((1, 0))
        elif self._direction == Direction.Left:
            offset = array((-1, 0))
            
        return offset
    
    @classmethod
    def random(cls):
        rnd = random.randint(0, 4)
        if rnd == 0:
            return NoDirection
        elif rnd == 1:
            return Up
        elif rnd == 2:
            return Right
        elif rnd == 3:
            return Down
        elif rnd == 4:
            return Left
        
        
    
    def __str__(self):
        if self._direction == Direction.Up:
            return "Up"
        elif self._direction == Direction.Right:
            return "Right"
        elif self._direction == Direction.Down:
            return "Down"
        elif self._direction == Direction.Left:
            return "Left"
        elif self._direction == Direction.NoDirection:
            return "No Direction"

NoDirection = Direction(0)
Up = Direction(1)
Right = Direction(2)
Down = Direction(3)
Left = Direction(4)

Directions = [Up, Right, Down, Left]