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
import logging


logger = logging.getLogger("entityprovider")
    
class EntiryProvider:
    def __init__(self, engine, tileManagers, directory):
        self._engine = engine
        self._tileManagers = tileManagers
        self._entityClasses = {}
        self._entityTemplates = {}
        self._directory = directory
        
    def _registerEntity(self, className, entityClass):
        self._entityClasses[className] = entityClass
    
    def getEntityTemplate(self, tileManagers, entityName):
        entityTemplate = None
        
        if entityName in self._entityTemplates:
            entityTemplate = self._entityTemplates[entityName]
        else:
            import xml.dom
            dom = xml.dom.minidom.parse('../' + self._directory +'/' + entityName + '.xml')
            rootElement = dom.firstChild
            entityClassName = rootElement.getAttribute('class')
            tileManager = rootElement.getAttribute('tileManager')
            
            if entityClassName in self._entityClasses:
                entityClass = self._entityClasses[entityClassName]
            else:
                moduleName = entityClassName[:entityClassName.rindex('.')]
                className = entityClassName[entityClassName.rindex('.')+1:]
                classObject = __import__(moduleName, globals(), locals(), [moduleName], -1)
                entityClass =  classObject.__dict__[className]
                self._entityClasses[entityClassName] = entityClass
                
                logger.info('entity type %s (%s) loaded successfully.' % (entityName, entityClassName))
                
            entityTemplate = entityClass.loadTemplate(self._engine, rootElement)
            entityTemplate['class'] = entityClass
            entityTemplate['tileManager'] = tileManager
            
            self._entityTemplates[entityName] = entityTemplate
                
        return entityTemplate

    def createEntityFromElement(self, engine, tileManagers, entityName, entityElement):
        entityTemplate = self.getEntityTemplate(tileManagers, entityName)
                
        entityClass = entityTemplate['class']
        return entityClass.load(engine, tileManagers, entityElement, entityTemplate)

    def createEntity(self, entityName, position):
        entityTemplate = self.getEntityTemplate(self._tileManagers, entityName)
                
        entityClass = entityTemplate['class']
        return entityClass(self._engine, self._tileManagers, position, entityTemplate)

