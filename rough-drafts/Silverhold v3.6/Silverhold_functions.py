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
        
    def moveCall_point(self, dx, dy):
        return point(self.x + dx, self.y + dy)

    def snapToGrid(self):
        self.x = int(self.x/20)
        self.y = int(self.y/20)

    def unsnapGrid(self):
        return point(20 * self.x, 20 * self.y)
class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, text_color, fileName: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.fileName = fileName
        
        topleft=point(x+width/2,y+height/2)
        self.toImage = Image(topleft, fileName, (width, height), 0)  
class Enemy:
    def __init__(self, pos: point, Type: str):
        # ENEMY DATA
        self.pos = pos
        self.size = enemyDict[Type]["Size"]
        self.type = Type
        self.dx = 0
        self.dy = 0

        # STATS
        self.Health = enemyDict[Type]["Health"]
        self.Speed = enemyDict[Type]["Speed"]
        self.Damage = enemyDict[Type]["Damage"]
        self.attackSpeed = enemyDict[Type]["attackSpeed"]
        self.attackType = enemyDict[Type]["attackType"]
        self.Value = enemyDict[Type]["Value"]
        self.Range = enemyDict[Type]["Range"]
        self.approachRange = enemyDict[Type]["approachRange"]

        # IMAGE
        self.imageFile = Image(self.pos, enemyDict[Type]["imageFile"], (300, 300), 0)

    # Find direction to attack player building
    def findEnemyPath(self, points: list):
        self.dx = findDirection(self.pos,findClosestPoint(points, self.pos))[0]
        self.dy = findDirection(self.pos,findClosestPoint(points, self.pos))[1]

    # Update enemy actions
    def step(self, structureList: list):
        self.findEnemyPath(structureList)
        if findDistance(findClosestPoint(structureList, self.pos), self.pos) >= self.approachRange:
            self.pos.move(self.dx, self.dy)
        self.imageFile.rotation = findRotation(self.dx, self.dy)
        self.imageFile.pos = self.pos.moveCall_point(-self.imageFile.resolution[0] / 2, -self.imageFile.resolution[1] / 2)

    def damage(self, amount):
        self.Health -= amount

class projectile:
    def __init__(self, pos: point, damage: float, target, Type: str):
        # DATA & IMAGE
        self.pos = pos
        self.type = Type
        self.resolution = projectileDict[Type]["resolution"]
        self.imageFile = Image(self.pos, projectileDict[Type]["imageFile"], self.resolution, 0)
        
        self.skew_dx = 0
        self.skew_dy = 0
        self.dx = 0
        self.dy = 0

        # STATS
        self.Damage = damage
        self.Speed = projectileDict[Type]["Speed"]

        # TARGETTING
        self.rotation = 0
        self.target = target

    def findTargetPath(self):
        if type(self.target) == structure:
            self.dx = findDirection(self.pos, self.target.center)[0]
            self.dy = findDirection(self.pos, self.target.center)[1]
        else:
            self.dx = findDirection(self.pos, self.target.pos)[0]
            self.dy = findDirection(self.pos, self.target.pos)[1]

    def step(self):
        self.pos.move(self.dx + self.skew_dx, self.dy + self.skew_dy)
        self.skew_dx = self.skew_dx * 0.99
        self.skew_dy = self.skew_dx * 0.99

        if self.type != "cannonball" and self.type != "explosive":
            self.imageFile.rotation = findRotation(self.dx, self.dy)
        else:
            self.imageFile.rotation = 0
        self.imageFile.pos = self.pos.moveCall_point(-self.imageFile.resolution[0] / 2, -self.imageFile.resolution[1] / 2)

    def draw(self, surface):
        self.imageFile.render(surface)

class structure:
    def __init__(self, gridPos: point, Type: str, level: int):
        # GENERAL DATA
        self.level = level
        self.gridPos = gridPos
        self.pos = gridPos.unsnapGrid()
        self.size = towerDict[Type]["Size"]
        self.type = Type

        # STATS
        self.Health = towerDict[Type]["level"+str(self.level)]["Health"]
        self.Damage = towerDict[Type]["level"+str(self.level)]["Damage"]
        self.Range = towerDict[Type]["level"+str(self.level)]["Range"]
        self.attackSpeed = towerDict[Type]["level"+str(self.level)]["attackSpeed"]
        self.attackType = towerDict[Type]["level"+str(self.level)]["attackType"]
        self.Value = towerDict[Type]["level"+str(self.level)]["Value"]

        # SPRITE DATA
        self.resolution = towerDict[Type]["resolution"]
        self.center = self.pos.moveCall_point(self.resolution[0] / 2, self.resolution[1] / 2)
        self.lastTargetPos = point(self.pos.x, 0)

        # IMAGE AND DRAWING
        self.imageFile = Image(self.center, towerDict[Type]["level"+str(self.level)]["imageFile"], self.resolution, 0)
        if Type in ["archer", "cannon"]:
            self.turretSprite = Image(self.center, towerDict[Type]["level"+str(self.level)]["turretSprite"], (100, 100), 0)
            
    def damage(self, amount):
        self.Health -= amount

    def updateTurretRotation(self):
        if self.type in ["archer", "cannon"]:
            self.turretSprite.rotation = findRotation(findDirection(self.pos, self.lastTargetPos)[0], findDirection(self.pos, self.lastTargetPos)[1])

    def draw(self, surface):
        self.imageFile.render(surface)
    
    def drawTurret(self, surface):
        if self.type in ["archer", "cannon"]:
            self.turretSprite.render(surface)

    def updateTowerLevel(self):
        self.Health = towerDict[self.type]["level"+str(self.level)]["Health"]
        self.Damage = towerDict[self.type]["level"+str(self.level)]["Damage"]
        self.Range = towerDict[self.type]["level"+str(self.level)]["Range"]
        self.attackSpeed = towerDict[self.type]["level"+str(self.level)]["attackSpeed"]
        self.attackType = towerDict[self.type]["level"+str(self.level)]["attackType"]
        self.Value = towerDict[self.type]["level"+str(self.level)]["Value"]

        self.imageFile = Image(self.center, towerDict[self.type]["level"+str(self.level)]["imageFile"], self.resolution, 0)
        if self.type in ["archer", "cannon"]:
            self.turretSprite = Image(self.center, towerDict[self.type]["level"+str(self.level)]["turretSprite"], (100, 100), 0)

