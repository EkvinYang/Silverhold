import math
import keyboard
import pygame
import os
from Silverhold_dictionaries import enemyDict, towerDict, projectileDict

directory = os.path.dirname(os.path.realpath(__file__))
# ==========
# OBJECTS
# ==========

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def call(self):
        return [self.x, self.y]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def moveCall_coord(self, dx, dy):
        return [self.x + dx, self.y + dy]
    
    def moveCall_point(self, dx, dy):
        return point(self.x + dx, self.y + dy)

    def snapToGrid(self):
        self.x = int(self.x/20)
        self.y = int(self.y/20)

    def unsnapGrid(self):
        return point(20 * self.x, 20 * self.y)
    
class Enemy:
    def __init__(self, pos: point, Type: str):
        self.pos = pos
        self.size = enemyDict[Type]["Size"]
        self.Health = enemyDict[Type]["Health"]
        self.Speed = enemyDict[Type]["Speed"]
        self.Damage = enemyDict[Type]["Damage"]
        self.attackSpeed = enemyDict[Type]["attackSpeed"]
        self.attackType = enemyDict[Type]["attackType"]
        self.Value = enemyDict[Type]["Value"]
        self.imageFile = Image(self.pos, enemyDict[Type]["imageFile"], (300, 300), 0)

        self.dx = 0
        self.dy = 0

    # Find direction to attack player building
    def findEnemyPath(self, points: list):
        self.dx = findDirection(self.pos,findClosestPoint(points,self.pos))[0]
        self.dy = findDirection(self.pos,findClosestPoint(points,self.pos))[1]

    def step(self):
        self.pos.move(self.dx,self.dy)
        self.imageFile.rotation = findRotation(self.dx, self.dy)
        self.imageFile.topLeft = self.pos.moveCall_point(-self.imageFile.resolution[0] / 2, -self.imageFile.resolution[1] / 2)

    def damage(self, amount):
        self.Health -= amount

class projectile:
    def __init__(self, pos: point, damage, type, speed, target: Enemy):
        self.pos = pos
        self.Damage = damage
        self.Type = type
        self.Speed = speed
        self.Target = target

    def findTargetPath(self):
        self.dx = findDirection(self.pos,self.Target.pos)[0]
        self.dy = findDirection(self.pos,self.Target.pos)[1]

    def step(self):
        self.pos.move(self.dx, self.dy)

class structure:
    def __init__(self, location: point, Type: str, level: int):
        # GENERAL DATA
        self.location = location
        self.Type = Type
        self.level = level
        self.size = towerDict[Type]["Size"]
        self.resolution = towerDict[Type]["resolution"]

        # STATS
        self.Health = towerDict[Type]["level"+str(self.level)]["Health"]
        self.Damage = towerDict[Type]["level"+str(self.level)]["Damage"]
        self.Range = towerDict[Type]["level"+str(self.level)]["Range"]
        self.attackSpeed = towerDict[Type]["level"+str(self.level)]["attackSpeed"]
        self.attackType = towerDict[Type]["level"+str(self.level)]["attackType"]
        self.Value = towerDict[Type]["level"+str(self.level)]["Value"]

        # SPRITE DATA
        self.topLeft = region(self.location, self.size)[0]
        self.center = self.topLeft.moveCall_point(1 - int(self.size / 2), 1 - int(self.size / 2))

        self.imageFile = Image(self.center.unsnapGrid(), 0, self.resolution, towerDict[Type]["level"+str(self.level)]["imageFile"])
        if Type in ["archer", "cannon"]:
            self.turretSprite = Image(self.topLeft.unsnapGrid(), towerDict[Type]["level"+str(self.level)]["turretSprite"], (100, 100), 0)

    def damage(self, amount):
        self.Health -= amount

# Key press detecting with help from ChatGPT
class KeyPressDetector:

    def __init__(self, key):
        self.key = key  # The key to detect
        self.key_pressed = False  # A flag to track if the specified key is currently pressed
        self.prev_key_pressed = False  # A flag to track the previous state of the key
        keyboard.hook(self.onKeyEvent)  # Register the event handler

    def onKeyEvent(self, event):
        if event.name == self.key:
            if event.event_type == 'down' and not self.key_pressed:
                self.key_pressed = True  # Set the flag to True when the specified key is pressed
            elif event.event_type == 'up':
                self.key_pressed = False  # Reset the flag when the specified key is released

    def keyJustPressed(self):
        if not self.prev_key_pressed and self.key_pressed:
            self.prev_key_pressed = self.key_pressed
            return True
        self.prev_key_pressed = self.key_pressed
        return False
    
