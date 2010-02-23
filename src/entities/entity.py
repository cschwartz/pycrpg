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


from renderable import renderable
from util import position

class Entity(renderable.Renderable):
    name = 'entity'
    
    def __init__(self, surface, engine, position, id = None):
        renderable.Renderable.__init__(self, surface, position)
        if id == None:
            newId = engine.getNextEntity()
            self._id = newId
            print self._id
        else:
            self._id = id
            
        self._is_solid = False
        
        self._engine = engine
        
        self._engine.addEntity(position, self)
        
    @property
    def is_solid(self):
        return True
    
    @is_solid.setter
    def is_solid(self, is_solid):
        self._is_solid = is_solid
        
    @property
    def is_opaque(self):
        return False
        
    @property
    def is_usable(self):
        return False    
    
    @property
    def id(self):
        return self._id

    @classmethod
    def loadEntityData(cls, engine, element):
        position = renderable.Renderable.loadRenderableData(element)
        id = None
        if element.hasAttribute('id'):
            id = int(element.getAttribute('id'))
        return (position, True, id)
    
    def updateEntityReferences(self, idToEntityMap):
        pass
    
    def __str__(self):
        return '%s(#%d)' % (self.name, self.id) 