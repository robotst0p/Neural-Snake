import pygame 
import random
import time

from pygame.locals import * 
from input_handler import *
from snake_class import *

SIZE = 1000, 1000
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)

key_dict = {K_DOWN: (0, 2), K_UP: (0, -2), K_LEFT: (-2, 0), K_RIGHT: (2, 0)}
print(key_dict)

pygame.init()
screen = pygame.display.set_mode(SIZE)

rect = Rect(0, 0, 10, 10)
rect = Rect(0, 10, 10, 10)  

running = True
setup = False

direction = 'none'

snake = []

snake_tile_x = random.randint(0, 1000)
snake_tile_y = random.randint(0, 1000)

food_tile_x = random.randint(0, 1000)
food_tile_y = random.randint(0, 1000)

food_tile = Rect(food_tile_x, food_tile_y, 10, 10)

snake_head = snake_tile(snake_tile_x, snake_tile_y, 10, 10, "")

input = input("")

def render(snake_head):
    pygame.draw.rect(screen, WHITE, snake_head)        

def update(snake_head):
    for event in pygame.event.get():
        if event.type == QUIT:
            snake_head.direction = ""

    while snake_head.direction == "right":
        snake_head.left += 1
        print(snake_head.x)
        render(snake_head)
        time.sleep(1)
        
    while snake_head.direction == "left":
        snake_head.x -= 1
        render(snake_head)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("KEY")
                key = pygame.key.name(event.key)
                input.direction_update(key)
                snake_head.direction = input.direction
                update(snake_head)
                return
 
    while snake_head.direction == "up":
        snake_head.y -= 1
        render(snake_head)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("KEY")
                key = pygame.key.name(event.key)
                input.direction_update(key)
                snake_head.direction = input.direction
                update(snake_head)
                return 
        
    while snake_head.direction == "down":
        snake_head.y += 1
        render(snake_head)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("KEY")
                key = pygame.key.name(event.key)
                input.direction_update(key)
                snake_head.direction = input.direction
                update(snake_head)
                return
pygame.display.set_caption("Neural Snake")        
#render loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(GRAY)
    pygame.draw.rect(screen, RED, food_tile)
    pygame.draw.rect(screen, WHITE, snake_head)
    pygame.display.flip()

    snake_head.direction = ""

    if event.type == KEYDOWN:
        print("KEY")
        key = key_dict[event.key]
        input.direction_update(key)
        snake_head.direction = key
        print(snake_head.direction)
        snake_head = pygame.Rect.move(snake_head.direction)

pygame.quit()
