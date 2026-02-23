from os.path import join
from sys import exit

import pygame
from entities import Character, Player
from groups import AllSprites
from pytmx.util_pygame import load_pygame
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites import AnimatedSprite, Sprite
from support import (
    all_character_import,
    coast_importer,
    import_folder,
    import_folder_dict,
    import_image,
    import_sub_folders,
    import_tilemap,
)


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
        self.tmx_maps = {
            'world': load_pygame(join('data', 'maps', 'world.tmx')),
            'hospital': load_pygame(join('data', 'maps', 'hospital.tmx')),
        }

        self.overworld_frames = {
            'water': import_folder('graphics', 'tilesets', 'water'),
            'coast': coast_importer(24, 12, 'graphics', 'tilesets', 'coast'),
            'characters': all_character_import('graphics', 'characters'),
        }

    # setup the map
    # TODO: make this generic to all locations
    # Note: This is all in order of drawing!! So terrain, then top etc.
    # Use sort order to do this rather than order in settings
    def setup(self, tmx_map, player_start_pos):

        # Simplify this double layering
        for layer in ['Terrain', 'Terrain Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # object layer render
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

        # grass patches
        for obj in tmx_map.get_layer_by_name('Monsters'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

        # loop over entity layer (player or character), this is an object layer not a tile layer
        for obj in tmx_map.get_layer_by_name('Entities'):
            # looking at objects name (player/character) and property of position (house, hospital etc.)
            if obj.name == 'Player':
                if obj.properties['pos'] == player_start_pos:
                    # here I now create a player
                    self.player = Player(
                        pos=(obj.x, obj.y),
                        frames=self.overworld_frames['characters']['player'],
                        groups=self.all_sprites,
                        facing_direction=obj.properties['direction'],
                    )
            else:
                self.Character = Character(
                    pos=(obj.x, obj.y),
                    frames=self.overworld_frames['characters'][obj.properties['graphic']],
                    groups=self.all_sprites,
                    facing_direction=obj.properties['direction'],
                )

        # water is animated, so multi frames per sprite
        for obj in tmx_map.get_layer_by_name('Water'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite((x, y), self.overworld_frames['water'], self.all_sprites)

        # coast animation
        for obj in tmx_map.get_layer_by_name('Coast'):
            terrain = obj.properties['terrain']
            side = obj.properties['side']
            AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites)

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

            # game logic - update sprites, fill background
            # pygame doesnt discard previous frame, just draws ontop
            # so fill out of the map with black
            # TODO: make the out of bounds a coast line
            # draw sprites and then display
            self.all_sprites.update(dt)
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
