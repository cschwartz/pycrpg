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


from ocempgui import widgets
import lootdialog, playerinventorydialog

class Gui(object):
    def __init__(self, screen):
        self._gui = widgets.Renderer()
        self._gui.screen = screen

        self._loot_dialog = lootdialog.LootDialog(self)
        
        self._player_inventory_dialog = playerinventorydialog.PlayerInventoryDialog(self)
        
    def show_loot_dialog(self, inventory, looter):
        self._loot_dialog.set_inventory(inventory)
        self._loot_dialog.looter = looter
        self._gui.add_widget(self._loot_dialog)
    
    def show_player_inventory_dialog(self, player):
        self._player_inventory_dialog.character = player
        self._player_inventory_dialog.set_inventory(player.inventory)
        self._gui.add_widget(self._player_inventory_dialog)
    
    def remove_dialog(self, dialog):
        self._gui.remove_widget(dialog)
        
    def refresh(self):
        self._gui.refresh()
        
    def distribute_events(self, events):
        self._gui.distribute_events(events)