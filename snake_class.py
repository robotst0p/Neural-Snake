import pygame

class snake_tile(pygame.Rect):
    def __init__(self, left, top, width, height, direction):
        self.direction = direction 
        super().__init__(left, top, width, height)

