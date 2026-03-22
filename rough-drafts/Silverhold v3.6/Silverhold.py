import pygame
import random
import math
import sys
import time
import os
from Silverhold_constants import *
from Silverhold_functions import *
from Silverhold_dictionaries import *
pygame.init()

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)
directory = os.path.dirname(os.path.realpath(__file__))
print(directory + "/sprites/")
# code from george
 
#code from sean

# Initialize global variables
# ---------------------------
white = (255,255,255)
black = (0, 0, 0)
button_color = (204, 106, 106)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# 1 = home, 2 = settings, 3 = help,  4 = gameplay
Current_Game_State = 1
# 1 = easy, 2 = medium, 3 = hard     difficulty number is enemy stat amplifier. 100%, 150%, 200%  for example
Game_Difficulty = 1
difficultyMultiplier = {1: 1, 2: 1.25, 3: 1.5}

# 1 = survival, 2 = hardcore    hardcore is 1 health towers
Game_Mode = 1

smallfont = pygame.font.SysFont('Corbel',35) 
text_surface = pygame.display.set_mode((100, 100))

# gamestate 1
title_button = Button(180, 80, 1000, 210, "", black, "SilverholdTitle.png")
play_button = Button(450, 250, 370, 160, "", black, "PlayButton.png")
settings_button = Button(20, 130, 80, 80, "", black, "menu_settings.png")
quit_button = Button(20, 20, 80, 80, "", black, "QuitButton.png")
help_button = Button(20, 250, 80, 80, "", black, "HelpButton.png")
MenuBackground = pygame.image.load(directory+"/sprites/MenuBackground2.png")

#gamestate 2
difficulty_easy = Button(170, 100, 200, 200, "Easy", black, "menu_challenges.png")
difficulty_medium = Button(540, 100, 200, 200, "Medium", black, "QuitButton.png")
difficulty_hard = Button(910, 100, 200, 200, "Hard", black, "QuitButton.png")
gamemode_survival = Button(300, 350, 200, 200, "Survival", black, "menu_challenges.png")
gamemode_hardcore = Button(780, 350, 200, 200, "Hardcore", black, "QuitButton.png")

# gamestate 3

help_info = Button(150, 50, 1080, 620, "", black, "TextBackground.png")
help_info_1 = Button(620, 55, 90,90,  "1. Survive as many waves as possible by protecting the central tower", black, "TextBackground.png")
help_info_2 = Button(620, 155, 90,90, "2. Enemies will spawn at the start of each wave, defeat them to progress", black,"TextBackground.png")
help_info_3 = Button(620, 255, 90,90, "3. Place and upgrade towers in order to defeat enemies", black, "TextBackground.png")
help_info_4 = Button(620, 355, 90,90, "4. Place and upgrade towers through their respective menus", black, "TextBackground.png")
help_info_5 = Button(620, 455, 90,90, "5. Change difficulties to unlock new challenges and different playstyes", black,"TextBackground.png")
help_info_6 = Button(620, 555, 90,90, "6. Have fun!", black, "TextBackground.png")
help_Buttons  = [help_info, help_info_1, help_info_2, help_info_3, help_info_4, help_info_5, help_info_6]
#gamestate 4
Money = 5000
MoneyText = Button(800, -70, 700, 300, "Money: "+ str(Money), black, "WoodPlank.png") 

Wave = 0
EnemiesKilled = 0
GameBackground = pygame.image.load(directory+"/sprites/game_background.png")
# boost shop
# Boost_Shop_Open = False
# open_boost_shop_button = Button(1180, 200, 75, 75, "shop", black, "menu_challenges.png")
# close_boost_shop_button = Button(1100, 200, 60, 60, "", black, "QuitButton.png")
# boost_Shop_Menu = []
# example_Boost_Button = Button(1180, 300, 50, 50, green, "$", black)

# tower shop
Tower_Shop_Open = False
open_tower_shop_button = Button (25, 200, 75, 75, "Towers", black, "menu_challenges.png")
close_tower_shop_button = Button(120, 200, 60, 60, "", black, "QuitButton.png")

