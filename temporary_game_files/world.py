import csv
from pygame.sprite import Sprite, Group
from pygame import Surface, SRCALPHA, mask
import os

from settings import TILE_WIDTH, TILE_HEIGHT, PATH_TO_BOUNDARIES, PATH_TO_GROUND


class Tile(Sprite):
    def __init__(self, name, pos, groups):
        super().__init__(groups)

        self.name = name
        self.pos = pos

        self.image = Surface((TILE_WIDTH, TILE_HEIGHT), SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = mask.from_surface(self.image)


def creation_each_tile(tiles_name, reader):
    row_counter = 0
    index_tile = 0

    for row in reader:
        col_counter = 0

        for col in row:
            col = int(col) # convert datatype from str to int
            if col != -1:
                pos_x_tile = TILE_WIDTH * col_counter
                pos_y_tile = TILE_HEIGHT * row_counter

                if tiles_name == "boundaries":
                    Tile(
                        name=index_tile,
                        pos=(pos_x_tile, pos_y_tile),
                        groups=sprite_boundaries
                    )
                elif tiles_name == "ground":
                    Tile(
                        name=index_tile,
                        pos=(pos_x_tile, pos_y_tile),
                        groups=sprite_ground
                    )
                else:
                    raise("Tiles name given doesn't exists.")
                
                index_tile += 1
            col_counter += 1
        row_counter += 1


sprite_boundaries = Group()
sprite_ground = Group()
sprite_roof = Group()


with open(PATH_TO_BOUNDARIES, newline='') as id_tiles_boundaries:
    reader_boundaries = csv.reader(id_tiles_boundaries, delimiter=',')

    creation_each_tile("boundaries", reader_boundaries)

with open(PATH_TO_GROUND, newline='') as id_tiles_ground:
    reader_ground = csv.reader(id_tiles_ground, delimiter=',')

    creation_each_tile("ground", reader_ground)
