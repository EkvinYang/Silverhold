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
    def takeDamage(self, damageTaken):
        self.Health -= damageTaken
    def checkCollision(self, occupiedTiles):
        canBePlaced = True
        for coordinate in centeredMatrix(self.size):
            if self.location.moveCall_coord(*coordinate) in occupiedTiles:
                canBePlaced = False
        return canBePlaced
    
    # Returns the locations of all conflicting tiles within build zone
    def findOverlapping(self, occupiedTiles):
        tileOverlaps = []
        for coordinate in centeredMatrix(self.size):
            if self.location.moveCall_coord(*coordinate) in occupiedTiles:
                tileOverlaps.append(self.location.moveCall_coord(*coordinate))
        return tileOverlaps
    
    # Returns the locations of all non-conflicting tiles within build zone
    def findPlaceableTiles(self, occupiedTiles):
        availableTiles = []
        for coordinate in centeredMatrix(self.size):
            if self.location.moveCall_coord(*coordinate) not in occupiedTiles:
                availableTiles.append(self.location.moveCall_coord(*coordinate))
        return availableTiles
class Image:
    def __init__(self, topLeft: point, rotation: float, resolution: tuple, fileName: str): # Rotation is CLOCKWISE
        self.topLeft = topLeft
        self.rotation = rotation
        self.resolution = resolution
        self.fileName = fileName
        print(fileName)
        self.imageFile = pygame.image.load(directory + "/sprites/" + fileName)
        self.imageFile = pygame.transform.scale(self.imageFile, resolution)
    def render(self, rotation, surface):
        surface.blit(pygame.transform.rotate(self.imageFile, rotation), self.topLeft.call())
class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, text_color, fileName: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.fileName = fileName
        
        topleft=point(x,y)
        self.toImage = Image(topleft, 0, (width, height), fileName)   
#code from sean
class Enemy:
    def __init__(self, location: point, type, target: structure):
        self.location = location
        self.target = target
        self.damage = type["Damage"]
        self.health = type["Health"]
        self.size = type["Size"]
        self.speed = type["Speed"]
        self.color = type["Color"]

    def move(self, dx, dy):
        self.location.x += dx
        self.location.y += dy
        
    def takeDamage(self, damageTaken: float):
        self.health -= damageTaken
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

# 1 = survival, 2 = hardcore    hardcore is 1 health towers, survival is 100 health
Game_Mode = 1

smallfont = pygame.font.SysFont('Corbel',35) 
display_surface = pygame.display.set_mode((100, 100))

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
Money = 0
Wave = 0
EnemiesKilled = 0
GameBackground = pygame.image.load(directory+"/sprites/game_background.png")
projectilesList = []
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

central_Tower = structure(point(32,16), "central", 1)
wizard_Tower_Button = Button(25, 300, 50, 50, "wizard", black, "tower_wizard1.png")
archer_Tower_Button = Button(125, 300, 50, 50, "archer", black, "tower_archer1.png")
cannon_Tower_Button = Button(25, 375, 50, 50, "cannon", black, "tower_cannon1.png")

tower_Shop_Menu  = []
tower_Shop_Menu.append(wizard_Tower_Button)
tower_Shop_Menu.append(archer_Tower_Button)
tower_Shop_Menu.append(cannon_Tower_Button)

# placing towers
structureList = []
Placing_Tower = False
Max_Towers = 0
Tower_Held = ""
grid = [[0]*int(WIDTH/20)]*int(HEIGHT/20)
occupiedTiles = []
# enemies
def calcDistance(location1: point, location2: point) -> float:
    return ((location1.x-location2.x)**2+(location1.y-location2.y)**2)**(1/2)
currentMobCount = 0
enemy_queue = []
last_spawn_time = 0
last_wave_time = 0
spawn_delay = 50
enemies = {"Red": {"Damage": 10, "Health": 100, "Size": 10, "Speed": 5, "Color": (255, 0 , 0)},
           "Blue": {"Damage": 5, "Health": 50, "Size": 5, "Speed": 10, "Color": (0, 0, 255)},
           "Green": {"Damage": 15, "Health": 200, "Size": 15, "Speed": 3, "Color": (0, 255, 0)}}
wave_enemies = []
base_pos = [WIDTH / 2, HEIGHT / 2]
# projectiles

#gamestate 5
GameOverText = Button(150, 100, 1000, 200, "", black, "GameOver.png")
WaveText = Button(120, 230, 1000, 300, "", black, "WoodPlank.png")
EnemiesKilledText = Button(120, 350, 1000, 300, "", black, "WoodPlank.png")
 
# draw a button with text
def draw_Button(button):
    
    button.toImage.render(button.toImage.rotation, screen)
    button_text = smallfont.render(button.text, True, button.text_color)
    button_textRect = button_text.get_rect()
    button_textRect.center = (button.x + button.width/2, button.y + button.height/2)
    display_surface.blit(button_text, button_textRect)
# check if a button is clicked at a certain x,y coord
def clicked_Button(button, mouse_x, mouse_y) -> bool:
    return (button.x < mouse_x and mouse_x < button.x+button.width and button.y < mouse_y and mouse_y < button.y+button.height)