class Image:
    def __init__(self, topLeft: point, file: str, resolution: tuple, rotation: float): # Rotation is CLOCKWISE
        self.topLeft = topLeft
        self.rotation = rotation
        self.resolution = resolution
        self.imageFile = pygame.image.load(directory + "/sprites/" + file)
        self.imageFile = pygame.transform.scale(self.imageFile, resolution)
    def render(self, rotation, surface):
        surface.blit(pygame.transform.rotate(self.imageFile, rotation), self.topLeft.call())

# ==========
# FUNCTIONS
# ==========

# Find distance between two points
# Return -> FLOAT
def findDistance(A: point, B: point):
    return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)

# Find closest point to origin in a set of points
# Return -> POINT
def findClosestPoint(points: list, pos: point):
    closestPoint = points[0].pos.unsnapGrid()

    # Finds point w/ smallest distance to origin
    for x in points:
        if findDistance(x.pos.unsnapGrid(), pos) < findDistance(closestPoint, pos):
            closestPoint = x.pos.unsnapGrid()
    return closestPoint

# Takes in start and end points and returns dx and dy (unit 1 pixel)
# Return -> [FLOAT, FLOAT]
def findDirection(start: point, end: point):
    return [(end.x - start.x) / findDistance(start,end), (end.y - start.y) / findDistance(start,end)]

# Takes direction and returns CCW rotation
# Return -> [FLOAT]
def findRotation(dx: float, dy: float):
    if dx > 0 and dy > 0:
        return -180 * (math.atan(dy/dx) / math.pi) - 90
    elif dx > 0 and dy < 0:
        return -180 * (math.atan(dy/dx) / math.pi) - 90
    elif dx < 0 and dy > 0:
        return -180 * (math.atan(dy/dx) / math.pi) + 90
    elif dx < 0 and dy < 0:
        return -180 * (math.atan(dy/dx) / math.pi) + 90
    else:
        return 0

# Returns the top left POINT and bottom right POINT coordinates of a given grid and size
# Return -> [POINT, POINT]
def region(gridCenterPos: point, size: int):
    topLeft = gridCenterPos.moveCall_point(-int(size / 2), -int(size / 2))
    bottomRight = topLeft.moveCall_point(size - 1, size - 1)
    return [topLeft, bottomRight]

# Creates a list of coordinates in a given matrix
# Return -> LIST of COORDINATES [x,y]
def matrix(gridCenterPos: point, size: int):
    coords = []
    topLeft = region(gridCenterPos, size)[0]
    for x in range(size):
        for y in range(size):
            coords.append([topLeft.x + x, topLeft.y + y])
    return coords
    
# Returns the locations of all conflicting tiles within build zone
# Return -> LIST: POINT
def findOverlapping(gridCenterPos, size: int, occupiedTiles):
    tileOverlaps = []
    for coordinate in matrix(gridCenterPos, size):
        if coordinate in occupiedTiles:
            tileOverlaps.append(coordinate)
    return tileOverlaps

# Returns the locations of all non-conflicting tiles within build zone
# Return -> LIST: POINT
def findPlaceableTiles(gridCenterPos, size: int, occupiedTiles):
    availableTiles = []
    for coordinate in matrix(gridCenterPos, size):
        if coordinate not in occupiedTiles:
            availableTiles.append(coordinate)
    return availableTiles

# Checks if the location collides with an existing structure
# Return -> BOOL
def checkCollision(gridCenterPos, size: int, occupiedTiles):
    canBePlaced = True
    for coordinate in matrix(gridCenterPos, size):
        if coordinate in occupiedTiles:
            canBePlaced = False
    return canBePlaced

# Checks if a point is within a region
# Return -> BOOL
def checkCollidePoint(gridCenterPos: point, size: int, collidingPointPos: point):
    x1 = region(gridCenterPos, size)[0].x
    y1 = region(gridCenterPos, size)[0].y
    x2 = region(gridCenterPos, size)[1].x
    y2 = region(gridCenterPos, size)[1].y

    if x1 <= collidingPointPos.x < x2 and y1 <= collidingPointPos.y < y2:
        return True
    else:
        return False