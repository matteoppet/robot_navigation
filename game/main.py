import pygame
from player import Player
from world import World
from sensors import create_sensors, draw_lines, sprite_group_sensors
from helpers import collide_player, collide_sensors, reset_game, mouse_function, create_distance_sprites, create_table_tiles, calculate_distance_boundaries
from settings import LENGTH_SENSOR


def update_and_draw_lines():
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

        if sprite.name in global_list_sensors_colliding:
            draw_lines(SCREEN, sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height, color="red")
        else:
            draw_lines(SCREEN, sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height)


pygame.init()
SCREEN = pygame.display.set_mode((1120, 992))
CLOCK = pygame.time.Clock()

# world section
WORLD = World()
WORLD.create_tiles() 
WORLD.create_objects()
sprite_group = WORLD.sprite_group
sprite_group_objects = WORLD.sprite_group_objects
sprite_group_boundaries_floor = WORLD.sprite_group_boundaries_floor
list_group_boundarties_floor = [sprite for sprite in sprite_group_boundaries_floor]
TABLE_TILES = create_table_tiles(sprite_group_boundaries_floor)

# player section
PLAYER = Player()

# sensors section
create_sensors(PLAYER.rect.centerx, PLAYER.rect.centery, length_sensor=LENGTH_SENSOR)
sprite_group_sens = sprite_group_sensors
global_list_sensors_colliding = []


# DISTANCE
create_distance_sprites()
sprite_group_for_distance = create_distance_sprites()


running = True
while running:
    
    # draw sprites
    sprite_group_boundaries_floor.draw(SCREEN)
    sprite_group.draw(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse_function(event, list_group_boundarties_floor, SCREEN)

    # draw and move player
    SCREEN.blit(PLAYER.image, (PLAYER.x, PLAYER.y))
    PLAYER.move()

    # update_and_draw_lines()

    # check collisions
    died = collide_player(PLAYER, list_group_boundarties_floor, "list")
    if died:
        reset_game(PLAYER)

    list_sensors_colliding = collide_sensors(sprite_group_sens, sprite_group_boundaries_floor)
    global_list_sensors_colliding = list_sensors_colliding

    # LEFT SOLVED
    direction_distance = {}
    for direction in ["left", "right", "up", "down"]:
        distance = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
        direction_distance[direction] = distance
        print(direction_distance)

    pygame.display.flip()
    CLOCK.tick(60)