def centeredMatrix(n: int):
    coords = []
    lowerBound = -int(n/2)
    upperBound = n + lowerBound
    for x in range(lowerBound, upperBound):
        for y in range(lowerBound, upperBound):
            coords.append([x,y])
    return coords

# Returns the coordinate of the TOP LEFT element
def findMatrixPos(center: point, n: int):
    lowerBound = -int(n/2)
    return [center.call()[0] + lowerBound, center.call()[1] + lowerBound]

# Checks if a point is within a square region
def checkCollidePoint(pointPos: point, tile: structure):
    x = findMatrixPos(tile.location, tile.size)[0]
    dx = tile.size
    y = findMatrixPos(tile.location, tile.size)[1]
    dy = tile.size
    if x <= (pointPos.call())[0] <= x + dx and y <= (pointPos.call())[1] <= y + dy:
        return True
    else:
        return False

def findClosestPoint(objects: list, location: point):
    closestPointIndex = 0
    closestPoint = objects[0].location
    # Finds point w/ smallest distance to origin
    index = 0
    while index < len(objects):
        targetStructure = objects[index]
        if calcDistance(targetStructure.location.unsnapGrid(), location) < calcDistance(closestPoint.unsnapGrid(), location):
            closestPoint = targetStructure.location.unsnapGrid()
            closestPointIndex = index
        index += 1 
    result = (closestPoint, closestPointIndex)
    return result
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
mouse_x = 0
mouse_y = 0

