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

from renderable import tile

import numpy
    
class Map(object):
    def __init__(self, (width, height), tileManager):
        self._tileManager = tileManager
        self._width = width
        self._height = height

        self.map = [[None for x in xrange(width)] for y in xrange(height)]
        
        self._black_surface = pygame.surface.Surface(tileManager.tilesize, masks = pygame.SRCALPHA)
        self._black_surface.set_alpha(128)
                        
    def __getitem__(self, position):
        return self.map[position[1]][position[0]]
    
    def __setitem__(self, position, value):
        self.map[position[1]][position[0]] = value
        
    def setCamera(self, camera):
        self.camera = camera
        
    def render(self, target):
        for y in xrange(self._height):
            for x in xrange(self._width):
                tile = self.map[y][x]
                if tile != None:
                    tile.render(target, self.camera)
                    if not self.camera.is_visible(tile.position) and self.camera.was_visible(tile.position):
                        target.blit(self._black_surface, (tile.size * (tile._position - self.camera.position)))
        
    def mayEntityMoveTo(self, entity, direction):
        position = entity.position
        originTile = self[position]
        position = direction.moveFrom(position)
        destinationTile = self[position]
        if destinationTile != None:
            entityIsInOrigin = originTile.hasEntity(entity)
            entityMayEnter = destinationTile.mayEnter(entity)
            return (entityIsInOrigin and entityMayEnter, originTile, destinationTile)
        else:
            return (False, originTile, None)
        
    def moveEntityTo(self, entity, direction):
        (validMove, originTile, destinationTile) = self.mayEntityMoveTo(entity, direction)
        if validMove:
            originTile.leave(entity)
            destinationTile.enter(entity)
            
        return validMove
    
    
    def save(self, document, parent):
        mapElement = document.createElement('map')
        parent.appendChild(mapElement)
        mapElement.setAttribute('width', str(self._width))
        mapElement.setAttribute('height', str(self._height))
        for y in xrange(self._height):
            for x in xrange(self._width):
                if self.map[y][x] != None:
                    self.map[y][x].save(document, mapElement)
                    
    @classmethod
    def load(cls, mapElement, engine, tileManagers):
        width = int(mapElement.getAttribute('width'))
        height = int(mapElement.getAttribute('height'))
        tilemap = mapElement.getAttribute('tilemap')
        tileManager = tileManagers['floor']
        map =  Map((width, height), tileManager)
        
        #parse tiles
        for tileElement in mapElement.getElementsByTagName('tile'):
            tile.Tile.load(tileManager, tileElement, map)
            
        return map
    
    def costFunc(self, position):
        tile = self[position[0], position[1]]
        if tile == None:
            return numpy.inf
        elif not tile.mayEnter(None):
            return numpy.inf
        else:
            return 1