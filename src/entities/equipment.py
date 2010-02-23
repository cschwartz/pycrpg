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


import item
import entity

class Equipment(item.Item):
    name = 'equipment'
    
    def __init__(self, engine, tileManagers, position, entityTemplate, id = None):
        item.Item.__init__(self, engine, tileManagers, position, entityTemplate, id)
        
        self.onUse = Equipment.__dict__[entityTemplate['onUse']]
        self._onUseName = entityTemplate['onUseName']
        self._slot = entityTemplate['slot']
        
        equipmentTileManager = tileManagers[entityTemplate['equipmentTileManager']]
        self._equipementSurface = equipmentTileManager[entityTemplate['equipmentApprearenceId']]
            
    @property
    def slot(self):
        return self._slot
            
    def equip(self, character):
        character.equipedItems.equip(self)
    
    def onEquip(self, character):
        self.position = character.position
        self._surface = self._equipementSurface
        
    def onUnequip(self):
        self.position = None
        self._surface = self._itemSurface
        
    @classmethod
    def load(cls, engine, tileManagers, itemElement, entityTemplate):
        (position, isSolid, id) = entity.Entity.loadEntityData(engine, itemElement) 
        equipment = Equipment(engine, tileManagers, position, entityTemplate, id)
        return equipment
    
    @classmethod
    def loadTemplate(cls, engine, templateElement):
        from xml.dom import Node
        entityTemplate = {}
        appearanceId = None
        
        entityTemplate['onUse'] = templateElement.getAttribute('onUse')
        entityTemplate['onUseName'] = templateElement.getAttribute('onUseName')
        entityTemplate['slot'] = templateElement.getAttribute('slot')
        
        for childElement in templateElement.childNodes:
            if childElement.nodeType == Node.ELEMENT_NODE:
                if childElement.localName == 'appearance':
                    appearanceId = int(childElement.getAttribute('id'))
                if childElement.localName == 'equipment':
                    equipmentTileManager = childElement.getAttribute('tileManager')
                    for equipmentChildElement in childElement.childNodes:
                        if equipmentChildElement.nodeType == Node.ELEMENT_NODE:
                            if equipmentChildElement.localName == 'appearance':
                                equipmentAppearanceId = int(equipmentChildElement.getAttribute('id'))
                                
        entityTemplate['appearanceId'] = appearanceId
        
        entityTemplate['equipmentTileManager'] = equipmentTileManager
        entityTemplate['equipmentApprearenceId'] = equipmentAppearanceId
        
        return entityTemplate