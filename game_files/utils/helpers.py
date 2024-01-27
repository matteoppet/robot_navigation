import pygame
import numpy as np


class Distance(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()

        self.name = direction
        self.rect = pygame.rect.Rect(100, 100, 20, 20)


def create_distance_sprites():
    sprite_group_for_distance = pygame.sprite.Group()

    for direction in ["left", "right", "down", "up"]:
        sprite_distance = Distance(direction)
        sprite_group_for_distance.add(sprite_distance)

    return sprite_group_for_distance


def create_table_tiles(sprite_tiles):
    table = {} # total 175 tiles

    for sprite in sprite_tiles:
        table[sprite.name] = dict(
            x1=sprite.rect.x,
            x2=sprite.rect.x+32,
            y1=sprite.rect.y,
            y2=sprite.rect.y+32
        )

    return table


def get_tile_index_left(player_x, player_y, table):
    topleft = [k for k, nested_dict in table.items() if player_y >= nested_dict["y1"] and player_y <= nested_dict["y2"] and player_x >= nested_dict["x2"]]
    tile_less_far_1 = max(topleft)
    bottomleft = [k for k, nested_dict in table.items() if (player_y+20) >= nested_dict["y1"] and (player_y+20) <= nested_dict["y2"] and player_x >= nested_dict["x2"]]
    tile_less_far_2 = max(bottomleft)

    return tile_less_far_1, tile_less_far_2

def get_tile_index_right(player_x, player_y, table):
    topleft = [k for k, nested_dict in table.items() if player_y >= nested_dict["y1"] and player_y <= nested_dict["y2"] and player_x <= nested_dict["x1"]]
    tile_less_far_1 = min(topleft)
    bottomleft = [k for k, nested_dict in table.items() if (player_y+20) >= nested_dict["y1"] and (player_y+20) <= nested_dict["y2"] and player_x <= nested_dict["x1"]]
    tile_less_far_2 = min(bottomleft)

    return tile_less_far_1, tile_less_far_2

def get_tile_index_up(player_x, player_y, table):
    topleft = [k for k, nested_dict in table.items() if player_x >= nested_dict["x1"] and player_x <= nested_dict["x2"] and player_y >= nested_dict["y2"]]
    tile_less_far_1 = max(topleft)
    bottomleft = [k for k, nested_dict in table.items() if (player_x+20) >= nested_dict["x1"] and (player_x+20) <= nested_dict["x2"] and player_y >= nested_dict["y2"]]
    tile_less_far_2 = max(bottomleft)

    return tile_less_far_1, tile_less_far_2

def get_tile_index_down(player_x, player_y, table):
    topleft = [k for k, nested_dict in table.items() if player_x >= nested_dict["x1"] and player_x <= nested_dict["x2"] and (player_y+20) <= nested_dict["y2"]]
    tile_less_far_1 = min(topleft)
    bottomleft = [k for k, nested_dict in table.items() if (player_x+20) >= nested_dict["x1"] and (player_x+20) <= nested_dict["x2"] and (player_y+20) <= nested_dict["y2"]]
    tile_less_far_2 = min(bottomleft)

    return tile_less_far_1, tile_less_far_2



def calculate_distance_boundaries(table, player, direction):
    player_x = player.rect.x
    player_y = player.rect.y

    table = table

    try:
        if direction == "left":
            index_tile_1, index_tile_2 = get_tile_index_left(player_x, player_y, table)

            coord1_tile_index1 = table[index_tile_1]["x2"]
            coord1_tile_index2 = table[index_tile_2]["x2"]

            # get the distance from the top and bottom side of the player
            distance_index_1 = np.linalg.norm(np.array([player_x, player_y]) - np.array([coord1_tile_index1, player_y]), axis=-1)
            distance_index_2 = np.linalg.norm(np.array([player_x, player_y+20]) - np.array([coord1_tile_index2, player_y+20]), axis=-1)

            return distance_index_1, distance_index_2, index_tile_1, index_tile_2

        elif direction == "right":
            index_tile_1, index_tile_2 = get_tile_index_right(player_x, player_y, table)

            coord1_tile_index1 = table[index_tile_1]["x1"]
            coord1_tile_index2 = table[index_tile_2]["x1"]

            distance_index_1 = np.linalg.norm(np.array([coord1_tile_index1, player_y]) - np.array([player_x+20, player_y]), axis=-1)
            distance_index_2 = np.linalg.norm(np.array([coord1_tile_index2, player_y+20]) - np.array([player_x+20, player_y+20]), axis=-1)

            return distance_index_1, distance_index_2, index_tile_1, index_tile_2
            
        elif direction == "up":
            index_tile_1, index_tile_2 = get_tile_index_up(player_x, player_y, table)
            
            coord1_tile_index1 = table[index_tile_1]["y2"]
            coord1_tile_index2 = table[index_tile_2]["y2"]

            distance_index_1 = np.linalg.norm(np.array([player_x, player_y]) - np.array([player_x, coord1_tile_index1]), axis=-1)
            distance_index_2 = np.linalg.norm(np.array([player_x+20, player_y]) - np.array([player_x+20, coord1_tile_index2]), axis=-1)

            return distance_index_1, distance_index_2, index_tile_1, index_tile_2
        
        elif direction == "down":
            index_tile_1, index_tile_2 = get_tile_index_down(player_x, player_y, table)

            coord1_tile_index1 = table[index_tile_1]["y1"]
            coord1_tile_index2 = table[index_tile_2]["y1"]

            distance_index_1 = np.linalg.norm(np.array([player_x, coord1_tile_index1]) - np.array([player_x, player_y+20]), axis=-1)
            distance_index_2 = np.linalg.norm(np.array([player_x+20, coord1_tile_index1]) - np.array([player_x+20, player_y+20]), axis=-1)

            return distance_index_1, distance_index_2, index_tile_1, index_tile_2
        
    except ValueError:
        return 0