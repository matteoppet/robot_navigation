import os

TILE_WIDTH = 16 # 16
TILE_HEIGHT = 16 # 16

WINDOW_X = 880
WINDOW_Y = 560

# file paths
path_boundaries_csv = "../temporary_map_files/tileset_tinyrooms/csv/map_walls.csv"
PATH_TO_BOUNDARIES = os.path.join(os.path.dirname(__file__), path_boundaries_csv)

path_ground_csv = "../temporary_map_files/tileset_tinyrooms/csv/map_ground.csv"
PATH_TO_GROUND = os.path.join(os.path.dirname(__file__), path_ground_csv)