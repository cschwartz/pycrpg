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

import numpy
from enum import direction

def shortestpath(sourcePosition, targetPosition, mapWidth, mapHeight, costFunc):
    distance = numpy.ones((mapWidth, mapHeight)) * numpy.inf
    predecessor = [[None for x in xrange(mapWidth)] for y in xrange(mapHeight)]
    directions = [[None for x in xrange(mapWidth)] for y in xrange(mapHeight)]
    distance[sourcePosition[0], sourcePosition[1]] = 0
    queue = [sourcePosition]
    while len(queue) != 0:
        closestTile = None
        closestTileDistance = numpy.inf
        for index in xrange(len(queue)):
            position = queue[index]
            if distance[position[0], position[1]] < closestTileDistance:
                closestTileDistance = distance[position[0], position[1]]
                closestTile = position 
        if closestTileDistance == numpy.inf:
            return []
        queue.remove(closestTile)
        for currentDirection in direction.Directions:
            newPosition = currentDirection.moveFrom(closestTile) 
            newDistance = closestTileDistance + costFunc(newPosition)
            oldDistance = distance[newPosition[0], newPosition[1]]
            if newDistance < oldDistance:
                distance[newPosition[0], newPosition[1]] = newDistance 
                directions[newPosition[1]][newPosition[0]] = currentDirection
                predecessor[newPosition[1]][newPosition[0]] = closestTile
                queue.append(newPosition)
            
    currentTilePosition = targetPosition
    directionsList = []
    while currentTilePosition != None and (currentTilePosition[0] != sourcePosition[0] or currentTilePosition[1] != sourcePosition[1]):
        directionsList.append(directions[currentTilePosition[1]][currentTilePosition[0]])
        currentTilePosition = predecessor[currentTilePosition[1]][currentTilePosition[0]]
        
    if currentTilePosition == None:
        return []
    
    directionsList.reverse()
    directionsList.pop()
    return directionsList