central_Tower = structure(point(50,16), "central", 1)
wizard_Tower_Button = Button(25, 300, 50, 50, "wizard", black, "tower_wizard1.png")
archer_Tower_Button = Button(25, 450, 50, 50, "archer", black, "tower_archer1.png")
cannon_Tower_Button = Button(25, 375, 50, 50, "cannon", black, "tower_cannon1.png")

tower_Shop_Menu  = []
tower_Shop_Menu.append(wizard_Tower_Button)
tower_Shop_Menu.append(archer_Tower_Button)
tower_Shop_Menu.append(cannon_Tower_Button)

# towers
structureList = []
Placing_Tower = False
Max_Towers = 0
Tower_Held = ""
grid = [[0]*int(WIDTH/20)]*int(HEIGHT/20)
occupiedTiles = []

# enemies
currentMobCount = 0
enemy_queue = []
last_spawn_time = 0
last_wave_time = 0
spawn_delay = 50
enemyList = []
base_pos = [WIDTH / 2, HEIGHT / 2]

# projectiles
projectileList = []
#gamestate 5
GameOverText = Button(150, 100, 1000, 200, "", black, "GameOver.png")
WaveText = Button(120, 230, 1000, 300, "", black, "WoodPlank.png")
EnemiesKilledText = Button(120, 350, 1000, 300, "", black, "WoodPlank.png")
 
drawingSurface = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
mouse_x = 0
mouse_y = 0

