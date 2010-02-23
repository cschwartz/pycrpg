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

import logging, logging.config
logging.config.fileConfig("../logging.conf")
    
import time

import pygame

from util import configuration, camera

import entities

import tilemanager
import entityprovider

from enum import direction, mode

from renderable import cursor

from gui import gui, lootdialog

import map
                  
class Engine(object):
    def __init__(self, configuration):
        pygame.init()
        
        (self._resolutionTuple, isFullscreen) = configuration.screen
        
        
        #build configuration map
        self._inputMap = {}
        for key in configuration.input:
            operation = Engine.__dict__[configuration.input[key]]
            keyCode = pygame.__dict__[key]
            self._inputMap[keyCode] = operation
        
        flags = 0
        if isFullscreen:
            flags |= pygame.FULLSCREEN
        self._screen = pygame.display.set_mode(self._resolutionTuple, flags)
        
        self._configureAssets(configuration.assetConfiguration)
        
        self._cursorManager = tilemanager.TileManager("../gfx/cursor.png", colorkey = (255, 255, 255));
        self._overlayManager = self._tileManagerProvider['overlay']
                
        self._mode = mode.Move
        
        self._quit = False
        
        self._nextEntityId = 0
        
        self._currentTime = 0
        
        logging.info("created engine")
        
        self._gui = gui.Gui(self._screen)

        
#        lootDialog = lootdialog.LootDialog()
#        self._gui.add_widget (lootDialog)

    def _configureAssets(self, configurationFilename):
        entityPath = None
        tilePath = None
        tileWidth = None
        tileHeight = None
        
        import xml, xml.dom.minidom
        dom = xml.dom.minidom.parse('../' + configurationFilename)
        assetConfiguration = dom.firstChild
        for node in assetConfiguration.childNodes:
            if node.nodeType == xml.dom.Node.ELEMENT_NODE:
                if node.localName == "entities":
                    entityPath = node.getAttribute('directory')
                elif node.localName == "tiles":
                    tilePath = node.getAttribute('directory')
                    tileWidth = int(node.getAttribute('width'))
                    tileHeight = int(node.getAttribute('height'))
                    
        self._tileManagerProvider = tilemanager.TileManagerProvider(tilePath, (tileWidth, tileHeight))
        self._entityProvider = entityprovider.EntiryProvider(self, self._tileManagerProvider, entityPath)
        
    @property
    def map(self):
        return self._map
    
    @property
    def current_time(self):
        return self._currentTime    
    
    @property
    def player(self):
        return self._player
    
    def addEntity(self, position, entity):
        self._entities.append(entity)
        self._nextEntityId = max(self._nextEntityId, entity.id + 1)
        if position != None:
            self._map[position].enter(entity)
        
    def remove_entity(self, entity):
        if entity.position != None:
            self._map[entity.position].leave(entity)
        
        self._entities.remove(entity)
        
    def remove_creature(self, creature):
        self._turnOrder.remove(creature)
        self._creatures.remove(creature)
        self.remove_entity(creature)
        
