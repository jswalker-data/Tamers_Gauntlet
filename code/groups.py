import pygame
from pygame.math import Vector2 as vector
from settings import WINDOW_HEIGHT, WINDOW_WIDTH


# this is a copy of the in built sprite group
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # always draw on display surface
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    # need a custom draw method
    def draw(self, player_center):
        self.offset.x = player_center[0] - WINDOW_WIDTH / 2
        self.offset.y = player_center[1] - WINDOW_HEIGHT / 2
        # return all sprites inside the group
        for sprite in self:
            # offset the image to the sprite
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
