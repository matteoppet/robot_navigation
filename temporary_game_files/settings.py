import os

TILE_WIDTH = 32 # 16
TILE_HEIGHT = 32 # 16

WINDOW_X = 35*32
WINDOW_Y = 32*32

# file paths
path_boundaries_csv = "../temporary_map_files/tileset_dungeon_2/csv/map_walls.csv"
PATH_TO_WALLS = os.path.join(os.path.dirname(__file__), path_boundaries_csv)

path_ground_csv = "../temporary_map_files/tileset_dungeon_2/csv/map_ground.csv"
PATH_TO_GROUND = os.path.join(os.path.dirname(__file__), path_ground_csv)

path_ground_csv = "../temporary_map_files/tileset_dungeon_2/csv/map_exits.csv"
PATH_TO_EXITS = os.path.join(os.path.dirname(__file__), path_ground_csv)