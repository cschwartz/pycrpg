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


class Mode(object):
    Move = 0
    Look = 1
    Use = 2
    
    def __init__(self, mode):
        self._mode = mode

    def __str__(self):
        if self._mode == Mode.Move:
            return "Move"
        elif self._mode == Mode.Look:
            return "Look"
        elif self._mode == Mode.Use:
            return "Use"
        
Move = Mode(Mode.Move)
Look = Mode(Mode.Look)
Use = Mode(Mode.Use)