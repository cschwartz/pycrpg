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


from components import inventory

from ocempgui.widgets import *
from pygame import Surface
import pygame

class ImageLabelItem(components.ListItem):
    def __init__(self, item):
        components.ListItem.__init__(self)
        self._item = item
        self._text = None
        self._image = None
        
        self.set_text(item.name)
        self.image = item._surface
            
    def set_text(self, text):
        if text and type (text) not in (str, unicode):
            raise TypeError ("text must be a string or unicode")
        self._text = text
        self._dirty = True
    
    def set_image(self, image):
        if image and type(image) != Surface:
            raise TypeError("image must be a surface")
        self._image = image
        self._dirty = True
        
    @property
    def item(self):
        return self._item
        
    text = property(lambda self:self._text, lambda self, var:self.set_text(var))
    image = property(lambda self:self._image, lambda self, var:self.set_image(var))

class LootDialogViewPort(ListViewPort):
    def __init__(self, listviewport):
        ListViewPort.__init__(self, listviewport)
        
    def draw_item(self, item, engine):
        try:
            return ListViewPort.draw_item(self, item, engine)
        except TypeError:
            if isinstance(item, ImageLabelItem):
                spacing = StyleInformation.StyleInformation.get("IMAGEBUTTON_SPACING")
                (imageWidth, imageHeight) = item.image.get_size()
                textsurface =  engine.draw_string (item.text, self.state, item.__class__, item.style)
                (textWidth, textHeight) = textsurface.get_size()
                targetWidth = 4*spacing + imageWidth + textWidth
                targetHeight = 2*spacing + max(imageHeight, textHeight)
                surface = Surface((targetWidth, targetHeight), pygame.SRCALPHA)
                surface.blit(item.image, (spacing, int((targetHeight - imageHeight)/2)))                  
                surface.blit(textsurface, (3*spacing + imageWidth, int((targetHeight - textHeight)/2)))                  
                val =  (surface, surface.get_rect())
                self._images[item] = val
                return val

class InventoryDialog(GenericDialog):
    def __init__(self, gui, name, (buttons, signals)):
        self._gui = gui
        self._inventory = None
        self._itemToImageLabelItem = None
        
        GenericDialog.__init__(self, name, buttons, signals)

        self._scrolledList = ScrolledList(200, 300)
        self.content.add_child(self._scrolledList)
        
        self._scrolledList.child = LootDialogViewPort(self._scrolledList)
        self._scrolledList.selectionmode = Constants.SELECTION_SINGLE

    def set_inventory(self, new_inventory):
        if self._inventory != None:
            self._inventory.removeObserver(self)
            
        self._inventory = new_inventory
        self._inventory.addObserver(self)
        
        self._inventoryItems = components.ListItemCollection()
        
        self._itemToImageLabelItem = {}
        for item in self._inventory:
            imageLabelItem = ImageLabelItem(item)
            self._inventoryItems.append (imageLabelItem)
            self._itemToImageLabelItem[item] = imageLabelItem
            
        self._scrolledList.items = self._inventoryItems
    
    def notify_observer(self, observable, property, args):
        pass