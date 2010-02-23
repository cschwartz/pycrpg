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


import pygame

from util import position

class Renderable(position.Position):
    def __init__(self, surface, renderablePosition):
        position.Position.__init__(self, renderablePosition)
        self._surface = surface
        self._size = surface.get_size()    
        
        self.overlays = []
        
    def render(self, target, offset):
        if self._position != None:
            target.blit(self._surface, (self._size * (self._position - offset)))
            for (displayTill, overlaySurface) in self.overlays:
                target.blit(overlaySurface, (self._size * (self._position - offset)))
    
    def getAbsoluteBoundingBox(self):
        return pygame.Rect((self._size * self._position), self._size)
    
    @classmethod
    def loadRenderableData(cls, renderableElement):
        return position.Position.loadPositionData(renderableElement)
    
    @property
    def size(self):
        return self._size
    
    def add_overlay(self, displayTill, surface):
        self.overlays.append((displayTill, surface))
    
    def update(self, newTime):
        for (displayTill, surface) in self.overlays:
            if displayTill < newTime:
                self.overlays.remove((displayTill, surface))