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

from components import equippeditems

import util.observer
import entity
import creature

class Character(creature.Creature, util.observer.Observable):
    name = 'character'
    
    def __init__(self, engine, tileManagers, position, entityTemplate, id = None):
        creature.Creature.__init__(self, engine, tileManagers, position, entityTemplate, id)
        util.observer.Observable.__init__(self)
        
        self._equipedItems = equippeditems.EquipedItems(self)
        
    @property
    def equipedItems(self):
        return self._equipedItems
        
    @property
    def is_solid(self):
        return False    
        
    def move(self, direction):
        success = creature.Creature.move(self, direction)
        if success:
            self.notifyChanged("move", (direction, success))
        return success
    
    def lookAt(self, direction):
        lookPosition = direction.moveFrom(self._position)
        toLookAt = self._engine._map[lookPosition]
        return toLookAt.description
    
    def use(self, direction):
        usePosition = direction.moveFrom(self._position)
        useTile = self._engine.map[usePosition]
        for entity in useTile.usable_entities:
            entity.use(self)
            
    def render(self, target, offset):
        creature.Creature.render(self, target, offset)
        self._equipedItems.postCharacterRender(target, offset)