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
from numpy import array

import xml, xml.dom.minidom

class TileManager(object):
    def __init__(self, filename, tilesize = (32, 32), colorkey = (0, 0, 0), inline = False):
        if not inline:
            tileSource = pygame.image.load('../gfx/' + filename).convert()
        else:
            tileSource = pygame.image.load('../gfx/' + filename).convert_alpha()
        self.tiles = {}
        self._tilesize = tilesize
        index = 0
        for y in range(tileSource.get_height() / tilesize[1]):
            for x in range(tileSource.get_width() / tilesize[0]):
                tile = None
                if inline:
                    tile = pygame.Surface(tilesize, pygame.SRCALPHA, 32)
                else:
                    tile = pygame.Surface(tilesize)
                    tile.set_colorkey(colorkey)
                
                tile.blit(tileSource, (0, 0), ((array((x, y)) * tilesize), tilesize))
                
                self.tiles[index] = tile
                index = index+1
    
    @property            
    def tilesize(self):
        return self._tilesize
                
    def __getitem__(self, index):
        return self.tiles[index]
    
class TileManagerProvider(object):
    def __init__(self, directory, tileSize = (32, 32)):
        self._tileManagers = {}
        self._tileSize = tileSize
        self._directory = directory
        
    def __getitem__(self, index):
        if index in self._tileManagers:
            return self._tileManagers[index]
        else:
            tileManager = self._loadTileManager(index)
            self._tileManagers[index] = tileManager
            return tileManager
        
    def _loadTileManager(self, type):
        dom = xml.dom.minidom.parse('../' + self._directory + '/' + type + '.xml')
        tileElement = dom.firstChild
        textureName = tileElement.getAttribute('filename')
        if tileElement.hasAttribute('alpha') and tileElement.getAttribute('alpha') == "inline":
            return TileManager(textureName, self._tileSize, inline = True)
        else:
            colorKeyR = None
            colorKeyG = None
            colorKeyB = None
            for childNode in tileElement.childNodes:
                if childNode.nodeType == xml.dom.Node.ELEMENT_NODE:
                    if childNode.localName == 'colorKey':
                        colorKeyR = int(childNode.getAttribute('r'))
                        colorKeyG = int(childNode.getAttribute('g'))
                        colorKeyB = int(childNode.getAttribute('b'))
            
            return TileManager(textureName, self._tileSize, colorkey = (colorKeyR, colorKeyG, colorKeyB))