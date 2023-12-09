import pygame
from pytmx.util_pygame import load_pygame


def collide_player(player, sprites):
    collisions = pygame.sprite.spritecollide(player, sprites, False, pygame.sprite.collide_mask)
    
    if collisions:
        print("Collision detected")


def create_list_boundaries(class_object, index):
    tmx_data = load_pygame("../assets/tsx/basic.tmx") # load assets
    boundire_points = [] # instintiated empty list

    for obj in tmx_data.objects: # go through object
        if obj.type == class_object: # go through object type
            if obj.name == f"Boundarie{index}": # check for the buondire with the index
                boundire_points = obj.points # set points on a variables
    
    list_points = [] # instintiated empty list
    for point in boundire_points: # go through points
        list_points.append([point.x, point.y]) # append the points in the list

    return list_points # return the list with the points to draw


def draw_lines(screen, player):
    # center to right
    pygame.draw.line(
        screen, 
        "white", 
        (player.rect.centerx, player.rect.centery), 
        (player.rect.centerx+100, player.rect.centery), 
        width=5)
    # center to left
    pygame.draw.line(
        screen, 
        "white", 
        (player.rect.centerx, player.rect.centery), 
        (player.rect.centerx-100, player.rect.centery), 
        width=5)
    # center to up
    pygame.draw.line(
        screen, 
        "white", 
        (player.rect.centerx, player.rect.centery), 
        (player.rect.centerx, player.rect.centery-100), 
        width=5)
    # center to low
    pygame.draw.line(
        screen, 
        "white", 
        (player.rect.centerx, player.rect.centery), 
        (player.rect.centerx, player.rect.centery+100), 
        width=5)