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


import xml.dom.minidom
import xml.dom

class Configuration:
    def __init__(self, filename):
        self.width = None
        self.height = None
        self.isFullscreen = None
        
        self.input = {}
        
        self.assetConfiguration = None
        
        dom = xml.dom.minidom.parse(filename)
        configuration = dom.firstChild
        for node in configuration.childNodes:
            if node.nodeType == xml.dom.Node.ELEMENT_NODE:
                if node.localName == "screen":
                    self.width = int(node.getAttribute("width"))
                    self.height= int(node.getAttribute("height"))
                    fullscreenValue = node.getAttribute("isFullscreen")
                    if fullscreenValue == "False":
                        self.isFullscreen = False
                    elif fullscreenValue == "True":
                        self.isFullscreen = True
                elif node.localName == "input":
                    for inputNode in node.childNodes:
                        if inputNode.nodeType == xml.dom.Node.ELEMENT_NODE:
                            if inputNode.localName == "mapping":
                                key = inputNode.getAttribute("key")
                                operation = inputNode.getAttribute("operation")
                                self.input[key] = operation
                elif node.localName == "assets":
                    self.assetConfiguration = node.getAttribute("configuration")

    @property
    def screen(self):
        return ((self.width, self.height), self.isFullscreen)
    
    @property
    def input(self):
        return self.input