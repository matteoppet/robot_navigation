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
    distance_sensors = {name: {"point_of_collision": None, "distance": 120} for name in data}

    for name in data:
        start = data[name]["pos_start"]
        end = data[name]["pos_end"]

        collisions = {}
        for obstacle in obstacles_sprites:
            points_collision = obstacle.rect.clipline(start, end)

            if points_collision:
                x_point, y_point = points_collision[0]
                
                distance = np.linalg.norm(
                    np.array([*start]) - np.array([x_point, y_point])
                )

                collisions[distance] = (x_point, y_point)

        if collisions != {}:
            key_min_obstacle_distance = min(collisions)
            point_of_collision = collisions[key_min_obstacle_distance]

            distance_sensors[name] = {
                "point_of_collision": point_of_collision,
                "distance": key_min_obstacle_distance
            }
            

    return distance_sensors
    

def lines_data(PLAYER):
    pos_start_x = PLAYER.rect.centerx
    pos_start_y = PLAYER.rect.centery

    section_1_end = 120
    section_2_end = 85
    section_3_end_type1 = 110
    section_3_end_type2 = 40

    width_height_player = 16

    return {
        "right": {"pos_start": (pos_start_x+width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx+section_1_end, PLAYER.rect.centery)},
        "left": {"pos_start": (pos_start_x-width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx-section_1_end, PLAYER.rect.centery)},
        "up": {"pos_start": (pos_start_x, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx, PLAYER.rect.centery-section_1_end)},
        "down": {"pos_start": (pos_start_x, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx, PLAYER.rect.centery+section_1_end)},

        "diagonal-up-right": {"pos_start": (pos_start_x+width_height_player, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx+section_2_end, PLAYER.rect.centery-section_2_end)},
        "diagonal-up-left": {"pos_start": (pos_start_x-width_height_player, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx-section_2_end, PLAYER.rect.centery-section_2_end)},
        "diagonal-down-right": {"pos_start": (pos_start_x+width_height_player, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx+section_2_end, PLAYER.rect.centery+section_2_end)},
        "diagonal-down-left": {"pos_start": (pos_start_x-width_height_player, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx-section_2_end, PLAYER.rect.centery+section_2_end)},

        "diagonal-up-up-right": {"pos_start": (pos_start_x+width_height_player-8, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx+section_3_end_type2, PLAYER.rect.centery-section_3_end_type1)},
        "diagonal-up-up-left": {"pos_start": (pos_start_x-width_height_player+8, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx-section_3_end_type2, PLAYER.rect.centery-section_3_end_type1)},
        "diagonal-right-right-up": {"pos_start": (pos_start_x+width_height_player, pos_start_y-8), "pos_end": (PLAYER.rect.centerx+section_3_end_type1, PLAYER.rect.centery-section_3_end_type2)},
        "diagonal-right-right-down": {"pos_start": (pos_start_x+width_height_player, pos_start_y+8), "pos_end": (PLAYER.rect.centerx+section_3_end_type1, PLAYER.rect.centery+section_3_end_type2)},
        "diagonal-left-left-up": {"pos_start": (pos_start_x-width_height_player, pos_start_y-8), "pos_end": (PLAYER.rect.centerx-section_3_end_type1, PLAYER.rect.centery-section_3_end_type2)},
        "diagonal-left-left-down": {"pos_start": (pos_start_x-width_height_player, pos_start_y+8), "pos_end": (PLAYER.rect.centerx-section_3_end_type1, PLAYER.rect.centery+section_3_end_type2)},
        "diagonal-down-down-right": {"pos_start": (pos_start_x+8, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx+45, PLAYER.rect.centery+section_3_end_type1)},
        "diagonal-down-down-left": {"pos_start": (pos_start_x-8, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx-45, PLAYER.rect.centery+section_3_end_type1)},
    }


# take the less far tile colliding