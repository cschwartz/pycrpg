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


from entities import entity
from gui import lootdialog

class Corpse(entity.Entity):
    name = 'corpse'
    
    def __init__(self, engine, tileManagers, position, entityTemplate, id = None):
        tileManager = tileManagers[entityTemplate['tileManager']]
        surface = tileManager[entityTemplate['appearanceId']]
        
        entity.Entity.__init__(self, surface, engine, position, id)
    
    @property
    def is_usable(self):
        return True
        
    @property
    def is_solid(self):
        return False
    
    @classmethod
    def loadTemplate(cls, engine, templateElement):
        from xml.dom import Node
        entityTemplate = {}
        appearanceId = None
        
        for childElement in templateElement.childNodes:
            if childElement.nodeType == Node.ELEMENT_NODE:
                if childElement.localName == 'appearance':
                    appearanceId = int(childElement.getAttribute('id'))
                            
        entityTemplate['appearanceId'] = appearanceId
        
        return entityTemplate
    
    @property
    def inventory(self):
        return self._inventory
    
    @inventory.setter
    def inventory(self, new_inventory):
        self._inventory = new_inventory
        
    def use(self, looter):
        print "being looted by %s" % str(looter)
        self._engine._gui.show_loot_dialog(self._inventory, looter)