import pygame

class snake_tile(pygame.Rect):
    def __init__(self, left, top, width, height, direction):
        super().__init__(left, top, width, height)
        self.direction = direction

    def move(self, x_offset, y_offset):
        new_instance = super().move(x_offset, y_offset)
        new_instance.direction = self.direction
        return new_instance

