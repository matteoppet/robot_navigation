import pygame
from player import Player
from world import World
from sensors import create_sensors, draw_lines, sprite_group_sensors
from boundaries import create_boundaries, sprite_group_boundaries
from helpers import collide_player, collide_sensors
from settings import LENGTH_SENSOR


pygame.init()
screen = pygame.display.set_mode((1120, 992))
clock = pygame.time.Clock()

# world section
WORLD = World()
WORLD.create_tiles() 
WORLD.create_objects()
sprite_group = WORLD.sprite_group
sprite_group_objects = WORLD.sprite_group_objects
sprite_group_floor = WORLD.sprite_group_floor
list_group_floor = [sprite for sprite in sprite_group_floor]

# player section
PLAYER = Player()

# boundaries section
create_boundaries()
sprite_group_bound = sprite_group_boundaries
list_boundaries = [sprite for sprite in sprite_group_boundaries]


# sensors section
create_sensors(PLAYER.rect.centerx, PLAYER.rect.centery, length_sensor=LENGTH_SENSOR)
sprite_group_sens = sprite_group_sensors


global_list_sensors_colliding = []
global_dictionary_info_positions = {}


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw sprites
    sprite_group_floor.draw(screen)
    sprite_group.draw(screen)

    # draw and move player
    screen.blit(PLAYER.image, (PLAYER.x, PLAYER.y))
    PLAYER.move()

    # draw lines player
    for sprite in sprite_group_sens:
        if sprite.name in ("right", "down"):
            sprite.rect.x = PLAYER.rect.centerx
            sprite.rect.y = PLAYER.rect.centery
        elif sprite.name == "left":
            sprite.rect.x = PLAYER.rect.centerx-LENGTH_SENSOR
            sprite.rect.y = PLAYER.rect.centery
        elif sprite.name == "up":
            sprite.rect.x = PLAYER.rect.centerx
            sprite.rect.y = PLAYER.rect.centery-LENGTH_SENSOR
        
        # if global_dict_info != {}:
        #     if sprite.name in global_dict_info:
        #         if sprite.name == "right":
        #             sensor_rect_x, floor_rect_x = global_dict_info["right"]
        #             # use the x position in RGB color, limit it to 255
        #             R = 255
        #             G = floor_rect_x - sensor_rect_x
        #             B = 0
        #         else:
        #             R = G = B = 255

        if sprite.name in global_list_sensors_colliding:
            draw_lines(screen, sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height, color="red")
        else:
            draw_lines(screen, sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height)

    # check collisions
    collide_player(PLAYER, list_group_floor)

    dictionary_info_positions, list_sensors_colliding = collide_sensors(sprite_group_sens, sprite_group_floor)
    global_list_sensors_colliding = list_sensors_colliding
    global_dictionary_info_positions = dictionary_info_positions

    pygame.display.flip()
    clock.tick(60)
