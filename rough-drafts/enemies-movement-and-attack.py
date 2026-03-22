import pygame
import random
import math
from pygame import mouse

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def call(self):
        return [self.x, self.y]

    def move(self, dx, dy):
        return [self.x + dx, self.y + dy]

    def moveX(self, dx, dy):
        return self.x + dx

    def moveY(self, dx, dy):
        return self.y + dy
    
    def movePoint(self, dx, dy):
        self.x += dx
        self.y += dy

    def snapToGrid(self):
       self.x = round(self.x/20)
       self.y = round(self.y/20)

class Enemy:
  def __init__(self, location: point, Type):
    self.location = location
    self.Type = Type
  
  Health = 0
  Speed = 0
  Damage = 0
  AttackSpeed = 0
  dx = 0
  dy = 0

  # find direction to attack player building
  def findEnemyPath(self, pointList):
    self.dx = findDirection(self.location,findClosestPoint(pointList,self.location))[0]
    self.dy = findDirection(self.location,findClosestPoint(pointList,self.location))[1]

  def step(self):
     self.location.movePoint(self.dx,self.dy)

# Find distance between two points
def findDistance(A: point, B: point):
  return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)
  
# Find closest point to origin in a set of points
def findClosestPoint(set, pos: point):
  closestPoint = set[0]

  # Finds point w/ smallest distance to origin
  for x in set:
    if findDistance(x, pos) < findDistance(closestPoint, pos):
      closestPoint = x
  return closestPoint

# Takes in start and end points and returns dx and dy (unit 1 pixel)
def findDirection(start: point, end: point):
  return [(end.x - start.x) / findDistance(start,end), (end.y - start.y) / findDistance(start,end)]

pygame.init()

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables
enemiesList = []
structuresList = [[500, 500],[900,300]]
structuresListAsPts = [point(500,500),point(900,300)]
# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            enemiesList.append(Enemy(point(*event.pos), 0))

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    for x in enemiesList:
      x.findEnemyPath(structuresListAsPts)
      for y in range(3):
        x.step()

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    for x in structuresList:
      pygame.draw.circle(screen, (0, 0, 255), (x[0], x[1]), 10)
      for y in enemiesList:
        if findDistance(point(*x),y.location) <= 30:
          enemiesList.remove(y)

    for x in enemiesList:
      pygame.draw.circle(screen, (225, 25, 0), (x.location.call()[0], x.location.call()[1]), 5)

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------

pygame.quit()