gameTick = 0
running = True
actionState = ""
while running:
    # EVENT HANDLING
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = mouse[0]
            mouse_y = mouse[1]
            if Current_Game_State == 1:
                if clicked_Button(quit_button, mouse_x, mouse_y):
                    running = False
                elif clicked_Button(settings_button, mouse_x, mouse_y):
                    Current_Game_State = 2
                elif clicked_Button(help_button, mouse_x, mouse_y):
                    Current_Game_State = 3
                elif clicked_Button(play_button, mouse_x, mouse_y):
                    Current_Game_State = 4
                    
                    structureList.append(central_Tower)
                    current_time = 0
                    last_wave_time = 0
            elif Current_Game_State == 2:
                if clicked_Button(quit_button, mouse_x, mouse_y):
                    Current_Game_State = 1
                elif (clicked_Button(difficulty_easy, mouse_x, mouse_y)):
                    if (Game_Difficulty != 1):
                        Game_Difficulty = 1
                        difficulty_easy.fileName = "menu_challenges.png"
                        difficulty_medium.fileName = "QuitButton.png"
                        difficulty_hard.fileName = "QuitButton.png"
                elif (clicked_Button(difficulty_medium, mouse_x, mouse_y)):
                    if (Game_Difficulty != 2):
                        Game_Difficulty = 2
                        difficulty_easy.fileName = "QuitButton.png"
                        difficulty_medium.fileName = "menu_challenges.png"
                        difficulty_hard.fileName = "QuitButton.png"
                elif (clicked_Button(difficulty_hard, mouse_x, mouse_y)):
                    if (Game_Difficulty != 3):
                        Game_Difficulty = 3
                        difficulty_easy.fileName = "QuitButton.png"
                        difficulty_medium.fileName = "QuitButton.png"
                        difficulty_hard.fileName = "menu_challenges.png"
                elif (clicked_Button(gamemode_survival, mouse_x, mouse_y)):
                    if (Game_Mode != 1):
                        Game_Mode = 1
                        gamemode_survival.fileName = "menu_challenges.png"
                        gamemode_hardcore.fileName = "QuitButton.png"
                elif (clicked_Button(gamemode_hardcore, mouse_x, mouse_y)):
                    if (Game_Mode != 2):
                        Game_Mode = 2
                        gamemode_survival.fileName = "QuitButton.png"
                        gamemode_hardcore.fileName = "menu_challenges.png"
            elif Current_Game_State == 3:
                if clicked_Button(quit_button, mouse_x, mouse_y):
                    Current_Game_State = 1
            elif Current_Game_State == 4:
                override_tower_placement = False
                if clicked_Button(quit_button, mouse_x, mouse_y):
                    Current_Game_State = 1
                    Tower_Shop_Open = False
                    structureList = []
                    occupiedTiles = []
                    current_time = 0
                    last_wave_time = 0
                    last_spawn_time = 0
                    enemyList = []
                    projectileList = []
                    Money = 5000
                    Wave = 0
                    gameTick = 0
                    EnemiesKilled = 0
                    currentMobCount = 0
                    override_tower_placement = True
                elif (clicked_Button(open_tower_shop_button, mouse_x, mouse_y)):
                    Tower_Shop_Open = True
                    override_tower_placement = True
                elif (clicked_Button(close_tower_shop_button, mouse_x, mouse_y)):
                    Tower_Shop_Open = False
                    override_tower_placement = True
                    Tower_Held = ""
                    actionState = "none"
                    Placing_Tower = False
                if key_q.keyJustPressed():
                    if actionState != "sell":
                        print("[debug]: toggled SELL mode on")
                        actionState = "sell"
                elif key_r.keyJustPressed():
                    if actionState != "repair":
                        print("[debug]: toggled REPAIR mode on")
                        actionState = "repair"
                elif key_d.keyJustPressed():
                    if actionState != "upgrade":
                        print("[debug]: toggled UPGRADE mode on")
                        actionState = "upgrade"
                        
                for tower_button in tower_Shop_Menu: #list of buttons
                    if clicked_Button(tower_button, mouse_x, mouse_y) and not Placing_Tower and Money >= towerDict[tower_button.text]["level1"]["Cost"]:
                        Tower_Held = tower_button.text
                        Placing_Tower = True
                        actionState = "place"
                        override_tower_placement = True
                    elif clicked_Button(tower_button, mouse_x, mouse_y) and Placing_Tower:
                        Tower_Held = ""
                        Placing_Tower = False
                        override_tower_placement = True 
                        actionState = "none"
                if actionState == "place" and event.button == 1 and not override_tower_placement and Placing_Tower and len(structureList) < 2*Game_Difficulty+9:
                    # When a tile is clicked, its location is snapped to grid and converted to structure object
                    # code from george
                    
                    clickedTile = point(*event.pos)
                    clickedTile.snapToGrid()
                    clickedVertex = region(clickedTile, testingSize)[0]
                    
                    if (gamemode_hardcore):
                        clickedTile.health = 1
                        
                    if checkCollision(clickedVertex, testingSize, occupiedTiles):
                        if Money >= towerDict[Tower_Held]["level1"]["Cost"]:
                            structureList.append(structure(clickedVertex, Tower_Held, 1))
                            Money -= towerDict[Tower_Held]["level1"]["Cost"]
                            actionState = "none"
                            Tower_Shop_Open = False
                            Tower_Held = ""
                            Placing_Tower = False
                
                    # Attempts to delete a tower upon right click
                elif actionState == "sell" and event.button == 3 and not override_tower_placement:
                    # code from george
                    clickedTile = point(*event.pos)
                    clickedTile.snapToGrid()
                    for tile in structureList:
                        if checkCollidePoint(tile.gridPos, tile.size, clickedTile) and tile.name != "central":
                            Money += int(tile.Value / 2)
                            structureList.remove(tile)
                            actionState = "none"
            elif Current_Game_State == 5:
                if clicked_Button(quit_button, mouse_x, mouse_y):
                    Current_Game_State = 1
                    Wave = 0
                    EnemiesKilled = 0
    # GAME STATE UPDATES

    # All game math and comparisons happen here
    gameTick += 1
    # code from george
    
    if  Current_Game_State == 4:
        # Generates all occupied tiles from the list of structures
        for tile in structureList:
            for coordinate in matrix(tile.gridPos, tile.size):
                occupiedTiles.append(coordinate)
        mouseGrid = point(*pygame.mouse.get_pos())
        mouseGrid.snapToGrid()
        #code from sean
        current_time = pygame.time.get_ticks()
        if currentMobCount == 0 and current_time - last_wave_time >= 1000:
            Wave += 1
            # random amount of mobs for the current wave
            currentMobCount = random.randint(10 + 10 * round(math.log2(Wave)), 20 + 10 * round(math.log2(Wave)))
            # spawn mobs
            for _ in range(currentMobCount):
                enemy_type = random.choice(["sailboat", "caravel", "brigantine"])
                # Ensure enemies spawn within bounds
                y = random.randint(0,720)
                enemy_queue.append((0, y, enemy_type))
        # ChatGPT
        if enemy_queue and current_time - last_spawn_time >= spawn_delay:
            x, y, enemy_type = enemy_queue.pop(0)
            spawnPoint = point(x, y)
            enemyList.append(Enemy(spawnPoint, enemy_type))
            last_spawn_time = current_time
            # Update spawn delay to a random value between 250 and 300 ms
            spawn_delay = random.randint(250, 300)
    # george
    # Structure mechanics
        for tile in structureList:
            if tile.Health <= 0:
                structureList.remove(tile)
                for coordinate in matrix(tile.gridPos, tile.size):
                    for occupiedTile in occupiedTiles:
                        if (occupiedTile == coordinate):
                            occupiedTiles.remove(occupiedTile)
                if (tile.type == "central"):
                    Tower_Shop_Open = False
                    structureList = []
                    enemyList = []
                    projectileList = []
                    currentMobCount = 0
                    gameTick = 0
                    current_time = 0
                    last_wave_time = 0
                    last_spawn_time = 0
                    override_tower_placement = True
                    Current_Game_State = 5
                    WaveText.text = "You reached wave " + str(Wave) + "!"
                    EnemiesKilledText.text  = "You killed " + str(EnemiesKilled) + " enemies!"
                    #json stats update
                    Wave = 0

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
    # george
    for enemy in enemyList:
        if enemy.Health <= 0:
            Money += enemy.Value
            enemyList.remove(enemy)
            currentMobCount -= 1
            EnemiesKilled += 1
            if (currentMobCount == 0):
                last_wave_time = current_time
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
    
        #george
        #projectile mechanic
    for bullet in projectileList:
        for i in range(bullet.Speed):
            if type(bullet.target) == structure:
                if findDistance(bullet.pos, bullet.target.center) <= 20:
                    bullet.target.damage(bullet.Damage)
                    projectileList.remove(bullet)
                    break
            elif type(bullet.target) == Enemy:
                if findDistance(bullet.pos, bullet.target.pos) <= 20:
                    bullet.target.damage(bullet.Damage)
                    projectileList.remove(bullet)
                    break
            bullet.findTargetPath()
            bullet.step()
    MoneyText.text = str("Money: " + str(Money))
    # DRAWING
    drawingSurface.fill(white)  # always the first drawing command
    if (Current_Game_State == 1):
        # home screen
        drawingSurface.blit(MenuBackground, (0,0))
        draw_Button(title_button, drawingSurface, text_surface, smallfont)
        draw_Button(play_button, drawingSurface, text_surface, smallfont)
        draw_Button(settings_button, drawingSurface, text_surface, smallfont)
        draw_Button(help_button, drawingSurface, text_surface, smallfont)
        draw_Button(quit_button, drawingSurface, text_surface, smallfont)
    elif (Current_Game_State == 2):
        drawingSurface.blit(MenuBackground, (0,0))
        # settings
        draw_Button(quit_button, drawingSurface, text_surface, smallfont)
        draw_Button(difficulty_easy, drawingSurface, text_surface, smallfont)
        draw_Button(difficulty_medium, drawingSurface, text_surface, smallfont)
        draw_Button(difficulty_hard, drawingSurface, text_surface, smallfont)
        draw_Button(gamemode_survival, drawingSurface, text_surface, smallfont)
        draw_Button(gamemode_hardcore, drawingSurface, text_surface, smallfont)
    elif (Current_Game_State == 3):
        drawingSurface.blit(MenuBackground, (0,0))
        # help
        for helpButton in help_Buttons:
            draw_Button(helpButton, drawingSurface, text_surface, smallfont)
        draw_Button(quit_button, drawingSurface, text_surface, smallfont)
    elif (Current_Game_State == 4):
        drawingSurface.blit(GameBackground, (0,0))
        draw_Button(MoneyText, drawingSurface, text_surface, smallfont)
        # inside game
        draw_Button(quit_button, drawingSurface, text_surface, smallfont)
        # Drawing all entities
        for tile in structureList:
            tile.draw(drawingSurface)
            tile.updateTurretRotation()
            tile.drawTurret(drawingSurface)
        for bullet in projectileList:
            bullet.imageFile.render(drawingSurface)
        for enemy in enemyList:
            enemy.imageFile.render(drawingSurface)     
            
        
        # tower shop MENU  
        draw_Button(open_tower_shop_button, drawingSurface, text_surface, smallfont)
        if (Tower_Shop_Open):
            draw_Button(close_tower_shop_button, drawingSurface, text_surface, smallfont)
            for towerButtonIcon in tower_Shop_Menu:
                draw_Button(towerButtonIcon, drawingSurface, text_surface, smallfont)
        print(actionState)
        print(Tower_Held)
        # if actionState == "place":
        #     # Draw a RED tile around the cursor if placement is impossible
        #     if (Tower_Held != ""):
        #         for tile in findOverlapping(mouseGrid, towerDict[Tower_Held]["Size"], occupiedTiles): # returns as a LIST, not a POINT
        #             pygame.draw.rect(drawingSurface, (255, 50, 50), (20 * tile[0]-10, 20 * tile[1]-10,20,20))

        #         # Draw a GREEN tile around the cursor if placement is possible
        #         for tile in findOverlapping(mouseGrid, towerDict[Tower_Held]["Size"], occupiedTiles): # returns as a LIST, not a POINT
        #             pygame.draw.rect(drawingSurface, (50, 255, 50), (20 * tile[0]-10, 20 * tile[1]-10,20,20))
       # Shadow placement; displays the region of placement when the player hovers their cursor on the map
        # The mouse vertex is the top left vertex of the shadow placement, converted to grid pos
        mouseVertex = point(*pygame.mouse.get_pos())
        mouseVertex.snapToGrid()
        mouseVertex = region(mouseVertex, testingSize)[0]

        # Rendering available and obstructed tiles when trying to place a structure
        if actionState == "place":
            # Draw a RED tile around the cursor if placement is impossible
            for tile in findOverlapping(mouseVertex, testingSize, occupiedTiles):
                pygame.draw.rect(drawingSurface, (255, 50, 50), (tile.x * 20, tile.y * 20, 20, 20))
        
            # Draw a GREEN tile around the cursor if placement is possible
            for tile in findPlaceableTiles(mouseVertex, testingSize, occupiedTiles):
                pygame.draw.rect(drawingSurface, (50, 255, 50), (tile.x * 20, tile.y * 20, 20, 20))

    elif(Current_Game_State == 5):
        drawingSurface.blit(MenuBackground, (0,0))
        draw_Button(GameOverText, drawingSurface, text_surface, smallfont)
        draw_Button(quit_button, drawingSurface, text_surface, smallfont)
        draw_Button(WaveText, drawingSurface, text_surface, smallfont)
        draw_Button(EnemiesKilledText, drawingSurface, text_surface, smallfont)
    # Must be the last two lines
    # of the game loop
    print("towerheld: "+ Tower_Held)
    print("action: "+ actionState)
    print("wave: " + str(Wave))
    print("mobcount: " + str(currentMobCount))
    print("Current time: " + str(gameTick))
    print("Last wave time: " + str(last_wave_time))
    print("enemieskilled: " + str(EnemiesKilled))
    pygame.display.flip()
    clock.tick(30)
    #---------------------------
pygame.quit()