running = True
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
                    Boost_Shop_Open = False
                    Tower_Shop_Open = False
                    structureList = []
                    wave_enemies = []
                    projectilesList = []
                    Money = 0
                    Wave = 0
                    EnemiesKilled = 0
                    currentMobCount = 0
                    override_tower_placement = True
                # elif (clicked_Button(open_boost_shop_button, mouse_x, mouse_y)):
                #     Boost_Shop_Open = True
                #     override_tower_placement = True
                # elif (clicked_Button(close_boost_shop_button, mouse_x, mouse_y)):
                #     Boost_Shop_Open = False
                #     override_tower_placement = True
                elif (clicked_Button(open_tower_shop_button, mouse_x, mouse_y)):
                    Tower_Shop_Open = True
                    override_tower_placement = True
                elif (clicked_Button(close_tower_shop_button, mouse_x, mouse_y)):
                    Tower_Shop_Open = False
                    override_tower_placement = True
                    Tower_Held = ""
                    Placing_Tower = False
                for tower_button in tower_Shop_Menu: #list of buttons
                    if (clicked_Button(tower_button, mouse_x, mouse_y) and not Placing_Tower):
                        Tower_Held = tower_button.text
                        Placing_Tower = True
                        override_tower_placement = True   
                    elif (clicked_Button(tower_button, mouse_x, mouse_y) and Placing_Tower):
                        Tower_Held = ""
                        Placing_Tower = False  
                        override_tower_placement = True 
                if event.button == 1 and not override_tower_placement and not Boost_Shop_Open and Placing_Tower and len(structureList) < 2*Game_Difficulty+7:
                    # When a tile is clicked, its location is snapped to grid and converted to structure object
                    # code from george
                    clickedTile = point(*event.pos)
                    clickedTile.snapToGrid()
                    clickedTile = structure(clickedTile, Tower_Held, 1)
                    if (gamemode_hardcore):
                        clickedTile.health = 1
                    if clickedTile.checkCollision(occupiedTiles):
                        structureList.append(clickedTile)
                
                    # Attempts to delete a tower upon right click
                elif event.button == 3 and not override_tower_placement and not Boost_Shop_Open and Placing_Tower:
                    # code from george
                    clickedTile = point(*event.pos)
                    clickedTile.snapToGrid()
                    for tile in structureList:
                        if checkCollidePoint(clickedTile, tile) and tile.name != "Central":
                            structureList.remove(tile)
            elif Current_Game_State == 5:
                if clicked_Button(quit_button, mouse_x, mouse_y):
                    Current_Game_State = 1
                    Wave = 0
                    EnemiesKilled = 0
    # GAME STATE UPDATES

    # All game math and comparisons happen here
    # code from george
    
    if  Current_Game_State == 4:
        occupiedTiles = []
        for tile in structureList:
            for coordinate in centeredMatrix(tile.size):
                occupiedTiles.append(tile.location.moveCall_coord(*coordinate))
        mouseGrid = point(*pygame.mouse.get_pos())
        mouseGrid.snapToGrid()
        #code from sean
        current_time = pygame.time.get_ticks()
        if currentMobCount == 0 and current_time - last_wave_time >= 3000:
            Wave += 1
            # random amount of mobs for the current wave
            currentMobCount = random.randint(10 + 10 * round(math.log2(Wave)), 20 + 10 * round(math.log2(Wave)))
            # spawn mobs
            for _ in range(currentMobCount):
                size = random.choice(["Red", "Blue", "Green"])
                enemy_type = enemies[size]
                # Ensure enemies spawn within bounds
                x = random.randint(enemy_type["Size"], WIDTH - enemy_type["Size"])
                y = random.randint(enemy_type["Size"], HEIGHT - enemy_type["Size"])
                enemy_queue.append((x, y, enemy_type))
        # ChatGPT
        if enemy_queue and current_time - last_spawn_time >= spawn_delay:
            x, y, enemy_type = enemy_queue.pop(0)
            spawnPoint = point(x, y)
            wave_enemies.append(Enemy(spawnPoint, enemy_type, structureList[0]))
            last_spawn_time = current_time
            # Update spawn delay to a random value between 25 and 50 ms
            spawn_delay = random.randint(25, 50)
    # moving mobs towards base
        for monster in wave_enemies:
            closestStructure = findClosestPoint(structureList, monster.location)
            #returns tuple with closest point [0] and index in list [1]
            monster.target = structureList[closestStructure[1]]
            dx = closestStructure[0].unsnapGrid().x - monster.location.x
            dy = closestStructure[0].unsnapGrid().y - monster.location.y
            distance = calcDistance(closestStructure[0].unsnapGrid(), monster.location)
            if distance > 30:
                monster.move(dx / distance * monster.speed, dy / distance * monster.speed)
            else:
                structureList[closestStructure[1]].takeDamage(monster.damage*difficultyMultiplier[Game_Difficulty])
                wave_enemies.remove(monster)
                currentMobCount -= 1
                if (currentMobCount == 0):
                    last_wave_time = current_time
        for _ in wave_enemies:
            if _.health <= 0:
                wave_enemies.remove(_)
                EnemiesKilled += 1
        for _ in structureList:
            if _.Health <= 0:
                structureList.remove(_)
                if (_.Type == "central"):
                    Boost_Shop_Open = False
                    Tower_Shop_Open = False
                    structureList = []
                    wave_enemies = []
                    projectilesList = []
                    Money = 0
                    currentMobCount = 0
                    override_tower_placement = True
                    Current_Game_State = 5
                    WaveText.text = "You reached wave " + str(Wave) + "!"
                    EnemiesKilledText.text  = "You killed " + str(EnemiesKilled) + " enemies!"
                       
    # DRAWING
    screen.fill(white)  # always the first drawing command
    if (Current_Game_State == 1):
        # home screen
        screen.blit(MenuBackground, (0,0))
        draw_Button(title_button)
        draw_Button(play_button)
        draw_Button(settings_button)
        draw_Button(help_button)
        draw_Button(quit_button)
    elif (Current_Game_State == 2):
        screen.blit(MenuBackground, (0,0))
        # settings
        draw_Button(quit_button)
        draw_Button(difficulty_easy)
        draw_Button(difficulty_medium)
        draw_Button(difficulty_hard)
        draw_Button(gamemode_survival)
        draw_Button(gamemode_hardcore)
    elif (Current_Game_State == 3):
        screen.blit(MenuBackground, (0,0))
        # help
        for helpButton in help_Buttons:
            draw_Button(helpButton)
        draw_Button(quit_button)
    elif (Current_Game_State == 4):
        screen.blit(GameBackground, (0,0))
        # inside game
        draw_Button(quit_button)
        # boost shop menu
        # draw_Button(open_boost_shop_button)
        # if (Boost_Shop_Open):
        #     draw_Button(close_boost_shop_button)
        # tower shop MENU
        draw_Button(open_tower_shop_button)
        if (Tower_Shop_Open):
            draw_Button(close_tower_shop_button)
            for tower in tower_Shop_Menu:
                draw_Button(tower)
        # code from george
        for tile in structureList: # returns as a STRUCTURE
            for coordinate in centeredMatrix(tile.size):
                tile.imageFile.render(0, screen)
                # pygame.draw.rect(screen, (25,25,255), (20 * (tile.location.moveCall(*coordinate)[0])-10, 20 * (tile.location.moveCall(*coordinate)[1])-10,20,20))

        if Placing_Tower:
            # Draw a RED tile around the cursor if placement is impossible
            for tile in structure(mouseGrid, Tower_Held, 1).findOverlapping(occupiedTiles): # returns as a LIST, not a POINT
                pygame.draw.rect(screen, (255, 50, 50), (20 * tile[0]-10, 20 * tile[1]-10,20,20))

            # Draw a GREEN tile around the cursor if placement is possible
            for tile in structure(mouseGrid, Tower_Held, 1).findPlaceableTiles(occupiedTiles): # returns as a LIST, not a POINT
                pygame.draw.rect(screen, (50, 255, 50), (20 * tile[0]-10, 20 * tile[1]-10,20,20))
        #enemies
        for monster in wave_enemies:
            pygame.draw.circle(screen, monster.color, (monster.location.x, monster.location.y), monster.size)
    elif(Current_Game_State == 5):
        screen.blit(MenuBackground, (0,0))
        draw_Button(GameOverText)
        draw_Button(quit_button)
        draw_Button(WaveText)
        draw_Button(EnemiesKilledText)
    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------
pygame.quit()