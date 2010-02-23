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


import entity

from util import xmlutils

class Door(entity.Entity):
    name = 'door'
    
    def __init__(self, engine, tileManagers, position, entityTemplate, id = None):
        tileManager = tileManagers[entityTemplate['tileManager']]
        openDecorationId = entityTemplate['openDecorationId']
        closedDecorationId = entityTemplate['closedDecorationId']
        self._openSurface = tileManager[openDecorationId]
        self._closeSurface = tileManager[closedDecorationId]
        
        entity.Entity.__init__(self, self._closeSurface, engine, position, id)
        
        self._open = False
        
    @property
    def is_open(self):
        return self._open
    
    @is_open.setter
    def is_open(self, open):
        self._open = open
        if open:
            self._surface = self._openSurface
        else:
            self._surface = self._closeSurface
        
    @property
    def is_solid(self):
        return not self._open
    
    @property
    def is_opaque(self):
        return not self._open
    
    @property
    def is_usable(self):
        return True
    
    def use(self, user):
        self.is_open = not self.is_open
    
    @classmethod
    def load(cls, engine, tileManagers, doorElement, entityTemplate):
        (position, isSolid, id) = entity.Entity.loadEntityData(engine, doorElement)
        
        door = Door(engine, tileManagers, position, entityTemplate, id)
        door.is_open = xmlutils.getBooleanAttribute(doorElement, 'open')
        return door 
    
    @classmethod
    def loadTemplate(cls, engine, templateElement):
        from xml.dom import Node
        entityTemplate = {}
        openDecorationId = None
        closedDecorationId = None
        
        for childElement in templateElement.childNodes:
            if childElement.nodeType == Node.ELEMENT_NODE:
                if childElement.localName == 'open':
                    openDecorationId = int(childElement.getAttribute('id'))
                elif childElement.localName == 'closed':
                    closedDecorationId = int(childElement.getAttribute('id'))
                            
        entityTemplate['openDecorationId'] = openDecorationId
        entityTemplate['closedDecorationId'] = closedDecorationId
        
        return entityTemplate