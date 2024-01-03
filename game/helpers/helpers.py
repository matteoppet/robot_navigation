import pygame
from pytmx.util_pygame import load_pygame
import time
import random 

def collide_player(player, target, type):

    if type == "list":
        for sprite in target:

            collisions = pygame.sprite.collide_rect(player, sprite)
            if collisions:
                return True
    else:
        collisions = pygame.sprite.collide_rect(player, target)
        if collisions:
            return True


def create_list_boundaries(class_object, index):
    tmx_data = load_pygame("../assets/tsx/basic.tmx")
    boundire_points = []

    for obj in tmx_data.objects:
        if obj.type == class_object:
            if obj.name == f"Boundarie{index}":
                boundire_points = obj.points
    
    list_points = [[point.x, point.y] for point in boundire_points]

    return list_points 


def collide_sensors(sensors, boundaries):
    collisions = pygame.sprite.groupcollide(sensors, boundaries, False, False)

    sensors_colliding = []
    for sensor, boundary_list in collisions.items():
        for boundary in boundary_list:
            sensors_colliding.append(sensor.name)

    return sensors_colliding


# IMPLEMENT BETTER THIS FUNCTION
def reset_game(player):
    x_player, y_player = player.reset()

    print()
    print(f"Died at position: x:{x_player}, y:{y_player}")
    print("Waiting 5 seconds before restart")
    time.sleep(5)
    print("Game restarted")
    print()


def check_possible_position_to_go(position_mouse, sprites):
    pos_x, pos_y = position_mouse

    temporary_rect = pygame.Rect(pos_x, pos_y, 20, 20)

    inside_boundaries = pygame.Rect.collidelist(temporary_rect, sprites)

    return inside_boundaries


def draw_circle_mouse(SCREEN, mouse_x, mouse_y, color):
    pygame.draw.circle(SCREEN, color, (mouse_x, mouse_y), 10)


def mouse_function(event, sprites, screen):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:
            position_mouse = pygame.mouse.get_pos()

            is_possible = check_possible_position_to_go(position_mouse, sprites)
            if is_possible == -1:
                print(f"Not accessible, ZONE: x({position_mouse[0]}), y({position_mouse[1]})")
                draw_circle_mouse(screen, position_mouse[0], position_mouse[1], "red")
                return (0,0)
            else:
                print(f"Accessible, ZONE: x({position_mouse[0]}), y({position_mouse[1]})")
                draw_circle_mouse(screen, position_mouse[0], position_mouse[1], "white")
                return position_mouse
            
    return (0,0)
            

def create_random_position_for_ai(sprites):
    r = True
    while r:
        min_pos = 0
        max_pos_y = 991
        max_pos_x = 1120

        x = random.randint(min_pos, max_pos_x)
        y = random.randint(min_pos, max_pos_y)
        position = (x, y)

        valid = check_possible_position_to_go(position, sprites)

        if valid != -1:
            r = False
            return position
        

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


def calculation_distance_left(player_x, player_y, table):
    topleft = [nested_dict['x2'] for nested_dict in table.values() if player_y >= nested_dict["y1"] and player_y <= nested_dict["y2"] and player_x >= nested_dict["x2"]]
    distance_topleft = player_x - max(topleft)
    bottomleft = [nested_dict['x2'] for nested_dict in table.values() if (player_y+20) >= nested_dict["y1"] and (player_y+20) <= nested_dict["y2"] and player_x >= nested_dict["x2"]]
    distance_bottomelft = player_x - max(bottomleft)

    return min(distance_topleft, distance_bottomelft)
    

def calculation_distance_right(player_x, player_y, table):
    topright = [nested_dict['x1'] for nested_dict in table.values() if player_y >= nested_dict["y1"] and player_y <= nested_dict["y2"] and player_x <= nested_dict["x1"]]
    distance_topright = min(topright) - (player_x+20)
    bottomright = [nested_dict['x1'] for nested_dict in table.values() if (player_y+20) >= nested_dict["y1"] and (player_y+20) <= nested_dict["y2"] and player_x <= nested_dict["x1"]]
    distance_bottomright = min(bottomright) - (player_x+20)

    return min(distance_topright, distance_bottomright)
    

def calculation_distance_up(player_x, player_y, table):
    leftup = [nested_dict['y2'] for nested_dict in table.values() if player_x >= nested_dict["x1"] and player_x <= nested_dict["x2"] and player_y >= nested_dict["y2"]]
    distance_leftup = player_y - max(leftup)
    rightup = [nested_dict['y2'] for nested_dict in table.values() if (player_x+20) >= nested_dict["x1"] and (player_x+20) <= nested_dict["x2"] and player_y >= nested_dict["y2"]]
    distance_rightup = player_y - max(rightup)

    return min(distance_leftup, distance_rightup)


def calculation_distance_down(player_x, player_y, table):
    leftdown = [nested_dict['y1'] for nested_dict in table.values() if player_x >= nested_dict["x1"] and player_x <= nested_dict["x2"] and (player_y+20) <= nested_dict["y2"]]
    distance_leftdown = min(leftdown) - (player_y+20)
    rightdown = [nested_dict['y1'] for nested_dict in table.values() if (player_x+20) >= nested_dict["x1"] and (player_x+20) <= nested_dict["x2"] and (player_y+20) <= nested_dict["y2"]]
    distance_rightdown = min(rightdown) - (player_y+20)

    return min(distance_leftdown, distance_rightdown)


def calculate_distance_boundaries(table, player, direction):
    player_x = player.rect.x
    player_y = player.rect.y

    table = table

    try:
        if direction == "left":
            number = calculation_distance_left(player_x, player_y, table)
            if number == None: return 0
            else: return number
            
        elif direction == "right":
            number = calculation_distance_right(player_x, player_y, table)
            if number == None: return 0
            else: return number
            
        elif direction == "up":
            number = calculation_distance_up(player_x, player_y, table)
            if number == None: return 0
            else: return number
        
        elif direction == "down":
            number = calculation_distance_down(player_x, player_y, table)
            if number == None: return 0
            else: return number
        
    except ValueError:
        return 0
        