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
# Game data
gameTick = 0
money = 1000000
displayTowerRange = False
towerRangePos = [0, 0]
towerRangeRadius = 0
enemyList = []
projectileList = []
occupiedTiles = []
structureList = []
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
directory = os.path.dirname(os.path.realpath(__file__))
print(directory + "/sprites/")
running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                if actionState == "place": # Attempts to place a tower on clicked location
                    clickedTile = point(*event.pos)
                    clickedTile.snapToGrid()
                    clickedVertex = region(clickedTile, testingSize)[0]

                    if checkCollision(clickedVertex, testingSize, occupiedTiles):
                        if money >= towerDict[towerType]["level1"]["Cost"]:
                            structureList.append(structure(clickedVertex, towerType, 1))
                            money -= towerDict[towerType]["level1"]["Cost"]
                            print(f"money: {money}")
                        else:
                            print("you are too broke")

                elif actionState == "sell": # Attempts to delete a tower upon left click
                    clickedTile = point(*event.pos)
                    for tile in structureList:
                        if checkCollidePoint(tile.gridPos, tile.size, clickedTile):
                            money += int(tile.Value / 2)
                            print(f"money: {money}")
                            structureList.remove(tile)

                elif actionState not in ["place", "sell"]: # Displays the tower's range
                    clickedTile = point(*event.pos)
                    displayTowerRange = False
                    for tile in structureList:
                        if checkCollidePoint(tile.gridPos, tile.size, clickedTile) and displayTowerRange == False:
                            towerRangePos = tile.center.call()
                            towerRangeRadius = tile.Range
                            displayTowerRange = True
                            break

            elif event.button == 3:
                if actionState == "place": # Attempts to place an enemy on right click
                    enemyList.append(Enemy(point(*event.pos), enemyType))
                
                elif actionState == "upgrade":
                    clickedTile = point(*event.pos)
                    for tile in structureList:
                        if checkCollidePoint(tile.gridPos, tile.size, clickedTile):
                            if tile.level == 1 and money >= towerDict[tile.type]["level2"]["upgradeCost"]:
                                tile.level += 1
                                money -= towerDict[tile.type]["level2"]["upgradeCost"]

                                #DEBUG
                                print(f"tile level: {tile.level}")
                                print(f"money: {money}")
                                upgradecost = towerDict[tile.type]["level2"]["upgradeCost"]
                                print(f"upgrade costed {upgradecost}")
                            elif tile.level == 2 and money >= towerDict[tile.type]["level3"]["upgradeCost"]:
                                tile.level += 1
                                money -= towerDict[tile.type]["level3"]["upgradeCost"]

                                #DEBUG
                                print(f"tile level: {tile.level}")
                                print(f"money: {money}")
                                upgradecost = towerDict[tile.type]["level3"]["upgradeCost"]
                                print(f"upgrade costed {upgradecost}")
                            else:
                                print("either you are broke or the tower is maxed")
                                print(f"money: {money}")
                            tile.updateTowerLevel()   

                            if towerRangePos == tile.center.call(): # Updating tower range after upgrade
                                towerRangeRadius = tile.Range



    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # Update game tick
    gameTick += 1

    # Generates all occupied tiles from the list of structures
    for tile in structureList:
        for coordinate in matrix(tile.gridPos, tile.size):
            occupiedTiles.append(coordinate)

    # Controls tower building state ("place", "sell", "repair")
    if key_q.keyJustPressed():
        if actionState != "sell":
            print("[debug]: toggled SELL mode on")
            actionState = "sell"
        else:
            print("[debug]: defaulted to PLACE mode")
            actionState = "place"
    elif key_r.keyJustPressed():
        if actionState != "repair":
            print("[debug]: toggled REPAIR mode on")
            actionState = "repair"
        else:
            print("[debug]: defaulted to PLACE mode")
            actionState = "place"
    elif key_d.keyJustPressed():
        if actionState != "upgrade":
            print("[debug]: toggled UPGRADE mode on")
            actionState = "upgrade"
        else:
            print("[debug]: defaulted to PLACE mode")
            actionState = "place"
    elif key_1.keyJustPressed():
        towerType = "archer"
    elif key_2.keyJustPressed():
        towerType = "cannon"
    elif key_3.keyJustPressed():
        towerType = "wizard"
        

    # ==========
    # MECHANICS & RENDERING
    # ==========    
    
    screen.blit(background, (0,0))  # always the first drawing command

    # Structure mechanics
    for tile in structureList:
        if tile.Health <= 0:
            structureList.remove(tile)

        # Attacking enemies
        if len(enemyList) >= 1 and gameTick % tile.attackSpeed == 0:
            closestEnemy = enemyList[0]
            for enemy in enemyList:
                if findDistance(tile.center, enemy.pos) <= findDistance(tile.center, closestEnemy.pos):
                    closestEnemy = enemy

            if findDistance(tile.center, closestEnemy.pos) <= tile.Range:
                tile.lastTargetPos = point(*closestEnemy.pos.call())
                if tile.type == "wizard":
                    for x in range(5):
                        magic_blast = projectile(point(*tile.center.call()), tile.Damage, closestEnemy, tile.attackType)
                        magic_blast.skew_dx = random.random() - 0.5
                        magic_blast.skew_dy = random.random() - 0.5
                        projectileList.append(magic_blast)
                else:
                    projectileList.append(projectile(point(*tile.center.call()), tile.Damage, closestEnemy, tile.attackType))

    # Enemy mechanics
    for enemy in enemyList:
        if enemy.Health <= 0:
            enemyList.remove(enemy)

        if len(structureList) >= 1:
            # Moving toward targets
            for y in range(enemy.Speed):
                enemy.step(structureList)
            
            # Attacking targets
            if gameTick % enemy.attackSpeed == 0:
                for tile in structureList:
                    print(tile.center.call())
                    print(findClosestPoint(structureList, enemy.pos).call())
                    if tile.center.call() == findClosestPoint(structureList, enemy.pos).call():
                        if findDistance(tile.center, enemy.pos) <= enemy.Range:
                            projectileList.append(projectile(point(*enemy.pos.call()), enemy.Damage, tile, enemy.attackType))

    # Projectile mechanics
    for bullet in projectileList:
        if len(projectileList) >= 1:
            for i in range(bullet.Speed):
                if type(bullet.target) == structure:
                    if findDistance(bullet.pos, bullet.target.center) <= 10:
                        bullet.target.damage(bullet.Damage)
                        projectileList.remove(bullet)
                        break
                elif type(bullet.target) == Enemy:
                    if findDistance(bullet.pos, bullet.target.pos) <= 10:
                        bullet.target.damage(bullet.Damage)
                        projectileList.remove(bullet)
                        break
                bullet.findTargetPath()
                bullet.step()

    # Drawing all entities
    for tile in structureList:
        tile.draw(screen)
    for bullet in projectileList:
        bullet.imageFile.render(screen)
    for tile in structureList:
        tile.updateTurretRotation()
        tile.drawTurret(screen)
    for enemy in enemyList:
        enemy.imageFile.render(screen)

    # Drawing tower radius
    towerRadiusSurface = pygame.Surface(SIZE, pygame.SRCALPHA)
    towerRadiusSurface = towerRadiusSurface.convert_alpha()

    if displayTowerRange == True:
        pygame.draw.circle(towerRadiusSurface, (255, 255, 255, 100), towerRangePos, towerRangeRadius)
    
    screen.blit(towerRadiusSurface, (0,0))



    # Shadow placement; displays the region of placement when the player hovers their cursor on the map
    # The mouse vertex is the top left vertex of the shadow placement, converted to grid pos
    mouseVertex = point(*pygame.mouse.get_pos())
    mouseVertex.snapToGrid()
    mouseVertex = region(mouseVertex, testingSize)[0]

    # Rendering available and obstructed tiles when trying to place a structure
    if actionState == "place":
        # Draw a RED tile around the cursor if placement is impossible
        for tile in findOverlapping(mouseVertex, testingSize, occupiedTiles):
            pygame.draw.rect(screen, (255, 50, 50), (tile[0] * 20, tile[1] * 20, 20, 20))
    
        # Draw a GREEN tile around the cursor if placement is possible
        for tile in findPlaceableTiles(mouseVertex, testingSize, occupiedTiles):
            pygame.draw.rect(screen, (50, 255, 50), (tile[0] * 20, tile[1] * 20, 20, 20))

    pygame.display.flip()
    clock.tick(30)
    #---------------------------

pygame.quit()
