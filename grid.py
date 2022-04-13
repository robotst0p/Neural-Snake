import pygame 
import random
import time

from pygame.locals import * 
from snake_class import *

SIZE = 1000, 1000
RED = (255, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)

key_dict = {K_DOWN: (0, 10), K_UP: (0, -10), K_LEFT: (-10, 0), K_RIGHT: (10, 0)}
snake_body = []

pygame.init()
screen = pygame.display.set_mode(SIZE) 

running = True

pygame.display.set_caption("Neural Snake")

key = (0,0)

def randomize():
    snake_tile_x = random.randrange(0, 600, 10)
    snake_tile_y = random.randrange(0, 600, 10)

    food_tile_x = random.randrange(0, 600, 10)
    food_tile_y = random.randrange(0, 600, 10)

    snake_head = snake_tile(snake_tile_x, snake_tile_y, 10, 10, (0,0))
    food_tile = Rect(food_tile_x, food_tile_y, 10, 10)

    return snake_head, food_tile

snake_head, food_tile = randomize()

def border_check(snake_head, food_tile, snake_body):
    for tile in snake_body:
        if snake_head.x == tile.x and snake_head.y == tile.y:
            snake_head, food_tile = randomize()
            snake_body = []

    if snake_head.x >= 1000 or snake_head.y >= 1000 or snake_head.x <= 0 or snake_head.y <= 0:
        snake_head, food_tile = randomize()
        snake_body = []

    return snake_head, food_tile, snake_body

def food_check(snake_head, food_tile, snake_body):
    if len(snake_body) > 0:
        last_tile = snake_body[0]
    elif len(snake_body) == 0:
        last_tile = snake_head

    if snake_head.x == food_tile.x and snake_head.y == food_tile.y:
        food_tile.x = random.randrange(0, 600, 10)
        food_tile.y = random.randrange(0, 600, 10)

        if last_tile.direction == (10, 0):
            new_tile = snake_tile(last_tile.x - 10, last_tile.y, 10, 10, (0,0))
        elif last_tile.direction == (-10, 0):
            new_tile = snake_tile(last_tile.x + 10, last_tile.y, 10, 10, (0,0))
        elif last_tile.direction == (0, 10):
            new_tile = snake_tile(last_tile.x, last_tile.y - 10, 10, 10, (0,0))     
        elif last_tile.direction == (0, -10):
            new_tile = snake_tile(last_tile.x, last_tile.y + 10, 10, 10, (0,0))
        snake_body.insert(0, new_tile)
    return snake_body

def dir_update(snake_body, snake_head):
    work_arr = []
    if len(snake_body) > 0:
        snake_body[-1].direction = snake_head.direction
    for i in range(0, len(snake_body) - 1):
        if snake_body[i + 1].x > snake_body[i].x:
            snake_body[i].direction = (10, 0)
        elif snake_body[i + 1].x < snake_body[i].x:
            snake_body[i].direction = (-10, 0)
        elif snake_body[i + 1].y < snake_body[i].y:
            snake_body[i].direction = (0, -10)
        elif snake_body[i + 1].y > snake_body[i].y:
            snake_body[i].direction = (0, 10)
        work_arr.append(snake_body[i])
    
    if len(snake_body) > 0:
        work_arr.append(snake_body[-1])

    snake_body = work_arr
    return snake_body

#render loop
while running:
    loop_body = []
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(GRAY)
    pygame.draw.rect(screen, RED, food_tile)
    pygame.draw.rect(screen, WHITE, snake_head)

    for tile in snake_body:
        pygame.draw.rect(screen, WHITE, tile)

    pygame.display.flip()

    if event.type == KEYDOWN:
        key = key_dict[event.key]
        if key[0] is not -snake_head.direction[0] or key[1] is not -snake_head.direction[1]:
            snake_head.direction = key
    
    snake_head = snake_head.move(snake_head.direction[0], snake_head.direction[1])
   
    for tile in snake_body:
        tile = tile.move(tile.direction[0], tile.direction[1])
        loop_body.append(tile)
    snake_body = loop_body
   
    snake_head, food_tile, snake_body = border_check(snake_head, food_tile, snake_body)
    snake_body = food_check(snake_head, food_tile, snake_body)

    snake_body = dir_update(snake_body, snake_head)
    time.sleep(.05)

pygame.quit()
