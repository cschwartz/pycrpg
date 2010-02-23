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


from inventorydialog import InventoryDialog, ImageLabelItem
from ocempgui.widgets import *

from components import inventory

class PlayerInventoryDialog(InventoryDialog):
    def __init__(self, gui):
        onUseButton = Button("None")
        buttons = [onUseButton, Button("Close")]
        signals = [Constants.DLGRESULT_USER, Constants.DLGRESULT_CLOSE]
       
        self._character = None
       
        InventoryDialog.__init__(self, gui, "Inventory", (buttons, signals))

        def itemSelected():
            if len(self._scrolledList.get_selected()) == 1:
                self._selectedItem = self._scrolledList.get_selected()[0].item
                onUseButton.text = self._selectedItem.onUseName
                
                
        self._scrolledList.connect_signal(Constants.SIG_SELECTCHANGED, itemSelected)
        
        def close():
            self.hide()
        
        def dialog_callback (result, dlg):
            if result == Constants.DLGRESULT_CLOSE:
                self.hide()
            elif result == Constants.DLGRESULT_USER:
                self._selectedItem.onUse(self._selectedItem, self._character)

        self.connect_signal (Constants.SIG_DIALOGRESPONSE, dialog_callback, self)
        
    @property
    def character(self):
        return self._character
    
    @character.setter
    def character(self, value):
        self._character = value
        
    def notify_observer(self, observable, property, args):
        if property == inventory.Inventory.PROPERTY_REMOVE_ITEM:
            item = args
            self._inventoryItems.remove(self._itemToImageLabelItem[item])
            del self._itemToImageLabelItem[item]
        elif property == inventory.Inventory.PROPERTY_REMOVE_ALL:
            for item in args:
                self._inventoryItems.remove(self._itemToImageLabelItem[item])
                del self._itemToImageLabelItem[item]
        elif property == inventory.Inventory.PROPERTY_ADD_ALL:
            for item in args:
                imageLabelItem = ImageLabelItem(item)
                self._inventoryItems.append (imageLabelItem)
                self._itemToImageLabelItem[item] = imageLabelItem
        elif property == inventory.Inventory.PROPERTY_ADD_ITEM:
            item = args
            imageLabelItem = ImageLabelItem(item)
            self._inventoryItems.append (imageLabelItem)
            self._itemToImageLabelItem[item] = imageLabelItem
            
    def hide(self):
        self._gui.remove_dialog(self)
