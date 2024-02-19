# import csv
# from pygame.sprite import Sprite, Group
# from pygame import Surface, SRCALPHA, mask
# import os

# from settings import TILE_WIDTH, TILE_HEIGHT, PATH_TO_BOUNDARIES, PATH_TO_GROUND

# obstacle_sprites_group = Group()
# class Obstacle(Sprite):
#     def __init__(self, name, pos, size, group):
#         super().__init__(group)
#         self.name = name
#         self.pos = pos
#         self.size = size

#         self.image = Surface((self.size))
#         self.rect = self.image.get_rect(topleft=pos)
#         self.mask = mask.from_surface(self.image)


# info_rects = [
#     # borders
#     {"x": 0, "y": 0, "width": 1080, "height": 30},
#     {"x": 0, "y": 0, "width": 30, "height": 950},
#     {"x": 0, "y": 920, "width": 1080, "height": 30},
#     {"x": 1050, "y": 0, "width": 30, "height": 950},

#     # objects on the center
#     # 5 squares at the top
#     {"x": 100, "y": 100, "width": 70, "height": 70},
#     {"x": 300, "y": 100, "width": 70, "height": 70},
#     {"x": 500, "y": 100, "width": 70, "height": 70},
#     {"x": 700, "y": 100, "width": 70, "height": 70},
#     {"x": 900, "y": 100, "width": 70, "height": 70},

#     {"x": 30, "y": 300, "width": 200, "height": 70},
#     {"x": 400, "y": 260, "width": 100, "height": 100},
#     {"x": 600, "y": 280, "width": 150, "height": 100},
#     {"x": 900, "y": 250, "width": 80, "height": 200},

#     {"x": 160, "y": 470, "width": 400, "height": 100},
#     {"x": 700, "y": 500, "width": 150, "height": 100},

#     # 5 squares down
#     {"x": 100, "y": 680, "width": 70, "height": 70},
#     {"x": 300, "y": 680, "width": 70, "height": 70},
#     {"x": 500, "y": 680, "width": 70, "height": 70},
#     {"x": 700, "y": 680, "width": 70, "height": 70},
#     {"x": 900, "y": 680, "width": 70, "height": 70},

#     {"x": 200, "y": 820, "width": 200, "height": 50},
#     {"x": 600, "y": 820, "width": 200, "height": 50},
# ]

# count = 0
# for rect in info_rects:
#     pos = (rect["x"], rect["y"])
#     size = (rect["width"], rect["height"])
#     name = count

#     Obstacle(name=name, pos=pos, size=size, group=obstacle_sprites_group)

#     count += 1


import csv
from pygame.sprite import Sprite, Group
from pygame import Surface, SRCALPHA, mask
import os

from settings import TILE_WIDTH, TILE_HEIGHT, PATH_TO_WALLS, PATH_TO_GROUND, PATH_TO_EXITS


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

                if tiles_name == "walls":
                    Tile(
                        name=index_tile,
                        pos=(pos_x_tile, pos_y_tile),
                        groups=walls_sprites_group
                    )
                elif tiles_name == "ground":
                    Tile(
                        name=index_tile,
                        pos=(pos_x_tile, pos_y_tile),
                        groups=ground_sprites_group
                    )
                elif tiles_name == "exits":
                    Tile(
                        name=index_tile,
                        pos=(pos_x_tile, pos_y_tile),
                        groups=exits_sprites_group
                    )
                else:
                    raise("Tiles name given doesn't exists.")
                
                index_tile += 1
            col_counter += 1
        row_counter += 1


walls_sprites_group = Group()
ground_sprites_group = Group()
exits_sprites_group = Group()


with open(PATH_TO_WALLS, newline='') as id_tiles_walls:
    reader_walls = csv.reader(id_tiles_walls, delimiter=',')

    creation_each_tile("walls", reader_walls)

with open(PATH_TO_GROUND, newline='') as id_tiles_ground:
    reader_ground = csv.reader(id_tiles_ground, delimiter=',')

    creation_each_tile("ground", reader_ground)

with open(PATH_TO_EXITS, newline='') as id_tiles_exits:
    reader_exits = csv.reader(id_tiles_exits, delimiter=',')

    creation_each_tile("exits", reader_exits)
