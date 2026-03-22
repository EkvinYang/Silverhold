'''
+=+ NOTES +=+
- The grid is made up of 20 x 20 pixel squares
- LEFT CLICK to place
- RIGHT CLICK on a blue tile to delete it
- WIDTH and HEIGHT should preferably both be multiples of 20
- towerSize should be a positive integer
+=+ END NOTES +=+ 
'''

import pygame
import random
import math
from pygame import mouse

# ==========
# OBJECTS
# ==========

# Define point and structure classes
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def call(self):
        return [self.x, self.y]
    
    def moveCall(self, dx, dy):
        return [self.x + dx, self.y + dy]
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def snapToGrid(self):
        self.x = round(self.x/20)
        self.y = round(self.y/20)

class structure:
    Health = 0
    buildTime = 0

    def __init__(self, pos: point, size: int):
        self.size = size
        self.pos = pos
    
    # Checks if the location collides with an existing structure
    def checkCollision(self, occupiedTiles):
        canBePlaced = True
        for coordinate in matrix(self.size):
            if self.pos.moveCall(*coordinate) in occupiedTiles:
                canBePlaced = False
        return canBePlaced
    
    # Returns the locations of all conflicting tiles within build zone
    def findOverlapping(self, occupiedTiles):
        tileOverlaps = []
        for coordinate in matrix(self.size):
            if self.pos.moveCall(*coordinate) in occupiedTiles:
                tileOverlaps.append(self.pos.moveCall(*coordinate))
        return tileOverlaps
    
    # Returns the locations of all non-conflicting tiles within build zone
    def findPlaceableTiles(self, occupiedTiles):
        availableTiles = []
        for coordinate in matrix(self.size):
            if self.pos.moveCall(*coordinate) not in occupiedTiles:
                availableTiles.append(self.pos.moveCall(*coordinate))
        return availableTiles
    
    # Returns the region occupied by the structure. RETURNS: top left point, bottom right point
    def region(self):
        posA = point(self.pos.x - int(self.size/2), self.pos.y - int(self.size/2))
        posB = posA.moveCall(self.size, self.size)
        return [posA.call(), posB]

# ==========
# FUNCTIONS
# ==========

# Returns each coordinate in an n x n matrix in a list, with the origin as the center:
# Note: for even values of n, the matrix is shifted up and to the left
# This is to make up for the fact that the cursor blocks a bit of the bottom right
def matrix(n: int):
    coords = []
    lowerBound = -int(n/2)
    upperBound = n + lowerBound
    for x in range(lowerBound, upperBound):
        for y in range(lowerBound, upperBound):
            coords.append([x,y])
    return coords

# Checks if a point is within a region
def checkCollidePoint(pos: point, tile: structure):
    x1 = tile.region()[0][0]
    y1 = tile.region()[0][1]
    x2 = tile.region()[1][0]
    y2 = tile.region()[1][1]
   
    if x1 <= pos.call()[0] < x2 and y1 <= pos.call()[1] < y2:
        return True
    else:
        return False

# ==========
# MAIN CODE
# ==========

pygame.init()

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

grid = [[0]*int(WIDTH/20)]*int(HEIGHT/20)
occupiedTiles = []
structureList = []

towerSize = 3
# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Attempts to place a tower on clicked location
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # When a tile is clicked, its location is snapped to grid and converted to structure object
                clickedTile = point(*event.pos)
                clickedTile.snapToGrid()
                clickedTile = structure(clickedTile, towerSize)
                if clickedTile.checkCollision(occupiedTiles):
                    structureList.append(clickedTile)
            
            # Attempts to delete a tower upon right click
            elif event.button == 3:
                clickedTile = point(*event.pos)
                clickedTile.snapToGrid()
                for tile in structureList:
                    if checkCollidePoint(clickedTile, tile):
                        structureList.remove(tile)

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # Generates all occupied tiles from the list of structures
    occupiedTiles = []
    for tile in structureList:
        for coordinate in matrix(tile.size):
                    occupiedTiles.append(tile.pos.moveCall(*coordinate))
    
    mouseGrid = point(*pygame.mouse.get_pos())
    mouseGrid.snapToGrid()

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    # Draw a BLUE tile for each occupied tile
    for tile in structureList: # returns as a STRUCTURE
        for coordinate in matrix(tile.size):
            pygame.draw.rect(screen, (25,25,255), (20 * (tile.pos.moveCall(*coordinate)[0])-10, 20 * (tile.pos.moveCall(*coordinate)[1])-10,20,20))

    # Draw a RED tile around the cursor if placement is impossible
    for tile in structure(mouseGrid, towerSize).findOverlapping(occupiedTiles): # returns as a LIST, not a POINT
        pygame.draw.rect(screen, (255, 50, 50), (20 * tile[0]-10, 20 * tile[1]-10,20,20))

    # Draw a GREEN tile around the cursor if placement is possible
    for tile in structure(mouseGrid, towerSize).findPlaceableTiles(occupiedTiles): # returns as a LIST, not a POINT
        pygame.draw.rect(screen, (50, 255, 50), (20 * tile[0]-10, 20 * tile[1]-10,20,20))

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
