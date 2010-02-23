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

import creature
import character
import algorithms.shortestpath
import enum.direction
import map

from numpy import dot

class AICreature(creature.Creature):
    name = 'aicreature'
    
    def __init__(self, engine, tileManagers, position, entityTemplate, id = None):
        creature.Creature.__init__(self, engine, tileManagers, position, entityTemplate, id)
        self._lastKnownPlayerPosition = None
        self._currentPath = []
        
    def _seesTile(self, x, y):
        tile = self._engine.map[x, y]
        if tile != None and len(tile.creatures) != 0:
            creature = tile.creatures[0]
            if isinstance(creature, character.Character):
                self._lastKnownPlayerPosition = creature.position
                self._currentPath = algorithms.shortestpath.shortestpath(self.position, self._lastKnownPlayerPosition, self._engine._map._width, self._engine._map._height, self._engine._map.costFunc)
                
    def ai_action(self):
        if len(self._currentPath) != 0:
            nextDirection = self._currentPath[0]
            self._currentPath.pop(0)
            if not self.move(nextDirection):
                self._currentPath = []
        elif dot(self._position - self._lastKnownPlayerPosition, self._position - self._lastKnownPlayerPosition) <= 1:
            tile = self._engine.map[self._lastKnownPlayerPosition]
            if len(tile.creatures) != 0 and tile.creatures[0] == self._engine.player:
                self.attack(self._engine.player)
            else:
                self._actions -= 1
        else:
            self._actions = 0
            
    @classmethod
    def load(cls, engine, tileManagers, creatureElement, entityTemplate):
        (position, isSolid, id) =  creature.Creature.loadCreatureData(engine, creatureElement)
        aiCreature = AICreature(engine, tileManagers, position, entityTemplate, id)
        
        return  aiCreature
    
    @classmethod
    def loadTemplate(cls, engine, templateElement):
        return creature.Creature.loadTemplate(engine, templateElement)