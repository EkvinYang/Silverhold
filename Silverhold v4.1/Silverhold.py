import pygame
import random
import math
import sys
import time
import os
import json
from Silverhold_constants import *
from Silverhold_functions import *
from Silverhold_dictionaries import *

pygame.init()
pygame.mixer.init()

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)
#kevin
screen = pygame.display.set_mode(SIZE)
directory = os.path.dirname(os.path.realpath(__file__))

# Initialize global variables
# ---------------------------
white = (255,255,255)
black = (0, 0, 0)

# 1 = home, 2 = settings, 3 = help,  4 = gameplay
Current_Game_State = 1
# 1 = easy, 2 = medium, 3 = hard     difficulty number is enemy stat amplifier. 100%, 150%, 200%  for example
Game_Difficulty = 1
difficultyMultiplier = {1: 1, 2: 1.25, 3: 1.5}

# 1 = survival, 2 = hardcore    hardcore is 1 health towers
Game_Mode = 1

smallfont = pygame.font.SysFont('Corbel',35) 
text_surface = pygame.display.set_mode((100, 100))

# SOUNDTRACKS George
menuSoundTrackFile = directory + "/menu_music.mp3"
gameSoundTrackFile = directory + "/game_music.mp3"
loseSoundTrackFile = directory + "/gameOver_music.mp3"

#Gamestates Kevin
# gamestate 1
menuSoundTrackTick = -20
title_button = Button(240, 60, 800, 450, "", black, "SilverholdTitle.png")
play_button = Button(496, 459, 288, 162, "", black, "PlayButton.png")
settings_button = Button(20, 130, 80, 80, "", black, "menu_settings.png")
quit_button = Button(20, 20, 80, 80, "", black, "QuitButton.png")
help_button = Button(20, 250, 80, 80, "", black, "HelpButton.png")
credits_button = Button(20, 360, 80, 80, "", black, "menu_credits.png")
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
help_info_5 = Button(620, 455, 90,90, "5. Hover mouse over towers to display structure information", black,"TextBackground.png")
help_info_6 = Button(620, 555, 90,90, "6. Have fun!", black, "TextBackground.png")
help_Buttons  = [help_info, help_info_1, help_info_2, help_info_3, help_info_4, help_info_5, help_info_6]

#gamestate 4
gameSoundTrackTick = -20
Money = 5000
MoneyCountDisplay = Button(782, -90, 700, 300, "Gold: "+ str(Money), black, "WoodPlank.png") 
Wave = 0
WaveCountDisplay = Button(782, -20, 700, 300, "Wave: " + str(Wave), black, "WoodPlank.png")
EnemiesKilled = 0
EnemiesKilledCountDisplay = Button(782, 50, 700, 300, "Kills: " + str(EnemiesKilled), black, "WoodPlank.png")
GameBackground = pygame.image.load(directory+"/sprites/game_background.png")

#gamestate 5
GameOverText = Button(150, 100, 1000, 200, "", black, "GameOver.png")
WaveText = Button(120, 230, 1000, 300, "", black, "WoodPlank.png")
EnemiesKilledText = Button(120, 350, 1000, 300, "", black, "WoodPlank.png")

#gamestate 6
Credits_Background = Button(150, 50, 1080, 520, "", black, "TextBackground.png")
Credits1 = Button(620, 55, 90,90,  "Kevin - Gamestates, Menu, Drawing, Sprites", black, "TextBackground.png")
Credits2 = Button(620, 155, 90,90,  "George - Towers, Pathfinding, Projectiles, Music", black, "TextBackground.png")
Credits3 = Button(620, 255, 90,90,  "Sean - Enemies, Wave Spawning, JSON", black, "TextBackground.png")
Credits4 = Button(620, 355, 90,90,  "Music by Tobi, Needlr, Mirera", black, "TextBackground.png")
Credits5 = Button(620, 455, 90,90,  "Code from ChatGPT", black, "TextBackground.png")
Credits  = [Credits_Background, Credits1, Credits2, Credits3, Credits4, Credits5]


# tower shop Kevin
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

# towers Kevin
structureList = []
Placing_Tower = False
Max_Towers = 0
Tower_Held = ""
grid = [[0]*int(WIDTH/20)]*int(HEIGHT/20)
occupiedTiles = []

# enemies All
currentMobCount = 0
enemy_queue = []
last_spawn_time = 0
last_wave_time = 0
spawn_delay = 50
enemyList = []

