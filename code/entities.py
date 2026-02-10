import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((100, 100))
        self.image.fill('red')
        self.rect = self.image.get_frect(center=pos)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            print('up')

    def move(self, df):
        pass

    # calls the update method
    def update(self):
        self.input()
