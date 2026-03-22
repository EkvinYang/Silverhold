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

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

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
                clickedVertex = region(clickedTile, testingSize)[0]

                if checkCollision(clickedVertex, testingSize, occupiedTiles):
                    if money >= towerDict[towerType]["level1"]["Cost"]:
                        structureList.append(structure(clickedVertex, towerType))
                        money -= towerDict[towerType]["level1"]["Cost"]
                        print(f"money: {money}")
                    else:
                        print("you are too broke")
            
            # Attempts to place an enemy on right click
            elif event.button == 3 and actionState == "place": 
                enemyList.append(Enemy(point(*event.pos), enemyType))

            # Attempts to delete a tower upon right click
            elif event.button == 1 and actionState == "sell":
                clickedTile = point(*event.pos)
                for tile in structureList:
                    if checkCollidePoint(tile.gridPos, tile.size, clickedTile):
                        money += int(tile.Value / 2)
                        print(f"money: {money}")
                        structureList.remove(tile)
            
            # Attempts to upgrade a tower upon right click
            elif event.button == 3 and actionState == "upgrade":
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



    # GAME STATE UPDATES
    # All game math and comparisons happen here

    currentTime = pygame.time.get_ticks() # amount of time the game has been running for
    if len(enemyList) == 0 and currentTime - lastWaveTime >= 3000:
        currentWave += 1
        # random amount of mobs for the current wave
        enemyCount = random.randint(10 + 10 * round(math.log2(currentWave)), 20 + 10 * round(math.log2(currentWave)))
        # create mobs to spawn
        for _ in range(enemyCount):
            # choosing a random mob
            enemyType = random.choice(["sailboat", "brigantine", "caravel"])
            print(enemyType)
            # random coordinates for it to spawn (not near the middle)
            while True:
                x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
                if (x < WIDTH / 4 or x > WIDTH - WIDTH / 4) or (y < HEIGHT / 4 or y > HEIGHT - HEIGHT / 4):
                    break
            enemyQueue.append((x, y, enemyType))

    if len(enemyQueue) > 0 and currentTime - lastSpawnTime >= spawnDelay:
        x, y, enemyType = enemyQueue.pop(0)
        enemyList.append(Enemy(point(x, y), enemyType))
        lastSpawnTime = currentTime
        # update spawn delay
        spawnDelay = random.randint(250, 500)


    # Update game tick
    gameTick += 1

    # Generates all occupied tiles from the list of structures
    occupiedTiles = []
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
    for bullet in projectileList:
        bullet.imageFile.render(screen)
    for tile in structureList:
        tile.updateTurretRotation()
        tile.draw(screen)
    for enemy in enemyList:
        enemy.imageFile.render(screen)



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

    waveText = font.render(f"Wave {currentWave}", True, (255, 255, 255))
    screen.blit(waveText, (WIDTH / 2, 50))

    pygame.display.flip()
    clock.tick(30)
    #---------------------------

pygame.quit()
