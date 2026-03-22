import pygame
import random
import math
import time

pygame.init()

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

class Enemy:
    def __init__(self, x: float, y: float, type):
        self.x = x
        self.y = y
        self.damage = type["Damage"]
        self.health = type["Health"]
        self.size = type["Size"]
        self.speed = type["Speed"]
        self.color = type["Color"]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def damageMob(self, damageTaken: float) -> float:
        self.health -= damageTaken
        return self.health

# ---------------------------
# Initialize global variables

# stats of enemies
enemies = {"Red": {"Damage": 10, "Health": 100, "Size": 10, "Speed": 5, "Color": (255, 0, 0)},
           "Blue": {"Damage": 5, "Health": 50, "Size": 5, "Speed": 20, "Color": (0, 0, 255)},
           "Green": {"Damage": 15, "Health": 200, "Size": 15, "Speed": 3, "Color": (0, 255, 0)}}
# waves system
current_wave = 0
wave_enemies = []
enemy_queue = []
last_spawn_time = 0
spawn_delay = 50
occupiedTiles = []
currentMobCount = 0
base_pos = [WIDTH / 2, HEIGHT / 2]

font = pygame.font.Font(None, 36)

# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for monster in wave_enemies[:]:
                if (monster.x - event.pos[0]) ** 2 + (monster.y - event.pos[1]) ** 2 <= monster.size ** 2:
                    wave_enemies.remove(monster)
                    currentMobCount -= 1

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    if currentMobCount == 0:
        time.sleep(3)
        current_wave += 1
        # random amount of mobs for the current wave
        currentMobCount = random.randint(10 + 10 * round(math.log2(current_wave)), 20 + 10 * round(math.log2(current_wave)))
        # spawn mobs
        for _ in range(currentMobCount):
            size = random.choice(["Red", "Blue", "Green"])
            enemy_type = enemies[size]
            # Ensure enemies spawn within bounds
            x = random.randint(enemy_type["Size"], WIDTH - enemy_type["Size"])
            y = random.randint(enemy_type["Size"], HEIGHT - enemy_type["Size"])
            enemy_queue.append((x, y, enemy_type))

    current_time = pygame.time.get_ticks()

    # ChatGPT
    if enemy_queue and current_time - last_spawn_time >= spawn_delay:
        x, y, enemy_type = enemy_queue.pop(0)
        wave_enemies.append(Enemy(x, y, enemy_type))
        last_spawn_time = current_time
        # Update spawn delay to a random value between 50 and 100 ms
        spawn_delay = random.randint(50, 100)
        
    # moving mobs towards base
    for monster in wave_enemies:
        dx = base_pos[0] - monster.x
        dy = base_pos[1] - monster.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 20:
            monster.move(dx / distance * monster.speed, dy / distance * monster.speed)
        else:
            wave_enemies.remove(monster)
            currentMobCount -= 1
            
    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    for monster in wave_enemies:
        pygame.draw.circle(screen, monster.color, (int(monster.x), int(monster.y)), monster.size)

    mobs_left_text = font.render(f'Mobs Left: {currentMobCount}', True, (0, 0, 0))
    wave_text = font.render(f'Wave {current_wave}', True, (0, 0, 0))
    screen.blit(mobs_left_text, (10, 10))
    screen.blit(wave_text, (10, 50))

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------

pygame.quit()
