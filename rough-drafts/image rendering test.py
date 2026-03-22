# Image rendering template taken from https://pythonprogramming.net/displaying-images-pygame/

import pygame

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def call(self):
        return [self.x, self.y]

    def moveCall(self, dx, dy):
        return [self.x + dx, self.y + dy]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def snapToGrid(self):
        self.x = round(self.x/20)
        self.y = round(self.y/20)

    def unsnapGrid(self):
        return point(20 * self.x, 20 * self.y)

class Image:
    def __init__(self, pos: point, file: str):
        self.pos = pos
        self.imageFile = pygame.image.load(file)
    
    def render(self):
        screen.blit(self.imageFile, (self.pos.call()[0], self.pos.call()[1]))


pygame.init()

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption('test image')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()

# Renders the image, image must be within the same folder as main code

x =  (WIDTH * 0.25)
y = (HEIGHT * 0.4)
testImage = Image(point(x,y),'1.png')

quitProgram = False

while not quitProgram:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitProgram = True

    screen.fill(white)
    testImage.render()

        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()