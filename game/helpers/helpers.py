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

    temporary_rect = pygame.Rect(pos_x, pos_y, 10, 10)

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
                print(f"Accessible, ZONE: x({position_mouse[0]}), y({position_mouse[1]})")
                draw_circle_mouse(screen, position_mouse[0], position_mouse[1], "white")
                return position_mouse
            else:
                print(f"Not accessible, ZONE: x({position_mouse[0]}), y({position_mouse[1]})")
                draw_circle_mouse(screen, position_mouse[0], position_mouse[1], "red")
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

        if valid == -1:
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


def s():
    # TODO: 1) Fuori questa funzione creare una tabella, ogni record contiene la x e la y di ogni tile
        # creare dictionary cosi:
            # {
                # "ogni quadrato": 
                    # "x1": [tutte le x1]
                    # "x2": [tutte le x2] aggiungere 32
                    # "y1": [tutte le y1]
                    # "y2": [tutte le y2] aggiungere 32
            # }

    # TODO: 2) Controllare i 4 lati
        
        # LEFT LATO
            # RIPETERE QUESTO PROCESSO PER L'ANGOLO IN ALTO E IN BASSO A SINISTRA: 
            # LA DISTANZA MINORE CHE ESCE TRA I DUE è QUELLO DA PRENDERE IN CONSIDERAZIONE

                # TODO: 3) prendere coordinate player, guardare se la y del player è maggiore/uguale di Yb1 e minore/uguale di Yb2
                # se si, calcolare distanza orizzontale (Xp - (Xb+32))
    
    ...


    # IN TILE, TENERE SOLO I TILE VICINO LA STRADA COME BOUNDARIES GRASS COSI DA DIMINUIRE LA PESANTEZZA DELLA TABELLA


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


def calculate_distance_boundaries(table, player, direction):
    player_x = player.rect.x
    player_y = player.rect.y

    distance_topleft = 10000
    distance_bottomleft = 10000 

    distance_topright = 10000
    distance_bottomright = 10000 

    distance_top_1 = 10000
    distance_top_2 = 10000

    distance_bottom_1 = 10000 
    distance_bottom_2 = 10000

    index_tile_y1_left = 0
    index_tile_y2_left = 0

    index_tile_y1_right = 0
    index_tile_y2_right = 0

    index_tile_x1_up = 0
    index_tile_x2_up = 0

    index_tile_x1_down = 0
    index_tile_x2_down = 0

    r = True
    while r:
        try:
            if direction == "left":

                if player_y >= table[index_tile_y1_left]["y1"] and player_y <= table[index_tile_y1_left]["y2"]:    
                    distance_topleft = player_x - (table[index_tile_y1_left]["x2"])
                else: index_tile_y1_left += 1

                if player_y+32 >= table[index_tile_y2_left]["y1"] and player_y+32 <= table[index_tile_y2_left]["y2"]:
                    distance_bottomleft = player_x - (table[index_tile_y2_left]["x2"])
                else: index_tile_y2_left += 1

                if distance_bottomleft != 10000 and distance_topleft != 10000:
                    r = False
                    return min(distance_topleft, distance_bottomleft)
                
            elif direction == "right":
                if player_y >= table[index_tile_y1_right]["y1"] and player_y <= table[index_tile_y1_right]["y2"] and player_x <= table[index_tile_y1_right]["x1"]:
                    distance_topright = table[index_tile_y1_right]["x1"] - (player_x+32)
                else: index_tile_y1_right += 1

                if player_y+32 >= table[index_tile_y2_right]["y1"] and player_y+32 <= table[index_tile_y2_right]["y2"] and player_x <= table[index_tile_y2_right]["x2"]:
                    distance_bottomright = table[index_tile_y2_right]["x1"] - (player_x+32)
                else: index_tile_y2_right += 1

                if distance_bottomright != 10000 and distance_topright != 10000:
                    r = False
                    return min(distance_topright, distance_bottomright)
                
            elif direction == "up":
                if player_x >= table[index_tile_x1_up]["x1"] and player_x <= table[index_tile_x1_up]["x2"] and player_y >= table[index_tile_x1_up]["y2"]:
                    distance_top_1 = player_y - table[index_tile_x1_up]["y2"]
                else: index_tile_x1_up += 1

                if player_x+32 >= table[index_tile_x2_up]["x1"] and player_x+32 <= table[index_tile_x2_up]["x2"] and player_y >= table[index_tile_x2_up]["y2"]:
                    distance_top_2 = player_y - table[index_tile_x2_up]["y2"]
                else: index_tile_x2_up += 1
                    
                if distance_top_1 != 10000 and distance_top_2 != 10000:
                    r = False
                    return min(distance_top_1, distance_top_2)

            elif direction == "down":
                if player_x >= table[index_tile_x1_down]["x1"] and player_x <= table[index_tile_x1_down]["x2"] and (player_y+32) <= table[index_tile_x1_down]["y1"]:
                    distance_bottom_1 = table[index_tile_x1_down]["y1"] - (player_y+32)
                else: index_tile_x1_down += 1

                if player_x+32 >= table[index_tile_x2_down]["x1"] and player_x+32 <= table[index_tile_x2_down]["x2"] and (player_y+32) <= table[index_tile_x2_down]["y1"]:
                    distance_bottom_2 = table[index_tile_x2_down]["y1"] - (player_y+32)
                else: index_tile_x2_down += 1

                if distance_bottom_1 != 10000 and distance_bottom_2 != 10000:
                    r = False
                    return min(distance_bottom_1, distance_bottom_2)
        except KeyError:
            raise KeyError("Index in the dictionary (table) not found. No tile corresponding.")
