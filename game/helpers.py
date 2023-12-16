import pygame
from pytmx.util_pygame import load_pygame


def collide_player(player, sprites):
    for sprite in sprites:

        collisions = pygame.sprite.collide_rect(player, sprite)
        if collisions:
            print("Collision detected")


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
    dictionary_info_positions = {}
    for sensor, boundary_list in collisions.items():
        for boundary in boundary_list:
            sensors_colliding.append(sensor.name)

            if sensor.name in ("left", "right"):
                dictionary_info_positions[sensor.name] = [sensor.rect.x, boundary.rect.x]
            else:
                dictionary_info_positions[sensor.name] = [sensor.rect.x, sensor.rect.y, boundary.rect.x, boundary.rect.y]

    return dictionary_info_positions, sensors_colliding
