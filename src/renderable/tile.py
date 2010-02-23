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

from util import xmlutils, position

import renderable
from entities import creature

    
class Tile(renderable.Renderable):
    def __init__(self, surfaceId, surface, map, position):
        renderable.Renderable.__init__(self, surface, position)
        
        self._surfaceId = surfaceId
        self._is_solid = False
        self._entities = []
        self._description = "Tile at <%s>" % self._position
        self._position = position
        self._map = map
        map[position] = self
        
    @property
    def description(self):
        return self._description
    
    def __str__(self):
        return "Tile at %s" % str(self.position)
        
    def render(self, target, camera):
        origin = camera.position
        if camera.is_visible(self._position):
            renderable.Renderable.render(self, target, origin)
            for entity in self._entities:
                entity.render(target, origin)
        else:
            if camera.was_visible(self._position):
                renderable.Renderable.render(self, target, origin)

    def mayEnter(self, entity):
        return not (self.is_solid or self._contains_solid_entity())
    
    @property
    def is_opaque(self):
        return (self.is_solid or self._contains_opaque_entity())
    
    def _contains_solid_entity(self):
        solid = False
        for entity in self._entities:
            solid |= entity.is_solid
            
        return solid
    
    def _contains_opaque_entity(self):
        opaque = False
        for entity in self._entities:
            opaque |= entity.is_opaque
            
        return opaque
    
    def hasEntity(self, entity):
        return entity in self._entities
    
    def enter(self, entity):
        self._entities.append(entity)
        entity.position = self.position.copy()

    def leave(self, entity):
        self._entities.remove(entity)
        
    @property
    def usable_entities(self):
        usable_entity_list = []
        for entity in self._entities:
            if entity.is_usable:
                usable_entity_list.append(entity)
        return usable_entity_list
    
    @property
    def creatures(self):
        creature_list = []
        for entity in self._entities:
            #FIXME: don't like the use of isinstance
            if isinstance(entity, creature.Creature):
                creature_list.append(entity)
                
        return creature_list
                
    
    @property
    def is_solid(self):
        return self._is_solid
    
    @is_solid.setter
    def is_solid(self, is_solid):
        self._is_solid = is_solid
        
    @classmethod
    def load(cls, floorManager, tileElement, map):
        position = renderable.Renderable.loadRenderableData(tileElement)
        surfaceId = int(tileElement.getAttribute('floorId'))
        tile = Tile(surfaceId, floorManager[surfaceId], map, position)
        tile.is_solid = xmlutils.getBooleanAttribute(tileElement, 'isSolid')
        return tile