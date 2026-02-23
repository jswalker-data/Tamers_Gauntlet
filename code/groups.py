import pygame
from pygame.math import Vector2 as vector
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, WORLD_LAYERS


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

        bg_sprites = [sprite for sprite in self if sprite.z < WORLD_LAYERS['main']]
        main_sprites = sorted(
            [sprite for sprite in self if sprite.z == WORLD_LAYERS['main']], key=lambda sprite: sprite.rect.centery
        )
        fg_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS['main']]

        for layer in (bg_sprites, main_sprites, fg_sprites):
            for sprite in layer:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
