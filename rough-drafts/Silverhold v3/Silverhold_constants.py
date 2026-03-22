import pygame
import os
from Silverhold_functions import KeyPressDetector

directory = os.path.dirname(os.path.realpath(__file__))
enemyList = []
projectileList = []
occupiedTiles = []
structureList = []

#colors
white = (255,255,255)
black = (0, 0, 0)
button_color = (204, 106, 106)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# # gamestate 1
# play_button = Button(370, 200, 500, 200, button_color, "Play", green)
# settings_button = Button(470, 450, 300, 100, button_color, "Settings", green)
# quit_button = Button(20, 20, 100, 100, button_color, "Quit", green)
# help_button = Button(1160, 600, 100, 100, button_color, "Help", green)

# #gamestate 2
# difficulty_easy = Button(170, 100, 200, 200, green, "Easy", black)
# difficulty_medium = Button(540, 100, 200, 200, red, "Medium", black)
# difficulty_hard = Button(910, 100, 200, 200, red, "Hard", black)
# gamemode_survival = Button(300, 350, 200, 200, green, "Survival", black)
# gamemode_hardcore = Button(780, 350, 200, 200, red, "Hardcore", black)

#gamestate 3
help_Text_1 = "1. Survive as many waves as possible by protecting the central tower"
help_Text_2 = "2. Enemies will spawn at the start of each wave, defeat them to progress"
help_Text_3 = "3. Place and upgrade towers in order to defeat enemies"
help_Text_4 = "4. Place towers and purchase boosts through their respective menus"
help_Text_5 = "5. Change difficulties to unlock new challenges and different playstyes"
help_Text_6 = "6. Have fun!"
# help_info = Button(150, 50, 1080, 620, green, "", black)
# help_info_1 = Button(640, 55, 100,100, green, help_Text_1, black)
# help_info_2 = Button(640, 155, 100,100, green, help_Text_2, black)
# help_info_3 = Button(640, 255, 100,100, green, help_Text_3, black)
# help_info_4 = Button(640, 355, 100,100, green, help_Text_4, black)
# help_info_5 = Button(640, 455, 100,100, green, help_Text_5, black)
# help_info_6 = Button(640, 555, 100,100, green, help_Text_6, black)
# help_Buttons  = [help_info, help_info_1, help_info_2, help_info_3, help_info_4, help_info_5, help_info_6]

#tower shop
# open_tower_shop_button = Button (25, 200, 75, 75, green, "Towers", black)
# close_tower_shop_button = Button(120, 200, 60, 60, red, "X", black)
# wizard_Tower_Button = Button(25, 300, 50, 50, green, "Wizard", black)
# archer_Tower_Button = Button(125, 300, 50, 50, green, "Archer", black)
# bomb_Tower_Button = Button(25, 375, 50, 50, green, "Bomb", black)


# Keys to detect
key_q = KeyPressDetector('q')
key_r = KeyPressDetector('r')
key_space = KeyPressDetector('space')

# Testing
actionState = "place"
towerType = "archer"
testingSize = 3
enemyType = "brigantine"
testProjectileSpeed = 10
background = pygame.image.load(directory+"/sprites/game_background.png")

gameTick = 0
