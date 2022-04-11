import pygame

class snake_tile(pygame.Rect):
    def __init__(self, left, top, width, height, direction = None):
        self.direction = direction if direction is not None else None
        super().__init__(left, top, width, height)

