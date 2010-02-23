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

class Stair(entity.Entity):
    name = 'stair'
    
    def __init__(self, is_up, engine, tileManagers, position, entityTemplate, id = None):
        tileManager = tileManagers[entityTemplate['tileManager']]
        if is_up:
            stairDecorationId = entityTemplate['upDecorationId']
        else:
            stairDecorationId = entityTemplate['downDecorationId']
        surface = tileManager[stairDecorationId]
        entity.Entity.__init__(self, surface, engine, position, id)
        
        self._is_up = is_up
        
    @property
    def is_solid(self):
        return True
    
    @property
    def is_usable(self):
        return True
    
    def use(self, user):
        pass # not implemented yet
    
    @classmethod
    def load(cls, engine, tileManagers, doorElement, entityTemplate):
        (position, isSolid, id) = entity.Entity.loadEntityData(engine, doorElement)
        is_up = xmlutils.getBooleanAttribute(doorElement, 'isUp')
        stairs = Stair(is_up, engine, tileManagers, position, entityTemplate, id)

        return stairs 

    @classmethod
    def loadTemplate(cls, engine, templateElement):
        from xml.dom import Node
        entityTemplate = {}
        upDecorationId = None
        downDecorationId = None
        
        for childElement in templateElement.childNodes:
            if childElement.nodeType == Node.ELEMENT_NODE:
                if childElement.localName == 'up':
                    upDecorationId = int(childElement.getAttribute('id'))
                elif childElement.localName == 'down':
                    downDecorationId = int(childElement.getAttribute('id'))
                            
        entityTemplate['upDecorationId'] = upDecorationId
        entityTemplate['downDecorationId'] = downDecorationId
        
        return entityTemplate