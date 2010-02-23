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

from numpy import array

class Item(entity.Entity):
    name = 'item'
    
    def __init__(self, engine, tileManagers, position, entityTemplate, id = None):
        tileManager = tileManagers[entityTemplate['tileManager']]
        self._itemSurface = tileManager[entityTemplate['appearanceId']]
        entity.Entity.__init__(self, self._itemSurface, engine, position, id)
        
        self.onUse = None
        self._onUseName = "None"
        
    @property
    def onUseName(self):
        return self._onUseName        
    
    @classmethod
    def load(cls, engine, tileManagers, itemElement, entityTemplate):
        (position, isSolid, id) = entity.Entity.loadEntityData(engine, itemElement) 
        item = Item(engine, tileManagers, position, entityTemplate, id)
        return item
    
    @classmethod
    def loadTemplate(cls, engine, templateElement):
        from xml.dom import Node
        entityTemplate = {}
        appearanceId = None
        
        entityTemplate['onUse'] = templateElement.getAttribute('onUse')
        
        for childElement in templateElement.childNodes:
            if childElement.nodeType == Node.ELEMENT_NODE:
                if childElement.localName == 'appearance':
                    appearanceId = int(childElement.getAttribute('id'))

        entityTemplate['appearanceId'] = appearanceId
        
        return entityTemplate