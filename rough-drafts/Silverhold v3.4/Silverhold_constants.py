import pygame
from Silverhold_functions import KeyPressDetector
from Silverhold_dictionaries import towerDict

enemyList = []
enemyQueue = []
projectileList = []
occupiedTiles = []
structureList = []

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
background = pygame.image.load("sprites/game_background.png")

# Game data
gameTick = 0
money = 1000000
currentWave = 0
lastSpawnTime = 0
lastWaveTime = 0
spawnDelay = 250
