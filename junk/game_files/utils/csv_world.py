import csv
from pygame.sprite import Sprite, Group
from pygame import Surface, SRCALPHA
import os


sprite_boundaries = Group()
sprite_path = Group()


class Tile(Sprite):
    def __init__(self, name, pos, groups):
        self.tile_width = 32
        self.tile_height = 32

        self.name = name
        self.pos = pos

        self.image = Surface((self.tile_width, self.tile_height), SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)

        super().__init__(groups)



file_path = os.path.join(os.path.dirname(__file__), "../../map_files/csv/basic_4_Boundaries grass.csv")
with open(file_path, newline='') as id_tiles:
    reader = csv.reader(id_tiles, delimiter=',')
    
    row_counter = 0
    index_tile = 0 # name of the tile
    for row in reader:
        col_counter = 0

        for col in row:

            # Convert DataType from str to int
            col = int(col)
            if col != -1:
                
                # multiply 32 per counter to get the position x and y of the tile
                pos_x_tile = 32 * col_counter
                pos_y_tile = 32 * row_counter

                Tile(name=index_tile, pos=(pos_x_tile, pos_y_tile), groups=sprite_boundaries)
                index_tile += 1
            
            col_counter += 1

        row_counter += 1

file_path = os.path.join(os.path.dirname(__file__), "../../map_files/csv/basic_4_Path.csv")
with open(file_path, newline='') as id_tiles:
    reader = csv.reader(id_tiles, delimiter=',')
    
    row_counter = 0
    index_tile = 0 # name of the tile
    for row in reader:
        col_counter = 0
    
        for col in row:

            # Convert DataType from str to int
            col = int(col)
            if col != -1:
                
                # multiply 32 per counter to get the position x and y of the tile
                pos_x_tile = 32 * col_counter
                pos_y_tile = 32 * row_counter

                Tile(name=index_tile, pos=(pos_x_tile, pos_y_tile), groups=sprite_path)
                index_tile += 1
            col_counter += 1

        row_counter += 1