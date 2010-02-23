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
import corpse
import algorithms.fov
from components import inventory

from numpy import array

class Creature(entity.Entity):
    name = 'creature'
    
    def __init__(self, engine, tileManagers, position, entityTemplate, id = None):
        tileManager = tileManagers[entityTemplate['tileManager']]
        surface = tileManager[entityTemplate['appearanceId']]
        
        entity.Entity.__init__(self, surface, engine, position, id)
        self._engine.addCreature(self)

        self._speed = entityTemplate['speed']
        self.constitution = entityTemplate['constitution'] 
        self.agility = entityTemplate['agility']
        
        width = engine._map._width
        height = engine._map._height
        
        self._inventory = inventory.Inventory(entityTemplate['items'])
        
        self._was_visible = [[False for x in xrange(width)] for y in xrange(height)]
        self._is_visible = [[False for x in xrange(width)] for y in xrange(height)]
    
        self.updateFov()
    
    def is_visible(self, position):
        return self._is_visible[position[1]][position[0]]
    
    def was_visible(self, position):
        return self._was_visible[position[1]][position[0]]
    
    @property
    def inventory(self):
        return self._inventory
    
    @property
    def speed(self):
        return self._speed
    
    @property
    def agility(self):
        return self._agility

    @agility.setter
    def agility(self, value):
        self._agility = value
        self._actions = self._agility
        
    @property
    def constitution(self):
        return self._agility

    @agility.setter
    def constitution(self, value):
        self._constitution = value
        self._hitpoints = self._constitution

    @property
    def actions(self):
        return self._actions
   
    def move(self, direction):
        if self._actions > 0:
            success = self._engine.map.moveEntityTo(self, direction)
            self._actions -= 1
            return success
        return False
    
    def attack(self, opponent):
        if self._actions > 0:
            self._actions -= 1
            if opponent.is_hit(1): #attack throw
                opponent.damage(1)
                print "%s attacking %s" % (self, opponent)
            
        return False    

    def is_hit(self, attackRoll):
        return True
    
    def damage(self, damage_value):
        self._hitpoints -= damage_value
        if self._hitpoints <= 0:
            self.kill()            
            corpseEntity = self._engine._entityProvider.createEntity("corpse", self._position)
            corpseEntity.add_overlay(self._engine.current_time + self._engine.minimumTimePerTurn, self._engine._overlayManager[0])
            corpseEntity.inventory = self._inventory
        else:
            self.add_overlay(self._engine.current_time + self._engine.minimumTimePerTurn, self._engine._overlayManager[0])
        
    def kill(self):
        self._engine.remove_creature(self)
        
    def endTurn(self):
        self._actions = self._agility
    
    def updateFov(self):
        playerX = self.position[0]
        playerY = self.position[1]
        mapWidth = self._engine._map._width
        mapHeight = self._engine._map._height

        visitedTiles = {}
        
        for y in xrange(mapHeight):
            for x in xrange(mapWidth):
                self._is_visible[y][x] = False
                
        def visitTile(x, y):
            self._was_visible[y][x] = True
            self._is_visible[y][x] = True
            self._seesTile(x, y)
            
        def isTileBlocked(x, y):
            tile = self._engine._map[(x, y)]
            if tile == None:
                return True
            
            return tile.is_opaque
                
        algorithms.fov.fieldOfView(playerX, playerY, mapWidth, mapHeight, 10, visitTile, isTileBlocked)
    
    def _seesTile(self, x, y):
        pass
    
    @classmethod
    def loadCreatureData(cls, engine, creatureElement):
        (position, isSolid, id) = entity.Entity.loadEntityData(engine, creatureElement)
        
        return (position, isSolid, id)     
    
    @classmethod
    def load(cls, engine, tileManagers, creatureElement, entityTemplate):
        (position, isSolid, id) =  Creature.loadCreatureData(engine, creatureElement)
        creature = Creature(engine, tileManagers, position, entityTemplate, id)
        
        return  creature
    
    @classmethod
    def loadTemplate(cls, engine, templateElement):
        from xml.dom import Node
        entityTemplate = {}
        appearanceId = None
        items = []
        
        for childElement in templateElement.childNodes:
            if childElement.nodeType == Node.ELEMENT_NODE:
                if childElement.localName == 'appearance':
                    appearanceId = int(childElement.getAttribute('id'))
                elif childElement.localName == 'attributes':
                    attributesElement = childElement
                    for attributeElement in attributesElement.childNodes:
                        if attributeElement.nodeType == Node.ELEMENT_NODE:
                            attributeName = attributeElement.localName
                            attributeText = ''
                            for textNode in attributeElement.childNodes:
                                attributeText += textNode.data
                            attributeValue = int(attributeText)
                            entityTemplate[attributeName] = attributeValue
                elif childElement.localName == 'inventory':
                    inventoryElement = childElement
                    for itemElement in inventoryElement.childNodes:
                        if itemElement.nodeType == Node.ELEMENT_NODE:
                            itemName = itemElement.localName
                            item = engine._entityProvider.createEntityFromElement(engine, engine._tileManagerProvider, itemName, itemElement)
                            items.append(item)
                            
        entityTemplate['appearanceId'] = appearanceId
        entityTemplate['items'] = items
        
        return entityTemplate