#        if creature == self._player: #hack until proper gamestates are implemented
 #           self._quit = True
        
    def addCreature(self, creature):
        self._creatures.append(creature)
        
    def getNextEntity(self):
        id = self._nextEntityId
        self._nextEntityId += 1
        return id
        
    minimumTimePerTurn = 250    
    
    def nextTurnMayOccur(self):    
        return self._lastTurn + Engine.minimumTimePerTurn <= self._currentTime
        
    def run(self):
        self._lastTurn = pygame.time.get_ticks()
        self._newDirection = None
        self._turnOrder = sorted(self._creatures, lambda x, y : y.agility - x.agility)
        
        turns = 0
        
        clock = pygame.time.Clock()
        while not self._quit:
            lastTime = self._currentTime
            self._currentTime = pygame.time.get_ticks()
            fps = 1.0/(self._currentTime - lastTime) * 1000.0
            for entity in self._entities:
                entity.update(self._currentTime)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self._quit = True
                elif e.type == pygame.KEYDOWN:
                    if self._inputMap.has_key(e.key):
                        self._inputMap[e.key](self)
                        
                self._gui.distribute_events(e)
                    
            if self.nextTurnMayOccur():
                pygame.display.set_caption('pyTest - FPS %d' % clock.get_fps())
            
                actionOccured = False
                currentCreature = self._turnOrder[0]
                if currentCreature == self._player:
                    if self._mode == mode.Move: 
                        if self._newDirection != None:
                            turns += 1
                            self._lastTurn = self._currentTime
                            
                            adjacentCreatures = self._map[self._newDirection.moveFrom(self._player.position)].creatures
                            if len(adjacentCreatures) != 0 and adjacentCreatures[0] != self._player:
                                self._player.attack(adjacentCreatures[0])
                            else:
                                self._player.move(self._newDirection)

                            actionOccured = True
                            self._newDirection = None
                            
                    elif self._mode == mode.Look:
                        if self._newDirection != None:
                            self._cursor.move(self._newDirection)
                else:
                    currentCreature.updateFov()
                    currentCreature.ai_action()
                    self._lastTurn = self._currentTime
                    actionOccured = True
                
                if actionOccured == True:
                    currentCreature.updateFov()    
                    
                if currentCreature.actions == 0:
                    self._turnOrder.remove(currentCreature)
                    self._turnOrder.append(currentCreature)
                    currentCreature.endTurn()

            self.render()
            clock.tick(60)
    def render(self):
        self._screen.fill((0, 0, 0))
        self._map.render(self._screen)
        self._cursor.render(self._screen, self._camera.position)
        
        self._gui.refresh()
        
        pygame.display.flip()
    
    #parsers
    floorName = 'floor'
    tileWidth = 'tileWidth'
    tileHeight = 'tileHeight'
    floorTileset = 'floorTileset'
    decorationTileset = 'decorationTileset'
    characterTileset = 'characterTileset'
    creatureTileset = 'creatureTileset'
    filename = 'filename'
    colorKey = 'colorKey'
    red = 'red'
    green = 'green'
    blue = 'blue'
    entities = 'entities'
    
    def load(self, filename):
        import xml.dom
        dom = xml.dom.minidom.parse(filename)
        floorElement = dom.firstChild
        
        self._tileWidth = int(floorElement.getAttribute(Engine.tileWidth))
        self._tileHeight = int(floorElement.getAttribute(Engine.tileHeight))
        self._tilesize = (self._tileWidth, self._tileHeight)
        
        self._player = None
        self._decorationArtwork = None
        self._decorationColorkey = None
        
        self._entities = []
        self._creatures = []
        self._nextEntityId = 0
                
        for childElement in floorElement.childNodes:
            if childElement.nodeType == xml.dom.Node.ELEMENT_NODE:
                if childElement.localName == 'entities':
                    entitiesElement = childElement
                    for entityElement in entitiesElement.childNodes:
                        if entityElement.nodeType == xml.dom.Node.ELEMENT_NODE:
                            entityName = entityElement.localName
                            self._entityProvider.createEntityFromElement(self, self._tileManagerProvider, entityName, entityElement)
                elif childElement.localName == 'map':
                    self._map = map.Map.load(childElement, self, self._tileManagerProvider)
                else:
                    logging.warn("unknown node %s" % childElement.localName)   
                    
        idToEntityMap = {}            
        
        for entity in self._entities:
            self._nextEntityId = max(self._nextEntityId, entity.id)
            idToEntityMap[entity.id] = entity
                            
        self._nextEntityId += 1
        
        for entity in self._entities:
            entity.updateEntityReferences(idToEntityMap)
            if isinstance(entity, entities.stair.Stair):
                self._player =  entities.character.Character(engine, self._tileManagerProvider, direction.Down.moveFrom(entity.position), self._entityProvider.getEntityTemplate(self._tileManagerProvider, 'character'))

        self._camera = camera.Camera(self._resolutionTuple, self._player)

        self._cursor = cursor.Cursor(self._cursorManager[0], self._player)

        self._map.setCamera(self._camera)
    
    def appendColorkeyElement(self, document, parent, name, (r, g, b)):
        colorkey = document.createElement('colorKey')
        parent.appendChild(colorkey)
        colorkey.setAttribute('red', str(r))
        colorkey.setAttribute('green', str(g))
        colorkey.setAttribute('blue', str(b))
        return document

    def getColorkey(self, colorKeyElement):
        red = int(colorKeyElement[0].getAttribute(Engine.red))
        green = int(colorKeyElement[0].getAttribute(Engine.green))
        blue = int(colorKeyElement[0].getAttribute(Engine.blue))
        
        return (red, green, blue)
        
    #control callbacks
    def move_left(self):
        self._newDirection = direction.Left
    
    def move_right(self):
        self._newDirection = direction.Right
    
    def move_up(self):
        self._newDirection = direction.Up
    
    def move_down(self):
        self._newDirection = direction.Down
    
    def show_inventory(self):
        self._gui.show_player_inventory_dialog(self._player)
    
    def mode_look(self):
        if self._mode == mode.Move:
            self._mode = mode.Look
            self._cursor.reset_to_player()
            self._cursor.do_show = True
        elif self._mode == mode.Look:
            self._newDirection = direction.NoDirection
            self._cursor.do_show = False
            self._mode = mode.Move
            print self._player.lookAt(self._cursor.relative_position)
    
    def mode_use(self):
        if self._mode == mode.Move:
            self._mode = mode.Look
            self._cursor.reset_to_player()
            self._cursor.do_show = True

        elif self._mode == mode.Look:
            self._newDirection = direction.NoDirection
            self._cursor.do_show = False
            self._mode = mode.Move
            self._player.use(self._cursor.relative_position)
        
    def quit(self):
        if self._mode == mode.Move:
            self._quit = True
        else:
            self._mode = mode.Move
            self._cursor.do_show = False
    
if __name__ == '__main__':
    configuration = configuration.Configuration("../configuration.xml")
    engine = Engine(configuration)
    engine.load('../demomap.xml')
    engine.run()