# projectiles George
projectileList = []

drawingSurface = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
mouse_x = 0
mouse_y = 0

# George
loseSoundTrackTick = 0
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
            # mouse input depending on game state Kevin 
            if Current_Game_State == 1:
                if clicked_Button(quit_button, mouse_x, mouse_y):
                    pygame.mixer.music.stop()
                    running = False
                elif clicked_Button(settings_button, mouse_x, mouse_y):
                    Current_Game_State = 2
                elif clicked_Button(help_button, mouse_x, mouse_y):
                    Current_Game_State = 3
                elif clicked_Button(play_button, mouse_x, mouse_y):
                    Current_Game_State = 4
                    #music from george
                    pygame.mixer.music.stop()
                    gameSoundTrackTick = -20
                    central_Tower.Health = towerDict["central"]["level1"]["Health"]
                    structureList.append(central_Tower)
                    current_time = 0
                    last_wave_time = 0
                elif clicked_Button(credits_button, mouse_x, mouse_y):
                    Current_Game_State = 6
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
                    pygame.mixer.music.stop()
                    menuSoundTrackTick = -20
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
                    actionState = "default"
                    Placing_Tower = False
                        
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
                        actionState = "default"
                
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
                            actionState = "default"
                            Tower_Shop_Open = False
                            Tower_Held = ""
                            Placing_Tower = False
                
                    # Attempts to delete a tower upon LEFT click
                elif actionState == "sell" and event.button == 1 and not override_tower_placement:
                    # code from george
                    clickedTile = point(*event.pos)
                    for tile in structureList:
                        if checkCollidePoint(tile.gridPos, tile.size, clickedTile) and tile.type != "central":
                            Money += int(tile.Value / 2)
                            structureList.remove(tile)
                            actionState = "default"

                elif actionState == "repair" and event.button == 1:
                    clickedTile = point(*event.pos)
                    for tile in structureList:
                        if checkCollidePoint(tile.gridPos, tile.size, clickedTile):
                            if tile.repairModeOn == True:
                                tile.repairModeOn = False
                            else:
                                tile.repairModeOn = True

                # Tower upgrading
                elif event.button == 3 and actionState == "default":
                    clickedTile = point(*event.pos)
                    for tile in structureList:
                        if checkCollidePoint(tile.gridPos, tile.size, clickedTile) and tile.type != "central":
                            if tile.level == 1 and Money >= towerDict[tile.type]["level2"]["upgradeCost"]:
                                tile.level += 1
                                Money -= towerDict[tile.type]["level2"]["upgradeCost"]
                                tile.updateTowerLevel()
                            elif tile.level == 2 and Money >= towerDict[tile.type]["level3"]["upgradeCost"]:
                                tile.level += 1
                                Money -= towerDict[tile.type]["level3"]["upgradeCost"]
                                tile.updateTowerLevel()

            elif Current_Game_State == 5:
                pygame.mixer.music.stop
                
                if clicked_Button(quit_button, mouse_x, mouse_y):
                    Current_Game_State = 1
                    pygame.mixer.music.stop()
                    menuSoundTrackTick = -20
                    Wave = 0
                    EnemiesKilled = 0
            elif Current_Game_State == 6:
                if clicked_Button(quit_button, mouse_x, mouse_y):
                    Current_Game_State = 1
    # GAME STATE UPDATES
    # All game math and comparisons happen here
    gameTick += 1
    mousePos = point(*pygame.mouse.get_pos())

    # Acion states
    if key_q.keyJustPressed():
        if actionState != "sell":
            actionState = "sell"
        else:
            actionState = "default"
    elif key_r.keyJustPressed():
        if actionState != "repair":
            actionState = "repair"
        else:
            actionState = "default"
    elif key_d.keyJustPressed():
        if actionState != "default":
            actionState = "default"

    # code from george
    if Current_Game_State == 4:
        gameSoundTrackTick += 1
        if gameSoundTrackTick % 3000 == 0:
            pygame.mixer.music.load(gameSoundTrackFile)
            pygame.mixer.music.play()
        occupiedTiles = []
        # Generates all occupied tiles from the list of structures
        for tile in structureList:
            for coordinate in matrix(tile.gridPos, tile.size):
                occupiedTiles.append(coordinate)
        mouseGrid = point(*pygame.mouse.get_pos())
        mouseGrid.snapToGrid()
        #code from sean
        current_time = pygame.time.get_ticks()
        
        # generating enemies Sean and Kevin
        if currentMobCount == 0 and current_time - last_wave_time >= 2000:
            Wave += 1
            healthModifier = 0.5
            if Wave > 0:
                healthModifier = math.sqrt(Wave)
            # random amount of mobs for the current wave
            currentMobCount = random.randint(3 + 3 * round(math.log2(Wave)), 6 + 3 * round(math.log2(Wave)))
            # spawn mobs
            for _ in range(currentMobCount):
                enemy_type = random.choice(["sailboat"] * 9 + ["caravel"] * (5 + Wave) + ["brigantine"] * Wave)
                # Ensure enemies spawn within bounds
                x = random.randint(5,15)
                y = random.randint(0,720)
                enemy_queue.append((x, y, enemy_type))

        # ChatGPT for enemy spawn delay
        if enemy_queue and current_time - last_spawn_time >= spawn_delay:
            x, y, enemy_type = enemy_queue.pop(0)
            spawnPoint = point(x, y)
            enemyList.append(Enemy(spawnPoint, enemy_type, healthModifier))
            last_spawn_time = current_time
            # Update spawn delay to a random value between 250 and 300 ms
            spawn_delay = random.randint(250, 300)
            
    # george
    # Structure mechanics
        for tile in structureList:
            if tile.Health <= 0:
                structureList.remove(tile)
                if (tile.type == "central"):
                    Tower_Shop_Open = False
                    structureList = []
                    enemyList = []
                    projectileList = []
                    currentMobCount = 0
                    gameTick = 0
                    Money = 5000
                    current_time = 0
                    last_wave_time = 0
                    last_spawn_time = 0
                    override_tower_placement = True

                    # Music
                    pygame.mixer.music.stop()
                    gameSoundTrackTick = -20
                    loseSoundTrackTick = -20
                    Current_Game_State = 5

                    dumped = False
                    WaveText.text = "You reached wave " + str(Wave) + "!"
                    EnemiesKilledText.text  = "You killed " + str(EnemiesKilled) + " enemies!"

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
    MoneyCountDisplay.text = str("Gold: " + str(Money))
    WaveCountDisplay.text = str("Wave: " + str(Wave))
    EnemiesKilledCountDisplay.text = str("Kills: " + str(EnemiesKilled))
    
    # DRAWING AND MUSIC
    #george
    drawingSurface.fill(white)  # always the first drawing command
    if Current_Game_State in [1, 2, 3, 6]:
        menuSoundTrackTick += 1
        menuTitleYAxisShift = round(5 * math.sin(menuSoundTrackTick / 20)) # Shifting the vertical title button for aesthetic
        title_button.shift(0, menuTitleYAxisShift)

        if menuSoundTrackTick % 6000 == 0:
            pygame.mixer.music.load(menuSoundTrackFile)
            pygame.mixer.music.play()
    #Kevin
    if (Current_Game_State == 1):
        # home screen
        drawingSurface.blit(MenuBackground, (0,0))
        draw_Button(title_button, drawingSurface, text_surface, smallfont)
        draw_Button(play_button, drawingSurface, text_surface, smallfont)
        draw_Button(settings_button, drawingSurface, text_surface, smallfont)
        draw_Button(help_button, drawingSurface, text_surface, smallfont)
        draw_Button(quit_button, drawingSurface, text_surface, smallfont)
        draw_Button(credits_button, drawingSurface, text_surface, smallfont)
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
        # Drawing all entities
        #functions from kevin and george
        for tile in structureList:
            tile.draw(drawingSurface)
        for bullet in projectileList:
            bullet.imageFile.render(drawingSurface)
        for tile in structureList:
            tile.updateTurretRotation()
            tile.drawTurret(drawingSurface)
            if tile.repair(Money, gameTick, screen):
                Money -= 1
        for enemy in enemyList:
            enemy.imageFile.render(drawingSurface) 
        draw_Button(MoneyCountDisplay, drawingSurface, text_surface, smallfont)
        draw_Button(WaveCountDisplay, drawingSurface, text_surface, smallfont)
        draw_Button(EnemiesKilledCountDisplay, drawingSurface, text_surface, smallfont)
        # inside game
        draw_Button(quit_button, drawingSurface, text_surface, smallfont)
            
        # Displaying a tower's range upon hover George
        displayTowerRange = False
        if actionState not in ["place", "sell"]:
            for tile in structureList:
                if checkCollidePoint(tile.gridPos, tile.size, mousePos) and displayTowerRange == False:
                    towerRangePos = tile.center.call()
                    towerRangeRadius = tile.Range
                    displayTowerRange = True

        # george
        # Drawing tower radius
        towerRadiusSurface = pygame.Surface(SIZE, pygame.SRCALPHA)
        towerRadiusSurface = towerRadiusSurface.convert_alpha()

        if displayTowerRange == True:
            pygame.draw.circle(towerRadiusSurface, (255, 255, 255, 100), towerRangePos, towerRangeRadius)

        screen.blit(towerRadiusSurface, (0,0))

        # Tower view: hovering over a tower displays its stats 
        # George
        if actionState != "place":
            for tile in structureList:
                if checkCollidePoint(tile.gridPos, tile.size, mousePos) and tile.type != "central":
                    infoPosX = tile.pos.call()[0]
                    infoPosY = tile.pos.call()[1]
                    infoFile = "info_" + tile.type + str(tile.level) + ".png"

                    if infoPosX + tile.size * 20 + 220 < 1280:
                        infoPosX += tile.size * 20 + 20
                    else:
                        infoPosX -= 220
                    if infoPosY + 150 > 720:
                        infoPosY -= 150 - tile.size * 20

                    healthBarPos = [infoPosX + 30, infoPosY + 75]
                    healthBarProgress = int(tile.Health / tile.maxHealth * 69)
                    infoImage = Image(point(infoPosX + 100, infoPosY + 70), infoFile, (200, 150), 0)
                    infoImage.render(screen)

                    pygame.draw.rect(screen, (255, 50, 50), (*healthBarPos, healthBarProgress, 14))
        
        # tower shop MENU   Kevin
        draw_Button(open_tower_shop_button, drawingSurface, text_surface, smallfont)
        if (Tower_Shop_Open):
            draw_Button(close_tower_shop_button, drawingSurface, text_surface, smallfont)
            for towerButtonIcon in tower_Shop_Menu:
                draw_Button(towerButtonIcon, drawingSurface, text_surface, smallfont)
        
        mouseVertex = point(*pygame.mouse.get_pos())
        mouseVertex.snapToGrid()
        mouseVertex = region(mouseVertex, testingSize)[0]

        # Rendering available and obstructed tiles when trying to place a structure Kevin and George
        if actionState == "place":
            # Draw a RED tile around the cursor if placement is impossible
            for tile in findOverlapping(mouseVertex, testingSize, occupiedTiles):
                pygame.draw.rect(drawingSurface, (255, 50, 50), (tile[0] * 20, tile[1] * 20, 20, 20))
        
            # Draw a GREEN tile around the cursor if placement is possible
            for tile in findPlaceableTiles(mouseVertex, testingSize, occupiedTiles):
                pygame.draw.rect(drawingSurface, (50, 255, 50), (tile[0] * 20, tile[1] * 20, 20, 20))

    elif Current_Game_State == 5:
        drawingSurface.blit(MenuBackground, (0,0))
        draw_Button(GameOverText, drawingSurface, text_surface, smallfont)
        draw_Button(quit_button, drawingSurface, text_surface, smallfont)
        draw_Button(WaveText, drawingSurface, text_surface, smallfont)
        draw_Button(EnemiesKilledText, drawingSurface, text_surface, smallfont)

        # Music
        loseSoundTrackTick += 1
        if loseSoundTrackTick % 3500 == 0:
            pygame.mixer.music.load(loseSoundTrackFile)
            pygame.mixer.music.play()
        
        #JSON data storage Sean
        with open('UserData.json', 'r') as userData:
            dataPayload = json.load(userData)
            updatedStats = {
                "Highest Wave": max(dataPayload["Highest Wave"], Wave),
                "Highest Enemies Killed": max(dataPayload["Highest Enemies Killed"], EnemiesKilled),
                "Total Enemies Killed": dataPayload["Total Enemies Killed"] + EnemiesKilled
            }
        if not dumped:
            with open('UserData.json', 'w') as userData:
                json.dump(updatedStats, userData)
        dumped = True
    elif Current_Game_State == 6:
         drawingSurface.blit(MenuBackground, (0,0))
         # help
         for credit in Credits:
            draw_Button(credit, drawingSurface, text_surface, smallfont)
         draw_Button(quit_button, drawingSurface, text_surface, smallfont)
    # Must be the last two lines of the game loop

    pygame.display.flip()
    clock.tick(30)
    #---------------------------

pygame.quit()
