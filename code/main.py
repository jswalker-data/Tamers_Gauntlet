from os.path import join
from sys import exit

import pygame
from entities import Player
from groups import AllSprites
from pytmx.util_pygame import load_pygame
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites import Sprite


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Tamers Gauntlet')
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()

        self.import_assets()
        self.setup(self.tmx_maps['world'], 'house')

    # create dict of assets and locations
    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(join('data', 'maps', 'world.tmx'))}

    # setup the map
    # TODO: make this generic to all locations
    def setup(self, tmx_map, player_start_pos):

        # loop over the terrain layer and create sprites of them
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # loop over entity layer (player or character), this is an object layer not a tile layer
        for obj in tmx_map.get_layer_by_name('Entities'):
            # looking at objects name (player/character) and property of position (house, hospital etc.)
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
                # here I now create a player
                self.player = Player((obj.x, obj.y), self.all_sprites)

    def run(self):
        while True:
            # for game clock we are using dt method, take speed of game
            # and divide it through speed to get steady rate on all hardware
            # FPS of source pc is 560 fps LOL
            # dt is in ms
            dt = self.clock.tick() / 1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # game logic
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
