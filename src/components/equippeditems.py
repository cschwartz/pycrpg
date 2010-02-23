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

from util import observer

class EquipedItems(observer.Observable):
    def __init__(self, character):
        observer.Observable.__init__(self)
        self._character = character

        self._character.addObserver(self)
        self._position = character.position
        
        #read from xml
        self._slotToOrder = {}
        self._slotToOrder['Legs'] = 0
        self._slotToOrder['Armor'] = 1
        self._slotToOrder['MainHand'] = 2
        
        self._equipedItems = {}
        self._renderingOrder = [None for i in range(max(self._slotToOrder.values()) + 1)]
            
    def equip(self, equipment):
        slot = equipment.slot
        order = self._slotToOrder[slot]
        if equipment.slot in self._equipedItems:
            item = self._equipedItems[slot]
            item.onUnequip()
            self._equipedItems[slot] = None
            self._renderingOrder[order] = None
            
        self._equipedItems[slot] = equipment
        self._renderingOrder[order] = equipment
        equipment.onEquip(self._character)
        print "equiped %s to slot %s" % (str(equipment), slot) 
        
    def postCharacterRender(self, target, offset):
        for renderable in self._renderingOrder:
            if renderable != None:
                renderable.render(target, offset)
            
    def notify_observer(self, origin, property, args):
        if property == "move":
            (direction, success) = args
            if success:
                position = self._character.position
                self._position = position
                for (slot, equipment) in self._equipedItems.items():
                    equipment.position = position