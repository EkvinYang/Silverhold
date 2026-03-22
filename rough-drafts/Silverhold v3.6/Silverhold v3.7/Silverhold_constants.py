import pygame
from Silverhold_functions import KeyPressDetector
from Silverhold_dictionaries import towerDict
import os
directory = os.path.dirname(os.path.realpath(__file__))

# Keys to detect
key_q = KeyPressDetector('q')
key_r = KeyPressDetector('r')
key_d = KeyPressDetector('d')
key_1 = KeyPressDetector('1')
key_2 = KeyPressDetector('2')
key_3 = KeyPressDetector('3')
key_space = KeyPressDetector('space')

# Testing
actionState = "place"
towerType = "cannon"
testingSize = towerDict[towerType]["Size"]
enemyType = "brigantine"
testlevel = "level1"
testProjectileSpeed = 10
background = pygame.image.load(directory+ "/sprites/game_background.png")
