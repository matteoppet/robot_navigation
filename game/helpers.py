import pygame
from pytmx.util_pygame import load_pygame
import time


def collide_player(player, sprites):
    for sprite in sprites:

        collisions = pygame.sprite.collide_rect(player, sprite)
        if collisions:
            return True

def create_list_boundaries(class_object, index):
    tmx_data = load_pygame("../assets/tsx/basic.tmx") # load assets
    boundire_points = [] # instintiated empty list

    for obj in tmx_data.objects: # go through object
        if obj.type == class_object: # go through object type
            if obj.name == f"Boundarie{index}": # check for the buondire with the index
                boundire_points = obj.points # set points on a variables
    
    list_points = [[point.x, point.y] for point in boundire_points] # instintiated empty list

    return list_points # return the list with the points to draw


def collide_sensors(sensors, boundaries):
    collisions = pygame.sprite.groupcollide(sensors, boundaries, False, False)

    sensors_colliding = []
    for sensor, boundary_list in collisions.items():
        for boundary in boundary_list:
            sensors_colliding.append(sensor.name)

    return sensors_colliding


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
            else:
                print(f"Not accessible, ZONE: x({position_mouse[0]}), y({position_mouse[1]})")
                draw_circle_mouse(screen, position_mouse[0], position_mouse[1], "red")