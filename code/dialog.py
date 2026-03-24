from settings import *
import pygame
from settings import COLOURS, WORLD_LAYERS
from pygame.math import Vector2 as vector


class DialogTree:
    def __init__(self, character, player, all_sprites, font):
        self.player = player
        self.character = character
        self.all_sprites = all_sprites
        self.font = font

        self.dialog = character.get_dialog()
        self.dialog_number = len(self.dialog)
        self.dialog_index = 0

        self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.character, self.all_sprites, self.font)

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE]:
            self.current_dialog.kill()


class DialogSprite(pygame.sprite.Sprite):
    def __init__(self, message, character, groups, font):
        super().__init__(groups)
        self.z = WORLD_LAYERS['top']

        # text
        text_surf = font.render(message, False, COLOURS['black'])
        padding = 5
        width = max(30, text_surf.get_width() + padding * 2)
        height = text_surf.get_height() + padding * 2

        # background
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        pygame.draw.rect(surf, COLOURS['pure white'], surf.get_frect(topleft=(0, 0)), 0, 4)
        surf.blit(text_surf, text_surf.get_frect(center=(width / 2, height / 2)))

        self.image = surf
        self.rect = self.image.get_rect(midbottom=character.rect.midtop + vector(0, -10))
