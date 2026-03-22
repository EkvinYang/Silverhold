'''
+===+ NOTES +===+
- The grid is made up of 20 x 20 pixel squares
- LEFT CLICK to place
- RIGHT CLICK on a blue tile to delete it
- MIDDLE CLICK to summon an enemy
- WIDTH and HEIGHT should preferably both be multiples of 20
+=+ END NOTES +=+ 
'''

import pygame
import random
import math
import keyboard
import os
import json
from pygame import mouse
from Silverhold_constants import *
from Silverhold_functions import *
from Silverhold_dictionaries import *

# ==========
# MAIN CODE
# ==========

pygame.init()


WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)
directory= os.getcwd()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Attempts to place a tower on clicked location
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and actionState == "place":
                clickedTile = point(*event.pos)
                clickedTile.snapToGrid()

                if checkCollision(clickedTile, testingSize, occupiedTiles):
                    structureList.append(structure(clickedTile, towerType))
            
            # Attempts to place an enemy on right click:
            elif event.button == 3 and actionState == "place": 
                enemyList.append(Enemy(point(*event.pos), enemyType))

            # Attempts to delete a tower upon right click
            elif event.button == 1 and actionState == "sell":
                clickedTile = point(*event.pos)
                clickedTile.snapToGrid()
                for tile in structureList:
                    if checkCollidePoint(tile.pos, tile.size, clickedTile):
                        structureList.remove(tile)

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # Update game tick
    gameTick += 1
    mouseGrid = point(*pygame.mouse.get_pos())
    mouseGrid.snapToGrid()

    # Generates all occupied tiles from the list of structures
    occupiedTiles = []
    for tile in structureList:
        for coordinate in matrix(tile.pos, tile.size):
            occupiedTiles.append(coordinate)

                
    # Controls tower building state ("place", "sell", "repair")
    if key_q.keyJustPressed():
        if actionState != "sell":
            actionState = "sell"
        else:
            actionState = "place"
    elif key_r.keyJustPressed():
        if actionState != "repair":
            actionState = "repair"
        else:
            actionState = "place"
# Structure mechanics; Damaging, attacking, getting hit, removing when dead
    for tile in structureList: # returns as a STRUCTURE
        # Render the structure
        tile.imageFile.render(0, screen)

        if tile.Health <= 0:
            structureList.remove(tile)

        # Attacking enemies
        if len(enemyList) >= 1:
            for enemy in enemyList:
                if findDistance(tile.pos.unsnapGrid(), enemy.pos) <= tile.Range and gameTick % tile.attackSpeed == 0:
                    projectileList.append(projectile(tile.pos.unsnapGrid(), tile.Damage, 0, testProjectileSpeed, enemy))
                if findDistance(tile.pos.unsnapGrid(), enemy.pos) <= 100 and gameTick % enemy.attackSpeed == 0:
                    tile.damage(enemy.Damage)

    # Projectile mechanics
    for bullet in projectileList:
        pygame.draw.circle(screen, (0, 0, 0), (bullet.pos.x, bullet.pos.y), 1)
        if len(projectileList) >= 1:
            for i in range(bullet.Speed):
                if findDistance(bullet.pos, bullet.Target.pos) <= 1 + bullet.Target.size:
                    bullet.Target.damage(bullet.Damage)
                    projectileList.remove(bullet)
                    break
                else:
                    bullet.findTargetPath()
                    bullet.step()
       # Enemy mechanics
    # Enemy pathfinding
    if len(structureList) >= 1:
        for enemy in enemyList:
            if findDistance(findClosestPoint(structureList, enemy.pos), enemy.pos) >= 90:
                enemy.findEnemyPath(structureList)
                for y in range(enemy.Speed):
                    enemy.step()
    # ==========
    # MECHANICS & RENDERING
    # ==========    
    
    screen.blit(background, (0,0))  # always the first drawing command

    
    # Rendering available and obstructed tiles when trying to place a structure
    if actionState == "place":
        # Draw a RED tile around the cursor if placement is impossible
        for tile in findOverlapping(mouseGrid, testingSize, occupiedTiles): # returns as a LIST, not a POINT
            pygame.draw.rect(screen, (255, 50, 50), (20 * tile[0], 20 * tile[1],20,20))
    
        # Draw a GREEN tile around the cursor if placement is possible
        for tile in findPlaceableTiles(mouseGrid, testingSize, occupiedTiles): # returns as a LIST, not a POINT
            pygame.draw.rect(screen, (50, 255, 50), (20 * tile[0], 20 * tile[1],20,20))

    # Deleting dead enemies + enemy rendering
    for enemy in enemyList:
        if enemy.Health <= 0:
            enemyList.remove(enemy)
        enemy.imageFile.render(enemy.imageFile.rotation, screen)

    pygame.display.flip()
    clock.tick(30)
    #---------------------------

pygame.quit()
