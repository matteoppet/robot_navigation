from pygame import Surface, draw
import numpy as np

class Sensor:
    def __init__(self, pos):
        width = 2
        height = 2
        pos = pos

        self.image = Surface((width, height))
        self.rect = self.image.get_rect(center=pos)

        self.color_sensor = ()


def calculate_distance(PLAYER, obstacles_sprites):
    data = lines_data(PLAYER)
    distance_sensors = {name: {"point_of_collision": None, "distance": 100} for name in data}

    for name in data:
        start = data[name]["pos_start"]
        end = data[name]["pos_end"]

        for obstacle in obstacles_sprites:
            collision = obstacle.rect.clipline(start, end)

            if collision:
                sensor = Sensor(collision[0])

                distance_sensors[name] = {
                    "point_of_collision": collision[0],
                    "distance": np.linalg.norm(np.array([start[0], start[1]] - np.array([collision[0][0], collision[0][1]])))
                    }

    return distance_sensors
    

def lines_data(PLAYER):
    pos_start_x = PLAYER.rect.centerx
    pos_start_y = PLAYER.rect.centery

    section_1_end = 45
    section_2_end = 30
    section_3_end_type1 = 40
    section_3_end_type2 = 15

    width_height_player = 9

    return {
        "right": {"pos_start": (pos_start_x+width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx+section_1_end, PLAYER.rect.centery)},
        "left": {"pos_start": (pos_start_x-width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx-section_1_end, PLAYER.rect.centery)},
        "up": {"pos_start": (pos_start_x, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx, PLAYER.rect.centery-section_1_end)},
        "down": {"pos_start": (pos_start_x, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx, PLAYER.rect.centery+section_1_end)},

        "diagonal-up-right": {"pos_start": (pos_start_x+width_height_player, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx+section_2_end, PLAYER.rect.centery-section_2_end)},
        "diagonal-up-left": {"pos_start": (pos_start_x-width_height_player, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx-section_2_end, PLAYER.rect.centery-section_2_end)},
        "diagonal-down-right": {"pos_start": (pos_start_x+width_height_player, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx+section_2_end, PLAYER.rect.centery+section_2_end)},
        "diagonal-down-left": {"pos_start": (pos_start_x-width_height_player, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx-section_2_end, PLAYER.rect.centery+section_2_end)},

        "diagonal-up-up-right": {"pos_start": (pos_start_x+width_height_player, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx+section_3_end_type2, PLAYER.rect.centery-section_3_end_type1)},
        "diagonal-up-up-left": {"pos_start": (pos_start_x-width_height_player, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx-section_3_end_type2, PLAYER.rect.centery-section_3_end_type1)},
        "diagonal-right-right-up": {"pos_start": (pos_start_x+width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx+section_3_end_type1, PLAYER.rect.centery-section_3_end_type2)},
        "diagonal-right-right-down": {"pos_start": (pos_start_x+width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx+section_3_end_type1, PLAYER.rect.centery+section_3_end_type2)},
        "diagonal-left-left-up": {"pos_start": (pos_start_x-width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx-section_3_end_type1, PLAYER.rect.centery-section_3_end_type2)},
        "diagonal-left-left-down": {"pos_start": (pos_start_x-width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx-section_3_end_type1, PLAYER.rect.centery+section_3_end_type2)},
        "diagonal-down-down-right": {"pos_start": (pos_start_x, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx+section_3_end_type2, PLAYER.rect.centery+section_3_end_type1)},
        "diagonal-down-down-left": {"pos_start": (pos_start_x, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx-section_3_end_type2, PLAYER.rect.centery+section_3_end_type1)},
    }


# distances sensor not correct and bugs in the middle of two tile