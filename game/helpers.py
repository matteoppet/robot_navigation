import pygame
from pytmx.util_pygame import load_pygame


def collide_player(player, sprite):
    if player.collide_rect(sprite):
        print("Collide detected")


def create_list_buondaries(class_object, index):
    tmx_data = load_pygame("../assets/tsx/basic.tmx") # load assets
    boundire_points = [] # instintiated empty list

    for obj in tmx_data.objects: # go through object
        if obj.type == class_object: # go through object type
            if obj.name == f"Boundire{index}": # check for the buondire with the index
                boundire_points = obj.points # set points on a variables
    
    list_points = [] # instintiated empty list
    for point in boundire_points: # go through points
        list_points.append([point.x, point.y]) # append the points in the list

    return list_points # return the list with the points to draw