class Image:
    def __init__(self, centerPos: point, file: str, resolution: tuple, rotation: float): # Rotation is CCW
        self.centerPos = centerPos
        self.pos = self.centerPos.moveCall_point(-resolution[0] / 2, -resolution[1] / 2)
        self.rotation = rotation
        self.resolution = resolution
        self.imageFile = pygame.image.load(directory + "/sprites/" + file)
        self.imageFile = pygame.transform.scale(self.imageFile, resolution)

    def render(self, surface):
        rotated_image = pygame.transform.rotate(self.imageFile, self.rotation)
        new_rect = rotated_image.get_rect(center = self.imageFile.get_rect(topleft = self.pos.call()).center)
        surface.blit(rotated_image, new_rect)
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

# ==========
# FUNCTIONS
# ==========

# Find distance between two points
# Return -> FLOAT
def findDistance(A: point, B: point):
    return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)

# draw a button with text
def draw_Button(button, drawingSurface, textSurface, font):
    
    button_text = font.render(button.text, True, button.text_color)
    button_textRect = button_text.get_rect()
    button_textRect.center = (button.x + button.width/2, button.y + button.height/2)

    button.toImage.render(drawingSurface)
    textSurface.blit(button_text, button_textRect)
#checks if mouse click is in button zone
def clicked_Button(button, mouse_x, mouse_y) -> bool:
    return (button.x < mouse_x and mouse_x < button.x+button.width and button.y < mouse_y and mouse_y < button.y+button.height)

# check if a button is clicked at a certain x,y coord
def centeredMatrix(n: int):
    coords = []
    lowerBound = -int(n/2)
    upperBound = n + lowerBound
    for x in range(lowerBound, upperBound):
        for y in range(lowerBound, upperBound):
            coords.append([x,y])
    return coords

# Find closest point to origin in a set of points
# Return -> POINT
def findClosestPoint(points: list, pos: point):
    if type(points[0]) == structure:
        closestPoint = point(*points[0].center.call())
        for x in points:
            if findDistance(x.center, pos) <= findDistance(closestPoint, pos):
                closestPoint = point(*x.center.call())
    else:
        closestPoint = point(*points[0].pos.call())
        for x in points:
            if findDistance(x.pos, pos) <= findDistance(closestPoint, pos):
                closestPoint = point(*x.pos.call())
    return closestPoint
def findClosestPointIndex(objects: list, location: point):
    closestPointIndex = 0
    closestPoint = objects[0].location
    # Finds point w/ smallest distance to origin
    index = 0
    while index < len(objects):
        targetStructure = objects[index]
        if findDistance(targetStructure.location.unsnapGrid(), location) < findDistance(closestPoint.unsnapGrid(), location):

            closestPointIndex = index
        index += 1 
    result = closestPointIndex
    return result
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
def matrix(gridPos: point, size: int):
    coords = []
    for x in range(size):
        for y in range(size):
            coords.append(gridPos.moveCall_point(x, y))
    return coords

# Returns the locations of all conflicting tiles within build zone
# Return -> LIST: POINT
def findOverlapping(gridPos: point, size: int, occupiedTiles):
    tileOverlaps = []
    for coordinate in matrix(gridPos, size):
        if coordinate in occupiedTiles:
            tileOverlaps.append(coordinate)
    return tileOverlaps

# Returns the locations of all non-conflicting tiles within build zone
# Return -> LIST: POINT
def findPlaceableTiles(gridPos: point, size: int, occupiedTiles):
    availableTiles = []
    for coordinate in matrix(gridPos, size):
        if coordinate not in occupiedTiles:
            availableTiles.append(coordinate)
    return availableTiles

# Checks if the location collides with an existing structure
# Return -> BOOL
def checkCollision(gridPos, size: int, occupiedTiles):
    canBePlaced = True
    for coordinate in matrix(gridPos, size):
        if coordinate in occupiedTiles:
            canBePlaced = False
    return canBePlaced

# Checks if a point is within a region
# Return -> BOOL
def checkCollidePoint(gridPos: point, size: int, collidingPointPos: point):
    x1 = gridPos.unsnapGrid().x
    y1 = gridPos.unsnapGrid().y
    x2 = x1 + size * 20
    y2 = y1 + size * 20

    if x1 <= collidingPointPos.x < x2 and y1 <= collidingPointPos.y < y2:
        return True
    else:
        return False
