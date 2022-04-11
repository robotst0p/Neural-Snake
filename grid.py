import pygame 
import random
import time

from pygame.locals import * 
from input_handler import *
from snake_class import *

SIZE = 1000, 1000
RED = (255, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)

key_dict = {K_DOWN: (0, 10), K_UP: (0, -10), K_LEFT: (-10, 0), K_RIGHT: (10, 0)}

pygame.init()
screen = pygame.display.set_mode(SIZE) 

running = True

pygame.display.set_caption("Neural Snake")

key = (0,0)

def randomize():
    snake_tile_x = random.randint(0, 1000)
    snake_tile_y = random.randint(0, 1000)

    food_tile_x = random.randint(0, 1000)
    food_tile_y = random.randint(0, 1000)

    snake_head = snake_tile(snake_tile_x, snake_tile_y, 10, 10, (0,0))
    food_tile = Rect(food_tile_x, food_tile_y, 10, 10)

    return snake_head, food_tile

snake_head, food_tile = randomize()

def border_check(snake_head, food_tile):
    if snake_head.x >= 1000 or snake_head.y >= 1000 or snake_head.x <= 0 or snake_head.y <= 0:
        snake_head, food_tile = randomize()

    return snake_head, food_tile


#render loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(GRAY)
    pygame.draw.rect(screen, RED, food_tile)
    pygame.draw.rect(screen, WHITE, snake_head)
    pygame.display.flip()

    if event.type == KEYDOWN:
        key = key_dict[event.key]
        snake_head.direction = key
    
    snake_head = snake_head.move(key[0], key[1])
    snake_head, food_tile = border_check(snake_head, food_tile)
    time.sleep(.05)


pygame.quit()
