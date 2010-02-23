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

class Inventory(observer.Observable):
    PROPERTY_ADD_ITEM = 'add_item'
    PROPERTY_ADD_ALL = 'add_all'
    PROPERTY_REMOVE_ITEM = 'remove_item'
    PROPERTY_REMOVE_ALL = 'remove_all'
    
    def __init__(self, items):
        observer.Observable.__init__(self)
        self._items = items            
        self.notifyChanged(Inventory.PROPERTY_ADD_ALL, None)
        
    def add(self, item):
        self._items.append(item)
        self.notifyChanged(Inventory.PROPERTY_ADD_ITEM, item)
    
    def remove(self, item):
        self._items.remove(item)
        self.notifyChanged(Inventory.PROPERTY_REMOVE_ITEM, item)
    
    def remove_all(self):
        old_items = self._items
        self._items = []
        self.notifyChanged(Inventory.PROPERTY_REMOVE_ALL, old_items)
        return old_items
        
    def __iter__(self):
        return self._items.__iter__()